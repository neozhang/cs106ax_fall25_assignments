/*
 * File: Enigma.js
 * ---------------
 * This program implements a graphical simulation of the Enigma machine.
 */

"use strict";

/* Main program */

function Enigma() {
  let enigmaImage = GImage("EnigmaTopView.png");
  enigmaImage.addEventListener("load", function () {
    let gw = GWindow(enigmaImage.getWidth(), enigmaImage.getHeight());
    gw.add(enigmaImage);
    runEnigmaSimulation(gw);
  });
}

// You are responsible for filling in the rest of the code.  Your
// implementation of runEnigmaSimulation should perform the
// following operations:
//
// 1. Create an object that encapsulates the state of the Enigma machine.
// 2. Create and add graphical objects that sit on top of the image.
// 3. Add listeners that forward mouse events to those objects.

function runEnigmaSimulation(gw) {
  let enigma = {};

  // initialize the graphcis
  const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  gw.add(createKeyboard(ALPHABET, 0, 0));
}

/* Graphics */

function createKeyboard(keys, x, y) {
  const compound = GCompound(x, y);
  for (let i = 0; i < keys.length; i++) {
    let posX = KEY_LOCATIONS[i]["x"] - KEY_RADIUS;
    let posY = KEY_LOCATIONS[i]["y"] - KEY_RADIUS;
    compound.add(createKeyboardKey(keys[i], posX, posY));
  }
  return compound;
}

function createKeyboardKey(key, x, y) {
  const compound = GCompound(x, y);
  const innerOval = GOval(
    KEY_BORDER,
    KEY_BORDER,
    (KEY_RADIUS - KEY_BORDER) * 2,
    (KEY_RADIUS - KEY_BORDER) * 2,
  );
  const outerOval = GOval(KEY_RADIUS * 2, KEY_RADIUS * 2);
  innerOval.setFilled(true);
  innerOval.setColor(KEY_BGCOLOR);
  outerOval.setFilled(true);
  outerOval.setColor(KEY_BORDER_COLOR);

  key = key.charAt(0).toUpperCase();
  const label = GLabel(key, KEY_RADIUS, KEY_RADIUS + KEY_LABEL_DY);
  label.setFont(KEY_FONT);
  label.setColor(KEY_UP_COLOR);
  label.setTextAlign("center");

  compound.add(outerOval);
  compound.add(innerOval);
  compound.add(label);

  return compound;
}

/* String ops & encryption */

// Applies a permutation to an index with an offset.
function applyPermutation(index, permutation, offset) {
  let shiftedIndex = (index + offset + 26) % 26;
  let permutedChar = permutation.charAt(shiftedIndex);
  return permutedChar.charCodeAt(0) - offset;
}

// Inverts the order of characters in the given key string, returning the reversed string.
function invertKey(key) {
  let inverted = [];
  for (let i = 0; i <= key.length; i++) {
    let ch = key.charAt(key.length - i);
    inverted.push(ch);
  }
  return inverted.join("");
}
