import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

interface CinematicSubtitleProps {
  text: string;
  startFrame: number;
  durationInFrames: number;
}

export const CinematicSubtitle: React.FC<CinematicSubtitleProps> = ({
  text,
  startFrame,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  const opacity = interpolate(
    localFrame,
    [0, 8, durationInFrames - 10, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  if (!text) return null;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingBottom: 74,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          width: '100%',
          height: 340,
          position: 'absolute',
          bottom: 0,
          background:
            'linear-gradient(to top, rgba(0,0,0,0.76), rgba(0,0,0,0.34), rgba(0,0,0,0))',
          opacity,
        }}
      />
      <div
        style={{
          maxWidth: '86%',
          textAlign: 'center',
          color: 'rgba(255,255,255,0.94)',
          fontSize: 54,
          lineHeight: 1.34,
          letterSpacing: 0.6,
          fontWeight: 650,
          textShadow: '0 3px 18px rgba(0,0,0,0.72)',
          opacity,
          whiteSpace: 'pre-line',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
