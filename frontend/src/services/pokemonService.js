import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const pokemonService = {
  // Obtener todos los pokémones con paginación
  obtenerTodos: (pagina = 1, limite = 20) => {
    return api.get('/api/pokemones', {
      params: { pagina, limite }
    });
  },

  // Obtener pokémon por ID
  obtenerPorId: (id) => {
    return api.get(`/api/pokemones/${id}`);
  },

  // Filtrar por tipo
  obtenerPorTipo: (tipo) => {
    return api.get(`/api/pokemones/tipo/${tipo}`);
  },

  // Obtener legendarios
  obtenerLegendarios: () => {
    return api.get('/api/pokemones/legendarios');
  },

  // Obtener estadísticas
  obtenerEstadisticas: () => {
    return api.get('/api/estadisticas');
  },

  // Obtener tipos
  obtenerTipos: () => {
    return api.get('/api/tipos');
  },

  // Información de la API
  obtenerInfo: () => {
    return api.get('/');
  },
};

export default api;
