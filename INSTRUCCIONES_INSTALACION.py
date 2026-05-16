"""
Guía paso a paso para instalar y ejecutar el sistema de Pokémon
Este script proporciona instrucciones detalladas para todas las etapas
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║         GUÍA DE INSTALACIÓN - SISTEMA POKÉMON                 ║
║     PokeAPI + Flask API + React Frontend + Dashboard          ║
╚════════════════════════════════════════════════════════════════╝

ÍNDICE:
1. Requisitos previos
2. Instalar Python y Node.js
3. Configurar entorno e instalar dependencias
4. Ejecutar el sistema
5. Acceder a la aplicación

═══════════════════════════════════════════════════════════════════

PASO 1: REQUISITOS PREVIOS
───────────────────────────

Necesitará tener instalado:
• Python 3.8 o superior
• Node.js 16 o superior (para el frontend React)
• Un editor de código (VS Code, etc.)
• Conexión a Internet (para consultar PokeAPI)

Descargue desde:
• Python: https://www.python.org/downloads/
• Node.js: https://nodejs.org/

NO se requiere base de datos. Los datos se obtienen directamente
desde PokeAPI en tiempo real.

═══════════════════════════════════════════════════════════════════

PASO 2: VERIFICAR INSTALACIÓN
──────────────────────────────

En una terminal (CMD, PowerShell, etc.), ejecute:

    python --version
    node --version
    pnpm --version

Deben mostrar versiones sin errores.

═══════════════════════════════════════════════════════════════════

PASO 3: INSTALAR DEPENDENCIAS
──────────────────────────────

A. Dependencias Python (backend):

    pip install -r requirements.txt

   O manualmente:

    pip install requests pandas flask flask-cors plotly

B. Dependencias Node.js (frontend):

    cd frontend
    pnpm install

═══════════════════════════════════════════════════════════════════

PASO 4: EJECUTAR EL SISTEMA
────────────────────────────

Abra 2 terminales en la carpeta del proyecto.

>>> TERMINAL 1: INICIAR API FLASK (BACKEND)

    python 3_api_pokemon.py

    Esto iniciará:
    ✓ Servidor en http://localhost:5000
    ✓ Datos obtenidos directamente desde PokeAPI
    ✓ 7 endpoints REST disponibles

    Manténgalo corriendo en segundo plano.


>>> TERMINAL 2: INICIAR FRONTEND REACT

    cd frontend
    pnpm start

    Abrirá automáticamente: http://localhost:3000
    (o http://localhost:3001 si el puerto está ocupado)


>>> OPCIONAL: GENERAR DASHBOARD PLOTLY

    python 4_dashboard_pokemon.py

    Esto creará:
    ✓ 10 archivos HTML con gráficos Plotly interactivos
    ✓ Requiere que la API Flask esté corriendo

═══════════════════════════════════════════════════════════════════

PASO 5: ACCEDER A LOS RESULTADOS
──────────────────────────────────

A. Frontend React (aplicación principal):

    http://localhost:3001

B. API REST directa:

    http://localhost:5000/api/pokemones
    http://localhost:5000/api/pokemones/1
    http://localhost:5000/api/pokemones/legendarios
    http://localhost:5000/api/estadisticas
    http://localhost:5000/api/tipos

C. Dashboard (si ejecutó el paso opcional):

    09_dashboard_general.html   → Dashboard completo
    01_distribucion_tipos.html  → Tipos
    02_altura_vs_peso.html      → Scatter plot
    ... (10 archivos HTML en total)

═══════════════════════════════════════════════════════════════════

VALIDACIÓN DEL SISTEMA
──────────────────────

Para verificar que todo está correcto, ejecute:

    python validar_sistema.py

═══════════════════════════════════════════════════════════════════

SOLUCIÓN DE PROBLEMAS
─────────────────────

❌ "ModuleNotFoundError: No module named 'flask'"
   → pip install flask flask-cors

❌ "Connection refused port 5000"
   → Asegúrese de que la API esté corriendo
   → Use otra terminal: python 3_api_pokemon.py

❌ "pnpm: command not found"
    → Instale pnpm (https://pnpm.io/installation)

❌ Error de CORS en el navegador
   → Verifique que flask-cors esté instalado
   → pip install flask-cors

═══════════════════════════════════════════════════════════════════

RESUMEN RÁPIDO (TL;DR)
──────────────────────

Terminal 1:  python 3_api_pokemon.py
Terminal 2:  cd frontend && pnpm start
Navegador:   http://localhost:3001

""")
