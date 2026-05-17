const POKEAPI_BASE = 'https://pokeapi.co/api/v2';
const REQUEST_TIMEOUT_MS = 8000;
const MAX_PAGE_LIMIT = 100;
const STATS_SAMPLE_SIZE = 200;

const LEGENDARIOS_IDS = [
  144, 145, 146, 150, 151,
  243, 244, 245, 249, 250, 251,
  377, 378, 379, 380, 381, 382, 383, 384, 385, 386,
  480, 481, 482, 483, 484, 485, 486, 487, 488, 489,
  490, 491, 492, 493, 494,
  638, 639, 640, 641, 642, 643, 644, 645, 646, 647,
  648, 649,
  716, 717, 718, 719, 720, 721,
  772, 773, 785, 786, 787, 788, 789, 790, 791, 792,
  800, 801, 802, 807, 808, 809,
  888, 889, 890, 891, 892, 893, 894, 895, 896, 897,
  898, 905,
  1001, 1002, 1003, 1004, 1007, 1008,
  1014, 1015, 1016, 1017,
  1020, 1021, 1022, 1023, 1024, 1025,
];
const LEGENDARIOS_SET = new Set(LEGENDARIOS_IDS);

const POKEMON_CACHE = new Map();
let TOTAL_POKEMON_CACHE = null;
let ESTADISTICAS_CACHE = null;
let TIPOS_CACHE = null;

function extractIdFromUrl(url) {
  if (!url) return null;
  const cleaned = url.replace(/\/$/, '');
  const parts = cleaned.split('/');
  const value = Number(parts[parts.length - 1]);
  return Number.isFinite(value) ? value : null;
}

