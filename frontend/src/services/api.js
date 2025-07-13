import axios from "axios";

export const api = axios.create({
  baseURL: "https://precificador-lika.onrender.com/api/fretes"
});