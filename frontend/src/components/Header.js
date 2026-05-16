import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <h1 className="logo">
            ⚡ POKÉDEX
          </h1>
          <p className="subtitle">Sistema Completo de Pokémon</p>
        </div>
        <div className="header-info">
          <p className="api-status">✓ API Conectada</p>
          <p className="version">v1.0</p>
        </div>
      </div>
    </header>
  );
}

export default Header;
