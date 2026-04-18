export type Sticker = {
  id: string;
  name: string;
  anchor: string;
  url: string;
};

export type FaceBox = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type AugmentResponse = {
  image: string;
  faces: FaceBox[];
  stickerId: string;
};

