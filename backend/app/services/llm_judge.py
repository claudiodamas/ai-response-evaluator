import json
import os
import re
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx


def load_env_file():
    """Carrega variáveis do arquivo .env caso existam e não estejam no ambiente."""
    project_root = Path(__file__).resolve().parents[3]
    env_paths = [
        Path.cwd() / ".env",
        project_root / ".env",
    ]
    for env_path in env_paths:
        if env_path.is_file():
            with env_path.open("r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip("'\"")
                        if key and key not in os.environ:
                            os.environ[key] = val
            break


# Carrega o .env na inicialização
load_env_file()


def build_dynamic_prompt(
    query: str,
    left_response: str,
    right_response: str,
    focus_criteria: Optional[List[str]] = None
) -> str:
    """
    Constrói um prompt dinâmico de julgamento comparativo (LLM-as-a-Judge)
    adaptando os critérios ao tipo de consulta e respostas fornecidas.
    """
    default_criteria = [
        "1. Corretude Factual: Ausência de erros, alucinações e inconsistências.",
        "2. Relevância Direta: Resposta objetiva e focada na pergunta sem rodeios desnecessários.",
        "3. Completude & Profundidade: Presença de todos os pontos-chave necessários para uma resposta completa.",
        "4. Clareza & Estrutura: Linguagem fluida, bem articulada, organizada e fácil de compreender."
    ]

    criteria_section = "\n".join(default_criteria)
    if focus_criteria:
        custom_items = [f"- {c}" for c in focus_criteria]
        criteria_section += "\n\nCritérios Especiais de Atenção:\n" + "\n".join(custom_items)

    prompt = f"""Você é um especialista em Avaliação Comparativa de Modelos de Inteligência Artificial (LLM-as-a-Judge).
Sua missão é realizar uma análise crítica, justa e aprofundada comparando duas respostas geradas por IA para uma mesma consulta do usuário.

[CONSULTA ORIGINAL]:
{query}

----------------------------------------
[RESPOSTA ESQUERDA (LEFT)]:
{left_response}
----------------------------------------
[RESPOSTA DIREITA (RIGHT)]:
{right_response}
----------------------------------------

[CRITÉRIOS DE AVALIAÇÃO]:
{criteria_section}

[INSTRUÇÕES DE JULGAMENTO]:
1. Avalie individualmente a Resposta Esquerda e a Resposta Direita sob cada critério.
2. Atribua uma nota numérica de 0.0 a 10.0 para cada lado (ex: 8.5, 9.0, 4.0).
3. Escreva um comentário comparativo direto em português explicando:
   - Qual resposta foi superior e por quê;
   - Os principais pontos fortes e eventuais falhas/omissões de cada resposta.
4. Responda ESTRITAMENTE em formato JSON com a seguinte estrutura:

{{
  "left_score": <float entre 0.0 e 10.0>,
  "right_score": <float entre 0.0 e 10.0>,
  "comment": "<justificativa comparativa detalhada>"
}}"""
    return prompt


def _clean_json_response(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()


def evaluate_with_gemini(query: str, left_response: str, right_response: str, api_key: str) -> Dict[str, Any]:
    model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    prompt = build_dynamic_prompt(query, left_response, right_response)
    
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    timeout = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "60"))
    max_retries = int(os.getenv("GEMINI_MAX_RETRIES", "2"))
    retryable_statuses = {429, 500, 502, 503, 504}

    with httpx.Client(timeout=timeout) as client:
        for attempt in range(max_retries + 1):
            try:
                response = client.post(url, params={"key": api_key}, json=payload)
                if response.status_code in retryable_statuses and attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue

                response.raise_for_status()
                data = response.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                clean_text = _clean_json_response(raw_text)
                return json.loads(clean_text)
            except httpx.TransportError:
                if attempt == max_retries:
                    raise
                time.sleep(2 ** attempt)


def evaluate_with_openai(query: str, left_response: str, right_response: str, api_key: str) -> Dict[str, Any]:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = build_dynamic_prompt(query, left_response, right_response)
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        raw_text = data["choices"][0]["message"]["content"]
        clean_text = _clean_json_response(raw_text)
        return json.loads(clean_text)


def evaluate_pairwise(query: str, left_response: str, right_response: str) -> Dict[str, Any]:
    """
    Avalia duas respostas candidatas utilizando LLM-as-a-Judge com prompt dinâmico.
    Carrega o provedor ativo (Gemini ou OpenAI) e recorre ao fallback se necessário.
    """
    load_env_file()
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    try:
        if provider == "gemini" and gemini_key:
            result = evaluate_with_gemini(query, left_response, right_response, gemini_key)
            return {
                "left_score": float(result.get("left_score", 5.0)),
                "right_score": float(result.get("right_score", 5.0)),
                "comment": str(result.get("comment", "Avaliação concluída pelo Gemini."))
            }
        elif provider == "openai" and openai_key:
            result = evaluate_with_openai(query, left_response, right_response, openai_key)
            return {
                "left_score": float(result.get("left_score", 5.0)),
                "right_score": float(result.get("right_score", 5.0)),
                "comment": str(result.get("comment", "Avaliação concluída pelo OpenAI."))
            }
        elif gemini_key:
            result = evaluate_with_gemini(query, left_response, right_response, gemini_key)
            return {
                "left_score": float(result.get("left_score", 5.0)),
                "right_score": float(result.get("right_score", 5.0)),
                "comment": str(result.get("comment", "Avaliação concluída pelo Gemini."))
            }
        elif openai_key:
            result = evaluate_with_openai(query, left_response, right_response, openai_key)
            return {
                "left_score": float(result.get("left_score", 5.0)),
                "right_score": float(result.get("right_score", 5.0)),
                "comment": str(result.get("comment", "Avaliação concluída pelo OpenAI."))
            }
    except httpx.HTTPStatusError as e:
        return {
            "left_score": 5.0,
            "right_score": 5.0,
            "comment": (
                "Avaliação gerada via fallback seguro porque o Gemini retornou "
                f"o status HTTP {e.response.status_code}. Verifique a cota e o modelo configurado."
            )
        }
    except (httpx.HTTPError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return {
            "left_score": 5.0,
            "right_score": 5.0,
            "comment": "Avaliação gerada via fallback seguro devido a uma falha temporária na LLM."
        }
        
    return {
        "left_score": 10.0,
        "right_score": 0.0,
        "comment": "Avaliação gerada via fallback determinístico (configure GEMINI_API_KEY ou OPENAI_API_KEY no .env para avaliação via LLM real)."
    }
