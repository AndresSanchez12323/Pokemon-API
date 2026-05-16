"""
ETAPA 2: Procesamiento de datos de Pokémon (SIN BASE DE DATOS)

Este script demuestra cómo procesar y transformar datos de Pokémon.
Los datos procesados se almacenan en memoria para análisis rápido.
"""

import json
import requests
from collections import defaultdict

POKEAPI_BASE = "https://pokeapi.co/api/v2"

def procesar_pokemon(pokemon_json):
    """Procesa y enriquece datos de un Pokémon"""
    return {
        'numero_pokedex': pokemon_json['numero_pokedex'],
        'nombre': pokemon_json['nombre'],
        'tipos': [pokemon_json['tipo_1']] + ([pokemon_json['tipo_2']] if pokemon_json['tipo_2'] else []),
        'altura_metro': round(pokemon_json['altura_dm'] * 0.1, 2),
        'peso_kg': round(pokemon_json['peso_hectogramos'] * 0.1, 2),
        'experiencia_base': pokemon_json['experiencia_base'],
        'imagen': pokemon_json['url_imagen_oficial']
    }

def calcular_estadisticas(pokemones):
    """Calcula estadísticas sobre los Pokémon"""
    
    # Inicializar variables
    total = len(pokemones)
    altura_total = sum(p['altura_dm'] for p in pokemones)
    peso_total = sum(p['peso_hectogramos'] for p in pokemones)
    exp_total = sum(p['experiencia_base'] for p in pokemones)
    
    # Contar tipos
    tipos = defaultdict(int)
    for p in pokemones:
        if p['tipo_1']:
            tipos[p['tipo_1']] += 1
        if p['tipo_2']:
            tipos[p['tipo_2']] += 1
    
    # Legendarios
    legendarios = [144, 145, 146, 149, 150, 151, 243, 244, 245, 249, 250, 251, 
                  384, 483, 484, 487, 643, 644, 645, 646]
    legendarios_count = sum(1 for p in pokemones if p['numero_pokedex'] in legendarios)
    
    return {
        'total_pokemones': total,
        'legendarios': legendarios_count,
        'altura_promedio_dm': round(altura_total / total, 2),
        'peso_promedio_hg': round(peso_total / total, 2),
        'exp_promedio': round(exp_total / total, 2),
        'distribucion_tipos': dict(tipos),
        'cantidad_tipos': len(tipos)
    }

def main():
    """Prueba el procesamiento de datos"""
    
    print("=" * 60)
    print("ETAPA 2: PROCESAMIENTO DE DATOS POKÉMON")
    print("=" * 60)
    print()
    
    print("📥 Cargando datos...")
    
    # Cargar muestra de datos
    pokemones = []
    for i in range(1, 151):
        try:
            url = f"{POKEAPI_BASE}/pokemon/{i}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
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
                }
                pokemones.append(pokemon)
                
                if i % 30 == 0:
                    print(f"   ✓ {i}/150 cargados")
        except:
            continue
    
    print(f"\n✓ {len(pokemones)} Pokémon cargados en memoria\n")
    
    # Procesar datos
    print("🔄 Procesando datos...")
    pokemones_procesados = [procesar_pokemon(p) for p in pokemones]
    
    # Calcular estadísticas
    print("📊 Calculando estadísticas...")
    stats = calcular_estadisticas(pokemones)
    
    print()
    print("=" * 60)
    print("ESTADÍSTICAS CALCULADAS")
    print("=" * 60)
    print(f"Total de Pokémon: {stats['total_pokemones']}")
    print(f"Legendarios: {stats['legendarios']}")
    print(f"Tipos únicos: {stats['cantidad_tipos']}")
    print(f"Altura promedio: {stats['altura_promedio_dm']} dm ({stats['altura_promedio_dm'] * 0.1:.2f} m)")
    print(f"Peso promedio: {stats['peso_promedio_hg']} hg ({stats['peso_promedio_hg'] * 0.1:.2f} kg)")
    print(f"EXP base promedio: {stats['exp_promedio']:.0f}")
    print()
    
    print("Distribución de tipos (top 5):")
    sorted_tipos = sorted(stats['distribucion_tipos'].items(), key=lambda x: x[1], reverse=True)[:5]
    for tipo, count in sorted_tipos:
        print(f"  {tipo.capitalize()}: {count} Pokémon")
    
    # Guardar datos procesados
    print()
    print("💾 Guardando datos procesados...")
    
    with open('pokemones_procesados.json', 'w', encoding='utf-8') as f:
        json.dump(pokemones_procesados, f, indent=2, ensure_ascii=False)
    
    with open('estadisticas.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print("✓ Archivos guardados:")
    print("  - pokemones_procesados.json")
    print("  - estadisticas.json")
    print()
    print("=" * 60)
    print("✅ DATOS LISTOS PARA LA API")
    print("=" * 60)
    print()
    print("Próximo paso: Ejecutar 3_api_pokemon.py")
    print()

if __name__ == "__main__":
    main()
