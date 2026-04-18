import type { RefObject } from "react";

type CameraStageProps = {
  augmentedImage: string;
  canvasRef: RefObject<HTMLCanvasElement | null>;
  videoRef: RefObject<HTMLVideoElement | null>;
};

type CameraStageProps = {
  augmentedImage: string;
  canvasRef: RefObject<HTMLCanvasElement | null>;
  videoRef: RefObject<HTMLVideoElement | null>;
};

export function CameraStage({ augmentedImage, canvasRef, videoRef }: CameraStageProps) {
  return (
    <section className="stage">
      <div className="camera-surface">
        <video
          ref={videoRef}
          className="source-video"
          style={{ opacity: augmentedImage ? 0 : 1 }}
          playsInline
          muted
        />
        {augmentedImage && (
          <img className="augmented-frame" src={augmentedImage} alt="Augmented camera frame" />
        )}
        <canvas ref={canvasRef} className="capture-canvas" />
      </div>
    </section>
  );
}
