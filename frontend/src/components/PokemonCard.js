import React from 'react';
import { Link } from 'react-router-dom';
import './PokemonCard.css';

function PokemonCard({ pokemon }) {
  const gradientClass = `type-${pokemon.tipo_1?.toLowerCase() || 'normal'}`;
  
  return (
    <Link to={`/pokemon/${pokemon.numero_pokedex}`} className="pokemon-card-link">
      <div className={`pokemon-card ${gradientClass}`}>
        <div className="pokemon-number">
          #{String(pokemon.numero_pokedex).padStart(3, '0')}
        </div>

        <div className="pokemon-image-container">
          {pokemon.url_imagen_oficial ? (
            <img
              src={pokemon.url_imagen_oficial}
              alt={pokemon.nombre}
              className="pokemon-image"
              onError={(e) => {
                e.target.src = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png';
              }}
            />
          ) : (
            <div className="pokemon-image-placeholder">
              No Image
            </div>
          )}
        </div>

        <div className="pokemon-info">
          <h3 className="pokemon-name">
            {pokemon.nombre}
          </h3>

          <div className="pokemon-types">
            <span className={`type-badge ${pokemon.tipo_1?.toLowerCase()}`}>
              {pokemon.tipo_1}
            </span>
            {pokemon.tipo_2 !== 'No definido' && (
              <span className={`type-badge ${pokemon.tipo_2?.toLowerCase()}`}>
                {pokemon.tipo_2}
              </span>
            )}
          </div>

          <div className="pokemon-stats">
            <div className="stat">
              <span className="stat-label">Altura:</span>
              <span className="stat-value">{pokemon.altura_dm} dm</span>
            </div>
            <div className="stat">
              <span className="stat-label">Peso:</span>
              <span className="stat-value">{pokemon.peso_hectogramos} hg</span>
            </div>
          </div>

          {pokemon.es_legendario && (
            <div className="legendary-badge">⭐ LEGENDARIO</div>
          )}
        </div>
      </div>
    </Link>
  );
}

export default PokemonCard;
