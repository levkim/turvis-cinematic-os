import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { DocumentaryComposition } from './compositions/DocumentaryComposition';
import { turvisTimeline } from './data/turvis.timeline';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="TurvisDocumentary"
      component={DocumentaryComposition}
      durationInFrames={turvisTimeline.composition.durationInFrames}
      fps={turvisTimeline.composition.fps}
      width={turvisTimeline.composition.width}
      height={turvisTimeline.composition.height}
      defaultProps={{ timeline: turvisTimeline }}
    />
  );
};

export default RemotionRoot;

registerRoot(RemotionRoot);
