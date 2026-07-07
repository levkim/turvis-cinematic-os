import type { TurvisRemotionTimeline } from '../types';

export const turvisTimeline: TurvisRemotionTimeline = {
  schema: 'turvis.remotion.timeline.v0.1',
  project: {
    id: 'current-project',
    title: 'TURVIS Documentary',
  },
  composition: {
    fps: 30,
    durationInFrames: 2700,
    aspectRatio: '16:9',
    resolution: '3840x2160',
    language: 'ko',
    width: 3840,
    height: 2160,
  },
  audio: {
    generateNarration: false,
    generateMusic: false,
    generateSoundEffects: false,
  },
  clips: [
    {
      id: 'beat-01',
      type: 'video-placeholder',
      startFrame: 0,
      durationInFrames: 300,
      beat: 'Opening',
      src: 'TBD',
      subtitle: 'TURVIS Documentary opening beat',
      subtitleStyle: 'premium-documentary',
      transition: 'cut',
      status: 'draft',
    },
  ],
};
