import "./index.css";
import { Composition } from "remotion";
import { SkolenLogo } from "./SkolenLogo";
import { SecretariaFeed } from "./SecretariaFeed";
import { SecretariaStory } from "./SecretariaStory";

const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="LogoReveal-Story"
        component={SkolenLogo}
        durationInFrames={90}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{ background: "#FFFFFF" }}
      />

      <Composition
        id="LogoReveal-Feed"
        component={SkolenLogo}
        durationInFrames={90}
        fps={FPS}
        width={1080}
        height={1080}
        defaultProps={{ background: "#FFFFFF" }}
      />

      <Composition
        id="Secretaria-Feed"
        component={SecretariaFeed}
        durationInFrames={120}
        fps={FPS}
        width={1080}
        height={1080}
      />

      <Composition
        id="Secretaria-Story"
        component={SecretariaStory}
        durationInFrames={120}
        fps={FPS}
        width={1080}
        height={1920}
      />
    </>
  );
};
