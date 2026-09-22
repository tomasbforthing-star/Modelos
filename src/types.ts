export type SupportedLang = 'es' | 'en';

export interface AttributeItem {
  titulo: string;
  subtitulo?: string;
  icono?: 'car' | 'cpu' | 'armchair' | 'shield' | 'battery' | 'zap' | 'sparkles' | 'gauge' | 'activity' | 'users' | 'package';
}

export interface ModelData {
  slug: string;
  nombre: string;
  categoriaEs: string;
  categoriaEn: string;
  imagenPrincipal: string;
  imagenTarjeta: string;
  esloganEs: string;
  esloganEn: string;
  descripcionEs: string;
  descripcionEn: string;
  atributosEs: AttributeItem[];
  atributosEn: AttributeItem[];
  fichaTecnicaUrl: string;
  sitioOficialUrl: string;
  activo: boolean;
  orden: number;
  heroPositionDesktop?: string;
  heroPositionMobile?: string;
  heroScaleDesktop?: string;
  heroScaleMobile?: string;
  heroGradientClass?: string;
}
