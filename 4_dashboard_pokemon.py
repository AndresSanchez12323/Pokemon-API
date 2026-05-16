"""
Dashboard interactivo de Pokémon con Plotly
Etapa 4: Visualización de datos
Consume datos desde la API Flask (3_api_pokemon.py) - SIN BASE DE DATOS
"""

import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

API_BASE = "http://localhost:5000"

def obtener_datos_api():
    """Obtiene datos de Pokémon desde la API Flask"""
    try:
        print("📡 Conectando a la API Flask...")
        pokemones = []
        
        # Obtener todos los pokémones (paginados)
        pagina = 1
        mientras_hay_datos = True
        
        while mientras_hay_datos:
            try:
                response = requests.get(f"{API_BASE}/api/pokemones", 
                                       params={'pagina': pagina, 'limite': 50},
                                       timeout=5)
                
                if response.status_code != 200:
                    break
                
                data = response.json()
                pokemones.extend(data['datos'])
                
                print(f"   ✓ Página {pagina} cargada ({len(pokemones)}/150)")
                
                # Si es la última página, salir
                if pagina >= data['total_paginas']:
                    mientras_hay_datos = False
                
                pagina += 1
            except Exception as e:
                print(f"   ⚠️  Error en página {pagina}: {e}")
                mientras_hay_datos = False
        
        # Convertir a DataFrame
        df = pd.DataFrame(pokemones)
        print(f"\n✓ Se cargaron {len(df)} registros desde la API")
        return df
    
    except Exception as e:
        print(f"✗ Error al conectar a la API: {e}")
        print(f"   Asegúrate de que Flask está corriendo en {API_BASE}")
        return None

