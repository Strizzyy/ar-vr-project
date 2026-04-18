const CAPTURE_WIDTH = 720;
const JPEG_QUALITY = 0.82;

export function captureVideoFrame(video: HTMLVideoElement, canvas: HTMLCanvasElement): string | null {
  if (video.videoWidth === 0 || video.videoHeight === 0) {
    return null;
  }

  const height = Math.round((video.videoHeight / video.videoWidth) * CAPTURE_WIDTH);
  canvas.width = CAPTURE_WIDTH;
  canvas.height = height;

  const context = canvas.getContext("2d");
  if (!context) {
    return null;
  }

  context.drawImage(video, 0, 0, CAPTURE_WIDTH, height);
  return canvas.toDataURL("image/jpeg", JPEG_QUALITY);
}

