import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

interface CinematicTitleCardProps {
  title: string;
  startFrame: number;
  durationInFrames: number;
}

export const CinematicTitleCard: React.FC<CinematicTitleCardProps> = ({
  title,
  startFrame,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  const opacity = interpolate(
    localFrame,
    [0, 12, durationInFrames - 12, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const translateY = interpolate(localFrame, [0, 30], [16, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          opacity,
          transform: `translateY(${translateY}px)`,
          color: 'rgba(255,255,255,0.96)',
          fontSize: 64,
          letterSpacing: 8,
          fontWeight: 600,
          textTransform: 'uppercase',
          textShadow: '0 5px 24px rgba(0,0,0,0.72)',
        }}
      >
        {title}
      </div>
    </AbsoluteFill>
  );
};
