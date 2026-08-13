export type Place = {
  id: string;
  names: { historical: string; modern: string; english?: string };
  coords: { lng: number; lat: number; precision: string };
  map?: { region?: string };
  notes?: string;
};

export type TimelineEvent = {
  year: string;
  date_note?: string;
  date_note_en?: string;
  title: string;
  title_en?: string;
  summary: string;
  summary_en?: string;
  place_id?: string | null;
  related_person_ids?: string[];
  sources?: string[];
  card_id?: string;
};

export type Relation = {
  type: string;
  target_id: string | null;
  note?: string;
  note_en?: string;
};

export type RoutePoint = {
  group: string;
  order: number;
  year?: string;
  place_id: string;
  event: string;
  event_en?: string;
};

export type BioPart =
  | { type: "text"; value: string }
  | { type: "link"; id: string; label: string };

export type Emperor = {
  id: string;
  tier: string;
  sort_key?: string;
  page_status?: "stub" | "draft" | "ready" | string;
  names: {
    display: string;
    display_en?: string;
    personal: string;
    personal_en?: string;
    temple?: string | null;
    posthumous?: string | null;
    aliases?: string[];
  };
  dynasty: { id: string; label: string; sequence?: number };
  reign: { start: string; end: string; eras?: string[] };
  life?: {
    birth?: string | null;
    death?: string | null;
    birth_place_id?: string | null;
    death_place_id?: string | null;
  };
  summary: string;
  summary_en?: string;
  tags?: string[];
  tags_en?: string[];
  timeline?: TimelineEvent[];
  relations?: Relation[];
  routes?: RoutePoint[];
  sources?: { title: string; note?: string }[];
  meta?: {
    status?: string;
    confidence?: string;
    page_status?: string;
    note?: string;
  };
  bio_parts?: BioPart[];
  bio_parts_en?: BioPart[];
  bio_md?: string;
  illustration?: string | null;
  portrait?: { disclaimer?: string };
};

export type CatalogStats = {
  total: number;
  stub: number;
  draft: number;
  quasi: number;
  emperor: number;
};

export type SiteData = {
  dynasties: { id: string; label: string; color?: string }[];
  places: Record<string, Place>;
  emperors: Emperor[];
  featured_ids: string[];
  catalog_stats?: CatalogStats;
};
