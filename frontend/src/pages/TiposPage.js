import React, { useEffect, useState } from 'react';
import { pokemonService } from '../services/pokemonService';
import './TiposPage.css';

function TiposPage() {
  const [tipos, setTipos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedTipo, setSelectedTipo] = useState(null);
  const [pokemonesTipo, setPokemonesTipo] = useState([]);
  const [loadingTipo, setLoadingTipo] = useState(false);

  useEffect(() => {
    fetchTipos();
  }, []);

  const fetchTipos = async () => {
    try {
      setLoading(true);
      const response = await pokemonService.obtenerTipos();
      const datosTipos = response?.data?.datos;

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
      setError('Error al cargar tipos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchPokemonesTipo = async (tipo) => {
    try {
      setLoadingTipo(true);
      const response = await pokemonService.obtenerPorTipo(tipo);
      setPokemonesTipo(response.data.datos || []);
    } catch (err) {
      console.error(err);
      setPokemonesTipo([]);
    } finally {
      setLoadingTipo(false);
    }
  };

  const handleSelectTipo = (tipo) => {
    setSelectedTipo(tipo);
    fetchPokemonesTipo(tipo);
  };

  const getTypeColor = (type) => {
    const colors = {
      normal: '#A8A878', fire: '#F08030', water: '#6890F0', grass: '#78C850',
      electric: '#F8D030', ice: '#98D8D8', fighting: '#C03028', poison: '#A040A0',
      ground: '#E0C068', flying: '#A890F0', psychic: '#F85888', bug: '#A8B820',
      rock: '#B8A038', ghost: '#705898', dragon: '#7038F8', dark: '#705848',
      steel: '#B8B8D0', fairy: '#EE99AC',
    };
    return colors[type?.toLowerCase()] || '#A8A878';
  };

  const tiposLista = Array.isArray(tipos) ? tipos : [];

  return (
    <div className="tipos-page">
      <div className="page-header">
        <h1>🎨 Tipos de Pokémon</h1>
        <p>Explora Pokémones agrupados por tipo</p>
      </div>

      <div className="tipos-container">
        {/* Panel de tipos */}
        <div className="tipos-panel">
          <h2>Tipos Disponibles</h2>
          {loading ? (
            <div className="loading">Cargando tipos...</div>
          ) : error ? (
            <div className="error">{error}</div>
          ) : (
            <div className="tipos-list">
              {tiposLista.map((tipo) => (
                <button
                  key={tipo.tipo}
                  className={`tipo-btn ${selectedTipo === tipo.tipo ? 'active' : ''}`}
                  onClick={() => handleSelectTipo(tipo.tipo)}
                  style={selectedTipo === tipo.tipo ? { backgroundColor: getTypeColor(tipo.tipo) } : {}}
                >
                  <span className="tipo-name">{tipo.tipo}</span>
                  <span className="tipo-count">{tipo.cantidad}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Panel de Pokémones */}
        <div className="pokemones-panel">
          {selectedTipo ? (
            <>
              <h2>Pokémones tipo {selectedTipo}</h2>
              {loadingTipo ? (
                <div className="loading">Cargando Pokémones...</div>
              ) : pokemonesTipo.length === 0 ? (
                <div className="no-results">No hay Pokémones de este tipo</div>
              ) : (
                <div className="pokemones-grid">
                  {pokemonesTipo.map((pokemon) => (
                    <div key={pokemon.id} className="pokemon-mini-card">
                      <img
                        src={pokemon.url_imagen_oficial || 'https://via.placeholder.com/100'}
                        alt={pokemon.nombre}
                        className="pokemon-mini-image"
                      />
                      <p className="pokemon-mini-name">{pokemon.nombre}</p>
                      <p className="pokemon-mini-number">#{String(pokemon.numero_pokedex).padStart(3, '0')}</p>
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="empty-state">
              <h2>Selecciona un tipo</h2>
              <p>Elige un tipo de la lista de la izquierda para ver los Pokémones correspondientes</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TiposPage;