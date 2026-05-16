"""
ETAPA 1: Obtener datos de Pokémon desde PokeAPI v2 (SIN BASE DE DATOS)

Este script demuestra cómo consumir directamente la API de PokeAPI.
Los datos se procesan en memoria y se pueden usar inmediatamente.
"""

import requests
import json
from datetime import datetime

POKEAPI_BASE = "https://pokeapi.co/api/v2"

def obtener_pokemon(id_numero):
    """Obtiene un Pokémon desde PokeAPI"""
    try:
        url = f"{POKEAPI_BASE}/pokemon/{id_numero}"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        # Extraer información importante
        tipos = [t['type']['name'] for t in data['types']]
        pokemon = {
            'numero_pokedex': data['id'],
            'nombre': data['name'].capitalize(),
            'tipo_1': tipos[0] if len(tipos) > 0 else None,
            'tipo_2': tipos[1] if len(tipos) > 1 else None,
            'altura_dm': data['height'],
            'peso_hectogramos': data['weight'],
            'experiencia_base': data['base_experience'],
            'url_imagen_oficial': data['sprites']['other']['official-artwork']['front_default'],
            'url_imagen_frontal': data['sprites']['front_default'],
            'url_imagen_trasera': data['sprites']['back_default'],
        }
        
        return pokemon
    
    except Exception as e:
        print(f"Error obteniendo Pokémon {id_numero}: {e}")
        return None

def main():
    """Descarga datos de Pokémon desde PokeAPI"""
    
    print("=" * 60)
    print("ETAPA 1: OBTENCIÓN DE DATOS DESDE PokeAPI v2")
    print("=" * 60)
    print()
    
    print(f"⏳ Iniciando descarga desde {POKEAPI_BASE}")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    pokemones = []
    errores = 0
    
    print("🔄 Descargando 150 Pokémon...")
    
    for i in range(1, 151):
        pokemon = obtener_pokemon(i)
        
        if pokemon:
            pokemones.append(pokemon)
            if i % 30 == 0:
                print(f"   ✓ {i}/150 descargados")
        else:
            errores += 1
    
    print()
    print("=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    print(f"✅ Total descargado: {len(pokemones)} Pokémon")
    print(f"⚠️  Errores: {errores}")
    print(f"📊 Tasa de éxito: {(len(pokemones)/150)*100:.1f}%")
    print()
    
    # Mostrar ejemplos
    print("MUESTRA DE DATOS DESCARGADOS:")
    print("-" * 60)
    for i in [0, 24, 149]:
        if i < len(pokemones):
            p = pokemones[i]
            print(f"\n#{p['numero_pokedex']:3d} - {p['nombre']}")
            print(f"    Tipos: {p['tipo_1']}" + (f", {p['tipo_2']}" if p['tipo_2'] else ""))
            print(f"    Altura: {p['altura_dm']} dm | Peso: {p['peso_hectogramos']} hg")
            print(f"    Base EXP: {p['experiencia_base']}")
    
    print()
    print("=" * 60)
    print("✅ DATOS LISTOS PARA USAR")
    print("=" * 60)
    print()
    print("OPCIONES:")
    print("1. Usar directamente en scripts Python")
    print("2. Consumir a través de la API Flask (3_api_pokemon.py)")
    print("3. Usar desde el frontend React (http://localhost:3001)")
    print()
    
    # Guardar ejemplo en JSON
    with open('pokemones_muestra.json', 'w', encoding='utf-8') as f:
        json.dump(pokemones[:10], f, indent=2, ensure_ascii=False)
    print("💾 Guardado muestra de 10 Pokémon en 'pokemones_muestra.json'")
    print()

if __name__ == "__main__":
    main()
