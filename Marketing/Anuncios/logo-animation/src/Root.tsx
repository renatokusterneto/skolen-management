import "./index.css";
import { Composition } from "remotion";
import { SkolenLogo } from "./SkolenLogo";
import { SecretariaFeed } from "./SecretariaFeed";
import { SecretariaStory } from "./SecretariaStory";
import { AvatarTemplate, type AvatarTemplateProps } from "./AvatarTemplate";
import { AvatarNewsTemplate, type AvatarNewsTemplateProps } from "./AvatarNewsTemplate";

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

      <Composition
        id="Avatar-Template"
        component={AvatarTemplate}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={300}
        defaultProps={{
          title: "Título do vídeo",
          avatarVideoSrc: "",
          durationInSeconds: 10,
          captions: [] as AvatarTemplateProps["captions"],
        }}
        calculateMetadata={async ({ props }) => ({
          durationInFrames: Math.ceil(props.durationInSeconds * FPS),
        })}
      />

      <Composition
        id="Avatar-News-Template"
        component={AvatarNewsTemplate}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={300}
        defaultProps={{
          title: "Título da matéria, traduzido e resumido",
          avatarVideoSrc: "",
          durationInSeconds: 10,
          quotes: [] as AvatarNewsTemplateProps["quotes"],
        }}
        calculateMetadata={async ({ props }) => ({
          durationInFrames: Math.ceil(props.durationInSeconds * FPS),
        })}
      />
    </>
  );
};
