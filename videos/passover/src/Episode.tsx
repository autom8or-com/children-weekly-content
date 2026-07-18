import React from "react";
import { Audio, staticFile } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { Scene } from "./components/Scene";
import type { EpisodeTiming } from "./types/episode";
import timingData from "../public/episode-timing.json";

const timing = timingData as unknown as EpisodeTiming;

const DEFAULT_TRANSITION_FRAMES = 15;

export const Episode: React.FC = () => {
  const findMusicTrack = (trackId: string | null) => {
    if (!trackId) return null;
    return timing.background_music_tracks.find((t) => t.id === trackId);
  };

  return (
    <TransitionSeries>
      {timing.scenes.map((scene, i) => {
        const musicTrack = findMusicTrack(scene.background_music);
        return (
          <React.Fragment key={scene.id}>
            {i > 0 && (
              <TransitionSeries.Transition
                presentation={fade()}
                timing={linearTiming({ durationInFrames: DEFAULT_TRANSITION_FRAMES })}
              />
            )}
            <TransitionSeries.Sequence durationInFrames={scene.duration_frames}>
              <Scene sceneData={scene} />
              {musicTrack?.audio_file && (
                <Audio
                  src={staticFile(musicTrack.audio_file)}
                  volume={0.12}
                  loop
                />
              )}
            </TransitionSeries.Sequence>
          </React.Fragment>
        );
      })}
    </TransitionSeries>
  );
};
