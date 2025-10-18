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

const KEY_STYLE = {
  radius: KEY_RADIUS,
  border: KEY_BORDER,
  borderColor: KEY_BORDER_COLOR,
  bgColor: KEY_BGCOLOR,
  colorMap: [KEY_UP_COLOR, KEY_DOWN_COLOR],
  labelDy: KEY_LABEL_DY,
  font: KEY_FONT,
  locations: KEY_LOCATIONS,
};
const LAMP_STYLE = {
  radius: LAMP_RADIUS,
  border: 1, // have to use a magic number ...
  borderColor: LAMP_BORDER_COLOR,
  bgColor: LAMP_BGCOLOR,
  colorMap: [LAMP_OFF_COLOR, LAMP_ON_COLOR],
  labelDy: LAMP_LABEL_DY,
  font: LAMP_FONT,
  locations: LAMP_LOCATIONS,
};

function runEnigmaSimulation(gw) {
  let enigma = {
    ALPHABET: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    keys: [],
    lamps: [],
    inputLetters: "",
  };

  // initialize the graphcis
  const keyboard = new Keyboard(enigma, gw, true);
  enigma.keys = keyboard.keys;
  const lampPanel = new Keyboard(enigma, gw, false);
  enigma.lamps = lampPanel.keys;
}

/* Graphics */

class Keyboard {
  constructor(enigma, gw, clickable) {
    this.enigma = enigma;
    this.gw = gw;
    this.style = clickable ? KEY_STYLE : LAMP_STYLE;
    const letters = enigma.ALPHABET;
    this.letters = letters;
    let keys = [];
    for (let i = 0; i < letters.length; i++) {
      let key = {
        index: i,
        letter: letters[i],
        color: this.style.colorMap[0],
        position: [
          this.style.locations[i]["x"] - this.style.radius,
          this.style.locations[i]["y"] - this.style.radius,
        ],
        element: this.createKey(
          letters[i],
          this.style.locations[i]["x"] - this.style.radius,
          this.style.locations[i]["y"] - this.style.radius,
          this.style.colorMap[0],
        ),
      };
      keys.push(key);
      this.gw.add(key.element);
    }

    this.keys = keys;
    if (clickable) this.attachListeners();
  }

  createKey(
    letter,
    x,
    y,
    keyColor,
    radius,
    border,
    borderColor,
    bgColor,
    labelDy,
    font,
  ) {
    const compound = GCompound(x, y);

    radius = radius ? radius : this.style.radius;
    border = border ? border : this.style.border;
    borderColor = borderColor ? borderColor : this.style.borderColor;
    bgColor = bgColor ? bgColor : this.style.bgColor;
    labelDy = labelDy ? labelDy : this.style.labelDy;
    font = font ? font : this.style.font;

    const innerOval = GOval(
      border,
      border,
      (radius - border) * 2,
      (radius - border) * 2,
    );
    const outerOval = GOval(radius * 2, radius * 2);
    innerOval.setFilled(true);
    innerOval.setColor(bgColor);
    outerOval.setFilled(true);
    outerOval.setColor(borderColor);

    letter = letter.charAt(0).toUpperCase();
    const label = GLabel(letter, radius, radius + labelDy);
    label.setFont(font);
    label.setColor(keyColor);
    label.setTextAlign("center");

    compound.add(outerOval);
    compound.add(innerOval);
    compound.add(label);

    return compound;
  }

  attachListeners() {
    const handleClick = (e) => {
      const obj = this.gw.getElementAt(e.getX(), e.getY());
      for (const key of this.keys) {
        if (key.element === obj) {
          this.toggleKeyColor(key);
          this.toggleLampColor(key);
        }
      }
    };
    this.gw.addEventListener("mousedown", handleClick);
    this.gw.addEventListener("mouseup", handleClick);
  }

  toggleKeyColor(key) {
    this.gw.remove(key.element);
    const newColor =
      this.keys[key.index].color === this.style.colorMap[0]
        ? this.style.colorMap[1]
        : this.style.colorMap[0];
    const newKeyElement = this.createKey(
      key.letter,
      key.position[0],
      key.position[1],
      newColor,
    );
    key.element = newKeyElement;
    key.color = newColor;
    this.keys[key.index] = key;
    this.gw.add(newKeyElement);
  }

  toggleLampColor(key) {
    const lamp = this.enigma.lamps[key.index];
    this.gw.remove(lamp.element);
    const newColor =
      lamp.color === LAMP_STYLE.colorMap[0]
        ? LAMP_STYLE.colorMap[1]
        : LAMP_STYLE.colorMap[0];
    const newLampElement = this.createKey(
      lamp.letter,
      lamp.position[0],
      lamp.position[1],
      newColor,
      LAMP_STYLE.radius,
      LAMP_STYLE.border,
      LAMP_STYLE.borderColor,
      LAMP_STYLE.bgColor,
      LAMP_STYLE.labelDy,
      LAMP_STYLE.font,
    );
    lamp.element = newLampElement;
    lamp.color = newColor;
    this.enigma.lamps[key.index] = lamp;
    this.gw.add(newLampElement);
  }
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
