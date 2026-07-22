import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from "remotion";
import { loadFont } from "@remotion/google-fonts/Nunito";

const { waitUntilDone } = loadFont("normal", { weights: ["700", "800", "900"] });

const YELLOW = "#FCD532";
const TEAL   = "#00EDBF";
const PINK   = "#FF6DA0";
const BLUE   = "#009CDE";
const TEXT   = "#253532";
const WHITE  = "#FFFFFF";

const makeSpring = (frame: number, startFrame: number, fps: number) =>
  spring({ frame: frame - startFrame, fps, from: 0, to: 1, config: { damping: 12, stiffness: 160, mass: 0.75 } });

const fadeRise = (frame: number, start: number, end: number) => ({
  opacity: interpolate(frame, [start, end], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  transform: `translateY(${interpolate(frame, [start, end], [28, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) })}px)`,
});

export const SecretariaFeed: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const [handle] = React.useState(() => {
    const h = (window as any).__remotion_delayRender?.("font") ?? null;
    return h;
  });
  React.useEffect(() => {
    waitUntilDone().then(() => {
      if (handle !== null) (window as any).__remotion_continueRender?.(handle);
    });
  }, [handle]);

  // Círculos — pop elástico com spring
  const sTL  = makeSpring(frame, 0,  fps);
  const sTR  = makeSpring(frame, 3,  fps);
  const sBL  = makeSpring(frame, 6,  fps);
  const sBR  = makeSpring(frame, 4,  fps);
  const sMid = makeSpring(frame, 10, fps);

  // Texto — fade + rise (usando wrapper para não conflitar com opacity fixo do subhead)
  const eyebrowAnim  = fadeRise(frame, 16, 26);
  const headlineAnim = fadeRise(frame, 22, 34);
  const subheadAnim  = fadeRise(frame, 29, 40);

  // CTA — entra perto do final (frame 75 = 2.5s de 4s)
  const ctaScale   = spring({ frame: frame - 75, fps, from: 0.82, to: 1, config: { damping: 10, stiffness: 200, mass: 0.6 } });
  const ctaOpacity = interpolate(frame, [75, 85], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // Logo — entra depois do CTA (frame 90 = 3s)
  const logoOpacity = interpolate(frame, [90, 100], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div style={{ width, height, background: WHITE, position: "relative", overflow: "hidden", fontFamily: "'Nunito', sans-serif" }}>

      {/* Círculo topo-esquerda — teal */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 340, height: 340, background: TEAL,
        top: -110, left: -110,
        transform: `scale(${sTL})`, transformOrigin: "top left",
      }} />

      {/* Círculo topo-direita — yellow */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 200, height: 200, background: YELLOW,
        top: -55, right: -55,
        transform: `scale(${sTR})`, transformOrigin: "top right",
      }} />

      {/* Círculo baixo-esquerda — yellow */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 170, height: 170, background: YELLOW,
        bottom: -45, left: -45,
        transform: `scale(${sBL})`, transformOrigin: "bottom left",
      }} />

      {/* Círculo baixo-direita — pink */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 300, height: 300, background: PINK,
        bottom: -85, right: -85,
        transform: `scale(${sBR})`, transformOrigin: "bottom right",
      }} />

      {/* Círculo meio — blue */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 110, height: 110, background: BLUE,
        top: 290, right: 90, opacity: 0.5,
        transform: `scale(${sMid})`, transformOrigin: "center",
      }} />

      {/* Corpo central */}
      <div style={{
        position: "absolute", inset: 0,
        display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center",
        padding: "100px 110px", textAlign: "center",
        zIndex: 2,
      }}>

        {/* Wrapper com opacity de animação — não conflita com estilos fixos internos */}
        <div style={{ ...eyebrowAnim, marginBottom: 32 }}>
          <p style={{ fontSize: 22, fontWeight: 800, color: TEAL, letterSpacing: 2, textTransform: "uppercase", filter: "brightness(0.75)", margin: 0 }}>
            Diretores de Escola
          </p>
        </div>

        <div style={{ ...headlineAnim, marginBottom: 40 }}>
          <h1 style={{ fontSize: 84, fontWeight: 900, color: TEXT, lineHeight: 1.0, letterSpacing: -2, margin: 0 }}>
            Sua secretária apaga<br />incêndio{" "}
            <em style={{ fontStyle: "normal", color: PINK }}>o dia todo?</em>
          </h1>
        </div>

        <div style={{ ...subheadAnim, marginBottom: 56 }}>
          <p style={{ fontSize: 38, fontWeight: 700, color: TEXT, opacity: 0.65, lineHeight: 1.35, margin: 0 }}>
            Matrícula, boleto e recado de pai<br />
            <strong style={{ color: BLUE, fontWeight: 900, opacity: 1 }}>dá pra ser automático.</strong>
          </p>
        </div>

        <span style={{
          display: "inline-block",
          background: TEXT, color: WHITE,
          fontSize: 28, fontWeight: 800,
          padding: "18px 48px", borderRadius: 100,
          letterSpacing: 0.5,
          transform: `scale(${ctaScale})`,
          opacity: ctaOpacity,
        }}>
          Conheça o Skolen →
        </span>
      </div>

      {/* Logo */}
      <div style={{
        position: "absolute", bottom: 56, left: 0, right: 0,
        display: "flex", alignItems: "center", justifyContent: "center",
        gap: 14, zIndex: 3, opacity: logoOpacity,
      }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 5, width: 80, height: 80 }}>
          {[YELLOW, TEAL, PINK, BLUE].map((c, i) => (
            <span key={i} style={{ display: "block", borderRadius: "50%", width: 35, height: 35, background: c }} />
          ))}
        </div>
        <span style={{ fontSize: 64, fontWeight: 900, color: TEXT, letterSpacing: -0.5 }}>Skolen</span>
      </div>
    </div>
  );
};
