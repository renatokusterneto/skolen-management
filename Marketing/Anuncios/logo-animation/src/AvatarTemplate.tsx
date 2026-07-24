import React from "react";
import { AbsoluteFill, Video, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { loadFont } from "@remotion/google-fonts/Nunito";

const { fontFamily } = loadFont("normal", { weights: ["700", "800", "900"] });

// Tokens — extraídos do template Claude Design (Template Video Avatar.html)
const COLOR = {
  yellow: "#FCD532",
  teal: "#00EDBF",
  pink: "#FF6DA0",
  blue: "#009CDE",
  ink: "#253532",
  white: "#FFFFFF",
  graySurface: "#F5F5F5",
};

const RADIUS_XL = 48;

export type CaptionSegment = { start: number; end: number; text: string };

export type AvatarTemplateProps = {
  title: string;
  avatarVideoSrc: string;
  durationInSeconds: number;
  captions: CaptionSegment[];
};

/** Respiração sutil e contínua — período diferente por bola para não ficarem em fase. */
const breathe = (frame: number, fps: number, periodSecs: number, amplitude: number, phase = 0) => {
  const cycle = (frame / fps / periodSecs + phase) * Math.PI * 2;
  return 1 + Math.sin(cycle) * amplitude;
};

export const AvatarTemplate: React.FC<AvatarTemplateProps> = ({
  title,
  avatarVideoSrc,
  captions,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const activeCaption = captions.find((c) => t >= c.start && t < c.end)?.text ?? "";

  // Entrada suave do bloco de texto nos primeiros 20 frames
  const introOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const scaleTeal = breathe(frame, fps, 4.5, 0.06, 0);
  const scaleYellow = breathe(frame, fps, 3.8, 0.07, 0.25);
  const scaleBlue = breathe(frame, fps, 5.2, 0.05, 0.5);
  const scalePink = breathe(frame, fps, 4.1, 0.065, 0.75);

  return (
    <AbsoluteFill
      style={{
        background: COLOR.white,
        fontFamily,
        boxSizing: "border-box",
        padding: "96px 64px 72px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* Círculos decorativos — respiração contínua (tamanho base +20%) */}
      <div
        style={{
          position: "absolute",
          top: -120,
          left: -120,
          width: 360,
          height: 360,
          borderRadius: "50%",
          background: COLOR.teal,
          transform: `scale(${scaleTeal})`,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: -90,
          right: -110,
          width: 276,
          height: 276,
          borderRadius: "50%",
          background: COLOR.yellow,
          transform: `scale(${scaleYellow})`,
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: -130,
          left: -100,
          width: 288,
          height: 288,
          borderRadius: "50%",
          background: COLOR.blue,
          zIndex: 2,
          transform: `scale(${scaleBlue})`,
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: -110,
          right: -120,
          width: 336,
          height: 336,
          borderRadius: "50%",
          background: COLOR.pink,
          zIndex: 2,
          transform: `scale(${scalePink})`,
        }}
      />

      {/* Título */}
      <div
        style={{
          width: "85%",
          margin: "0 auto",
          textAlign: "center",
          position: "relative",
          zIndex: 1,
          opacity: introOpacity,
        }}
      >
        <p
          style={{
            margin: 0,
            fontWeight: 900,
            fontSize: 68,
            lineHeight: 1.05,
            letterSpacing: "-0.03em",
            color: COLOR.teal,
            textWrap: "balance",
          }}
        >
          {title}
        </p>
      </div>

      {/* Legenda — sincronizada via Whisper, troca por segmento */}
      <div
        style={{
          width: "100%",
          boxSizing: "border-box",
          marginTop: 44,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          height: 150,
          overflow: "hidden",
          position: "relative",
          zIndex: 1,
        }}
      >
        <p
          style={{
            margin: 0,
            fontWeight: 800,
            fontSize: 36,
            lineHeight: 1.25,
            color: COLOR.ink,
          }}
        >
          {activeCaption}
        </p>
      </div>

      {/* Avatar — vídeo HeyGen (slot -15%) */}
      <div
        style={{
          width: "100%",
          flex: 0.85,
          marginTop: 40,
          borderRadius: RADIUS_XL,
          overflow: "hidden",
          position: "relative",
          zIndex: 1,
          background: COLOR.graySurface,
        }}
      >
        <Video
          src={avatarVideoSrc.startsWith("http") ? avatarVideoSrc : staticFile(avatarVideoSrc)}
          style={{ width: "100%", height: "100%", objectFit: "contain" }}
        />
      </div>
    </AbsoluteFill>
  );
};
