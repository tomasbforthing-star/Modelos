import React, { createContext, useContext, useState, useEffect } from 'react';
import { SupportedLang } from '../types';

interface LanguageContextType {
  lang: SupportedLang;
  setLang: (lang: SupportedLang) => void;
  toggleLang: () => void;
  t: (key: string) => string;
}

const translations: Record<SupportedLang, Record<string, string>> = {
  es: {
    'nav.instagram': '@forthingargentina',
    'nav.allModels': 'Ver todos los modelos',
    'nav.backToCatalog': 'Volver al catálogo',
    'catalog.badge': 'Gama Oficial Forthing Argentina',
    'catalog.title': 'Elegí tu próximo Forthing',
    'catalog.subtitle': 'Diseño vanguardista, tecnología híbrida y eléctrica de última generación, y una experiencia de conducción superior.',
    'catalog.viewModel': 'Ver modelo',
    'catalog.qrShare': 'Código QR',
    'catalog.activeModels': 'modelos disponibles',
    'model.downloadSpecs': 'VER FICHA TÉCNICA',
    'model.viewOfficialSite': 'VER SITIO OFICIAL',
    'model.featuresTitle': 'TODO LO QUE BUSCÁS EN UN FORTHING',
    'model.featuresSubtitle': 'Tecnología, seguridad y confort diseñados para una experiencia superior.',
    'model.specsPending': 'Ficha técnica próximamente disponible',
    'footer.followUs': 'SEGUINOS',
    'footer.rights': 'Forthing Argentina. Todos los derechos reservados.',
    'footer.officialWeb': 'Sitio Web Oficial',
    'notFound.title': 'Modelo no encontrado',
    'notFound.desc': 'El vehículo que buscás no existe o fue retirado del catálogo oficial.',
    'notFound.button': 'Ir al Catálogo General',
    'qrModal.title': 'Código QR Oficial',
    'qrModal.desc': 'Escaneá este código para acceder directamente a la ficha digital de este vehículo desde cualquier smartphone o tablet.',
    'qrModal.productionUrl': 'URL pública para códigos QR impresos:',
    'qrModal.localUrl': 'URL de prueba local:',
    'qrModal.qrTypeSelector': 'Tipo de QR a generar:',
    'qrModal.productionMode': 'QR para Impresión / Producción (HTTPS)',
    'qrModal.devMode': 'QR Local (Pruebas)',
    'qrModal.download': 'Descargar imagen QR (Alta Resolución)',
    'qrModal.warningLocal': 'Atención: Los QR con URL local sólo funcionan en esta computadora.',
    'qrModal.readyPrint': 'Listo para imprenta y flyers',
    'qrModal.close': 'Cerrar'
  },
  en: {
    'nav.instagram': '@forthingargentina',
    'nav.allModels': 'All models',
    'nav.backToCatalog': 'Back to catalog',
    'catalog.badge': 'Official Forthing Argentina Lineup',
    'catalog.title': 'Choose your next Forthing',
    'catalog.subtitle': 'Avant-garde styling, next-generation hybrid and electric powertrains, and a superior driving experience.',
    'catalog.viewModel': 'View model',
    'catalog.qrShare': 'QR Code',
    'catalog.activeModels': 'available models',
    'model.downloadSpecs': 'VIEW TECH SPECS',
    'model.viewOfficialSite': 'VISIT OFFICIAL SITE',
    'model.featuresTitle': 'EVERYTHING YOU LOOK FOR IN A FORTHING',
    'model.featuresSubtitle': 'Technology, safety and comfort engineered for an elevated driving experience.',
    'model.specsPending': 'Technical specifications coming soon',
    'footer.followUs': 'FOLLOW US',
    'footer.rights': 'Forthing Argentina. All rights reserved.',
    'footer.officialWeb': 'Official Website',
    'notFound.title': 'Model not found',
    'notFound.desc': 'The requested vehicle does not exist or has been removed from the official catalog.',
    'notFound.button': 'Go to General Catalog',
    'qrModal.title': 'Official QR Code',
    'qrModal.desc': 'Scan this code to directly access this vehicle digital spec sheet from any smartphone or tablet.',
    'qrModal.productionUrl': 'Public URL for printed QR codes:',
    'qrModal.localUrl': 'Local test URL:',
    'qrModal.qrTypeSelector': 'QR Code type to generate:',
    'qrModal.productionMode': 'Print / Production QR (HTTPS)',
    'qrModal.devMode': 'Local Test QR',
    'qrModal.download': 'Download QR Image (High Resolution)',
    'qrModal.warningLocal': 'Warning: QR codes with local URLs only work on this machine.',
    'qrModal.readyPrint': 'Ready for print & flyers',
    'qrModal.close': 'Close'
  }
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [lang, setLangState] = useState<SupportedLang>(() => {
    const saved = localStorage.getItem('forthing_lang');
    if (saved === 'es' || saved === 'en') return saved;
    const browser = navigator.language.slice(0, 2);
    return browser === 'en' ? 'en' : 'es';
  });

  const setLang = (newLang: SupportedLang) => {
    setLangState(newLang);
    localStorage.setItem('forthing_lang', newLang);
  };

  const toggleLang = () => {
    setLang(lang === 'es' ? 'en' : 'es');
  };

  const t = (key: string): string => {
    return translations[lang][key] || key;
  };

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  return (
    <LanguageContext.Provider value={{ lang, setLang, toggleLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
