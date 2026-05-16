import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { pokemonService } from '../services/pokemonService';
import './HomePage.css';

function HomePage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await pokemonService.obtenerEstadisticas();
      // La API retorna los datos directamente en response.data
      setStats(response.data);
    } catch (err) {
      setError('Error al cargar estadísticas: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Bienvenido a POKÉDEX</h1>
          <p className="hero-subtitle">
            Explora el mundo de los Pokémon con nuestra base de datos interactiva
          </p>
          <div className="hero-buttons">
            <Link to="/pokemones" className="btn btn-primary">
              🔍 Ver Pokédex Completa
            </Link>
            <Link to="/tipos" className="btn btn-secondary">
              🎨 Explorar por Tipos
            </Link>
          </div>
        </div>
      </section>

      <section className="stats-section">
        <h2 className="section-title">📊 Estadísticas Generales</h2>
        
        {loading ? (
          <div className="loading">Cargando estadísticas...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : stats ? (
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">📚</div>
              <div className="stat-content">
                <h3>Total de Pokémon</h3>
                <p className="stat-number">{stats.total_pokemones}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">⭐</div>
              <div className="stat-content">
                <h3>Legendarios</h3>
                <p className="stat-number">{stats.pokemones_legendarios}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">🎨</div>
              <div className="stat-content">
                <h3>Tipos Únicos</h3>
                <p className="stat-number">{stats.cantidad_tipos}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">📏</div>
              <div className="stat-content">
                <h3>Altura Promedio</h3>
                <p className="stat-number">{stats.altura_promedio_dm} dm</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">⚖️</div>
              <div className="stat-content">
                <h3>Peso Promedio</h3>
                <p className="stat-number">{stats.peso_promedio_hg} hg</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">✨</div>
              <div className="stat-content">
                <h3>Exp Base Promedio</h3>
                <p className="stat-number">{stats.experiencia_base_promedio}</p>
              </div>
            </div>
          </div>
        ) : null}
      </section>

      <section className="quick-links-section">
        <h2 className="section-title">🚀 Acceso Rápido</h2>
        <div className="quick-links">
          <Link to="/pokemones" className="quick-link-card">
            <span className="icon">📋</span>
            <span className="title">Pokédex</span>
            <span className="description">Ver todos los Pokémon</span>
          </Link>

          <Link to="/tipos" className="quick-link-card">
            <span className="icon">🎨</span>
            <span className="title">Tipos</span>
            <span className="description">Explorar por tipo</span>
          </Link>

          <Link to="/legendarios" className="quick-link-card">
            <span className="icon">⭐</span>
            <span className="title">Legendarios</span>
            <span className="description">Pokémon legendarios</span>
          </Link>

          <Link to="/estadisticas" className="quick-link-card">
            <span className="icon">📊</span>
            <span className="title">Estadísticas</span>
            <span className="description">Análisis completo</span>
          </Link>
        </div>
      </section>

      <section className="info-section">
        <h2 className="section-title">ℹ️ Sobre POKÉDEX</h2>
        <div className="info-content">
          <p>
            Este es un sistema completo de Pokédex que combina:
          </p>
          <ul className="features-list">
            <li>✓ API REST con 1025 Pokémon de todas las generaciones</li>
            <li>✓ Datos en tiempo real desde PokeAPI v2</li>
            <li>✓ Interface moderna con React</li>
            <li>✓ Búsqueda por tipo, legendarios y estadísticas</li>
            <li>✓ Información detallada de cada Pokémon</li>
            <li>✓ Visualización de imágenes oficiales</li>
          </ul>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
