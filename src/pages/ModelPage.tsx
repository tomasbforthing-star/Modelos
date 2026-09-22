import React, { useEffect } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import { 
  FileText, 
  ExternalLink, 
  Car, 
  Cpu, 
  Armchair, 
  ShieldCheck, 
  BatteryCharging, 
  Zap, 
  Sparkles,
  Gauge,
  Activity,
  Package,
  Users
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ModelData, AttributeItem } from '../types';
import rawModels from '../data/models.json';

// Helper to render dynamic automotive icons
const renderAttributeIcon = (iconName?: string) => {
  const className = "w-7 h-7 sm:w-8 sm:h-8 text-[#DD0A14] transition-transform duration-200 group-hover:scale-110";
  switch (iconName) {
    case 'cpu':
      return <Cpu className={className} />;
    case 'armchair':
      return <Armchair className={className} />;
    case 'shield':
      return <ShieldCheck className={className} />;
    case 'battery':
      return <BatteryCharging className={className} />;
    case 'zap':
      return <Zap className={className} />;
    case 'sparkles':
      return <Sparkles className={className} />;
    case 'gauge':
      return <Gauge className={className} />;
    case 'activity':
      return <Activity className={className} />;
    case 'package':
      return <Package className={className} />;
    case 'users':
      return <Users className={className} />;
    case 'car':
    default:
      return <Car className={className} />;
  }
};

