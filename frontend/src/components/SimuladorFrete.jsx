import { useState } from "react";
import { api } from "../services/api";

export default function SimuladorFrete() {
  const [dados, setDados] = useState({
    marketplace: "",
    modalidade: "",
    preco_produto: "",
    peso: "",
    categoria: "",
    nivel_logistico: ""
  });

  const [resultado, setResultado] = useState(null);

  const handleChange = (e) => {
    setDados({ ...dados, [e.target.name]: e.target.value });
  };

  const calcularFrete = async () => {
    try {
      const res = await api.post("/calcular", dados);
      setResultado(res.data.valor);
    } catch (err) {
      console.error("Erro ao calcular frete:", err);
    }
  };

  return (
    <div className="p-6 bg-white shadow-md rounded max-w-lg mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Simulador de Frete</h2>
      <input className="input" name="marketplace" placeholder="Marketplace" onChange={handleChange} />
      <input className="input" name="modalidade" placeholder="Modalidade" onChange={handleChange} />
      <input className="input" name="preco_produto" placeholder="Preço do Produto" type="number" onChange={handleChange} />
      <input className="input" name="peso" placeholder="Peso (kg)" type="number" onChange={handleChange} />
      <input className="input" name="categoria" placeholder="Categoria" onChange={handleChange} />
      <input className="input" name="nivel_logistico" placeholder="Nível Logístico" onChange={handleChange} />
      <button onClick={calcularFrete} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Calcular
      </button>
      {resultado !== null && (
        <div className="mt-4 text-lg font-medium text-green-700">
          Valor do Frete: R$ {resultado.toFixed(2)}
        </div>
      )}
    </div>
  );
}