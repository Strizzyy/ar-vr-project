import type { Sticker } from "../types";

type ControlPanelProps = {
  activeSticker?: Sticker;
  cameraError: string;
  faceCount: number;
  isLive: boolean;
  onRestartCamera: () => void;
  onSelectSticker: (stickerId: string) => void;
  onToggleLive: () => void;
  selectedSticker: string;
  status: string;
  stickerError: string;
  stickers: Sticker[];
};

export function ControlPanel({
  activeSticker,
  cameraError,
  faceCount,
  isLive,
  onRestartCamera,
  onSelectSticker,
  onToggleLive,
  selectedSticker,
  status,
  stickerError,
  stickers,
}: ControlPanelProps) {
  return (
    <aside className="controls">
      <div>
        <p className="eyebrow">OpenCV AR Studio</p>
        <h1>Face stickers that follow the frame.</h1>
        <p className="status">{cameraError || stickerError || status}</p>
      </div>

      <div className="meta-row">
        <span>
          {faceCount} face{faceCount === 1 ? "" : "s"}
        </span>
        <span>{activeSticker?.name ?? "Sticker"}</span>
      </div>

      <div className="sticker-grid" aria-label="Choose a sticker">
        {stickers.map((sticker) => (
          <button
            className={sticker.id === selectedSticker ? "sticker active" : "sticker"}
            key={sticker.id}
            onClick={() => onSelectSticker(sticker.id)}
            type="button"
          >
            <img src={sticker.url} alt="" />
            <span>{sticker.name}</span>
          </button>
        ))}
      </div>

      <div className="actions">
        <button type="button" onClick={onToggleLive}>
          {isLive ? "Pause AR" : "Resume AR"}
        </button>
        <button type="button" onClick={onRestartCamera}>
          Restart camera
        </button>
      </div>
    </aside>
  );
}

