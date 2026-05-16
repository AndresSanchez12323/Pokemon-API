"""
INICIO RÁPIDO - Sistema Pokémon (5 minutos)

Este script te guiará por los pasos esenciales para empezar.
Ejecuta este archivo y sigue las instrucciones.
"""

import os
import sys

def mostrar_menu_inicial():
    """Muestra menú de inicio"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    SISTEMA POKÉMON                           ║
║         Scraping + API + Dashboard (5 minutos)               ║
╚═══════════════════════════════════════════════════════════════╝

¿Qué quieres hacer?

1. 📖 Ver documentación (recomendado para primera vez)
2. 🚀 Ejecutar el sistema paso a paso
3. ✅ Validar instalación
4. 📊 Ver resumen ejecutivo
5. ❓ Ver documentación técnica
6. ⚙️ Ver instrucciones de instalación
7. 📋 Ver guía unificada (README)

Selecciona una opción (1-7):
""")

def opcion_documentacion():
    """Muestra documentación"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                   DOCUMENTACIÓN PRINCIPAL                    ║
╚═══════════════════════════════════════════════════════════════╝

Se recomienda leer en este orden:

📄 README.md
   └─ Guía completa con todos los detalles
   └─ Mejor para entender TODO el proyecto

📄 RESUMEN_EJECUTIVO.py
   └─ Resumen ejecutivo (no técnico)
   └─ Mejor para managers/evaluadores

📄 DOCUMENTACION_TECNICA.py
   └─ Referencia técnica detallada
   └─ Mejor para developers/estudiantes

Para abrir README.md desde terminal:
   Windows: start README.md
   Linux:   cat README.md | less
   Mac:     open README.md

¿Deseas continuar? (s/n): """)
    
    respuesta = input().strip().lower()
    if respuesta == 's':
        print("\n✓ Abre README.md en tu editor favorito para leerlo.\n")
        return True
    return False

def opcion_ejecutar_sistema():
    """Guía para ejecutar el sistema"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                EJECUTAR EL SISTEMA (3 pasos)                 ║
╚═══════════════════════════════════════════════════════════════╝

ETAPA 1: Iniciar API REST (mientras corre)
─────────────────────────────────────────
Terminal 1, ejecuta:

    python 3_api_pokemon.py

Verás: "Running on http://0.0.0.0:5000"

MANTÉN ESTA TERMINAL ABIERTA


ETAPA 2: Iniciar Frontend React
───────────────────────────────
Terminal 2 (NUEVA), ejecuta:

    cd frontend
    pnpm start

Verás: "Compiled successfully!"


ETAPA 3 (OPCIONAL): Generar Dashboard Plotly
────────────────────────────────────────────
Terminal 3 (NUEVA), ejecuta:

    python 4_dashboard_pokemon.py

Verás: "✓ Dashboard creado exitosamente!"


AHORA:
─────
1. Abre navegador: http://localhost:3001
2. O abre: 09_dashboard_general.html (doble clic)
3. ¡Interactúa con los gráficos!

Presiona Enter para continuar...
""")
    input()

def opcion_validar():
    """Valida la instalación"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                   VALIDAR INSTALACIÓN                        ║
╚═══════════════════════════════════════════════════════════════╝

Ejecutando validación...
""")
    
    os.system("python validar_sistema.py")
    
    print("\n\nSi todo está ✓, estás listo para ejecutar el sistema.")
    print("Si hay ✗, consulta la sección 'SOLUCIÓN DE PROBLEMAS' en README.md")
    input("Presiona Enter para continuar...")

def opcion_resumen():
    """Muestra resumen ejecutivo"""
    print("\n")
    os.system("python RESUMEN_EJECUTIVO.py")
    input("\nPresiona Enter para continuar...")

def opcion_tecnicaDocumentacion():
    """Muestra documentación técnica"""
    print("\n")
    os.system("python DOCUMENTACION_TECNICA.py | head -100")
    print("\n... (para ver todo, ejecuta: python DOCUMENTACION_TECNICA.py)")
    input("Presiona Enter para continuar...")

def opcion_instalacion():
    """Muestra instrucciones de instalación"""
    print("\n")
    os.system("python INSTRUCCIONES_INSTALACION.py | head -100")
    print("\n... (para ver todo, ejecuta: python INSTRUCCIONES_INSTALACION.py)")
    input("Presiona Enter para continuar...")

def opcion_indice():
    """Muestra guía unificada del proyecto"""
    print("\nMostrando primeras 50 líneas de README.md:\n")
    try:
        with open("README.md", "r", encoding="utf-8") as archivo:
            for i, linea in enumerate(archivo):
                if i >= 50:
                    break
                print(linea.rstrip())
    except Exception as e:
        print(f"No se pudo abrir README.md: {e}")
    print("\n... (para ver todo, abre README.md)")
    input("\nPresiona Enter para continuar...")

def main():
    """Menú principal"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        mostrar_menu_inicial()
        
        try:
            opcion = input("Tu opción: ").strip()
            
            os.system("cls" if os.name == "nt" else "clear")
            
            if opcion == "1":
                if opcion_documentacion():
                    continue
            elif opcion == "2":
                opcion_ejecutar_sistema()
            elif opcion == "3":
                opcion_validar()
            elif opcion == "4":
                opcion_resumen()
            elif opcion == "5":
                opcion_tecnicaDocumentacion()
            elif opcion == "6":
                opcion_instalacion()
            elif opcion == "7":
                opcion_indice()
            else:
                print("❌ Opción no válida. Intenta nuevamente.")
                input("Presiona Enter...")
                continue
            
            # Preguntar si continuar
            print("\n" + "=" * 60)
            print("¿Deseas volver al menú? (s/n): ", end="")
            if input().strip().lower() != "s":
                print("✓ ¡Hasta luego!")
                break
                
        except KeyboardInterrupt:
            print("\n\n✓ Saliendo...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Presiona Enter...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)
