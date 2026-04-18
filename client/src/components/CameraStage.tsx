import type { RefObject } from "react";

type CameraStageProps = {
  augmentedImage: string;
  canvasRef: RefObject<HTMLCanvasElement | null>;
  videoRef: RefObject<HTMLVideoElement | null>;
};

export function CameraStage({ augmentedImage, canvasRef, videoRef }: CameraStageProps) {
  return (
    <section className="stage">
      <div className="camera-surface">
        <video ref={videoRef} className="source-video" playsInline muted />
        {augmentedImage ? (
          <img className="augmented-frame" src={augmentedImage} alt="Augmented camera frame" />
        ) : (
          <div className="empty-state">Allow camera access to begin.</div>
        )}
        <canvas ref={canvasRef} className="capture-canvas" />
      </div>
    </section>
  );
}