def crear_dashboard(df):
    """Crea un dashboard con múltiples visualizaciones"""
    print("\n" + "=" * 60)
    print("ETAPA 4: DASHBOARD DE VISUALIZACIÓN")
    print("=" * 60)
    
    # Reemplazar valores nulos
    df['tipo_2'] = df['tipo_2'].fillna('Sin tipo')
    
    # GRÁFICO 1: Distribución de tipos (Histograma)
    print("\n1. Creando gráfico de distribución de tipos...")
    fig1 = px.histogram(
        df, 
        x='tipo_1',
        title='Cantidad de Pokémones por Tipo Principal',
        labels={'tipo_1': 'Tipo', 'count': 'Cantidad'},
        color='tipo_1',
        height=500
    )
    fig1.update_layout(showlegend=False)
    fig1.write_html('01_distribucion_tipos.html')
    print("   ✓ Guardado como: 01_distribucion_tipos.html")
    
    # GRÁFICO 2: Altura vs Peso (Scatter)
    print("2. Creando gráfico de altura vs peso...")
    fig2 = px.scatter(
        df,
        x='altura_dm',
        y='peso_hectogramos',
        size='experiencia_base',
        color='tipo_1',
        hover_name='nombre',
        title='Relación Altura-Peso de Pokémones',
        labels={'altura_dm': 'Altura (dm)', 'peso_hectogramos': 'Peso (hg)', 'tipo_1': 'Tipo'},
        height=600
    )
    fig2.write_html('02_altura_vs_peso.html')
    print("   ✓ Guardado como: 02_altura_vs_peso.html")
    
    # GRÁFICO 3: Experiencia base por tipo (Box plot)
    print("3. Creando gráfico de experiencia base por tipo...")
    fig3 = px.box(
        df,
        x='tipo_1',
        y='experiencia_base',
        color='tipo_1',
        title='Distribución de Experiencia Base por Tipo',
        labels={'tipo_1': 'Tipo', 'experiencia_base': 'Experiencia Base'},
        height=500
    )
    fig3.update_layout(showlegend=False)
    fig3.write_html('03_experiencia_por_tipo.html')
    print("   ✓ Guardado como: 03_experiencia_por_tipo.html")
    
    # GRÁFICO 4: Top 20 Pokémones por peso
    print("4. Creando gráfico de Pokémones más pesados...")
    top_peso = df.nlargest(20, 'peso_hectogramos')[['nombre', 'peso_hectogramos', 'tipo_1']]
    fig4 = px.bar(
        top_peso,
        x='peso_hectogramos',
        y='nombre',
        color='tipo_1',
        orientation='h',
        title='Top 20: Pokémones Más Pesados',
        labels={'peso_hectogramos': 'Peso (hg)', 'nombre': 'Pokémon'},
        height=700
    )
    fig4.update_layout(yaxis=dict(autorange="reversed"))
    fig4.write_html('04_pokemones_mas_pesados.html')
    print("   ✓ Guardado como: 04_pokemones_mas_pesados.html")
    
    # GRÁFICO 5: Top 20 Pokémones más altos
    print("5. Creando gráfico de Pokémones más altos...")
    top_altura = df.nlargest(20, 'altura_dm')[['nombre', 'altura_dm', 'tipo_1']]
    fig5 = px.bar(
        top_altura,
        x='altura_dm',
        y='nombre',
        color='tipo_1',
        orientation='h',
        title='Top 20: Pokémones Más Altos',
        labels={'altura_dm': 'Altura (dm)', 'nombre': 'Pokémon'},
        height=700
    )
    fig5.update_layout(yaxis=dict(autorange="reversed"))
    fig5.write_html('05_pokemones_mas_altos.html')
    print("   ✓ Guardado como: 05_pokemones_mas_altos.html")
    
    # GRÁFICO 6: Comparación legendarios vs no legendarios
    print("6. Creando gráfico de legendarios vs no legendarios...")
    legendarios_count = df['es_legendario'].value_counts()
    etiquetas = ['No Legendarios', 'Legendarios']
    valores = [legendarios_count.get(0, 0), legendarios_count.get(1, 0)]
    
    fig6 = go.Figure(data=[go.Pie(
        labels=etiquetas,
        values=valores,
        marker=dict(colors=['#4287f5', '#f54242']),
        textposition='inside',
        textinfo='label+percent'
    )])
    fig6.update_layout(
        title='Proporción de Pokémones Legendarios vs No Legendarios',
        height=500
    )
    fig6.write_html('06_legendarios_pie.html')
    print("   ✓ Guardado como: 06_legendarios_pie.html")
    
    # GRÁFICO 7: Experiencia promedio por tipo (Bar)
    print("7. Creando gráfico de experiencia promedio por tipo...")
    exp_por_tipo = df.groupby('tipo_1')['experiencia_base'].mean().sort_values(ascending=True)
    fig7 = px.bar(
        x=exp_por_tipo.values,
        y=exp_por_tipo.index,
        orientation='h',
        title='Experiencia Base Promedio por Tipo',
        labels={'x': 'Experiencia Base Promedio', 'y': 'Tipo'},
        color=exp_por_tipo.values,
        color_continuous_scale='Viridis',
        height=500
    )
    fig7.write_html('07_experiencia_promedio_tipo.html')
    print("   ✓ Guardado como: 07_experiencia_promedio_tipo.html")
    
    # GRÁFICO 8: Tipos secundarios distribution
    print("8. Creando gráfico de tipos secundarios...")
    secundarios = df[df['tipo_2'] != 'Sin tipo']['tipo_2'].value_counts()
    if len(secundarios) > 0:
        fig8 = px.bar(
            x=secundarios.values,
            y=secundarios.index,
            orientation='h',
            title='Cantidad de Pokémones por Tipo Secundario',
            labels={'x': 'Cantidad', 'y': 'Tipo'},
            color=secundarios.values,
            color_continuous_scale='Blues',
            height=500
        )
        fig8.write_html('08_tipos_secundarios.html')
        print("   ✓ Guardado como: 08_tipos_secundarios.html")
    
    # GRÁFICO 9: Dashboard general (Subplots)
    print("9. Creando dashboard general integrado...")
    fig9 = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Pokémones por Tipo", "Legendarios Distribution", 
                       "Altura vs Peso", "Experiencia Base Top 10"),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Subtítulo 1: Tipos
    tipos_conteo = df['tipo_1'].value_counts().head(10)
    fig9.add_trace(
        go.Bar(x=tipos_conteo.index, y=tipos_conteo.values, name='Tipos'),
        row=1, col=1
    )
    
    # Subtítulo 2: Legendarios
    leg_counts = df['es_legendario'].value_counts()
    fig9.add_trace(
        go.Pie(labels=['No Legendarios', 'Legendarios'], 
               values=[leg_counts.get(0, 0), leg_counts.get(1, 0)],
               name='Estado'),
        row=1, col=2
    )
    
    # Subtítulo 3: Altura vs Peso (muestra)
    fig9.add_trace(
        go.Scatter(x=df['altura_dm'], y=df['peso_hectogramos'], 
                  mode='markers', name='Pokémones'),
        row=2, col=1
    )
    
    # Subtítulo 4: Top experiencia
    top_exp = df.nlargest(10, 'experiencia_base')
    fig9.add_trace(
        go.Bar(x=top_exp['nombre'], y=top_exp['experiencia_base'], name='Exp'),
        row=2, col=2
    )
    
    fig9.update_xaxes(title_text="Tipo", row=1, col=1)
    fig9.update_xaxes(title_text="Altura (dm)", row=2, col=1)
    fig9.update_xaxes(title_text="Pokémon", row=2, col=2)
    
    fig9.update_yaxes(title_text="Cantidad", row=1, col=1)
    fig9.update_yaxes(title_text="Peso (hg)", row=2, col=1)
    fig9.update_yaxes(title_text="Experiencia", row=2, col=2)
    
    fig9.update_layout(height=900, title_text="Dashboard General de Pokémon", showlegend=False)
    fig9.write_html('09_dashboard_general.html')
    print("   ✓ Guardado como: 09_dashboard_general.html")
    
    # GRÁFICO 10: Tabla interactiva de Pokémones
    print("10. Creando tabla interactiva de Pokémones...")
    df_tabla = df[['numero_pokedex', 'nombre', 'tipo_1', 'tipo_2', 'altura_dm', 'peso_hectogramos', 'experiencia_base', 'es_legendario']].copy()
    df_tabla.columns = ['Pokedex', 'Nombre', 'Tipo 1', 'Tipo 2', 'Altura', 'Peso', 'Experiencia', 'Legendario']
    
    fig10 = go.Figure(data=[go.Table(
        header=dict(values=list(df_tabla.columns),
                   fill_color='paleturquoise',
                   align='left',
                   font=dict(size=12)),
        cells=dict(values=[df_tabla[col] for col in df_tabla.columns],
                  fill_color='lavender',
                  align='left',
                  font=dict(size=11),
                  height=25)
    )])
    
    fig10.update_layout(title='Tabla Completa de Pokémones', height=800)
    fig10.write_html('10_tabla_pokemones.html')
    print("   ✓ Guardado como: 10_tabla_pokemones.html")
    
    print("\n" + "=" * 60)
    print("RESUMEN DE DASHBOARD:")
    print("=" * 60)
    print(f"✓ Total de gráficos generados: 10")
    print(f"✓ Total de registros visualizados: {len(df)}")
    print(f"\nArchivos HTML generados:")
    print("  - 01_distribucion_tipos.html")
    print("  - 02_altura_vs_peso.html")
    print("  - 03_experiencia_por_tipo.html")
    print("  - 04_pokemones_mas_pesados.html")
    print("  - 05_pokemones_mas_altos.html")
    print("  - 06_legendarios_pie.html")
    print("  - 07_experiencia_promedio_tipo.html")
    print("  - 08_tipos_secundarios.html")
    print("  - 09_dashboard_general.html")
    print("  - 10_tabla_pokemones.html")
    print("\nAbra cualquiera de estos archivos en su navegador")
    print("para ver los gráficos interactivos.")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SISTEMA DE POKEMON - DASHBOARD")
    print("=" * 60)
    
    df = obtener_datos_api()
    
    if df is not None and len(df) > 0:
        crear_dashboard(df)
        print("\n Creado exitosamente!")
    else:
        print("\n No se pudieron cargar los datos. Verifica que la API Flask este corriendo en http://localhost:5000")
