import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { pokemonService } from '../services/pokemonService';
import './PokemonDetailPage.css';

function PokemonDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [pokemon, setPokemon] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPokemonDetail();
  }, [id]);

  const fetchPokemonDetail = async () => {
    try {
      setLoading(true);
      const response = await pokemonService.obtenerPorId(id);
      setPokemon(response.data.datos);
      setError(null);
    } catch (err) {
      setError('Error al cargar Pokémon: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      normal: '#A8A878',
      fire: '#F08030',
      water: '#6890F0',
      grass: '#78C850',
      electric: '#F8D030',
      ice: '#98D8D8',
      fighting: '#C03028',
      poison: '#A040A0',
      ground: '#E0C068',
      flying: '#A890F0',
      psychic: '#F85888',
      bug: '#A8B820',
      rock: '#B8A038',
      ghost: '#705898',
      dragon: '#7038F8',
      dark: '#705848',
      steel: '#B8B8D0',
      fairy: '#EE99AC',
    };
    return colors[type?.toLowerCase()] || '#A8A878';
  };

  if (loading) {
    return (
      <div className="detail-page">
        <div className="loading-detail">⏳ Cargando información del Pokémon...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="detail-page">
        <button className="back-btn" onClick={() => navigate('/pokemones')}>
          ← Volver
        </button>
        <div className="error-detail">{error}</div>
      </div>
    );
  }

  if (!pokemon) {
    return (
      <div className="detail-page">
        <button className="back-btn" onClick={() => navigate('/pokemones')}>
          ← Volver
        </button>
        <div className="error-detail">Pokémon no encontrado</div>
      </div>
    );
  }

  return (
    <div className="detail-page">
      <button className="back-btn" onClick={() => navigate('/pokemones')}>
        ← Volver a Pokédex
      </button>

      <div className="detail-container">
        <div className="detail-header">
          <h1 className="pokemon-name-detail">
            {pokemon.nombre}
          </h1>
          <div className="pokemon-number-detail">
            #{String(pokemon.numero_pokedex).padStart(3, '0')}
          </div>
        </div>

        <div className="detail-grid">
          {/* Columna izquierda - Imagen */}
          <div className="detail-image-section">
            <div className="image-container">
              {pokemon.url_imagen_oficial ? (
                <img
                  src={pokemon.url_imagen_oficial}
                  alt={pokemon.nombre}
                  className="detail-image"
                  onError={(e) => {
                    e.target.src = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png';
                  }}
                />
              ) : (
                <div className="placeholder">No Image</div>
              )}
            </div>

            {pokemon.es_legendario && (
              <div className="legendary-large">⭐ LEGENDARIO</div>
            )}
          </div>

          {/* Columna derecha - Información */}
          <div className="detail-info-section">
            {/* Tipos */}
            <div className="info-card">
              <h3>Tipos</h3>
              <div className="types-container">
                <span
                  className="type-badge-large"
                  style={{ backgroundColor: getTypeColor(pokemon.tipo_1) }}
                >
                  {pokemon.tipo_1}
                </span>
                {pokemon.tipo_2 !== 'No definido' && (
                  <span
                    className="type-badge-large"
                    style={{ backgroundColor: getTypeColor(pokemon.tipo_2) }}
                  >
                    {pokemon.tipo_2}
                  </span>
                )}
              </div>
            </div>

            {/* Medidas */}
            <div className="info-card">
              <h3>Medidas</h3>
              <div className="measurements">
                <div className="measurement">
                  <span className="label">Altura:</span>
                  <span className="value">{pokemon.altura_dm} dm ({(pokemon.altura_dm * 10) / 100} m)</span>
                </div>
                <div className="measurement">
                  <span className="label">Peso:</span>
                  <span className="value">{pokemon.peso_hectogramos} hg ({pokemon.peso_hectogramos / 10} kg)</span>
                </div>
              </div>
            </div>

            {/* Experiencia */}
            <div className="info-card">
              <h3>Experiencia Base</h3>
              <div className="exp-bar">
                <div
                  className="exp-fill"
                  style={{ width: `${(pokemon.experiencia_base / 300) * 100}%` }}
                ></div>
              </div>
              <p className="exp-value">{pokemon.experiencia_base} puntos</p>
            </div>

            {/* Imágenes */}
            <div className="info-card">
              <h3>Imágenes</h3>
              <div className="images-gallery">
                {pokemon.url_imagen_frontal && (
                  <div className="gallery-item">
                    <span className="gallery-label">Frontal</span>
                    <img
                      src={pokemon.url_imagen_frontal}
                      alt="Frontal"
                      className="gallery-image"
                    />
                  </div>
                )}
                {pokemon.url_imagen_trasera && (
                  <div className="gallery-item">
                    <span className="gallery-label">Trasera</span>
                    <img
                      src={pokemon.url_imagen_trasera}
                      alt="Trasera"
                      className="gallery-image"
                    />
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PokemonDetailPage;