async function fetchJson(url, timeoutMs = REQUEST_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) {
      return null;
    }
    return await response.json();
  } catch (_) {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

async function obtenerTotalPokemones() {
  if (TOTAL_POKEMON_CACHE !== null) return TOTAL_POKEMON_CACHE;

  const data = await fetchJson(`${POKEAPI_BASE}/pokemon-species?limit=1`);
  TOTAL_POKEMON_CACHE = Number.isFinite(data?.count) ? data.count : 1025;
  return TOTAL_POKEMON_CACHE;
}

async function obtenerPokemonPokeapi(idNumero) {
  if (!idNumero || idNumero <= 0) return null;
  if (POKEMON_CACHE.has(idNumero)) return POKEMON_CACHE.get(idNumero);

  const data = await fetchJson(`${POKEAPI_BASE}/pokemon/${idNumero}`);
  if (!data) return null;

  const tipos = (data.types || []).map((t) => t?.type?.name).filter(Boolean);
  const artwork = data?.sprites?.other?.['official-artwork']?.front_default;

  const pokemon = {
    id: data.id,
    numero_pokedex: data.id,
    nombre: (data.name || '').charAt(0).toUpperCase() + (data.name || '').slice(1),
    tipo_1: tipos[0] || null,
    tipo_2: tipos[1] || null,
    altura_dm: data.height || 0,
    peso_hectogramos: data.weight || 0,
    experiencia_base: data.base_experience || 0,
    es_legendario: LEGENDARIOS_SET.has(data.id) ? 1 : 0,
    url_imagen_oficial: artwork || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${data.id}.png`,
    url_imagen_frontal: data?.sprites?.front_default || null,
    url_imagen_trasera: data?.sprites?.back_default || null,
  };

  POKEMON_CACHE.set(idNumero, pokemon);
  return pokemon;
}

async function fetchWithConcurrency(items, limit, fn) {
  const results = [];
  let index = 0;

  const workers = new Array(limit).fill(null).map(async () => {
    while (index < items.length) {
      const currentIndex = index++;
      const item = items[currentIndex];
      const result = await fn(item);
      if (result) results.push(result);
    }
  });

  await Promise.all(workers);
  return results;
}

async function obtenerPokemonesPorIds(ids, maxWorkers = 12) {
  const results = await fetchWithConcurrency(ids, maxWorkers, obtenerPokemonPokeapi);
  return results.sort((a, b) => a.id - b.id);
}

// Simulador de Axios: devuelven objetos { data: { exitoso, ... } }
export const pokemonService = {
  obtenerTodos: async (pagina = 1, limiteQuery = 20) => {
    let limite = Number(limiteQuery || 20);
    if (!Number.isFinite(limite) || limite <= 0) limite = 20;
    limite = Math.min(limite, MAX_PAGE_LIMIT);

    const total = await obtenerTotalPokemones();
    const totalPaginas = Math.max(1, Math.ceil(total / limite));
    const offset = (pagina - 1) * limite;

    const ids = [];
    if (offset < total) {
      const fin = Math.min(offset + limite, total);
      for (let i = offset + 1; i <= fin; i += 1) {
        ids.push(i);
      }
    }

    const pokemones = await obtenerPokemonesPorIds(ids, 10);
    
    return {
      data: {
        exitoso: true,
        total_registros: total,
        pagina_actual: pagina,
        total_paginas: totalPaginas,
        cantidad_en_pagina: pokemones.length,
        datos: pokemones,
      }
    };
  },

  obtenerPorId: async (id) => {
    const pokemon = await obtenerPokemonPokeapi(id);
    if (!pokemon) {
      throw new Error('Pokemon no encontrado');
    }
    return { data: { exitoso: true, datos: pokemon } };
  },

  obtenerPorTipo: async (tipo) => {
    const tipoNormalizado = (tipo || '').toLowerCase();
    const data = await fetchJson(`${POKEAPI_BASE}/type/${tipoNormalizado}`);

    if (!data) {
      throw new Error('Tipo no encontrado');
    }

    const total = await obtenerTotalPokemones();
    const ids = new Set();
    for (const entry of data.pokemon || []) {
      const id = extractIdFromUrl(entry?.pokemon?.url);
      if (id && id <= total) ids.add(id);
    }

    const pokemones = await obtenerPokemonesPorIds(Array.from(ids), 10);
    return {
      data: {
        exitoso: true,
        tipo: tipoNormalizado,
        cantidad: pokemones.length,
        datos: pokemones,
      }
    };
  },

  obtenerLegendarios: async () => {
    const total = await obtenerTotalPokemones();
    const ids = LEGENDARIOS_IDS.filter((id) => id <= total);
    const pokemones = await obtenerPokemonesPorIds(ids, 12);
    return {
      data: {
        exitoso: true,
        tipo: 'legendarios',
        cantidad: pokemones.length,
        datos: pokemones,
      }
    };
  },

  obtenerEstadisticas: async () => {
    if (ESTADISTICAS_CACHE) {
      return { data: ESTADISTICAS_CACHE };
    }

    const total = await obtenerTotalPokemones();
    const sampleSize = Math.min(STATS_SAMPLE_SIZE, total);
    const ids = Array.from({ length: sampleSize }, (_, idx) => idx + 1);
    const pokemones = await obtenerPokemonesPorIds(ids, 10);

    if (pokemones.length === 0) {
      throw new Error('No se pudieron calcular estadisticas');
    }

    const legendariosCount = LEGENDARIOS_IDS.filter((id) => id <= total).length;
    const alturaPromedio = pokemones.reduce((sum, p) => sum + (p.altura_dm || 0), 0) / pokemones.length;
    const pesoPromedio = pokemones.reduce((sum, p) => sum + (p.peso_hectogramos || 0), 0) / pokemones.length;
    const expPromedio = pokemones.reduce((sum, p) => sum + (p.experiencia_base || 0), 0) / pokemones.length;

    ESTADISTICAS_CACHE = {
      exitoso: true,
      total_pokemones: total,
      pokemones_legendarios: legendariosCount,
      cantidad_tipos: 18,
      altura_promedio_dm: Number(alturaPromedio.toFixed(2)),
      peso_promedio_hg: Number(pesoPromedio.toFixed(2)),
      experiencia_base_promedio: Number(expPromedio.toFixed(2)),
      distribucion_tipos: {},
      nota: `Promedios calculados sobre una muestra de ${sampleSize} Pokemon`,
    };

    return { data: ESTADISTICAS_CACHE };
  },

  obtenerTipos: async () => {
    if (TIPOS_CACHE) {
      return { data: TIPOS_CACHE };
    }

    const data = await fetchJson(`${POKEAPI_BASE}/type?limit=1000`);
    if (!data) {
      throw new Error('No se pudieron obtener tipos');
    }

    const total = await obtenerTotalPokemones();
    const tiposData = {};

    for (const tipo of data.results || []) {
      const nombreTipo = tipo?.name;
      if (!nombreTipo) continue;

      const tipoDetalle = await fetchJson(`${POKEAPI_BASE}/type/${nombreTipo}`);
      if (!tipoDetalle) continue;

      const ids = new Set();
      for (const entrada of tipoDetalle.pokemon || []) {
        const id = extractIdFromUrl(entrada?.pokemon?.url);
        if (id && id <= total) ids.add(id);
      }

      tiposData[nombreTipo] = ids.size;
    }

    TIPOS_CACHE = {
      exitoso: true,
      cantidad_tipos: Object.keys(tiposData).length,
      datos: tiposData,
    };

    return { data: TIPOS_CACHE };
  },

  obtenerInfo: async () => {
    return {
      data: {
        mensaje: 'API Pokemon Direct (Client-Side)',
        descripcion: 'Sistema de gestion de Pokemon sin servidor',
      }
    };
  },
};

export default pokemonService;
