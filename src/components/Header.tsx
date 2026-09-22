import React from 'react';
import { Link } from 'react-router-dom';
import { Instagram } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const Header: React.FC = () => {
  const { lang, setLang } = useLanguage();

  return (
    <header className="w-full bg-[#222223] border-b border-[#333538] sticky top-0 z-40 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 h-16 sm:h-20 flex items-center justify-between gap-2">
        
        {/* Logo Forthing Argentina (White lettering PNG on dark navbar) */}
        <Link 
          to="/" 
          className="flex items-center group focus:outline-none focus:ring-2 focus:ring-[#DD0A14] rounded-sm py-1 shrink-0"
          aria-label="Forthing Argentina - Inicio"
        >
          <img 
            src="/assets/logo-forthing-white.png" 
            alt="Forthing Argentina" 
            className="h-8 sm:h-10 md:h-11 w-auto max-w-[190px] sm:max-w-none object-contain transition-transform duration-300 group-hover:scale-[1.02]"
          />
        </Link>

        {/* Right navigation elements (Instagram + Language Switcher) */}
        <div className="flex items-center gap-2.5 sm:gap-5 shrink-0">
          
          {/* Instagram link */}
          <a
            href="https://www.instagram.com/forthingargentina/?hl=es"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 sm:gap-2 text-[#A0A3A6] hover:text-white transition-colors duration-200 text-xs sm:text-sm font-medium group"
            aria-label="Instagram Forthing Argentina"
          >
            <div className="p-1 sm:p-1.5 rounded-full bg-white/5 group-hover:bg-[#DD0A14]/20 transition-colors">
              <Instagram className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-white" />
            </div>
            <span className="hidden sm:inline font-sans font-normal text-xs sm:text-sm">@forthingargentina</span>
          </a>

          {/* Divider */}
          <div className="h-4 w-[1px] bg-[#4B4F54]" aria-hidden="true" />

          {/* Language Switcher ES | EN */}
          <div className="flex items-center space-x-1 sm:space-x-1.5 text-xs sm:text-sm font-bold tracking-wider font-mono">
            <button
              onClick={() => setLang('es')}
              className={`px-1 sm:px-1.5 py-0.5 rounded transition-all duration-200 focus:outline-none focus:ring-1 focus:ring-[#DD0A14] ${
                lang === 'es'
                  ? 'text-[#DD0A14] font-extrabold scale-105'
                  : 'text-[#75787B] hover:text-white'
              }`}
              aria-label="Cambiar idioma a Español"
              aria-pressed={lang === 'es'}
            >
              ES
            </button>
            <span className="text-[#4B4F54] select-none text-xs">|</span>
            <button
              onClick={() => setLang('en')}
              className={`px-1 sm:px-1.5 py-0.5 rounded transition-all duration-200 focus:outline-none focus:ring-1 focus:ring-[#DD0A14] ${
                lang === 'en'
                  ? 'text-[#DD0A14] font-extrabold scale-105'
                  : 'text-[#75787B] hover:text-white'
              }`}
              aria-label="Switch language to English"
              aria-pressed={lang === 'en'}
            >
              EN
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
