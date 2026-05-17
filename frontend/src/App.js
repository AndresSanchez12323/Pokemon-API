import React, { useState } from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Navigation from './components/Navigation';
import HomePage from './pages/HomePage';
import PokemonListPage from './pages/PokemonListPage';
import PokemonDetailPage from './pages/PokemonDetailPage';
import TiposPage from './pages/TiposPage';
import LegendariosPage from './pages/LegendariosPage';
import EstadisticasPage from './pages/EstadisticasPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/pokemones" element={<PokemonListPage />} />
            <Route path="/pokemon/:id" element={<PokemonDetailPage />} />
            <Route path="/tipos" element={<TiposPage />} />
            <Route path="/legendarios" element={<LegendariosPage />} />
            <Route path="/estadisticas" element={<EstadisticasPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
