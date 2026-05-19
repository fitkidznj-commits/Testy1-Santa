import React from 'react';
import { Composition } from 'remotion';
import { MaidFairy } from './MaidFairy';

export function RemotionRoot() {
  return (
    <Composition
      id="MaidFairy"
      component={MaidFairy}
      durationInFrames={360}
      fps={30}
      width={1920}
      height={1080}
    />
  );
}
