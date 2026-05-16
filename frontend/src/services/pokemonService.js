import axios from 'axios';

const isLocalhost = typeof window !== 'undefined' && window.location.hostname === 'localhost';
const DEFAULT_LOCAL_API = 'http://localhost:5000/api';
const DEFAULT_PROD_API = '/api';
const API_BASE_URL = process.env.REACT_APP_API_URL || (isLocalhost ? DEFAULT_LOCAL_API : DEFAULT_PROD_API);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const pokemonService = {
  // Obtener todos los pokémones con paginación
  obtenerTodos: (pagina = 1, limite = 20) => {
    return api.get('/pokemones', {
      params: { pagina, limite }
    });
  },

  // Obtener pokémon por ID
  obtenerPorId: (id) => {
    return api.get(`/pokemones/${id}`);
  },

  // Filtrar por tipo
  obtenerPorTipo: (tipo) => {
    return api.get(`/pokemones/tipo/${tipo}`);
  },

  // Obtener legendarios
  obtenerLegendarios: () => {
    return api.get('/pokemones/legendarios');
  },

  // Obtener estadísticas
  obtenerEstadisticas: () => {
    return api.get('/estadisticas');
  },

  // Obtener tipos
  obtenerTipos: () => {
    return api.get('/tipos');
  },

  // Información de la API
  obtenerInfo: () => {
    return api.get('/');
  },
};

export default api;
