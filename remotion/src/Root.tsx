import React from 'react';
import { Composition } from 'remotion';
import { DocumentaryComposition } from './compositions/DocumentaryComposition';
import { mangystauDay3Timeline } from './data/mangystau-day3.timeline';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MangystauDay3"
      component={DocumentaryComposition}
      durationInFrames={mangystauDay3Timeline.durationInFrames}
      fps={mangystauDay3Timeline.fps}
      width={mangystauDay3Timeline.width}
      height={mangystauDay3Timeline.height}
      defaultProps={{ timeline: mangystauDay3Timeline }}
    />
  );
};

export default RemotionRoot;
