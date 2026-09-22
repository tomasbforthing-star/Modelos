import React from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle, ArrowLeft } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const NotFoundPage: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-16 bg-[#222223] text-center">
      <div className="max-w-md w-full p-8 rounded-2xl bg-[#1C1C1D] border border-[#333538] shadow-2xl">
        <div className="w-16 h-16 mx-auto rounded-full bg-[#DD0A14]/15 border border-[#DD0A14]/30 flex items-center justify-center text-[#DD0A14] mb-6">
          <AlertCircle className="w-8 h-8" />
        </div>
        
        <h1 className="text-2xl sm:text-3xl font-black font-automotive-title text-white mb-3">
          {t('notFound.title')}
        </h1>
        
        <p className="text-sm text-[#A0A3A6] mb-8 leading-relaxed">
          {t('notFound.desc')}
        </p>

        <Link
          to="/"
          className="inline-flex items-center justify-center gap-2 w-full py-3.5 px-6 bg-[#DD0A14] hover:bg-[#BE0811] text-white font-bold text-xs uppercase tracking-wider rounded-lg transition-colors shadow-lg shadow-[#DD0A14]/20"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{t('notFound.button')}</span>
        </Link>
      </div>
    </div>
  );
};
