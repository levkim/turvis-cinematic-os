import React from 'react';
import { AbsoluteFill, interpolate, OffthreadVideo, Sequence, useCurrentFrame } from 'remotion';
import type { RemotionClip, TurvisRemotionTimeline } from '../types';
import { CinematicSubtitle } from '../components/CinematicSubtitle';
import { CinematicTitleCard } from '../components/CinematicTitleCard';
import { FilmFade } from '../components/FilmFade';

interface DocumentaryCompositionProps {
  timeline: TurvisRemotionTimeline;
}

const isUsableVideoSource = (clip: RemotionClip): boolean => {
  const src = clip.src;
  return clip.type === 'video' && Boolean(src && src !== 'TBD' && !src.toLowerCase().includes('candidate from'));
};

const PlaceholderLayer: React.FC<{ clip: RemotionClip }> = ({ clip }) => {
  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #050505 0%, #1d1d1d 100%)',
        color: 'white',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'sans-serif',
        padding: 80,
        textAlign: 'center',
      }}
    >
      <div style={{ fontSize: 26, opacity: 0.6, marginBottom: 24 }}>TURVIS DOCUMENTARY PLACEHOLDER</div>
      <div style={{ fontSize: 56, fontWeight: 700, marginBottom: 20 }}>{clip.beat}</div>
      <div style={{ fontSize: 24, opacity: 0.75 }}>{clip.src}</div>
    </AbsoluteFill>
  );
};

const ClipLayer: React.FC<{ clip: RemotionClip }> = ({ clip }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - clip.startFrame;

  const scale = interpolate(localFrame, [0, clip.durationInFrames], [1, 1.04], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const opacity = interpolate(
    localFrame,
    [0, 12, Math.max(13, clip.durationInFrames - 12), clip.durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {isUsableVideoSource(clip) ? (
        <OffthreadVideo
          src={clip.src}
          startFrom={0}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: `scale(${scale})`,
            opacity,
          }}
        />
      ) : (
        <PlaceholderLayer clip={clip} />
      )}

      {clip.beat ? (
        <CinematicTitleCard title={clip.beat} startFrame={clip.startFrame} durationInFrames={Math.min(clip.durationInFrames, 90)} />
      ) : null}

      {clip.subtitle ? (
        <CinematicSubtitle text={clip.subtitle} startFrame={clip.startFrame} durationInFrames={clip.durationInFrames} />
      ) : null}

      {clip.transition === 'dip-to-black' ? (
        <FilmFade startFrame={clip.startFrame + clip.durationInFrames - 18} durationInFrames={18} type="dip" />
      ) : null}
    </AbsoluteFill>
  );
};

export const DocumentaryComposition: React.FC<DocumentaryCompositionProps> = ({ timeline }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {timeline.clips.map((clip) => (
        <Sequence key={clip.id} from={clip.startFrame} durationInFrames={clip.durationInFrames}>
          <ClipLayer clip={clip} />
        </Sequence>
      ))}
      <FilmFade startFrame={0} durationInFrames={12} type="in" />
      <FilmFade startFrame={Math.max(0, timeline.composition.durationInFrames - 60)} durationInFrames={60} type="out" />
    </AbsoluteFill>
  );
};
