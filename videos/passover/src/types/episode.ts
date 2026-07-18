export type DialogueTiming = {
  id: string;
  start_frame: number;
  duration_frames: number;
  audio_file: string | null;
  character: string;
  text: string;
};

export type SfxTiming = {
  id: string;
  start_frame: number;
  duration_frames: number;
  audio_file: string | null;
};

export type SceneVisualData = {
  type: "image" | "video" | "title-card" | "section-header";
  asset_file: string | null;
  animation: string;
  bg_color?: string;
  eyebrow?: string;
  title?: string;
  subtitle?: string;
  footer?: string;
  verse_overlay?: boolean;
  diary_card?: boolean;
  caption_strip?: boolean;
};

export type SceneTiming = {
  id: string;
  scene_type: string;
  title: string;
  start_frame: number;
  duration_frames: number;
  transition: string;
  transition_frames: number;
  visual: SceneVisualData;
  dialogue: DialogueTiming[];
  sound_effects: SfxTiming[];
  background_music: string | null;
};

export type EpisodeMeta = {
  title: string;
  series_name: string;
  episode_number: number;
  theme: string;
  target_age: string;
  total_duration_seconds: number;
  fps: number;
  width: number;
  height: number;
};

export type MusicTrackData = {
  id: string;
  description: string;
  audio_file: string | null;
  duration_seconds: number | null;
};

export type EpisodeTiming = {
  fps: number;
  width: number;
  height: number;
  total_frames: number;
  total_seconds: number;
  title_card_frames: number;
  end_card_frames: number;
  scenes: SceneTiming[];
  meta: EpisodeMeta;
  background_music_tracks: MusicTrackData[];
};
