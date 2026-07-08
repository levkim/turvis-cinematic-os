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
    [0, 10, Math.max(11, durationInFrames - 10), durationInFrames],
    [0, 0.82, 0.82, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-start',
        alignItems: 'flex-start',
        pointerEvents: 'none',
        padding: 54,
      }}
    >
      <div
        style={{
          opacity,
          color: 'rgba(255,255,255,0.9)',
          fontSize: 28,
          lineHeight: 1.25,
          letterSpacing: 0,
          fontWeight: 600,
          textShadow: '0 3px 16px rgba(0,0,0,0.86)',
          background: 'rgba(0,0,0,0.32)',
          border: '1px solid rgba(255,255,255,0.14)',
          borderRadius: 6,
          padding: '12px 16px',
          maxWidth: '46%',
        }}
      >
        {title}
      </div>
    </AbsoluteFill>
  );
};
