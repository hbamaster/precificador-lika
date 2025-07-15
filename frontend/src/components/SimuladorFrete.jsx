import { useState } from "react"
import { api } from "../services/api"

export default function SimuladorFrete() {
  const [dados, setDados] = useState({
    marketplace: "",
    modalidade: "",
    preco_produto: "",
    peso: "",
    categoria: "",
    nivel_logistico: ""
  })

  const [resultado, setResultado] = useState(null)
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState("")

  const handleChange = e => {
    setDados({ ...dados, [e.target.name]: e.target.value })
  }

  const camposObrigatorios = ["modalidade", "preco_produto", "peso"]

  const calcularFrete = async () => {
    setErro("")
    setResultado(null)

    // Validação simples
    for (const campo of camposObrigatorios) {
      if (!dados[campo]) {
        setErro(`Preencha o campo "${campo}"`)
        return
      }
    }

    setLoading(true)
    try {
      const res = await api.post("/calcular", dados)
      setResultado(res.data.valor)
    } catch (err) {
      setErro("Erro ao calcular frete. Verifique os dados ou tente novamente.")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 bg-white shadow-md rounded max-w-lg mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Simulador de Frete</h2>

      <div className="space-y-3">
        <input className="input" name="marketplace" placeholder="Marketplace" onChange={handleChange} />
        <input className="input" name="modalidade" placeholder="Modalidade*" onChange={handleChange} />
        <input className="input" name="preco_produto" placeholder="Preço do Produto*" type="number" onChange={handleChange} />
        <input className="input" name="peso" placeholder="Peso (kg)*" type="number" onChange={handleChange} />
        <input className="input" name="categoria" placeholder="Categoria" onChange={handleChange} />
        <input className="input" name="nivel_logistico" placeholder="Nível Logístico" onChange={handleChange} />
      </div>

      {erro && <div className="mt-4 text-red-600">{erro}</div>}

      <button
        onClick={calcularFrete}
        className={`mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
        disabled={loading}
      >
        {loading ? "Calculando..." : "Calcular"}
      </button>

      {resultado !== null && (
        <div className="mt-4 text-lg font-medium text-green-700">
          Valor do Frete: R$ {resultado.toFixed(2)}
        </div>
      )}
    </div>
  )
}