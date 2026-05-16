"""
Script de validación del sistema
Verifica que todos los componentes están funcionando correctamente
(SIN base de datos - Consumiendo PokeAPI directamente)
"""

import os
import sys
import requests
import json

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN 1: ARCHIVOS DEL PROYECTO")
    print("=" * 60)
    
    archivos_requeridos = [
        '1_obtener_datos_pokemon.py',
        '2_procesar_datos.py',
        '3_api_pokemon.py',
        '4_dashboard_pokemon.py',
        'config.py',
        'requirements.txt',
        'README.md'
    ]
    
    todos_existen = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo) / 1024  # KB
            print(f"✓ {archivo:<35} ({tamaño:.1f} KB)")
        else:
            print(f"✗ {archivo:<35} (FALTA)")
            todos_existen = False
    
    return todos_existen

def verificar_dependencias():
    """Verifica que las librerías están instaladas"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN 2: DEPENDENCIAS INSTALADAS")
    print("=" * 60)
    
    dependencias = ['requests', 'pandas', 'flask', 'flask_cors', 'plotly']
    
    todas_instaladas = True
    for dep in dependencias:
        try:
            if dep == 'flask_cors':
                __import__('flask_cors')
            else:
                __import__(dep)
            print(f"✓ {dep:<20} (Instalado)")
        except ImportError:
            print(f"✗ {dep:<20} (NO INSTALADO)")
            todas_instaladas = False
    
    return todas_instaladas

def verificar_pokeapi():
    """Verifica que PokeAPI esté accesible"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN 3: ACCESO A PokeAPI")
    print("=" * 60)
    
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon/1", timeout=5)
        if response.status_code == 200:
            print(f"✓ PokeAPI accesible")
            data = response.json()
            print(f"✓ Datos válidos: {data.get('name', 'N/A')}")
            return True
        else:
            print(f"✗ Error al conectar: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        return False

def verificar_flask_api():
    """Verifica que la API Flask esté corriendo"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN 4: API FLASK")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:5000/api/pokemones/1", timeout=5)
        if response.status_code == 200:
            print(f"✓ API Flask funcionando en http://localhost:5000")
            data = response.json()
            if data.get('exitoso'):
                print(f"✓ Respuesta válida: {data['datos'].get('nombre', 'N/A')}")
                return True
        else:
            print(f"⚠ API no responde (Status {response.status_code})")
            print(f"  Ejecuta: python 3_api_pokemon.py")
            return False
    except Exception as e:
        print(f"⚠ API Flask no está corriendo")
        print(f"  Ejecuta: python 3_api_pokemon.py")
        return False

def verificar_frontend():
    """Verifica que el frontend React esté corriendo"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN 5: FRONTEND REACT")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print(f"✓ Frontend React corriendo en http://localhost:3001")
            return True
    except Exception as e:
        print(f"⚠ Frontend React no está corriendo")
        print(f"  Ejecuta en frontend/: pnpm start")
        return False

def mostrar_resumen_etapas():
    """Muestra el resumen de ejecución"""
    print("\n" + "=" * 60)
    print("GUÍA DE EJECUCIÓN DEL SISTEMA")
    print("=" * 60)
    
    etapas = [
        {
            'numero': 1,
            'nombre': 'DESCARGA DE DATOS',
            'archivo': '1_obtener_datos_pokemon.py',
            'entrada': 'PokeAPI v2',
            'salida': '150 Pokémon en memoria',
            'comando': 'python 1_obtener_datos_pokemon.py'
        },
        {
            'numero': 2,
            'nombre': 'PROCESAMIENTO DE DATOS',
            'archivo': '2_procesar_datos.py',
            'entrada': 'Datos de PokeAPI',
            'salida': 'JSON procesados (opcional)',
            'comando': 'python 2_procesar_datos.py'
        },
        {
            'numero': 3,
            'nombre': 'API REST (BACKEND)',
            'archivo': '3_api_pokemon.py',
            'entrada': 'PokeAPI v2',
            'salida': 'API en http://localhost:5000 (7 endpoints)',
            'comando': 'python 3_api_pokemon.py'
        },
        {
            'numero': 4,
            'nombre': 'DASHBOARD OPCIONAL',
            'archivo': '4_dashboard_pokemon.py',
            'entrada': 'API Flask',
            'salida': '10 archivos HTML con gráficos Plotly',
            'comando': 'python 4_dashboard_pokemon.py'
        },
        {
            'numero': 5,
            'nombre': 'FRONTEND (REACT)',
            'archivo': 'frontend/',
            'entrada': 'API Flask',
            'salida': 'Aplicación web en http://localhost:3001',
            'comando': 'cd frontend && pnpm start'
        }
    ]
    
    for etapa in etapas:
        print(f"\nETAPA {etapa['numero']}: {etapa['nombre']}")
        print(f"  Archivo: {etapa['archivo']}")
        print(f"  Entrada: {etapa['entrada']}")
        print(f"  Salida: {etapa['salida']}")
        print(f"  Comando: {etapa['comando']}")

def main():
    """Ejecuta todas las verificaciones"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "VALIDACIÓN DEL SISTEMA" + " " * 21 + "║")
    print("║" + " " * 8 + "Pokédex: PokeAPI + Flask + React (SIN DB)" + " " * 8 + "║")
    print("╚" + "=" * 58 + "╝")
    
    resultados = {
        'Archivos': verificar_archivos(),
        'Dependencias': verificar_dependencias(),
        'PokeAPI': verificar_pokeapi(),
        'Flask API': verificar_flask_api(),
        'Frontend': verificar_frontend()
    }
    
    mostrar_resumen_etapas()
    
    print("\n" + "=" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    for aspecto, resultado in resultados.items():
        estado = "✓ LISTO" if resultado else "⚠ REVISAR"
        print(f"{aspecto:<20}: {estado}")
    
    print("\n" + "=" * 60)
    
    if resultados['Archivos'] and resultados['Dependencias'] and resultados['PokeAPI']:
        print("✓ SISTEMA LISTO PARA USAR")
        print("")
        print("Pasos recomendados:")
        print("1. Inicia la API: python 3_api_pokemon.py")
        print("2. Inicia el frontend: cd frontend && pnpm start")
        print("3. Abre browser: http://localhost:3001")
    else:
        print("⚠ Faltan completar algunos pasos")
        print("Ver arriba para más detalles")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
