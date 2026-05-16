import React, { useEffect, useState } from 'react';
import { pokemonService } from '../services/pokemonService';
import './EstadisticasPage.css';

function EstadisticasPage() {
  const [stats, setStats] = useState(null);
  const [tipos, setTipos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsRes, tiposRes] = await Promise.all([
        pokemonService.obtenerEstadisticas(),
        pokemonService.obtenerTipos(),
      ]);
      // La API devuelve los datos directamente, no en .estadisticas
      setStats(statsRes.data);

      const datosTipos = tiposRes?.data?.datos;
      // Soporta ambos formatos: array [{tipo, cantidad}] o diccionario {tipo: cantidad}
      const tiposArray = Array.isArray(datosTipos)
        ? datosTipos
        : Object.entries(datosTipos || {}).map(([nombre, cantidad]) => ({
            tipo: nombre,
            cantidad: cantidad,
          }));

      setTipos(tiposArray);
      setError(null);
    } catch (err) {
      setError('Error al cargar estadísticas: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="estadisticas-page">
        <div className="loading">⏳ Cargando estadísticas...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="estadisticas-page">
        <div className="error">{error}</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="estadisticas-page">
        <div className="error">No hay datos disponibles</div>
      </div>
    );
  }

  const tiposLista = Array.isArray(tipos) ? tipos : [];
  const maxTipoCount = tiposLista.length > 0 ? Math.max(...tiposLista.map((t) => t.cantidad || 0)) : 1;

  return (
    <div className="estadisticas-page">
      <div className="page-header">
        <h1>📊 Estadísticas Completas</h1>
        <p>Análisis detallado de la base de datos Pokémon</p>
      </div>

      <div className="stats-grid-large">
        <div className="stat-card-large">
          <div className="stat-icon-large">📚</div>
          <div className="stat-details">
            <h3>Total de Pokémon</h3>
            <p className="stat-number-large">{stats.total_pokemones}</p>
            <p className="stat-description">Pokémones en la base de datos</p>
          </div>
        </div>

        <div className="stat-card-large">
          <div className="stat-icon-large">⭐</div>
          <div className="stat-details">
            <h3>Pokémones Legendarios</h3>
            <p className="stat-number-large">{stats.pokemones_legendarios}</p>
            <p className="stat-description">
              {((stats.pokemones_legendarios / stats.total_pokemones) * 100).toFixed(1)}% del total
            </p>
          </div>
        </div>

        <div className="stat-card-large">
          <div className="stat-icon-large">🎨</div>
          <div className="stat-details">
            <h3>Tipos Disponibles</h3>
            <p className="stat-number-large">{stats.cantidad_tipos}</p>
            <p className="stat-description">Tipos únicos descobertos</p>
          </div>
        </div>

        <div className="stat-card-large">
          <div className="stat-icon-large">📏</div>
          <div className="stat-details">
            <h3>Altura Promedio</h3>
            <p className="stat-number-large">{stats.altura_promedio_dm} dm</p>
            <p className="stat-description">{(stats.altura_promedio_dm * 10 / 100).toFixed(2)} metros</p>
          </div>
        </div>

        <div className="stat-card-large">
          <div className="stat-icon-large">⚖️</div>
          <div className="stat-details">
            <h3>Peso Promedio</h3>
            <p className="stat-number-large">{stats.peso_promedio_hg} hg</p>
            <p className="stat-description">{(stats.peso_promedio_hg / 10).toFixed(2)} kilogramos</p>
          </div>
        </div>

        <div className="stat-card-large">
          <div className="stat-icon-large">✨</div>
          <div className="stat-details">
            <h3>Experiencia Base Promedio</h3>
            <p className="stat-number-large">{stats.experiencia_base_promedio}</p>
            <p className="stat-description">Puntos de experiencia</p>
          </div>
        </div>
      </div>

      <div className="tipos-distribution">
        <h2>Distribución de Tipos</h2>
        <div className="tipos-bars">
          {tiposLista.map((tipo) => (
            <div key={tipo.tipo} className="tipo-bar-item">
              <div className="tipo-bar-label">{tipo.tipo}</div>
              <div className="tipo-bar-container">
                <div
                  className="tipo-bar-fill"
                  style={{ width: `${((tipo.cantidad || 0) / maxTipoCount) * 100}%` }}
                >
                  {tipo.cantidad}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default EstadisticasPage;