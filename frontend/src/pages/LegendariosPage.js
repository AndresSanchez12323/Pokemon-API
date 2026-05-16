import React, { useEffect, useState } from 'react';
import { pokemonService } from '../services/pokemonService';
import PokemonCard from '../components/PokemonCard';
import './LegendariosPage.css';

function LegendariosPage() {
  const [pokemones, setPokemones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLegendarios();
  }, []);

  const fetchLegendarios = async () => {
    try {
      setLoading(true);
      const response = await pokemonService.obtenerLegendarios();
      setPokemones(response.data.datos || []);
      setError(null);
    } catch (err) {
      setError('Error al cargar Pokémones legendarios: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="legendarios-page">
      <div className="page-header legendary-header">
        <h1>⭐ Pokémones Legendarios</h1>
        <p>Los Pokémones más poderosos y raros de la región</p>
      </div>

      {loading ? (
        <div className="loading">⏳ Cargando Pokémones legendarios...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : pokemones.length === 0 ? (
        <div className="no-results">
          😢 No se encontraron Pokémones legendarios
        </div>
      ) : (
        <div className="legendary-container">
          <div className="legendary-info">
            <p>Se encontraron <strong>{pokemones.length} Pokémones legendarios</strong></p>
          </div>

          <div className="pokemon-grid">
            {pokemones.map((pokemon) => (
              <PokemonCard key={pokemon.id} pokemon={pokemon} />
            ))}
          </div>

          <div className="legendary-footer">
            <p>
              Los Pokémones legendarios son criaturas extraordinarias, a menudo únicos
              o en cantidades limitadas. Poseen un poder incomparable a los Pokémones ordinarios.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default LegendariosPage;