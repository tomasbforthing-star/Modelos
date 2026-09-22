import React, { useRef } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { X, Download, ExternalLink, QrCode, CheckCircle2, AlertTriangle } from 'lucide-react';
import { ModelData } from '../types';
import { useLanguage } from '../context/LanguageContext';

interface QrModalProps {
  model: ModelData | null;
  isOpen: boolean;
  onClose: () => void;
}

/**
 * DEFINITIVE_PUBLIC_URL:
 * Configured production domain for official QR codes and print distribution.
 */
export const DEFINITIVE_PUBLIC_URL: string = 'https://modelos-forthing.vercel.app';

export const QrModal: React.FC<QrModalProps> = ({ model, isOpen, onClose }) => {
  const { lang, t } = useLanguage();
  const svgRef = useRef<HTMLDivElement>(null);

  if (!isOpen || !model) return null;

  const isProductionConfigured = Boolean(
    typeof DEFINITIVE_PUBLIC_URL === 'string' &&
    DEFINITIVE_PUBLIC_URL.trim().length > 0 &&
    DEFINITIVE_PUBLIC_URL.startsWith('http')
  );
  
  const currentOrigin = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000';
  const activeQrUrl = isProductionConfigured
    ? `${DEFINITIVE_PUBLIC_URL.replace(/\/$/, '')}/modelos/${model.slug}`
    : `${currentOrigin}/modelos/${model.slug}`;

  const isTestMode = !isProductionConfigured;

  const handleDownloadQR = () => {
    if (!svgRef.current) return;
    const svgElement = svgRef.current.querySelector('svg');
    if (!svgElement) return;

    const svgData = new XMLSerializer().serializeToString(svgElement);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();

    // 1200x1200px High-resolution master for offset and digital printing
    canvas.width = 1200;
    canvas.height = 1200;

    img.onload = () => {
      if (!ctx) return;
      // Clean white background
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1200, 1200);
      
      // Top test banner if in test mode
      if (isTestMode) {
        ctx.fillStyle = '#FFFBEB';
        ctx.fillRect(0, 0, 1200, 70);
        ctx.fillStyle = '#B45309';
        ctx.font = 'bold 22px Montserrat, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('CÓDIGO QR - SOLO PARA PRUEBAS (ENTORNO PROVISORIO)', 600, 44);
      }

      // Draw QR code with generous quiet-zone padding
      ctx.drawImage(img, 175, 120, 850, 850);
      
      // Model Title
      ctx.fillStyle = '#222223';
      ctx.font = 'bold 42px Montserrat, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`FORTHING ${model.nombre.toUpperCase()}`, 600, 1050);

      // Public URL
      ctx.fillStyle = '#75787B';
      ctx.font = 'bold 24px Inter, sans-serif';
      ctx.fillText(activeQrUrl, 600, 1105);

      if (isTestMode) {
        ctx.fillStyle = '#DD0A14';
        ctx.font = 'bold 20px Inter, sans-serif';
        ctx.fillText('[ SOLO PARA PRUEBAS - NO APTO PARA IMPRENTA OFICIAL ]', 600, 1145);
      }

      const a = document.createElement('a');
      const filename = isTestMode
        ? `qr-prueba-forthing-${model.slug}.png`
        : `qr-oficial-forthing-${model.slug}.png`;
      a.download = filename;
      a.href = canvas.toDataURL('image/png');
      a.click();
    };

    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fadeIn"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="qr-modal-title"
    >
      <div 
        className="bg-[#1C1C1D] border border-[#3D4145] rounded-2xl max-w-lg w-full p-6 sm:p-8 text-center relative shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-[#75787B] hover:text-white rounded-full bg-white/5 hover:bg-white/10 transition-colors"
          aria-label={t('qrModal.close')}
        >
          <X className="w-5 h-5" />
        </button>

        {/* Icon & Title */}
        <div className="inline-flex p-2.5 rounded-full bg-[#DD0A14]/15 text-[#DD0A14] mb-3">
          <QrCode className="w-6 h-6" />
        </div>

        <h3 id="qr-modal-title" className="text-xl sm:text-2xl font-black font-automotive-title text-white">
          FORTHING {model.nombre}
        </h3>
        
        <p className="text-xs sm:text-sm text-[#A0A3A6] mt-1.5 mb-4">
          {t('qrModal.desc')}
        </p>

        {/* Status Badge */}
        {isProductionConfigured ? (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold mb-4">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{t('qrModal.readyPrint')}</span>
          </div>
        ) : (
          <div className="flex items-center justify-center gap-2 p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-amber-300 text-xs font-medium mb-4 text-left">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
            <div>
              <p className="font-bold text-amber-200">
                {lang === 'en' ? 'Testing Mode Only' : 'Código QR solo para pruebas'}
              </p>
              <p className="text-[11px] text-amber-300/80 mt-0.5">
                {lang === 'en'
                  ? 'Official print-ready QR codes will be generated once the definitive public URL is deployed.'
                  : 'Los QR oficiales para imprenta se habilitarán al configurar la URL pública definitiva.'}
              </p>
            </div>
          </div>
        )}

        {/* QR Code Container */}
        <div className="bg-white p-4 rounded-xl inline-block shadow-inner mx-auto mb-4 relative" ref={svgRef}>
          <QRCodeSVG
            value={activeQrUrl}
            size={190}
            level="H"
            includeMargin={false}
            fgColor="#222223"
            bgColor="#FFFFFF"
          />
        </div>

        {/* Encoded URL Box */}
        <div className="bg-[#2A2D30] rounded-lg p-2.5 mb-5 text-xs text-[#A0A3A6] font-mono break-all flex items-center justify-between gap-2 border border-[#3D4145]">
          <span className="truncate text-left text-white/90 font-medium">{activeQrUrl}</span>
          <a
            href={activeQrUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#DD0A14] hover:underline flex items-center gap-1 font-sans font-bold flex-shrink-0"
          >
            <span>Abrir</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>

        {/* Download Action */}
        <button
          onClick={handleDownloadQR}
          className="w-full py-3.5 px-4 bg-[#DD0A14] hover:bg-[#BE0811] text-white font-bold rounded-lg flex items-center justify-center gap-2 transition-colors duration-200 text-xs sm:text-sm shadow-lg shadow-[#DD0A14]/25 uppercase tracking-wider"
        >
          <Download className="w-4 h-4" />
          <span>
            {isTestMode
              ? (lang === 'en' ? 'Download QR (Testing only)' : 'Descargar QR (Solo para pruebas)')
              : (lang === 'en' ? 'Download Official Print QR' : 'Descargar QR Oficial (Alta Resolución)')}
          </span>
        </button>
      </div>
    </div>
  );
};
