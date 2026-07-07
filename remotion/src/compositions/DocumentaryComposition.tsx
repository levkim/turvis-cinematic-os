import React from 'react';
import { AbsoluteFill, interpolate, Sequence, useCurrentFrame, Video } from 'remotion';
import type { DocumentaryTimeline, TimelineClip } from '../types';
import { CinematicSubtitle } from '../components/CinematicSubtitle';
import { CinematicTitleCard } from '../components/CinematicTitleCard';
import { FilmFade } from '../components/FilmFade';

interface DocumentaryCompositionProps {
  timeline: DocumentaryTimeline;
}

const ClipLayer: React.FC<{ clip: TimelineClip }> = ({ clip }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - clip.startFrame;

  const scale = interpolate(
    localFrame,
    [0, clip.durationInFrames],
    [clip.scaleFrom ?? 1, clip.scaleTo ?? 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const opacity = interpolate(
    localFrame,
    [0, 12, clip.durationInFrames - 12, clip.durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      <Video
        src={clip.src}
        startFrom={0}
        style={{
          width: '100%',
          height: '100%',
          objectFit: clip.objectFit ?? 'cover',
          transform: `scale(${scale})`,
          opacity,
        }}
      />
      {clip.titleCard ? (
        <CinematicTitleCard
          title={clip.titleCard}
          startFrame={clip.startFrame}
          durationInFrames={Math.min(clip.durationInFrames, 120)}
        />
      ) : null}
      {clip.subtitle ? (
        <CinematicSubtitle
          text={clip.subtitle}
          startFrame={clip.startFrame}
          durationInFrames={clip.durationInFrames}
        />
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
      <FilmFade startFrame={0} durationInFrames={30} type="in" />
      <FilmFade startFrame={timeline.durationInFrames - 60} durationInFrames={60} type="out" />
    </AbsoluteFill>
  );
};
