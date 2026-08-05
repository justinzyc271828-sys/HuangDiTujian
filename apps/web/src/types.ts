export type Place = {
  id: string;
  names: { historical: string; modern: string };
  coords: { lng: number; lat: number; precision: string };
  map?: { region?: string };
  notes?: string;
};

export type TimelineEvent = {
  year: string;
  date_note?: string;
  title: string;
  summary: string;
  place_id?: string | null;
  related_person_ids?: string[];
  sources?: string[];
};

export type Relation = {
  type: string;
  target_id: string | null;
  note?: string;
};

export type RoutePoint = {
  group: string;
  order: number;
  year?: string;
  place_id: string;
  event: string;
};

export type BioPart =
  | { type: "text"; value: string }
  | { type: "link"; id: string; label: string };

export type Emperor = {
  id: string;
  tier: string;
  sort_key?: string;
  names: {
    display: string;
    personal: string;
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
  tags?: string[];
  timeline?: TimelineEvent[];
  relations?: Relation[];
  routes?: RoutePoint[];
  sources?: { title: string; note?: string }[];
  meta?: { status?: string; confidence?: string };
  bio_parts?: BioPart[];
  bio_md?: string;
  portrait?: { disclaimer?: string };
};

export type SiteData = {
  dynasties: { id: string; label: string; color?: string }[];
  places: Record<string, Place>;
  emperors: Emperor[];
  featured_ids: string[];
};
