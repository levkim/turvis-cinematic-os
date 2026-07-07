export interface RemotionClip {
  id: string;
  type: 'video-placeholder' | 'video';
  startFrame: number;
  durationInFrames: number;
  beat: string;
  src: string;
  subtitle?: string;
  subtitleStyle?: string;
  transition?: string;
  status?: string;
}

export interface TurvisRemotionTimeline {
  schema: string;
  project: {
    id?: string;
    title?: string;
  };
  composition: {
    fps: number;
    durationInFrames: number;
    aspectRatio: string;
    resolution: string;
    language: string;
    width: number;
    height: number;
  };
  audio: {
    generateNarration: boolean;
    generateMusic: boolean;
    generateSoundEffects: boolean;
  };
  clips: RemotionClip[];
}
