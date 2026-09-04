import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL ?? ''
const EMPTY_FORM = { query: '', left_response: '', right_response: '' }

function ScoreCard({ side, score, response }) {
  const name = side === 'left' ? 'Resposta A' : 'Resposta B'
  return (
    <article className={`score-card ${side}`}>
      <div className="score-card__topline"><span>{name}</span><span className="score-label">Nota</span></div>
      <strong>{Number(score).toFixed(1)}<small>/10</small></strong>
      <p>{response}</p>
    </article>
  )
}

function Result({ evaluation }) {
  if (!evaluation) return null
  return (
    <section className="result" aria-live="polite">
      <div className="result__heading"><span className="eyebrow">Resultado da avaliação</span><span className="complete">● concluída</span></div>
      <h2>Uma nova perspectiva para a sua comparação.</h2>
      <div className="scores">
        <ScoreCard side="left" score={evaluation.left_score} response={evaluation.left_response} />
        <div className="versus">VS</div>
        <ScoreCard side="right" score={evaluation.right_score} response={evaluation.right_response} />
      </div>
      <div className="assessment"><span>✦</span><div><h3>O que foi avaliado</h3><p>{evaluation.comment}</p></div></div>
    </section>
  )
}

function App() {
  const [form, setForm] = useState(EMPTY_FORM)
  const [evaluation, setEvaluation] = useState(null)
  const [history, setHistory] = useState([])
  const [historyOpen, setHistoryOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [historyLoading, setHistoryLoading] = useState(false)
  const [error, setError] = useState('')

  const update = (field) => (event) => setForm({ ...form, [field]: event.target.value })

  async function request(path, options) {
    const response = await fetch(`${API_URL}${path}`, options)
    if (!response.ok) {
      const body = await response.json().catch(() => null)
      throw new Error(body?.detail?.[0]?.msg || 'Não foi possível concluir a solicitação.')
    }
    return response.json()
  }

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const result = await request('/evaluations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      setEvaluation(result)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  async function openHistory() {
    setHistoryOpen(true)
    setError('')
    setHistoryLoading(true)
    try {
      setHistory(await request('/evaluations/history?email=user@example.com'))
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setHistoryLoading(false)
    }
  }

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Duelo de Respostas">◈ <span>duelo</span></a>
        <button className="history-button" onClick={openHistory}>Histórico <span>↗</span></button>
      </header>

      <div className="shell" id="top">
        <section className="hero">
          <span className="eyebrow">Avaliação comparativa por IA</span>
          <h1>Qual resposta<br /><em>vence?</em></h1>
          <p>Coloque duas respostas lado a lado. Nossa IA analisa precisão, clareza e profundidade para revelar a melhor.</p>
        </section>

        <form className="comparison-form" onSubmit={submit}>
          <label className="query-field"><span>Sua pergunta ou contexto</span><input required value={form.query} onChange={update('query')} placeholder="Ex.: Quantos dias tem um ano?" /></label>
          <div className="response-fields">
            <label><span><i className="marker marker-a">A</i> Resposta A</span><textarea required value={form.left_response} onChange={update('left_response')} placeholder="Cole a primeira resposta aqui..." /></label>
            <label><span><i className="marker marker-b">B</i> Resposta B</span><textarea required value={form.right_response} onChange={update('right_response')} placeholder="Cole a segunda resposta aqui..." /></label>
          </div>
          <div className="form-actions">
            <button type="button" className="clear-button" onClick={() => setForm(EMPTY_FORM)}>Limpar campos</button>
            <button className="evaluate-button" disabled={loading}>{loading ? 'Avaliando…' : 'Avaliar respostas'} <span>→</span></button>
          </div>
          {error && <p className="error" role="alert">{error}</p>}
        </form>

        {loading && <section className="loading-result" aria-live="polite">
          <span className="loading-orbit" aria-hidden="true" />
          <div><strong>A IA está avaliando as respostas</strong><p>Comparando precisão, clareza e profundidade…</p></div>
        </section>}

        <Result evaluation={evaluation} />
      </div>

      {historyOpen && <div className="modal-backdrop" role="presentation" onMouseDown={() => setHistoryOpen(false)}>
        <aside className="history-panel" role="dialog" aria-modal="true" aria-label="Histórico de avaliações" onMouseDown={(event) => event.stopPropagation()}>
          <div className="panel-heading"><div><span className="eyebrow">Suas comparações</span><h2>Histórico</h2></div><button onClick={() => setHistoryOpen(false)} aria-label="Fechar histórico">×</button></div>
          {historyLoading ? <p className="empty">Carregando avaliações…</p> : history.length === 0 ? <p className="empty">Ainda não há avaliações salvas.</p> : <div className="history-list">{history.slice().reverse().map((item) => <button key={item.id} className="history-item" onClick={() => { setEvaluation(item); setHistoryOpen(false) }}><span>{item.query}</span><small>A {Number(item.left_score).toFixed(1)} · B {Number(item.right_score).toFixed(1)}</small></button>)}</div>}
        </aside>
      </div>}
    </main>
  )
}

export default App
