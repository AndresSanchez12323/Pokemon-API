import React, { useEffect, useState } from 'react';
import { pokemonService } from '../services/pokemonService';
import PokemonCard from '../components/PokemonCard';
import './PokemonListPage.css';

function PokemonListPage() {
  const [pokemones, setPokemones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [limite, setLimite] = useState(20);
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    fetchPokemones();
  }, [currentPage, limite]);

  const fetchPokemones = async () => {
    try {
      setLoading(true);
      const response = await pokemonService.obtenerTodos(currentPage, limite);
      setPokemones(response.data.datos || []);
      setTotalPages(response.data.total_paginas);
      setError(null);
    } catch (err) {
      setError('Error al cargar Pokémon: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const pokemonesFiltered = pokemones.filter(pokemon =>
    pokemon.nombre.toLowerCase().includes(busqueda.toLowerCase())
  );

  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
      window.scrollTo(0, 0);
    }
  };

  return (
    <div className="pokemon-list-page">
      <div className="page-header">
        <h1>📋 Pokédex Completa</h1>
        <p>Explora la base de datos completa de Pokémon</p>
      </div>

      <div className="controls-section">
        <div className="search-box">
          <input
            type="text"
            placeholder="🔍 Buscar Pokémon por nombre..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-controls">
          <div className="filter-group">
            <label htmlFor="limite">Pokémon por página:</label>
            <select
              id="limite"
              value={limite}
              onChange={(e) => {
                setLimite(Number(e.target.value));
                setCurrentPage(1);
              }}
              className="select-control"
            >
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={30}>30</option>
              <option value={50}>50</option>
            </select>
          </div>

          <div className="results-info">
            Mostrando {pokemonesFiltered.length} de {pokemones.length} resultados
          </div>
        </div>
      </div>

      {loading ? (
        <div className="loading">⏳ Cargando Pokémon...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : pokemonesFiltered.length === 0 ? (
        <div className="no-results">
          😢 No se encontraron Pokémon con ese nombre
        </div>
      ) : (
        <>
          <div className="pokemon-grid">
            {pokemonesFiltered.map((pokemon) => (
              <PokemonCard key={pokemon.id} pokemon={pokemon} />
            ))}
          </div>

          <div className="pagination">
            <button
              onClick={() => goToPage(1)}
              disabled={currentPage === 1}
              className="pagination-btn"
            >
              ⏮️ Primera
            </button>

            <button
              onClick={() => goToPage(currentPage - 1)}
              disabled={currentPage === 1}
              className="pagination-btn"
            >
              ⬅️ Anterior
            </button>

            <div className="page-info">
              Página {currentPage} de {totalPages}
            </div>

            <button
              onClick={() => goToPage(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="pagination-btn"
            >
              Siguiente ➡️
            </button>

            <button
              onClick={() => goToPage(totalPages)}
              disabled={currentPage === totalPages}
              className="pagination-btn"
            >
              Última ⏭️
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default PokemonListPage;
