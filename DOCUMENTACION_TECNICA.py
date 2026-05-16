#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DOCUMENTACION TECNICA - SISTEMA POKEMON
PokeAPI + Flask + React + Dashboard Plotly

Fecha: Marzo 2026
Version: 2.0 (sin base de datos)
"""

print("""
╔═══════════════════════════════════════════════════════════════╗
║                 DOCUMENTACION TECNICA                        ║
║         Sistema Pokemon: PokeAPI + Flask + React             ║
╚═══════════════════════════════════════════════════════════════╝

DESCRIPCION GENERAL
───────────────────
Sistema completo de Pokédex que:
1. Consume datos en tiempo real desde PokeAPI v2
2. Expone una API REST con Flask (proxy con caché en memoria)
3. Muestra un frontend interactivo con React
4. Genera visualizaciones con Plotly (opcional)

No se requiere base de datos. Toda la información se obtiene
directamente desde https://pokeapi.co/api/v2/

ARQUITECTURA
────────────

┌─────────────────────────────────────────────────────────────┐
│                  ARQUITECTURA DEL SISTEMA                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  POKEAPI v2 (https://pokeapi.co/api/v2/)                  │
│           ↓                                                 │
│  [3_api_pokemon.py] - Flask Backend                        │
│  - Proxy con caché en memoria (dict)                       │
│  - Soporte 1025 Pokémones (todas las generaciones)         │
│  - Carga paralela con ThreadPoolExecutor(max=20)           │
│  - 7 endpoints REST                                        │
│           ↓                                                 │
│  [frontend/src/] - React Frontend                          │
│  - Puerto :3001                                            │
│  - React Router 6 (5 páginas)                              │
│  - Axios para consumir la API                              │
│           ↓                                                 │
│  [4_dashboard_pokemon.py] - OPCIONAL                       │
│  - Plotly: 10 gráficos HTML interactivos                   │
│  - Consume la API Flask                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

ESTRUCTURA DE ARCHIVOS
──────────────────────

API/
├── 3_api_pokemon.py          ← Backend principal (EJECUTAR PRIMERO)
├── 1_obtener_datos_pokemon.py ← Demo de consumo de PokeAPI
├── 2_procesar_datos.py        ← Demo de procesamiento de datos
├── 4_dashboard_pokemon.py     ← Dashboard Plotly (opcional)
├── config.py                  ← Configuracion (API_POKEMON_BASE)
├── requirements.txt           ← Dependencias Python
├── validar_sistema.py         ← Verificacion del sistema
└── frontend/                 ← Aplicacion React
    ├── package.json
    └── src/
        ├── App.js
        ├── services/pokemonService.js  ← Cliente Axios
        ├── pages/                      ← Paginas React
        └── components/                 ← Componentes reutilizables

ENDPOINTS API (3_api_pokemon.py)
─────────────────────────────────

Puerto: 5000

1. GET /
   Informacion de la API y endpoints disponibles

2. GET /api/pokemones?pagina=1&limite=20
   Lista paginada. Max 100 por pagina. Total: 1025

3. GET /api/pokemones/<id>
   Pokemon por ID (1 - 1025)
   Respuesta: {exitoso, datos:{nombre, tipos, imagen, ...}}

4. GET /api/pokemones/legendarios
   98 Pokémon legendarios/miticos de todas las generaciones

5. GET /api/pokemones/tipo/<tipo>
   Filtrar por tipo (fire, water, grass, etc.)

6. GET /api/estadisticas
   Estadísticas globales (lento primera vez ~60s, luego cache)

7. GET /api/tipos
   Tipos disponibles con conteo de Pokémones por tipo

SISTEMA DE CACHE EN MEMORIA
────────────────────────────

El backend tiene 4 cachés en dict Python:
- POKEMON_CACHE       : por ID, permanente
- ESTADISTICAS_CACHE  : datos globales
- TIPOS_CACHE         : distribución de tipos
- total_pokemones     : conteo total (1025)

Primera carga de /api/estadisticas puede tardar ~60s.
Las siguientes llamadas responden en <100ms.

LEGENDARIOS SOPORTADOS
───────────────────────

98 Pokémones legendarios y miticos de Gen I a Gen IX:
- Gen I:   Articuno, Zapdos, Moltres, Mewtwo, Mew
- Gen II:  Raikou, Entei, Suicune, Lugia, Ho-Oh, Celebi
- Gen III: Regirock, Regice, Registeel, Latias, Latios, Kyogre,
           Groudon, Rayquaza, Jirachi, Deoxys
- Gen IV:  Uxie, Mesprit, Azelf, Dialga, Palkia, Heatran,
           Regigigas, Giratina, Cresselia, Phione, Manaphy,
           Darkrai, Shaymin, Arceus
- Gen V:   Victini, Cobalion, Terrakion, Virizion, Tornadus,
           Thundurus, Reshiram, Zekrom, Landorus, Kyurem,
           Keldeo, Meloetta, Genesect
- Gen VI:  Xerneas, Yveltal, Zygarde, Diancie, Hoopa, Volcanion
- Gen VII: Type: Null, Silvally, Tapus, Solgaleo, Lunala,
           Nihilego, Necrozma, Magearna, Marshadow, Zeraora
- Gen VIII: Zacian, Zamazenta, Eternatus, Kubfu, Urshifu,
            Zarude, Regis, Calyrex, Glastrier, Spectrier
- Gen IX:  Koraidon, Miraidon, Wo-Chien, Chien-Pao, Ting-Lu,
           Chi-Yu, Ogerpon, Terapagos, Pecharunt

DEPENDENCIAS
────────────

Python (requirements.txt):
- flask==3.0.0
- flask-cors==4.0.0
- requests==2.31.0
- pandas==2.1.3
- plotly==5.17.0
- python-dotenv==1.0.0

Node.js (frontend/package.json):
- react 18.2
- react-router-dom 6.8
- axios

REQUISITOS TECNICOS
───────────────────

- Python 3.8+
- Node.js 16+
- Conexion a Internet (PokeAPI)
- RAM: 512 MB minimo
- NO requiere MySQL, SQLite ni ninguna base de datos

EJECUCION
─────────

Terminal 1:  python 3_api_pokemon.py
Terminal 2:  cd frontend && pnpm start
Navegador:   http://localhost:3001

""")
