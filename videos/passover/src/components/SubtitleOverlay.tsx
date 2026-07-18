import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

type SubtitleOverlayProps = {
  text: string;
  character: string;
};

// Friendly cartoon-style palette per character
const CHARACTER_COLORS: Record<string, string> = {
  Narrator: "#FFD580",
  Angela:   "#FF9CCB",
};

export const SubtitleOverlay: React.FC<SubtitleOverlayProps> = ({
  text,
  character,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Slide up entrance
  const enterProgress = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 120 },
  });

  const translateY = interpolate(enterProgress, [0, 1], [30, 0]);
  const opacity = enterProgress;

  const charColor = CHARACTER_COLORS[character] || "#FFD580";

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 100,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          background: "rgba(20, 20, 30, 0.78)",
          borderRadius: 24,
          padding: "20px 40px",
          maxWidth: "80%",
          transform: `translateY(${translateY}px)`,
          opacity,
          boxShadow: "0 8px 30px rgba(0,0,0,0.35)",
          border: "2px solid rgba(255,255,255,0.12)",
        }}
      >
        <div
          style={{
            fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif",
            fontSize: 24,
            fontWeight: 700,
            color: charColor,
            marginBottom: 6,
            letterSpacing: 1,
          }}
        >
          {character}
        </div>
        <div
          style={{
            fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif",
            fontSize: 38,
            fontWeight: 600,
            color: "white",
            lineHeight: 1.35,
            textAlign: "center",
            textShadow: "2px 2px 4px rgba(0,0,0,0.4)",
          }}
        >
          {text}
        </div>
      </div>
    </AbsoluteFill>
  );
};
