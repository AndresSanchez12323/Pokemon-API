import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FiMenu, FiX } from 'react-icons/fi';
import './Navigation.css';

function Navigation() {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <button className="menu-toggle" onClick={toggleMenu}>
          {menuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
        </button>

        <ul className={`nav-menu ${menuOpen ? 'active' : ''}`}>
          <li className="nav-item">
            <Link to="/" className="nav-link" onClick={() => setMenuOpen(false)}>
              🏠 Inicio
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/pokemones" className="nav-link" onClick={() => setMenuOpen(false)}>
              📋 Pokédex
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/tipos" className="nav-link" onClick={() => setMenuOpen(false)}>
              🎨 Tipos
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/legendarios" className="nav-link" onClick={() => setMenuOpen(false)}>
              ⭐ Legendarios
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/estadisticas" className="nav-link" onClick={() => setMenuOpen(false)}>
              📊 Estadísticas
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
