import React from 'react';
import { Instagram, ExternalLink } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const Footer: React.FC = () => {
  const { t } = useLanguage();

  return (
    <footer className="w-full bg-[#181819] border-t border-[#2D3033] py-6 text-[#75787B] text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        
        {/* Left: Copyright */}
        <p className="text-center sm:text-left text-[#A0A3A6]">
          © {new Date().getFullYear()} {t('footer.rights')}
        </p>

        {/* Center/Right: Instagram & Official Site */}
        <div className="flex items-center gap-6">
          <a
            href="https://www.instagram.com/forthingargentina/?hl=es"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-[#A0A3A6] hover:text-white transition-colors"
          >
            <Instagram className="w-3.5 h-3.5 text-[#DD0A14]" />
            <span className="font-normal">@forthingargentina</span>
          </a>

          <div className="h-3 w-[1px] bg-[#3D4145]" aria-hidden="true" />

          <a
            href="https://forthing.com.ar/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-[#A0A3A6] hover:text-white transition-colors"
          >
            <span>{t('footer.officialWeb')}</span>
            <ExternalLink className="w-3 h-3 text-[#DD0A14]" />
          </a>
        </div>

      </div>
    </footer>
  );
};
