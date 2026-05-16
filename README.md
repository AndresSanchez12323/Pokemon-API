# 🐍 Pokédex: Aplicación Completa (PokeAPI + Flask + React)

## 📋 Descripción

Sistema completo de Pokédex que **consume directamente PokeAPI v2 sin base de datos**. Incluye:
- Backend REST API con Flask
- Frontend interactivo con React
- Dashboard de visualización con Plotly
- Scripts de demostración

```
┌─────────────────┐
│   PokeAPI v2    │
│  (Oficial)      │
└────────┬────────┘
         │
┌────────▼────────────────┐
│    Flask API (Caché)    │  ← Backend
│  :5000/api/pokemones    │
└────────┬────────────────┘
         │
    ┌────┴────┐
    │          │
┌───▼──┐  ┌───▼──┐
│React │  │HTML  │  ← Frontend + Dashboard
│:3001 │  │Plotly│
└──────┘  └──────┘
```

## 🚀 Inicio Rápido (3 pasos)

### Paso 1: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 2: Iniciar Backend (Terminal 1)

```bash
python 3_api_pokemon.py
```

Verás: `* Running on http://localhost:5000`

### Paso 3: Iniciar Frontend (Terminal 2)

```bash
cd frontend
pnpm install
pnpm start
```

Verás: `webpack compiled successfully` → Abre [http://localhost:3001](http://localhost:3001)
Nota: se usa `pnpm` como gestor de paquetes.

**¡Listo!** 🎉 Tu Pokédex está funcionando

---

## 📦 ¿Qué incluye?

### Backend Flask (3_api_pokemon.py)

**7 Endpoints disponibles:**

```
GET  /api/pokemones                    → Lista paginada (20/50/100 por página)
GET  /api/pokemones/<id>              → Detalle de 1 Pokémon
GET  /api/pokemones/tipo/<tipo>       → Filtrar por tipo (fire, water, etc)
GET  /api/pokemones/legendarios       → Solo los 20 legendarios
GET  /api/estadisticas                → Stats globales (altura prom, etc)
GET  /api/tipos                       → Lista de tipos con conteos
GET  /                                → Info de la API
```

**Data por Pokémon:**

```json
{
  "id": 25,
  "numero_pokedex": 25,
  "nombre": "Pikachu",
  "tipo_1": "electric",
  "tipo_2": null,
  "altura_dm": 4,
  "peso_hectogramos": 60,
  "experiencia_base": 112,
  "es_legendario": 0,
  "url_imagen_oficial": "https://raw.githubusercontent.com/...",
  "url_imagen_frontal": "...",
  "url_imagen_trasera": "..."
}
```

### Frontend React (localhost:3001)

**6 Páginas:**

1. **🏠 Inicio** - Resumen de estadísticas
2. **📚 Pokédex** - Lista paginable + búsqueda
3. **👁️ Detalle** - Info completa + imágenes
4. **🎨 Tipos** - Filtrar por tipo
5. **⭐ Legendarios** - Solo los especiales
6. **📊 Estadísticas** - Dashboard completo

**Características:**
- ✅ Imágenes de PokeAPI
- ✅ Búsqueda en tiempo real
- ✅ Paginación inteligente
- ✅ Responsive (móvil+desktop)
- ✅ Estadísticas en vivo

### Dashboard Plotly (Opcional)

Generar 10 gráficos HTML:

```bash
python 4_dashboard_pokemon.py
```

Crea archivos como:
- `01_distribucion_tipos.html`
- `02_altura_vs_peso.html`
- `09_dashboard_general.html`
- etc...

---

## 🔌 API REST Ejemplos

### Obtener lista paginada

```bash
curl "http://localhost:5000/api/pokemones?pagina=1&limite=20"
```

### Obtener Pokémon específico

```bash
curl "http://localhost:5000/api/pokemones/25"
```

### Filtrar por tipo

```bash
curl "http://localhost:5000/api/pokemones/tipo/fire"
```

### Legendarios

```bash
curl "http://localhost:5000/api/pokemones/legendarios"
```

### Estadísticas

```bash
curl "http://localhost:5000/api/estadisticas"
```

---

## 📁 Estructura

```
.
├── 3_api_pokemon.py            ← BACKEND (Inicia aquí)
├── frontend/
│   ├── src/
│   │   ├── pages/              → 6 páginas React
│   │   ├── components/         → Componentes reutilizables
│   │   ├── services/           → API calls (pokemonService.js)
│   │   └── App.js              → Router principal
│   ├── package.json
│   └── ...
├── 4_dashboard_pokemon.py       ← Dashboard (opcional)
├── 1_obtener_datos_pokemon.py  ← Demo descarga
├── 2_procesar_datos.py         ← Demo procesamiento
├── requirements.txt             → Dependencias Python
└── README.md                    ← Este archivo
```

---

## 🛠️ Instalación Detallada

### Requisitos previos

- Python 3.8+
- Node.js 14+ (para React)
- Conexión a internet

### Backend

```bash
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. Ejecutar backend
python 3_api_pokemon.py
# Esperado: * Running on http://localhost:5000
```

### Frontend

```bash
# 1. Ir a carpeta frontend
cd frontend

# 2. Instalar dependencias Node
pnpm install

# 3. Iniciar desarrollo
pnpm start
# Esperado: Local: http://localhost:3001
```

---

## 🎯 Scripts Auxiliares

### Ver datos de ejemplo

```bash
python 1_obtener_datos_pokemon.py
# Genera: pokemones_muestra.json
```

### Procesar datos internos

```bash
python 2_procesar_datos.py
# Genera: pokemones_procesados.json, estadisticas.json
```

### Generar dashboard Plotly

```bash
python 4_dashboard_pokemon.py
# Genera: 01_distribucion_tipos.html, etc...
```

### Validar sistema

```bash
python validar_sistema.py
# Verifica: archivos, dependencias, API, frontend
```

---

## 📊 Datos

**150 Pokémon** de generación I (Kanto)

Campos por Pokémon:
- Número Pokédex (1-150)
- Nombre
- Tipos (principal + secundario)
- Altura (decímetros)
- Peso (hectogramos)
- Experiencia base
- ¿Legendario?
- Imágenes (oficial, frente, atrás)

**20 Legendarios identificados:**
94, 145, 146, 149, 150, 151, 243, 244, 245, 249, 250, 251, 384, 483, 484, 487, 643, 644, 645, 646

---

## 🔧 Tecnologías

| Componente | Tecnología | Versión |
|---|---|---|
| **Backend API** | Flask | 3.0+ |
| **Frontend Web** | React | 18.2+ |
| **HTTP Client** | Axios | 1.3+ |
| **Datos**| PokeAPI v2 | - |
| **Visualización** | Plotly | 5.17+ |
| **Router** | React Router | 6.8+ |
| **Icons** | React Icons | 4.7+ |

---

## ⚡ Performance

- **Caché en memoria** en Backend (respuestas más rápidas)
- **Paginación** en frontend (carga optimizada)
- **Lazy loading** de imágenes
- **JSON comprimido** desde API

Tiempos típicos:
- Primera carga API: ~1-2s (150 Pokémon)
- Siguiente: <100ms (caché)
- UI interactiva: <300ms

---

## 🐛 Solución de problemas

### Backend no inicia

```
Error: [Errno 10048] Only one usage of each socket address...
```

↳ Puerto 5000 en uso. Solución:
```bash
# Limpiar sesión anterior
taskkill /IM python.exe /F
# O cambiar puerto en código
```

### Frontend no conecta

Verifica:
1. Backend corriendo: `http://localhost:5000`
2. CORS habilitado: Mira consola F12
3. Network tab: ve si `/api/pokemones` responde

### Imágenes no cargan

Normal si:
- PokeAPI CDN lento
- Conexión internet deficiente

Sistema usa fallback:
- GitHub sprite repository si falla
- Muestra "Pikachu genérico" si ambas fallan

---

## 📚 Conceptos Implementados

✅ **Consumo de API REST** (PokeAPI v2)
✅ **Backend REST** (Flask + CORS)
✅ **Frontend SPA** (React Router)
✅ **State management** (Hooks: useState, useEffect)
✅ **Async/await** y Promises
✅ **Error handling** (try/catch)
✅ **Paginación**
✅ **Filtrado en tiempo real**
✅ **Visualización de datos** (Plotly)
✅ **Caché en memoria**

---

## 🎓 Aprendizaje

Este proyecto es excelente para entender:

- Cómo funciona una API REST completa
- Arquitectura de aplicaciones web modernas
- React hooks y gestión de estado
- Consumo de APIs externas
- Diseño responsive
- Visualización de datos

---

## 📞 Soporte

Para issues/preguntas:

1. Mira la sección "Solución de problemas"
2. Verifica que todos los servicios estén corriendo
3. Revisa los logs en terminal
4. Limpia caché: `Ctrl+Shift+R` en browser

---

## 📄 Licencia

Proyecto educativo - Uso libre

---

