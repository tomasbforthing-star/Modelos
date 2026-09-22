import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight, QrCode, Sparkles } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ModelData } from '../types';
import rawModels from '../data/models.json';
import { QrModal } from '../components/QrModal';

export const CatalogPage: React.FC = () => {
  const { t, lang } = useLanguage();
  const [selectedQrModel, setSelectedQrModel] = useState<ModelData | null>(null);

  const models: ModelData[] = (rawModels as unknown as ModelData[])
    .filter((m) => m.activo)
    .sort((a, b) => a.orden - b.orden);

  return (
    <div className="min-h-screen bg-[#222223] flex flex-col">
      
      {/* Hero Banner for Catalog */}
      <section className="relative overflow-hidden pt-10 pb-12 sm:pt-14 sm:pb-16 border-b border-[#333538] bg-gradient-to-b from-[#1C1C1D] to-[#222223]">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[250px] bg-[#DD0A14]/10 blur-[100px] rounded-full pointer-events-none" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#DD0A14]/15 border border-[#DD0A14]/30 text-[#DD0A14] text-xs font-bold tracking-widest uppercase mb-3 animate-pulse">
            <Sparkles className="w-3.5 h-3.5" />
            <span>{t('catalog.badge')}</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black font-automotive-title tracking-tight text-white mb-3">
            {t('catalog.title')}
          </h1>

          <p className="max-w-2xl mx-auto text-sm sm:text-base text-[#A0A3A6] leading-relaxed">
            {t('catalog.subtitle')}
          </p>
        </div>
      </section>

      {/* Models Grid Section (5 Official Models) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14 flex-1 w-full">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {models.map((model) => {
            const category = lang === 'en' ? model.categoriaEn : model.categoriaEs;
            const slogan = lang === 'en' ? model.esloganEn : model.esloganEs;

            return (
              <article
                key={model.slug}
                className="group bg-[#1C1C1D] border border-[#333538] hover:border-[#DD0A14]/60 rounded-xl overflow-hidden flex flex-col transition-all duration-300 hover:shadow-xl hover:shadow-[#DD0A14]/10 hover:-translate-y-1"
              >
                {/* Vehicle Card Image Container */}
                <div className="relative aspect-[16/10] bg-[#151516] overflow-hidden">
                  <img
                    src={model.imagenTarjeta || model.imagenPrincipal}
                    alt={`${model.nombre} - Forthing Argentina`}
                    className="w-full h-full object-cover object-center transition-transform duration-500 group-hover:scale-105"
                    loading="lazy"
                  />
                  
                  {/* Category Tag */}
                  <div className="absolute top-3 left-3">
                    <span className="px-2.5 py-1 bg-[#222223]/90 backdrop-blur-md text-white border border-white/10 text-[11px] font-semibold tracking-wider uppercase rounded shadow">
                      {category}
                    </span>
                  </div>

                  {/* QR Fast Access Button */}
                  <button
                    onClick={() => setSelectedQrModel(model)}
                    className="absolute top-3 right-3 p-2 bg-[#222223]/90 hover:bg-[#DD0A14] text-white/80 hover:text-white rounded-lg backdrop-blur-md border border-white/10 transition-colors shadow-lg"
                    title={`${t('catalog.qrShare')}: ${model.nombre}`}
                    aria-label={`Ver QR de ${model.nombre}`}
                  >
                    <QrCode className="w-4 h-4" />
                  </button>
                </div>

                {/* Card Body */}
                <div className="p-5 sm:p-6 flex-1 flex flex-col justify-between">
                  <div>
                    <h2 className="text-xl sm:text-2xl font-black font-automotive-title text-white group-hover:text-[#DD0A14] transition-colors mb-1.5">
                      {model.nombre}
                    </h2>

                    {slogan && (
                      <p className="text-xs sm:text-sm font-semibold text-[#DD0A14] mb-2 leading-snug">
                        {slogan}
                      </p>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div className="pt-4 border-t border-[#2A2D30] flex items-center gap-3">
                    <Link
                      to={`/modelos/${model.slug}`}
                      className="flex-1 py-3 px-4 bg-[#DD0A14] hover:bg-[#BE0811] text-white font-bold text-xs uppercase tracking-wider rounded-md flex items-center justify-center gap-2 transition-all duration-200 shadow-md shadow-[#DD0A14]/20 group-hover:gap-3"
                    >
                      <span>{t('catalog.viewModel')}</span>
                      <ChevronRight className="w-4 h-4" />
                    </Link>

                    <button
                      onClick={() => setSelectedQrModel(model)}
                      className="p-3 bg-[#2A2D30] hover:bg-[#3D4145] text-white/90 hover:text-white rounded-md border border-[#4B4F54]/50 transition-colors flex items-center justify-center"
                      title={t('catalog.qrShare')}
                      aria-label="Abrir código QR"
                    >
                      <QrCode className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      </section>

      {/* QR Modal */}
      <QrModal
        model={selectedQrModel}
        isOpen={Boolean(selectedQrModel)}
        onClose={() => setSelectedQrModel(null)}
      />
    </div>
  );
};
