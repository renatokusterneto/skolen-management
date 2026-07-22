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

const fadeRise = (frame: number, start: number, end: number, dy = 36) => ({
  opacity: interpolate(frame, [start, end], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  transform: `translateY(${interpolate(frame, [start, end], [dy, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) })}px)`,
});

export const SecretariaStory: React.FC = () => {
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

  // Círculos
  const sTL     = makeSpring(frame, 0,  fps);
  const sTR     = makeSpring(frame, 3,  fps);
  const sBL     = makeSpring(frame, 6,  fps);
  const sBR     = makeSpring(frame, 5,  fps);
  const sMidTop = makeSpring(frame, 11, fps);
  const sMidBot = makeSpring(frame, 13, fps);

  // Texto — wrappers para não conflitar com opacity fixos internos
  const eyebrowAnim  = fadeRise(frame, 18, 28);
  const headlineAnim = fadeRise(frame, 24, 36);
  const subheadAnim  = fadeRise(frame, 31, 42);

  // CTA — entra perto do final (frame 75 = 2.5s de 4s)
  const ctaScale   = spring({ frame: frame - 75, fps, from: 0.82, to: 1, config: { damping: 10, stiffness: 200, mass: 0.6 } });
  const ctaOpacity = interpolate(frame, [75, 85], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // Logo — entra depois do CTA (frame 90 = 3s)
  const logoOpacity = interpolate(frame, [90, 100], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div style={{ width, height, background: WHITE, position: "relative", overflow: "hidden", fontFamily: "'Nunito', sans-serif" }}>

      {/* Topo-esquerda — teal */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 500, height: 500, background: TEAL,
        top: -160, left: -160,
        transform: `scale(${sTL})`, transformOrigin: "top left",
      }} />

      {/* Topo-direita — yellow */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 300, height: 300, background: YELLOW,
        top: -80, right: -80,
        transform: `scale(${sTR})`, transformOrigin: "top right",
      }} />

      {/* Baixo-esquerda — yellow */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 260, height: 260, background: YELLOW,
        bottom: -70, left: -70,
        transform: `scale(${sBL})`, transformOrigin: "bottom left",
      }} />

      {/* Baixo-direita — pink */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 460, height: 460, background: PINK,
        bottom: -130, right: -130,
        transform: `scale(${sBR})`, transformOrigin: "bottom right",
      }} />

      {/* Meio-topo — blue */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 160, height: 160, background: BLUE,
        top: 520, right: 130, opacity: 0.4,
        transform: `scale(${sMidTop})`, transformOrigin: "center",
      }} />

      {/* Meio-baixo — pink */}
      <div style={{
        position: "absolute", borderRadius: "50%",
        width: 100, height: 100, background: PINK,
        bottom: 480, left: 110, opacity: 0.35,
        transform: `scale(${sMidBot})`, transformOrigin: "center",
      }} />

      {/* Corpo central */}
      <div style={{
        position: "absolute", inset: 0,
        display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center",
        padding: "120px 100px", textAlign: "center",
        zIndex: 2,
      }}>

        <div style={{ ...eyebrowAnim, marginBottom: 48 }}>
          <p style={{ fontSize: 30, fontWeight: 800, color: TEAL, letterSpacing: 2.5, textTransform: "uppercase", filter: "brightness(0.75)", margin: 0 }}>
            Diretores de Escola
          </p>
        </div>

        <div style={{ ...headlineAnim, marginBottom: 56 }}>
          <h1 style={{ fontSize: 118, fontWeight: 900, color: TEXT, lineHeight: 1.0, letterSpacing: -3, margin: 0 }}>
            Sua secretária<br />apaga incêndio<br />
            <em style={{ fontStyle: "normal", color: PINK }}>o dia todo?</em>
          </h1>
        </div>

        <div style={{ ...subheadAnim, marginBottom: 80 }}>
          <p style={{ fontSize: 52, fontWeight: 700, color: TEXT, opacity: 0.65, lineHeight: 1.35, margin: 0 }}>
            Matrícula, boleto e<br />recado de pai<br />
            <strong style={{ color: BLUE, fontWeight: 900, opacity: 1 }}>dá pra ser automático.</strong>
          </p>
        </div>

        <span style={{
          display: "inline-block",
          background: TEXT, color: WHITE,
          fontSize: 34, fontWeight: 800,
          padding: "22px 56px", borderRadius: 100,
          letterSpacing: 0.5,
          transform: `scale(${ctaScale})`,
          opacity: ctaOpacity,
        }}>
          Conheça o Skolen →
        </span>
      </div>

      {/* Logo */}
      <div style={{
        position: "absolute", bottom: 80, left: 0, right: 0,
        display: "flex", alignItems: "center", justifyContent: "center",
        gap: 18, zIndex: 3, opacity: logoOpacity,
      }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 7, width: 96, height: 96 }}>
          {[YELLOW, TEAL, PINK, BLUE].map((c, i) => (
            <span key={i} style={{ display: "block", borderRadius: "50%", width: 42, height: 42, background: c }} />
          ))}
        </div>
        <span style={{ fontSize: 80, fontWeight: 900, color: TEXT, letterSpacing: -0.5 }}>Skolen</span>
      </div>
    </div>
  );
};
