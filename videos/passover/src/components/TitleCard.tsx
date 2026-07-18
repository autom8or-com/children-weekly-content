import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

type TitleCardProps = {
  bgColor?: string;
  eyebrow?: string;
  title: string;
  subtitle?: string;
  footer?: string;
};

export const TitleCard: React.FC<TitleCardProps> = ({
  bgColor = "#1a2845",
  eyebrow,
  title,
  subtitle,
  footer,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring entrance for title
  const titleProgress = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  // Delayed spring for subtitle
  const subtitleProgress = spring({
    frame: frame - 15,
    fps,
    config: { damping: 15, stiffness: 80 },
  });

  // Eyebrow fades in first
  const eyebrowProgress = spring({
    frame: frame - 5,
    fps,
    config: { damping: 20, stiffness: 120 },
  });

  const titleScale = interpolate(titleProgress, [0, 1], [0.6, 1]);
  const titleOpacity = titleProgress;
  const subtitleOpacity = Math.max(0, subtitleProgress);
  const eyebrowOpacity = Math.max(0, eyebrowProgress);

  // Split title on \n for multi-line
  const titleLines = title.split("\n");

  return (
    <AbsoluteFill
      style={{
        background: bgColor,
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif",
        padding: 60,
      }}
    >
      {eyebrow && (
        <div
          style={{
            position: "absolute",
            top: 90,
            fontSize: 32,
            fontWeight: 600,
            color: "#FFD580",
            letterSpacing: 4,
            textAlign: "center",
            opacity: eyebrowOpacity,
            textShadow: "2px 2px 4px rgba(0,0,0,0.3)",
          }}
        >
          {eyebrow}
        </div>
      )}

      <div
        style={{
          fontSize: 110,
          fontWeight: 800,
          color: "white",
          textAlign: "center",
          textShadow: "4px 4px 12px rgba(0,0,0,0.4)",
          transform: `scale(${titleScale})`,
          opacity: titleOpacity,
          lineHeight: 1.1,
          maxWidth: "85%",
        }}
      >
        {titleLines.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </div>

      {subtitle && (
        <div
          style={{
            fontSize: 38,
            fontWeight: 500,
            color: "rgba(255,255,255,0.9)",
            textAlign: "center",
            marginTop: 36,
            opacity: subtitleOpacity,
            textShadow: "2px 2px 4px rgba(0,0,0,0.3)",
            maxWidth: "80%",
          }}
        >
          {subtitle}
        </div>
      )}

      {footer && (
        <div
          style={{
            position: "absolute",
            bottom: 80,
            fontSize: 28,
            fontWeight: 500,
            color: "rgba(255,255,255,0.7)",
            letterSpacing: 2,
            textAlign: "center",
            opacity: subtitleOpacity,
          }}
        >
          {footer}
        </div>
      )}
    </AbsoluteFill>
  );
};
