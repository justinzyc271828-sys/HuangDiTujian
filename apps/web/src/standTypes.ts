export type StandAxis = {
  key: string;
  label: string;
  jojo: string;
  desc: string;
};

export type StandScores = Record<string, number>;

export type StandProfile = {
  stand_name: string;
  stand_type: string;
  cry: string;
  scores: StandScores;
  ability: string;
  weakness: string;
};

export type StandStatsFile = {
  version: string;
  note: string;
  axes: StandAxis[];
  grades: string[];
  profiles: Record<string, StandProfile>;
};

export type StyleId =
  | "jojo-dark"
  | "jojo-gold"
  | "memorial"
  | "stele"
  | "tcg";
