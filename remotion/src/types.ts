export type ShotType =
  | 'drone-reveal'
  | 'drone-orbit'
  | 'drone-top-down'
  | 'drone-forward-push'
  | 'drone-pull-back'
  | 'vehicle-journey'
  | 'walking-scale'
  | 'camp-life'
  | 'geological-detail'
  | 'hero-landscape'
  | 'night-sky'
  | 'transition';

export type BeatType =
  | 'threshold'
  | 'discovery'
  | 'texture'
  | 'scale'
  | 'arrival'
  | 'cosmic';

export type TransitionType = 'cut' | 'cross-dissolve' | 'fade' | 'dip-to-black';

export interface TimelineClip {
  id: string;
  startFrame: number;
  durationInFrames: number;
  src: string;
  shotType: ShotType;
  beatType: BeatType;
  emotion: string;
  subtitle?: string;
  titleCard?: string;
  transition?: TransitionType;
  objectFit?: 'cover' | 'contain';
  scaleFrom?: number;
  scaleTo?: number;
}

export interface DocumentaryTimeline {
  id: string;
  title: string;
  fps: number;
  width: number;
  height: number;
  durationInFrames: number;
  clips: TimelineClip[];
}
