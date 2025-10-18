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
  let enigma = {
    ALPHABET: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    keys: [],
    inputLetters: "",
  };

  // initialize the graphcis
  enigma.keys = initializeKeyboard(enigma.ALPHABET, 0, 0);
  for (const key of enigma.keys) {
    gw.add(key.element);
  }
  // initialize the event listeners
  setEventListeners(gw, enigma);
}

/* Graphics */

function initializeKeyboard(letters, x, y) {
  let keys = [];
  for (let i = 0; i < letters.length; i++) {
    let posX = KEY_LOCATIONS[i]["x"] - KEY_RADIUS;
    let posY = KEY_LOCATIONS[i]["y"] - KEY_RADIUS;
    let key = {
      letter: letters[i],
      element: createKeyboardKey(
        letters[i],
        KEY_LOCATIONS[i]["x"] - KEY_RADIUS,
        KEY_LOCATIONS[i]["y"] - KEY_RADIUS,
        KEY_UP_COLOR,
      ),
    };
    keys.push(key);
  }

  return keys;
}

function createKeyboardKey(letter, x, y, keyColor) {
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

  letter = letter.charAt(0).toUpperCase();
  const label = GLabel(letter, KEY_RADIUS, KEY_RADIUS + KEY_LABEL_DY);
  label.setFont(KEY_FONT);
  label.setColor(keyColor);
  label.setTextAlign("center");

  compound.add(outerOval);
  compound.add(innerOval);
  compound.add(label);

  return compound;
}

/* Event Listeners */

function setEventListeners(gw, enigma) {
  // set up mouseDownAction for gw and forward to each key
  let mouseDownAction = function (e) {
    let obj = gw.getElementAt(e.getX(), e.getY());
    if (obj === null) return;
    for (const key of enigma.keys) {
      if (key.element === obj) {
        gw.remove(obj);
        const newKeyElement = createKeyboardKey(
          key.letter,
          key.element.getX(),
          key.element.getY(),
          KEY_DOWN_COLOR,
        );
        gw.add(newKeyElement);
        key.element = newKeyElement;
        break;
      }
    }
  };

  let mouseUpAction = function (e) {
    let obj = gw.getElementAt(e.getX(), e.getY());
    if (obj === null) return;
    for (const key of enigma.keys) {
      if (key.element === obj) {
        gw.remove(obj);
        const newKeyElement = createKeyboardKey(
          key.letter,
          key.element.getX(),
          key.element.getY(),
          KEY_UP_COLOR,
        );
        gw.add(newKeyElement);
        key.element = newKeyElement;
        break;
      }
    }
  };

  gw.addEventListener("mousedown", mouseDownAction);
  gw.addEventListener("mouseup", mouseUpAction);
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
