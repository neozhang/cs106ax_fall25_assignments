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

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

function runEnigmaSimulation(gw) {
  const enigma = {
    permutations: buildPermutations(),
    keys: [],
    lamps: [],
    rotors: [],
    rotorLetters: [],
  };

  // initialize the graphcis
  const keyboard = new Keyboard(enigma, gw, true);
  enigma.keys = keyboard.keys;
  const lampPanel = new Keyboard(enigma, gw, false);
  enigma.lamps = lampPanel.keys;
  const rotorPanel = new RotorPanel(enigma, gw);
  enigma.rotors = rotorPanel.rotors;

  // set up the event forwarder
  const eventForwarder = new EventForwarder(
    enigma,
    gw,
    keyboard,
    lampPanel,
    rotorPanel,
  );
}

/* Graphics */

class Keyboard {
  constructor(enigma, gw, clickable) {
    this.enigma = enigma;
    this.gw = gw;
    this.clickable = clickable;
    this.style = clickable ? KEY_STYLE : LAMP_STYLE;
    this.letters = ALPHABET;
    let keys = [];
    for (let i = 0; i < this.letters.length; i++) {
      let key = {
        index: i,
        letter: this.letters[i],
        color: this.style.colorMap[0],
        position: [
          this.style.locations[i]["x"] - this.style.radius,
          this.style.locations[i]["y"] - this.style.radius,
        ],
        element: this.createKey(
          this.letters[i],
          this.style.locations[i]["x"] - this.style.radius,
          this.style.locations[i]["y"] - this.style.radius,
          this.style.colorMap[0],
        ),
      };
      keys.push(key);
      this.gw.add(key.element);
    }

    this.keys = keys;
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

  permuteKeytoLamp(key) {
    const letter = key.letter;
    const idx = ALPHABET.indexOf(letter);
    let permutedIdx = idx;
    const offsets = buildOffsets(this.enigma.rotorLetters);
    for (let i = 0; i < this.enigma.permutations.length; i++) {
      let permuation = this.enigma.permutations[i];
      permutedIdx = applyPermutation(permutedIdx, permuation, offsets[i]);
    }
    return this.enigma.lamps[permutedIdx];
  }
}

class RotorPanel {
  constructor(enigma, gw) {
    this.enigma = enigma;
    this.gw = gw;
    let rotors = [];
    let letters = ["A", "A", "A"];
    for (let i = 0; i < ROTOR_PERMUTATIONS.length; i++) {
      let rotor = {
        index: i,
        letter: ALPHABET[0],
        position: [ROTOR_LOCATIONS[i]["x"], ROTOR_LOCATIONS[i]["y"]],
        element: this.createRotor(
          ALPHABET[0],
          ROTOR_LOCATIONS[i]["x"],
          ROTOR_LOCATIONS[i]["y"],
        ),
      };
      rotors.push(rotor);
      this.gw.add(rotor.element);
    }
    this.rotors = rotors;
    this.enigma.rotorLetters = letters;
  }

  createRotor(letter, x, y) {
    const compound = GCompound(x, y);
    const rect = GRect(
      -ROTOR_WIDTH / 2,
      -ROTOR_HEIGHT / 2,
      ROTOR_WIDTH,
      ROTOR_HEIGHT,
    );
    rect.setFilled(true);
    rect.setColor(ROTOR_BGCOLOR);
    const label = GLabel(letter, 0, ROTOR_LABEL_DY);
    label.setFont(ROTOR_FONT);
    label.setColor(ROTOR_COLOR);
    label.setTextAlign("center");
    compound.add(rect);
    compound.add(label);
    return compound;
  }

  advanceRotor(rotor) {
    const idx = rotor.index;
    const currentLetter = rotor.letter;
    const currentPos = ALPHABET.indexOf(currentLetter);
    const nextLetter =
      currentPos < ALPHABET.length - 1
        ? ALPHABET[currentPos + 1]
        : ALPHABET[currentPos - ALPHABET.length + 1];
    if (nextLetter === "A" && idx !== 0) {
      this.advanceRotor(this.enigma.rotors[idx - 1]); // carry to the next rotor
    }
    const x = rotor.position[0];
    const y = rotor.position[1];
    this.gw.remove(this.rotors[idx].element);
    const newRotor = this.createRotor(nextLetter, x, y);
    this.enigma.rotors[idx] = {
      index: idx,
      letter: nextLetter,
      position: [x, y],
      element: newRotor,
    };
    this.gw.add(newRotor);
    this.enigma.rotorLetters[idx] = nextLetter;
  }
}

/* Event Forwarder */

class EventForwarder {
  constructor(enigma, gw, keyboard, lampPanel, rotorPanel) {
    this.enigma = enigma;
    this.gw = gw;
    this.keyboard = keyboard;
    this.lampPanel = lampPanel;
    this.rotorPanel = rotorPanel;

    this.gw.addEventListener("mousedown", this.handleDown);
    this.gw.addEventListener("mouseup", this.handleUp);
  }

  handleDown = (e) => {
    const obj = this.gw.getElementAt(e.getX(), e.getY());
    for (const key of this.enigma.keys) {
      if (key.element === obj) {
        const fastRotor = this.enigma.rotors[2];
        this.rotorPanel.advanceRotor(fastRotor); // advance the fast rotor
        this.key = key;
        this.keyboard.toggleKeyColor(this.key);
        this.lamp = this.keyboard.permuteKeytoLamp(key);
        this.lampPanel.toggleLampColor(this.lamp);
      }
    }
    for (const rotor of this.enigma.rotors) {
      if (rotor.element === obj) this.rotorPanel.advanceRotor(rotor);
    }
  };

  handleUp = (e) => {
    const obj = this.gw.getElementAt(e.getX(), e.getY());
    for (const key of this.enigma.keys) {
      if (key.element === obj) {
        this.keyboard.toggleKeyColor(this.key);
        this.lampPanel.toggleLampColor(this.lamp);
      }
    }
  };
}

/* String ops & encryption */

// Applies a permutation to an index with an offset.
function applyPermutation(index, permutation, offset) {
  const shifted = (index + offset) % 26;
  const wiredChar = permutation.charAt(shifted);
  const wiredIndex = wiredChar.charCodeAt(0) - "A".charCodeAt(0);
  return (wiredIndex - offset + 26) % 26;
}

// Inverts the order of characters in the given key string, returning the reversed string.
function invertKey(key) {
  let inverted = "";
  for (let i = 0; i < key.length; i++) {
    let ch = ALPHABET.charAt(key.indexOf(ALPHABET.charAt(i)));
    inverted += ch;
  }
  return inverted;
}

// Builds the permuation array from ROTOR_PERMUTATIONS and REFLECTOR_PERMUTATION
function buildPermutations() {
  const reversedRotorPermuations = [...ROTOR_PERMUTATIONS].reverse();
  const permutations = [...reversedRotorPermuations, REFLECTOR_PERMUTATION];
  for (const key of ROTOR_PERMUTATIONS) permutations.push(invertKey(key));
  return permutations;
}

// Builds the offset array from rotorLetters string based on the fast -> slow -> reflector -> slow -> fast order
function buildOffsets(rotorLetters) {
  const offsets = [];
  const letters = [...rotorLetters].reverse(); // fast -> slow
  letters.push("A", ...rotorLetters); // reflector doesn't return so use "A"
  for (const letter of letters) {
    offsets.push(letter.charCodeAt(0) - "A".charCodeAt(0));
  }
  return offsets;
}
