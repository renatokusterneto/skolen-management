import React from "react";
import { AbsoluteFill, Video, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { loadFont } from "@remotion/google-fonts/Nunito";

const { fontFamily } = loadFont("normal", { weights: ["700", "800", "900"] });

// Tokens — mesma base do Avatar-Template (Template Video Avatar.html)
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
const RADIUS_MD = 28;

export type NewsQuote = {
  /** Início e fim (segundos) em que este trecho fica em tela, sincronizado com o roteiro do avatar. */
  start: number;
  end: number;
  /**
   * Trecho/citação da matéria. Envolva as palavras-chave em `==...==` para
   * marcar com highlight (marca-texto), ex: "precisão de ==88% a 92%==".
   */
  text: string;
  /** Fonte da citação, ex: "EdWeek, 2026" ou "Sponte/TOTVS, 2026". */
  source: string;
};

export type AvatarNewsTemplateProps = {
  /** CTA/título — a manchete da matéria, traduzida e resumida em PT-BR. */
  title: string;
  avatarVideoSrc: string;
  durationInSeconds: number;
  quotes: NewsQuote[];
};

/** Respiração sutil e contínua — período diferente por bola para não ficarem em fase. */
const breathe = (frame: number, fps: number, periodSecs: number, amplitude: number, phase = 0) => {
  const cycle = (frame / fps / periodSecs + phase) * Math.PI * 2;
  return 1 + Math.sin(cycle) * amplitude;
};

/** Quebra `texto ==destaque== texto` em partes, renderizando os trechos marcados com <mark>. */
const renderHighlighted = (text: string) => {
  const parts = text.split(/(==[^=]+==)/g);
  return parts.map((part, i) => {
    const match = part.match(/^==([^=]+)==$/);
    if (!match) return <React.Fragment key={i}>{part}</React.Fragment>;
    return (
      <mark
        key={i}
        style={{
          background: COLOR.yellow,
          color: COLOR.ink,
          padding: "0 6px",
          borderRadius: 6,
          boxDecorationBreak: "clone",
          WebkitBoxDecorationBreak: "clone",
        }}
      >
        {match[1]}
      </mark>
    );
  });
};

export const AvatarNewsTemplate: React.FC<AvatarNewsTemplateProps> = ({
  title,
  avatarVideoSrc,
  quotes,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const activeQuote = quotes.find((q) => t >= q.start && t < q.end) ?? null;

  // Entrada suave do bloco de texto nos primeiros 20 frames
  const introOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Fade sutil ao trocar de card de citação
  const quoteStartFrame = activeQuote ? Math.round(activeQuote.start * fps) : 0;
  const quoteFadeOpacity = interpolate(
    frame - quoteStartFrame,
    [0, 10],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

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
        padding: "88px 64px 0",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* Círculos decorativos — respiração contínua */}
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

      {/* CTA — manchete da matéria, traduzida/resumida */}
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
            fontSize: 56,
            lineHeight: 1.08,
            letterSpacing: "-0.03em",
            color: COLOR.teal,
            textWrap: "balance",
          }}
        >
          {title}
        </p>
      </div>

      {/* Card de citação — trecho da matéria com highlight + fonte, troca sincronizada */}
      <div
        style={{
          width: "100%",
          marginTop: 36,
          minHeight: 220,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
          zIndex: 1,
        }}
      >
        {activeQuote && (
          <div
            style={{
              width: "100%",
              boxSizing: "border-box",
              background: COLOR.graySurface,
              borderRadius: RADIUS_MD,
              padding: "32px 36px",
              opacity: quoteFadeOpacity,
              borderLeft: `8px solid ${COLOR.teal}`,
            }}
          >
            <p
              style={{
                margin: 0,
                fontWeight: 800,
                fontSize: 34,
                lineHeight: 1.3,
                color: COLOR.ink,
              }}
            >
              &ldquo;{renderHighlighted(activeQuote.text)}&rdquo;
            </p>
            <p
              style={{
                margin: "16px 0 0",
                fontWeight: 700,
                fontSize: 24,
                color: COLOR.blue,
                textTransform: "uppercase",
                letterSpacing: "0.02em",
              }}
            >
              — {activeQuote.source}
            </p>
          </div>
        )}
      </div>

      {/* Avatar — vídeo HeyGen, rodapé */}
      <div
        style={{
          width: "100%",
          flex: 1,
          marginTop: 32,
          borderTopLeftRadius: RADIUS_XL,
          borderTopRightRadius: RADIUS_XL,
          overflow: "hidden",
          position: "relative",
          zIndex: 1,
          background: COLOR.white,
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
