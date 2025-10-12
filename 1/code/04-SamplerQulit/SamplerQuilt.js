/*
 * File: SamplerQuilt.js
 * ---------------------
 * This program uses the object-oriented graphics model to draw
 * a Sampler Quilt to the screen. :)
 */

"use strict";

/* Constants */
const PATCH_DIMENSION = 75;
const NUM_ROWS = 7;
const NUM_COLUMNS = 7;
const BORDER_COLOR = "Black";
const BULLSEYE_BOLD_COLOR = "Red";
const BULLSEYE_MILD_COLOR = "White";
const LOG_COLOR = "Tan";
const LOVE_FRAME_COLOR = "Pink";
const LOVE_MAT_COLOR = "White";

/* Derived Constants */
const WINDOW_WIDTH = NUM_COLUMNS * PATCH_DIMENSION;
const WINDOW_HEIGHT = NUM_ROWS * PATCH_DIMENSION;

/*
 * Function: DrawSamplerQuilt
 * --------------------------
 * Draws a sampler quilt as outlined in the assignment handout.
 */

function DrawSamplerQuilt() {
  let gw = GWindow(WINDOW_WIDTH, WINDOW_HEIGHT);
  drawQuilt(gw);
}

/*
 * Function: drawQuilt
 * --------------------------
 * Inserts all of the sampler quilt into the supplied graphics window.
 */
function drawQuilt(gw) {
  for (let row = 0; row < NUM_ROWS; row++) {
    for (let col = 0; col < NUM_COLUMNS; col++) {
      let patch;
      switch ((col + row) % 4) {
        case 0:
          patch = createBullsEyePatch();
          gw.add(patch, col * PATCH_DIMENSION, row * PATCH_DIMENSION);
          break;
        case 1:
          patch = createLogCabinPatch();
          gw.add(patch, col * PATCH_DIMENSION, row * PATCH_DIMENSION);
          break;
        case 2:
          patch = createFlowerPatch();
          gw.add(patch, col * PATCH_DIMENSION, row * PATCH_DIMENSION);
          break;
        case 3:
          patch = createLovePatch();
          gw.add(patch, col * PATCH_DIMENSION, row * PATCH_DIMENSION);
          break;
      }

      let box = createBox();
      gw.add(box, col * PATCH_DIMENSION, row * PATCH_DIMENSION);
    }
  }
}

/* Patches */

function createBullsEyePatch() {
  let bullseye = GCompound();
  const GAP = 5;
  const MARGIN = 4;
  // Draw 7 circles, with alternating colors (red and white)
  // Define GAP and MARGIN
  // the i-th circle has the size of PATCH_DIMENSION - MARGIN * 2 - i * GAP * 2
  // the i-th circle has the offset of MARGIN - i * GAP
  for (let i = 0; i < 7; i++) {
    let offset = i * GAP + MARGIN;
    let size = PATCH_DIMENSION - MARGIN * 2 - i * GAP * 2;
    let eye = GOval(offset, offset, size, size);
    eye.setColor(BORDER_COLOR);
    let filled = i % 2 === 0;
    if (filled) {
      eye.setFilled(true);
      eye.setFillColor(BULLSEYE_BOLD_COLOR);
    } else {
      eye.setFilled(true);
      eye.setFillColor(BULLSEYE_MILD_COLOR);
    }
    bullseye.add(eye);
  }
  return bullseye;
}

function createFlowerPatch() {
  let flower = GCompound();
  const MARGIN = 4;
  const GAP = 4;
  const SIZE = (PATCH_DIMENSION - MARGIN * 2 - GAP * 1) / 2;
  // Draw 5 circles, with 5 different colors
  // 4 on the corner, 1 in the center
  for (let x = 0; x < 2; x++) {
    for (let y = 0; y < 2; y++) {
      let offset_x = MARGIN + SIZE * x + GAP * x;
      let offset_y = MARGIN + SIZE * y + GAP * y;
      let bud = GOval(offset_x, offset_y, SIZE, SIZE);
      bud.setFilled(true);
      bud.setFillColor(randomColor());
      bud.setColor(BORDER_COLOR);
      flower.add(bud);
    }
  }
  // add the center one
  let bud = GOval(
    (PATCH_DIMENSION - SIZE) / 2,
    (PATCH_DIMENSION - SIZE) / 2,
    SIZE,
    SIZE,
  );
  bud.setFilled(true);
  bud.setFillColor(randomColor());
  bud.setColor(BORDER_COLOR);
  flower.add(bud);
  return flower;
}

function createLogCabinPatch() {
  const THICKNESS = 8;
  let patch = GCompound();
  for (let i = 0; i < 4; i++) {
    let layer = createLogCabinLayer(
      PATCH_DIMENSION - THICKNESS * i * 2,
      THICKNESS,
      LOG_COLOR,
    );
    layer.setLocation(THICKNESS * i, THICKNESS * i);
    patch.add(layer);
  }

  return patch;
}

function createLovePatch() {
  const THICKNESS = 8;
  let patch = GCompound();
  let photo = randomPhoto();
  patch.add(photo);
  for (let i = 0; i < 2; i++) {
    let layer = createLogCabinLayer(
      PATCH_DIMENSION - THICKNESS * i * 2,
      THICKNESS,
      i % 2 == 0 ? LOVE_FRAME_COLOR : LOVE_MAT_COLOR,
    );
    layer.setLocation(THICKNESS * i, THICKNESS * i);
    patch.add(layer);
  }

  return patch;
}

/* Helper Functions */

function createLogCabinLayer(size, thickness, color) {
  let layer = GCompound();
  let up = createLogCabinItem(0, 0, size - thickness, thickness, color);
  let right = createLogCabinItem(
    size - thickness,
    0,
    thickness,
    size - thickness,
    color,
  );
  let down = createLogCabinItem(
    thickness,
    size - thickness,
    size - thickness,
    thickness,
    color,
  );
  let left = createLogCabinItem(
    0,
    thickness,
    thickness,
    size - thickness,
    color,
  );
  layer.add(up);
  layer.add(right);
  layer.add(down);
  layer.add(left);
  return layer;
}

function createLogCabinItem(offset_x, offset_y, width, height, color) {
  let logCabinItem = GRect(offset_x, offset_y, width, height);
  logCabinItem.setFilled(true);
  logCabinItem.setFillColor(color);
  logCabinItem.setColor(BORDER_COLOR);
  return logCabinItem;
}

function randomPhoto() {
  const ROOT = "https://cs106ax.stanford.edu/img/";
  const TA = ["andy", "diego", "eugene", "jenny", "sabrina", "tina"];
  const i = Math.floor(Math.random() * 6);
  let photo = GImage(ROOT + TA[i] + ".png");
  return photo;
}

function createBox() {
  return GRect(PATCH_DIMENSION, PATCH_DIMENSION);
}
