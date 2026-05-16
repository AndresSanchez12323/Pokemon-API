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

async function obtenerPokemones(req, res) {
  const pagina = Math.max(1, Number(req.query.pagina || 1));
  let limite = Number(req.query.limite || 20);
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

  res.status(200).json({
    exitoso: true,
    total_registros: total,
    pagina_actual: pagina,
    total_paginas: totalPaginas,
    cantidad_en_pagina: pokemones.length,
    datos: pokemones,
  });
}

async function obtenerPokemonPorId(id, res) {
  const pokemon = await obtenerPokemonPokeapi(id);
  if (!pokemon) {
    res.status(404).json({ exitoso: false, error: 'Pokemon no encontrado' });
    return;
  }

  res.status(200).json({ exitoso: true, datos: pokemon });
}

async function obtenerLegendarios(res) {
  const total = await obtenerTotalPokemones();
  const ids = LEGENDARIOS_IDS.filter((id) => id <= total);
  const pokemones = await obtenerPokemonesPorIds(ids, 12);

  res.status(200).json({
    exitoso: true,
    tipo: 'legendarios',
    cantidad: pokemones.length,
    datos: pokemones,
  });
}

async function obtenerPorTipo(tipo, res) {
  const tipoNormalizado = (tipo || '').toLowerCase();
  const data = await fetchJson(`${POKEAPI_BASE}/type/${tipoNormalizado}`);

  if (!data) {
    res.status(404).json({ exitoso: false, error: 'Tipo no encontrado' });
    return;
  }

  const total = await obtenerTotalPokemones();
  const ids = new Set();
  for (const entry of data.pokemon || []) {
    const id = extractIdFromUrl(entry?.pokemon?.url);
    if (id && id <= total) ids.add(id);
  }

  const pokemones = await obtenerPokemonesPorIds(Array.from(ids), 10);
  res.status(200).json({
    exitoso: true,
    tipo: tipoNormalizado,
    cantidad: pokemones.length,
    datos: pokemones,
  });
}

async function obtenerTipos(req, res) {
  const refresh = String(req.query.refresh || 'false').toLowerCase() === 'true';
  if (TIPOS_CACHE && !refresh) {
    res.status(200).json(TIPOS_CACHE);
    return;
  }

  const data = await fetchJson(`${POKEAPI_BASE}/type?limit=1000`);
  if (!data) {
    res.status(500).json({ exitoso: false, error: 'No se pudieron obtener tipos' });
    return;
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

  res.status(200).json(TIPOS_CACHE);
}

async function obtenerEstadisticas(req, res) {
  const refresh = String(req.query.refresh || 'false').toLowerCase() === 'true';
  if (ESTADISTICAS_CACHE && !refresh) {
    res.status(200).json(ESTADISTICAS_CACHE);
    return;
  }

  const total = await obtenerTotalPokemones();
  const sampleSize = Math.min(STATS_SAMPLE_SIZE, total);
  const ids = Array.from({ length: sampleSize }, (_, idx) => idx + 1);
  const pokemones = await obtenerPokemonesPorIds(ids, 10);

  if (pokemones.length === 0) {
    res.status(500).json({ exitoso: false, error: 'No se pudieron calcular estadisticas' });
    return;
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

  res.status(200).json(ESTADISTICAS_CACHE);
}

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    res.status(405).json({ exitoso: false, error: 'Metodo no permitido' });
    return;
  }

  const pathParam = req.query.path || [];
  const segments = Array.isArray(pathParam) ? pathParam : [pathParam];

  if (segments.length === 0 || segments[0] === '') {
    res.status(200).json({
      mensaje: 'API Pokemon v2.0 - PokeAPI Direct',
      descripcion: 'Sistema de gestion de Pokemon sin base de datos',
      endpoints: {
        'GET /api/pokemones': 'Obtener todos los Pokemon (paginado)',
        'GET /api/pokemones/<id>': 'Obtener Pokemon por ID',
        'GET /api/pokemones/tipo/<tipo>': 'Filtrar por tipo',
        'GET /api/pokemones/legendarios': 'Solo Pokemon legendarios/miticos',
        'GET /api/estadisticas': 'Estadisticas generales',
        'GET /api/tipos': 'Listar tipos disponibles',
      },
    });
    return;
  }

  const [resource, second, third] = segments;

  try {
    if (resource === 'pokemones') {
      if (!second) {
        await obtenerPokemones(req, res);
        return;
      }

      if (second === 'legendarios') {
        await obtenerLegendarios(res);
        return;
      }

      if (second === 'tipo' && third) {
        await obtenerPorTipo(third, res);
        return;
      }

      const pokemonId = Number(second);
      if (Number.isFinite(pokemonId)) {
        await obtenerPokemonPorId(pokemonId, res);
        return;
      }

      res.status(400).json({ exitoso: false, error: 'Ruta invalida' });
      return;
    }

    if (resource === 'estadisticas') {
      await obtenerEstadisticas(req, res);
      return;
    }

    if (resource === 'tipos') {
      await obtenerTipos(req, res);
      return;
    }

    res.status(404).json({ exitoso: false, error: 'Endpoint no encontrado' });
  } catch (error) {
    res.status(500).json({ exitoso: false, error: error?.message || 'Error interno' });
  }
}
