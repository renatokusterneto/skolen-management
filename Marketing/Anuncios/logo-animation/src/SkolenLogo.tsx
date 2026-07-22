import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
  continueRender,
  delayRender,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Nunito";

const { waitUntilDone } = loadFont("normal", { weights: ["400", "500", "600"] });

// Brand colors — pixel-sampled from Marketing/Assets/marca/logo.png
const YELLOW = "#FCD532";
const TEAL = "#00EDBF";
const PINK = "#FF6DA0";
const BLUE = "#009CDE";
const TEXT = "#253532";

type SkolenLogoProps = {
  background?: string;
};

export const SkolenLogo: React.FC<SkolenLogoProps> = ({
  background = "#FFFFFF",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const [handle] = React.useState(() => delayRender("Loading font"));
  React.useEffect(() => {
    waitUntilDone().then(() => continueRender(handle));
  }, [handle]);

  // Each circle pops in with a spring, staggered
  const makeCircleScale = (startFrame: number) =>
    spring({ frame: frame - startFrame, fps, from: 0, to: 1, config: { damping: 10, stiffness: 180, mass: 0.7 } });

  const scaleYellow = makeCircleScale(0);
  const scaleTeal   = makeCircleScale(6);
  const scalePink   = makeCircleScale(12);
  const scaleBlue   = makeCircleScale(18);

  // Wordmark slides in + fades after circles
  const wordmarkOpacity = interpolate(frame, [30, 50], [0, 1], { extrapolateRight: "clamp" });
  const wordmarkX = interpolate(frame, [30, 50], [30, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const circleSize = Math.round(width * 0.12);
  const overlap = Math.round(circleSize * 0.18); // how much circles overlap
  const wordFontSize = Math.round(width * 0.1);

  // Grid dimensions
  const gridW = circleSize * 2 - overlap;
  const gridH = circleSize * 2 - overlap;

  // Total logo width = grid + gap + wordmark estimate
  const gap = Math.round(circleSize * 0.45);

  return (
    <div
      style={{
        width,
        height,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background,
        overflow: "hidden",
        position: "relative",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap }}>
        {/* 2×2 circles mark */}
        <div
          style={{
            width: gridW,
            height: gridH,
            position: "relative",
            flexShrink: 0,
          }}
        >
          {/* Top-left: Yellow */}
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: circleSize,
              height: circleSize,
              borderRadius: "50%",
              background: YELLOW,
              transform: `scale(${scaleYellow})`,
              transformOrigin: "center center",
            }}
          />
          {/* Top-right: Teal */}
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              width: circleSize,
              height: circleSize,
              borderRadius: "50%",
              background: TEAL,
              transform: `scale(${scaleTeal})`,
              transformOrigin: "center center",
            }}
          />
          {/* Bottom-left: Pink */}
          <div
            style={{
              position: "absolute",
              bottom: 0,
              left: 0,
              width: circleSize,
              height: circleSize,
              borderRadius: "50%",
              background: PINK,
              transform: `scale(${scalePink})`,
              transformOrigin: "center center",
            }}
          />
          {/* Bottom-right: Blue */}
          <div
            style={{
              position: "absolute",
              bottom: 0,
              right: 0,
              width: circleSize,
              height: circleSize,
              borderRadius: "50%",
              background: BLUE,
              transform: `scale(${scaleBlue})`,
              transformOrigin: "center center",
            }}
          />
        </div>

        {/* Wordmark */}
        <div
          style={{
            opacity: wordmarkOpacity,
            transform: `translateX(${wordmarkX}px)`,
          }}
        >
          <span
            style={{
              fontFamily: "'Nunito', sans-serif",
              fontWeight: 600,
              fontSize: wordFontSize,
              color: TEXT,
              letterSpacing: "-0.01em",
              lineHeight: 1,
              userSelect: "none",
            }}
          >
            Skolen
          </span>
        </div>
      </div>
    </div>
  );
};
