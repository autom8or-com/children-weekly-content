import React from "react";
import { Composition } from "remotion";
import { Episode } from "./Episode";
import timingData from "../public/episode-timing.json";

const timing = timingData as unknown as {
  total_frames: number;
  fps: number;
  width: number;
  height: number;
};

export const Root: React.FC = () => {
  return (
    <Composition
      id="Episode"
      component={Episode}
      durationInFrames={timing.total_frames}
      fps={timing.fps}
      width={timing.width}
      height={timing.height}
    />
  );
};
