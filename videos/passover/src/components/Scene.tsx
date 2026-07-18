import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { SubtitleOverlay } from "./SubtitleOverlay";
import { TitleCard } from "./TitleCard";
import type { SceneTiming } from "../types/episode";

type SceneProps = {
  sceneData: SceneTiming;
};

export const Scene: React.FC<SceneProps> = ({ sceneData }) => {
  const frame = useCurrentFrame();
  const visual = sceneData.visual;

  // Title cards / section headers: full-screen text card
  if (visual.type === "title-card" || visual.type === "section-header") {
    return (
      <AbsoluteFill>
        <TitleCard
          bgColor={visual.bg_color || "#1a2845"}
          eyebrow={visual.eyebrow}
          title={visual.title || sceneData.title}
          subtitle={visual.subtitle}
          footer={visual.footer}
        />
        {sceneData.dialogue.map((line) =>
          line.audio_file ? (
            <Sequence
              key={line.id}
              from={line.start_frame}
              durationInFrames={line.duration_frames}
            >
              <Audio src={staticFile(line.audio_file)} />
            </Sequence>
          ) : null
        )}
        {sceneData.sound_effects.map((sfx) =>
          sfx.audio_file ? (
            <Sequence
              key={sfx.id}
              from={sfx.start_frame}
              durationInFrames={sfx.duration_frames}
            >
              <Audio src={staticFile(sfx.audio_file)} volume={0.5} />
            </Sequence>
          ) : null
        )}
      </AbsoluteFill>
    );
  }

  // Image-based scenes (story-cards, diary-cards, recap, etc.)
  const scale = interpolate(
    frame,
    [0, sceneData.duration_frames],
    [1, 1.12],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {/* Background image with Ken Burns */}
      <AbsoluteFill>
        {visual.asset_file ? (
          <Img
            src={staticFile(visual.asset_file)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${scale})`,
            }}
          />
        ) : (
          <AbsoluteFill style={{ background: "linear-gradient(135deg, #2a1a45, #1a2845)" }} />
        )}
      </AbsoluteFill>

      {/* Top-left scene title chip */}
      {sceneData.title && (
        <div
          style={{
            position: "absolute",
            top: 28,
            left: 36,
            background: "rgba(0,0,0,0.55)",
            color: "white",
            padding: "10px 22px",
            borderRadius: 16,
            fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif",
            fontSize: 22,
            fontWeight: 600,
            letterSpacing: 0.5,
            maxWidth: "60%",
            textShadow: "1px 1px 2px rgba(0,0,0,0.4)",
          }}
        >
          {sceneData.title}
        </div>
      )}

      {/* Verse overlay (memory verse or bridge) */}
      {visual.verse_overlay && (
        <div
          style={{
            position: "absolute",
            top: 90,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              background: "rgba(255, 248, 220, 0.92)",
              borderRadius: 24,
              padding: "26px 50px",
              maxWidth: "70%",
              textAlign: "center",
              fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif",
              fontSize: 40,
              fontWeight: 700,
              color: "#3a1a1a",
              lineHeight: 1.3,
              boxShadow: "0 8px 24px rgba(0,0,0,0.25)",
              border: "3px solid #d4a017",
            }}
          >
            {sceneData.dialogue[sceneData.dialogue.length - 1]?.text}
          </div>
        </div>
      )}

      {/* Diary card label */}
      {visual.diary_card && (
        <div
          style={{
            position: "absolute",
            top: 28,
            right: 36,
            background: "rgba(255, 156, 203, 0.95)",
            color: "#5a1a45",
            padding: "10px 22px",
            borderRadius: 16,
            fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif",
            fontSize: 22,
            fontWeight: 700,
            letterSpacing: 0.5,
            boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
          }}
        >
          📓 Angela's Diary
        </div>
      )}

      {/* Dialogue audio + subtitles */}
      {sceneData.dialogue.map((line) =>
        line.audio_file ? (
          <Sequence
            key={line.id}
            from={line.start_frame}
            durationInFrames={line.duration_frames}
          >
            <Audio src={staticFile(line.audio_file)} />
            <SubtitleOverlay text={line.text} character={line.character} />
          </Sequence>
        ) : null
      )}

      {/* Sound effects */}
      {sceneData.sound_effects.map((sfx) =>
        sfx.audio_file ? (
          <Sequence
            key={sfx.id}
            from={sfx.start_frame}
            durationInFrames={sfx.duration_frames}
          >
            <Audio src={staticFile(sfx.audio_file)} volume={0.55} />
          </Sequence>
        ) : null
      )}
    </AbsoluteFill>
  );
};
