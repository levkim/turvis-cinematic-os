import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

interface FilmFadeProps {
  startFrame: number;
  durationInFrames: number;
  type?: 'in' | 'out' | 'dip';
}

export const FilmFade: React.FC<FilmFadeProps> = ({
  startFrame,
  durationInFrames,
  type = 'out',
}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  const opacity =
    type === 'in'
      ? interpolate(localFrame, [0, durationInFrames], [1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : type === 'dip'
        ? interpolate(
            localFrame,
            [0, durationInFrames / 2, durationInFrames],
            [0, 0.55, 0],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          )
        : interpolate(localFrame, [0, durationInFrames], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

  return <AbsoluteFill style={{ backgroundColor: 'black', opacity, pointerEvents: 'none' }} />;
};