export const ModelPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { t, lang } = useLanguage();

  const models: ModelData[] = rawModels as unknown as ModelData[];
  const model = models.find(
    (m) => m.slug.toLowerCase() === slug?.toLowerCase() && m.activo
  );

  // Update document title dynamically
  useEffect(() => {
    if (model) {
      document.title = `Forthing Argentina | ${model.nombre}`;
    } else {
      document.title = 'Forthing Argentina | Modelo no encontrado';
    }
    window.scrollTo(0, 0);
  }, [model]);

  if (!model) {
    return <Navigate to="/404" replace />;
  }

  const category = lang === 'en' ? model.categoriaEn : model.categoriaEs;
  const slogan = lang === 'en' ? model.esloganEn : model.esloganEs;
  const description = lang === 'en' ? model.descripcionEn : model.descripcionEs;
  const attributes: AttributeItem[] = lang === 'en' ? model.atributosEn : model.atributosEs;
  const hasAttributes = attributes && attributes.length > 0;
  const hasFichaTecnica = Boolean(model.fichaTecnicaUrl && model.fichaTecnicaUrl.trim().length > 0);

  return (
    <div className="min-h-screen bg-[#222223] flex flex-col justify-between selection:bg-[#DD0A14] selection:text-white">
      
      {/* 
        ============================================================
        HERO SECTION (High-Contrast Vehicle with targeted subtle edge blend)
        ============================================================
      */}
      <section className="w-full bg-[#FFFFFF] text-[#222223] relative overflow-hidden border-b border-[#E5E7EB]">
        
        {/* Desktop Seamless Right Vehicle Photo */}
        <div className="hidden lg:block absolute inset-y-0 right-0 w-[58%] xl:w-[62%] z-0 overflow-hidden pointer-events-none flex items-center justify-end">
          <img
            src={model.imagenPrincipal}
            alt={`${model.nombre} - Forthing Argentina`}
            className="w-full h-full object-contain object-right"
            loading="eager"
          />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10 lg:py-12 relative z-10">
          
          {/* Main Hero Container */}
          <div className="grid grid-cols-1 lg:grid-cols-12 items-center min-h-[420px]">
            
            {/* Left Content Area */}
            <div className="lg:col-span-6 xl:col-span-5 flex flex-col justify-center text-center lg:text-left z-10 pr-0 lg:pr-4">
              
              {/* Category Tag */}
              <div className="inline-flex items-center gap-2 self-center lg:self-start px-3 py-1 rounded bg-[#222223]/5 border border-[#222223]/10 text-[#4B4F54] text-xs font-bold uppercase tracking-widest mb-3">
                <span>{category}</span>
              </div>

              {/* Model Title: FORTHING on top, unbroken model name on next line */}
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black font-automotive-title tracking-tight text-[#222223] leading-none mb-3">
                <span className="block text-2xl sm:text-3xl lg:text-4xl text-[#4B4F54] font-extrabold tracking-wider mb-1">
                  FORTHING
                </span>
                <span className="whitespace-nowrap text-[#222223]">
                  {model.nombre}
                </span>
              </h1>

              {/* Slogan */}
              {slogan && (
                <h2 className="text-base sm:text-xl font-bold text-[#222223] tracking-tight leading-snug mb-2 font-sans">
                  {slogan}
                </h2>
              )}

              {/* Description */}
              {description && (
                <p className="text-xs sm:text-sm text-[#75787B] leading-relaxed max-w-xl mx-auto lg:mx-0 mb-4 sm:mb-6 font-normal">
                  {description}
                </p>
              )}

              {/* Mobile/Tablet Seamless Vehicle Photo (Natural Aspect Ratio) */}
              <div className="block lg:hidden my-4 sm:my-6 w-full">
                <div className="relative w-full flex items-center justify-center">
                  <img
                    src={model.imagenPrincipal}
                    alt={`${model.nombre} - Forthing Argentina`}
                    className="w-full h-auto max-h-[340px] sm:max-h-[420px] object-contain object-center"
                    loading="eager"
                  />
                </div>
              </div>

              {/* Action Buttons with Exact Matching Height */}
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-center lg:justify-start gap-3 pt-2 w-full">
                
                {/* Button 1: Ver Ficha Técnica (Red #DD0A14) */}
                {hasFichaTecnica ? (
                  <a
                    href={model.fichaTecnicaUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="h-12 px-6 bg-[#DD0A14] hover:bg-[#BE0811] text-white font-bold text-xs uppercase tracking-wider rounded transition-all duration-200 shadow-md shadow-[#DD0A14]/25 hover:shadow-lg hover:shadow-[#DD0A14]/35 hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2 text-center"
                  >
                    <FileText className="w-4 h-4 text-white" />
                    <span>{t('model.downloadSpecs')}</span>
                  </a>
                ) : (
                  <button
                    disabled
                    className="h-12 px-6 bg-[#DD0A14]/40 text-white/70 font-bold text-xs uppercase tracking-wider rounded cursor-not-allowed flex items-center justify-center gap-2 text-center"
                    title={t('model.specsPending')}
                  >
                    <FileText className="w-4 h-4 text-white/60" />
                    <span>{t('model.downloadSpecs')}</span>
                  </button>
                )}

                {/* Button 2: Ver Sitio Oficial (White with dark border) */}
                <a
                  href={model.sitioOficialUrl || "https://forthing.com.ar/"}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="h-12 px-6 bg-white hover:bg-gray-50 text-[#222223] font-bold text-xs uppercase tracking-wider rounded border-2 border-[#222223] transition-all duration-200 hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2 text-center shadow-sm"
                >
                  <span>{t('model.viewOfficialSite')}</span>
                  <ExternalLink className="w-4 h-4 text-[#222223]" />
                </a>

              </div>

            </div>

            {/* Right Spacer for Desktop Layout */}
            <div className="hidden lg:block lg:col-span-6 xl:col-span-7 pointer-events-none" />

          </div>

        </div>
      </section>

      {/* 
        ============================================================
        ATTRIBUTES SECTION (Unbroken continuous row)
        ============================================================
      */}
      {hasAttributes && (
        <section className="w-full bg-[#222223] text-white py-10 sm:py-14 border-t border-[#333538] relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            {/* Section Heading: TODO LO QUE BUSCÁS EN UN FORTHING */}
            <div className="mb-10 text-center lg:text-left">
              <h3 className="text-xl sm:text-2xl lg:text-3xl font-black font-automotive-title tracking-wider text-white">
                {t('model.featuresTitle')}
              </h3>
              <div className="w-16 h-1 bg-[#DD0A14] mt-2.5 mx-auto lg:mx-0 rounded-full" />
            </div>

            {/* Continuous Attributes Grid */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 divide-y lg:divide-y-0 lg:divide-x divide-[#3D4145]/40">
              {attributes.map((attr, index) => (
                <div
                  key={index}
                  className={`group flex flex-col justify-between pt-4 lg:pt-0 ${
                    index > 0 ? 'lg:pl-8' : ''
                  }`}
                >
                  <div>
                    {/* Icon */}
                    <div className="mb-4">
                      {renderAttributeIcon(attr.icono)}
                    </div>

                    {/* Title */}
                    <h4 className="text-sm sm:text-base font-bold text-white group-hover:text-[#DD0A14] transition-colors leading-snug mb-1.5 font-sans">
                      {attr.titulo}
                    </h4>

                    {/* Subtitle / Description */}
                    {attr.subtitulo && (
                      <p className="text-xs text-[#A0A3A6] leading-relaxed">
                        {attr.subtitulo}
                      </p>
                    )}
                  </div>

                  {/* Red accent line beneath attribute */}
                  <div className="w-8 h-[2px] bg-[#DD0A14] mt-4 group-hover:w-16 transition-all duration-300" />
                </div>
              ))}
            </div>

          </div>
        </section>
      )}

    </div>
  );
};
