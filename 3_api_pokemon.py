"""
API REST para consultar datos de Pokémon
Etapa 3: API con Flask - Consumiendo directamente PokeAPI v2
Soporta Pokémon de todas las generaciones (sin base de datos).
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import requests
import os

app = Flask(__name__)
CORS(app)

POKEAPI_BASE = "https://pokeapi.co/api/v2"
REQUEST_TIMEOUT = 8
MAX_PAGE_LIMIT = 100

# Lista amplia de legendarios + míticos (todas las generaciones principales).
LEGENDARIOS_IDS = sorted(set([
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
]))
LEGENDARIOS_SET = set(LEGENDARIOS_IDS)

# Cachés en memoria para acelerar respuestas
POKEMON_CACHE = {}
TOTAL_POKEMON_CACHE = None
ESTADISTICAS_CACHE = None
TIPOS_CACHE = None


def extraer_id_desde_url(url):
    """Extrae el ID numérico desde una URL de PokeAPI."""
    try:
        return int(url.rstrip('/').split('/')[-1])
    except Exception:
        return None


def obtener_total_pokemones():
    """Obtiene cantidad total de especies Pokémon disponibles en PokeAPI."""
    global TOTAL_POKEMON_CACHE

    if TOTAL_POKEMON_CACHE is not None:
        return TOTAL_POKEMON_CACHE

    try:
        resp = requests.get(f"{POKEAPI_BASE}/pokemon-species?limit=1", timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            TOTAL_POKEMON_CACHE = int(resp.json().get('count', 1025))
            return TOTAL_POKEMON_CACHE
    except Exception:
        pass

    TOTAL_POKEMON_CACHE = 1025
    return TOTAL_POKEMON_CACHE


def obtener_pokemon_pokeapi(id_numero):
    """Obtiene un Pokémon desde PokeAPI por ID."""
    if id_numero <= 0:
        return None

    if id_numero in POKEMON_CACHE:
        return POKEMON_CACHE[id_numero]

    try:
        resp = requests.get(f"{POKEAPI_BASE}/pokemon/{id_numero}", timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return None

        data = resp.json()
        tipos = [t['type']['name'] for t in data.get('types', [])]

        artwork = (
            data.get('sprites', {})
            .get('other', {})
            .get('official-artwork', {})
            .get('front_default')
        )

        pokemon = {
            'id': data['id'],
            'numero_pokedex': data['id'],
            'nombre': data['name'].capitalize(),
            'tipo_1': tipos[0] if len(tipos) > 0 else None,
            'tipo_2': tipos[1] if len(tipos) > 1 else None,
            'altura_dm': data.get('height', 0),
            'peso_hectogramos': data.get('weight', 0),
            'experiencia_base': data.get('base_experience') or 0,
            'es_legendario': 1 if data['id'] in LEGENDARIOS_SET else 0,
            'url_imagen_oficial': artwork or (
                f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png"
            ),
            'url_imagen_frontal': data.get('sprites', {}).get('front_default'),
            'url_imagen_trasera': data.get('sprites', {}).get('back_default'),
        }

        POKEMON_CACHE[id_numero] = pokemon
        return pokemon
    except Exception as err:
        print(f"Error obteniendo Pokémon {id_numero}: {err}")
        return None


def obtener_pokemones_por_ids(ids, max_workers=20):
    """Obtiene varios Pokémon en paralelo para mejorar tiempos de respuesta."""
    resultados = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(obtener_pokemon_pokeapi, pokemon_id): pokemon_id for pokemon_id in ids}
        for future in as_completed(futures):
            pokemon = future.result()
            if pokemon:
                resultados.append(pokemon)

    resultados.sort(key=lambda p: p['id'])
    return resultados


@app.route('/', methods=['GET'])
def inicio():
    """Endpoint raíz con información de la API."""
    return jsonify({
        'mensaje': 'API de Pokémon v2.0 - PokeAPI Direct',
        'descripcion': 'Sistema de gestión de Pokémon sin base de datos (todas las generaciones)',
        'endpoints': {
            'GET /api/pokemones': 'Obtener todos los Pokémones (paginado)',
            'GET /api/pokemones/<id>': 'Obtener Pokémon por ID',
            'GET /api/pokemones/tipo/<tipo>': 'Filtrar por tipo',
            'GET /api/pokemones/legendarios': 'Solo Pokémones legendarios/míticos',
            'GET /api/estadisticas': 'Estadísticas generales',
            'GET /api/tipos': 'Listar tipos disponibles',
        }
    })


@app.route('/api/pokemones', methods=['GET'])
def obtener_pokemones():
    """Obtiene lista de todos los Pokémones con paginación."""
    try:
        pagina = max(1, request.args.get('pagina', 1, type=int))
        limite = request.args.get('limite', 20, type=int)
        limite = 20 if limite is None else max(1, min(limite, MAX_PAGE_LIMIT))

        total = obtener_total_pokemones()
        total_paginas = max(1, math.ceil(total / limite))
        offset = (pagina - 1) * limite

        pokemones = []
        if offset < total:
            fin = min(offset + limite, total)
            for i in range(offset + 1, fin + 1):
                pokemon = obtener_pokemon_pokeapi(i)
                if pokemon:
                    pokemones.append(pokemon)

        return jsonify({
            'exitoso': True,
            'total_registros': total,
            'pagina_actual': pagina,
            'total_paginas': total_paginas,
            'cantidad_en_pagina': len(pokemones),
            'datos': pokemones,
        })
    except Exception as err:
        return jsonify({'exitoso': False, 'error': str(err)}), 500


@app.route('/api/pokemones/<int:pokemon_id>', methods=['GET'])
def obtener_pokemon(pokemon_id):
    """Obtiene un Pokémon específico por ID."""
    try:
        if pokemon_id < 1:
            return jsonify({'exitoso': False, 'error': 'Pokémon no encontrado'}), 404

        pokemon = obtener_pokemon_pokeapi(pokemon_id)
        if pokemon:
            return jsonify({'exitoso': True, 'datos': pokemon})

        return jsonify({'exitoso': False, 'error': 'Pokémon no encontrado'}), 404
    except Exception as err:
        return jsonify({'exitoso': False, 'error': str(err)}), 500


@app.route('/api/pokemones/tipo/<tipo>', methods=['GET'])
def filtrar_por_tipo(tipo):
    """Filtra Pokémones por tipo."""
    try:
        tipo = tipo.lower()
        resp = requests.get(f"{POKEAPI_BASE}/type/{tipo}", timeout=REQUEST_TIMEOUT)

        if resp.status_code != 200:
            return jsonify({'exitoso': False, 'error': 'Tipo no encontrado'}), 404

        data = resp.json()
        total = obtener_total_pokemones()
        ids_unicos = set()
        pokemones_del_tipo = []

        for pokemon_data in data.get('pokemon', []):
            id_pokemon = extraer_id_desde_url(pokemon_data.get('pokemon', {}).get('url', ''))
            if not id_pokemon or id_pokemon > total or id_pokemon in ids_unicos:
                continue

            ids_unicos.add(id_pokemon)
            pokemon = obtener_pokemon_pokeapi(id_pokemon)
            if pokemon:
                pokemones_del_tipo.append(pokemon)

        pokemones_del_tipo.sort(key=lambda p: p['id'])
        return jsonify({
            'exitoso': True,
            'tipo': tipo,
            'cantidad': len(pokemones_del_tipo),
            'datos': pokemones_del_tipo,
        })
    except Exception as err:
        return jsonify({'exitoso': False, 'error': str(err)}), 500


@app.route('/api/pokemones/legendarios', methods=['GET'])
def obtener_legendarios():
    """Obtiene Pokémones legendarios y míticos de todas las generaciones."""
    try:
        total = obtener_total_pokemones()
        ids_legendarios = [pokemon_id for pokemon_id in LEGENDARIOS_IDS if pokemon_id <= total]
        pokemones = obtener_pokemones_por_ids(ids_legendarios, max_workers=12)

        return jsonify({
            'exitoso': True,
            'tipo': 'legendarios',
            'cantidad': len(pokemones),
            'datos': pokemones,
        })
    except Exception as err:
        return jsonify({'exitoso': False, 'error': str(err)}), 500


@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """Obtiene estadísticas generales del dataset completo."""
    global ESTADISTICAS_CACHE

    try:
        refresh = request.args.get('refresh', 'false').lower() == 'true'
        if ESTADISTICAS_CACHE is not None and not refresh:
            return jsonify(ESTADISTICAS_CACHE)

        total = obtener_total_pokemones()

        # Precarga en paralelo los que falten en caché para cálculos globales.
        ids_faltantes = [i for i in range(1, total + 1) if i not in POKEMON_CACHE]
        if ids_faltantes:
            chunk_size = 200
            for i in range(0, len(ids_faltantes), chunk_size):
                chunk = ids_faltantes[i:i + chunk_size]
                obtener_pokemones_por_ids(chunk, max_workers=20)

        pokemones = [POKEMON_CACHE[i] for i in range(1, total + 1) if i in POKEMON_CACHE]
        if not pokemones:
            return jsonify({'exitoso': False, 'error': 'No se pudieron calcular estadísticas'}), 500

        legendarios_count = sum(1 for p in pokemones if p['es_legendario'])
        altura_promedio = sum(p['altura_dm'] for p in pokemones) / len(pokemones)
        peso_promedio = sum(p['peso_hectogramos'] for p in pokemones) / len(pokemones)
        exp_promedio = sum(p['experiencia_base'] for p in pokemones) / len(pokemones)

        tipos_count = {}
        for pokemon in pokemones:
            if pokemon['tipo_1']:
                tipos_count[pokemon['tipo_1']] = tipos_count.get(pokemon['tipo_1'], 0) + 1
            if pokemon['tipo_2']:
                tipos_count[pokemon['tipo_2']] = tipos_count.get(pokemon['tipo_2'], 0) + 1

        ESTADISTICAS_CACHE = {
            'exitoso': True,
            'total_pokemones': total,
            'pokemones_legendarios': legendarios_count,
            'cantidad_tipos': len(tipos_count),
            'altura_promedio_dm': round(altura_promedio, 2),
            'peso_promedio_hg': round(peso_promedio, 2),
            'experiencia_base_promedio': round(exp_promedio, 2),
            'distribucion_tipos': tipos_count,
        }
        return jsonify(ESTADISTICAS_CACHE)
    except Exception as err:
        return jsonify({'exitoso': False, 'error': str(err)}), 500


@app.route('/api/tipos', methods=['GET'])
def obtener_tipos():
    """Obtiene lista de tipos y cantidad de Pokémones por tipo (todas las generaciones)."""
    global TIPOS_CACHE

    try:
        refresh = request.args.get('refresh', 'false').lower() == 'true'
        if TIPOS_CACHE is not None and not refresh:
            return jsonify(TIPOS_CACHE)

        resp = requests.get(f"{POKEAPI_BASE}/type?limit=1000", timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return jsonify({'exitoso': False, 'error': 'No se pudieron obtener tipos'}), 500

        total = obtener_total_pokemones()
        tipos_data = {}
        for tipo in resp.json().get('results', []):
            nombre_tipo = tipo.get('name')
            if not nombre_tipo:
                continue

            try:
                tipo_resp = requests.get(f"{POKEAPI_BASE}/type/{nombre_tipo}", timeout=REQUEST_TIMEOUT)
                if tipo_resp.status_code != 200:
                    continue

                tipo_json = tipo_resp.json()
                ids_tipo = set()
                for entrada in tipo_json.get('pokemon', []):
                    pokemon_url = entrada.get('pokemon', {}).get('url', '')
                    pokemon_id = extraer_id_desde_url(pokemon_url)
                    if pokemon_id and pokemon_id <= total:
                        ids_tipo.add(pokemon_id)

                tipos_data[nombre_tipo] = len(ids_tipo)
            except Exception:
                continue

        TIPOS_CACHE = {
            'exitoso': True,
            'cantidad_tipos': len(tipos_data),
            'datos': tipos_data,
        }
        return jsonify(TIPOS_CACHE)
    except Exception as err:
        return jsonify({'exitoso': False, 'error': str(err)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("API POKÉMON v2.0 - Todas las generaciones")
    print("=" * 60)
    print("Conectando a PokeAPI...")
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')

    print(f"Corriendo en http://{host}:{port}")
    print("CORS habilitado para React frontend")
    print("=" * 60)
    app.run(host=host, port=port, debug=debug_mode)
