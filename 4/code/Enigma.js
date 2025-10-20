/*
 * File: Enigma.js
 * ---------------
 * This program implements a graphical simulation of the Enigma machine.
 */

"use strict";

/* Main program */

/**
 * Initializes the Enigma simulation once the top view image is loaded.
 */
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

/**
 * Represents either the keyboard or the lamp panel overlay.
 */
class Keyboard {
  constructor(enigma, gw, clickable) {
    this.enigma = enigma;
    this.gw = gw;
    this.clickable = clickable;
    this.style = clickable ? KEY_STYLE : LAMP_STYLE;
    this.letters = ALPHABET;
    let keys = [];
    for (let i = 0; i < this.letters.length; i++) {
      const { x, y } = this.style.locations[i];
      let key = {
        index: i,
        letter: this.letters[i],
        color: this.style.colorMap[0],
        position: [x - this.style.radius, y - this.style.radius],
        element: this.createKey(
          this.letters[i],
          x - this.style.radius,
          y - this.style.radius,
          this.style.colorMap[0],
        ),
      };
      keys.push(key);
      this.gw.add(key.element);
    }

    this.keys = keys;
  }

  /**
   * Creates a single key compound with the specified styling.
   */
  createKey(letter, x, y, overrideColor) {
    const { radius, border, borderColor, bgColor, labelDy, font } = this.style;

    const compound = GCompound(x, y);

    const outerOval = GOval(radius * 2, radius * 2);
    outerOval.setFilled(true);
    outerOval.setColor(borderColor);

    const innerOval = GOval(
      border,
      border,
      (radius - border) * 2,
      (radius - border) * 2,
    );
    innerOval.setFilled(true);
    innerOval.setColor(bgColor);

    const label = GLabel(
      letter.charAt(0).toUpperCase(),
      radius,
      radius + labelDy,
    );
    label.setFont(font);
    label.setColor(overrideColor ?? this.style.colorMap[0]);
    label.setTextAlign("center");

    compound.add(outerOval);
    compound.add(innerOval);
    compound.add(label);

    compound.label = label;

    return compound;
  }

  /**
   * Flips a keyboard key between its up and down colors.
   */
  toggleKeyColor(key) {
    const [upColor, downColor] = this.style.colorMap;
    const nextColor = key.color === upColor ? downColor : upColor;
    key.color = nextColor;
    key.element.label.setColor(nextColor);
  }

  /**
   * Maps a pressed key to the lamp that should light up via permutations.
   */
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

/**
 * Displays and advances the rotor stack above the machine.
 */
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

  /**
   * Creates the compound graphics for a single rotor slot.
   */
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
    compound.label = label;
    return compound;
  }

  /**
   * Advances a rotor by one position, cascading carry to slower rotors.
   */
  advanceRotor(rotor) {
    const next =
      ALPHABET[(ALPHABET.indexOf(rotor.letter) + 1) % ALPHABET.length];
    if (next === "A" && rotor.index !== 0) {
      this.advanceRotor(this.enigma.rotors[rotor.index - 1]);
    }
    rotor.letter = next;
    rotor.element.label.setLabel(next);
    this.enigma.rotorLetters[rotor.index] = next;
  }
}

/* Event Forwarder */

/**
 * Forwards mouse interactions from the window to keys, lamps, and rotors.
 */
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

  /**
   * Handles mouse press events, toggling keys, lamps, and rotors.
   */
  handleDown = (e) => {
    const obj = this.gw.getElementAt(e.getX(), e.getY());
    for (const key of this.enigma.keys) {
      if (key.element === obj) {
        const fastRotor = this.enigma.rotors[2];
        this.rotorPanel.advanceRotor(fastRotor); // advance the fast rotor
        this.key = key;
        this.keyboard.toggleKeyColor(this.key);
        this.lamp = this.keyboard.permuteKeytoLamp(key);
        this.lampPanel.toggleKeyColor(this.lamp);
        break;
      }
    }
    for (const rotor of this.enigma.rotors) {
      if (rotor.element === obj) {
        this.rotorPanel.advanceRotor(rotor);
        break;
      }
    }
  };

  /**
   * Handles mouse release events to reset keys and lamps.
   */
  handleUp = (e) => {
    if (!this.key) return; // early return if no key is pressed
    const obj = this.gw.getElementAt(e.getX(), e.getY());
    for (const key of this.enigma.keys) {
      if (key.element === obj) {
        this.keyboard.toggleKeyColor(this.key);
        this.lampPanel.toggleKeyColor(this.lamp);
        break;
      }
    }
  };
}

/* String ops & encryption */

/**
 * Applies an alphabet permutation to a letter index with the rotor offset.
 */
function applyPermutation(index, permutation, offset) {
  const shifted = (index + offset) % 26;
  const wiredChar = permutation.charAt(shifted);
  const wiredIndex = wiredChar.charCodeAt(0) - "A".charCodeAt(0);
  return (wiredIndex - offset + 26) % 26;
}

/**
 * Produces the inverse wiring for a permutation string.
 */
function invertKey(key) {
  let inverted = "";
  for (let i = 0; i < key.length; i++) {
    let ch = ALPHABET.charAt(key.indexOf(ALPHABET.charAt(i)));
    inverted += ch;
  }
  return inverted;
}

/**
 * Combines rotor, reflector, and inverse rotor permutations into one list.
 */
function buildPermutations() {
  const reversedRotorPermuations = [...ROTOR_PERMUTATIONS].reverse();
  const permutations = [...reversedRotorPermuations, REFLECTOR_PERMUTATION];
  for (const key of ROTOR_PERMUTATIONS) permutations.push(invertKey(key));
  return permutations;
}

/**
 * Generates the offset sequence for forward and reflected rotor traversal.
 */
function buildOffsets(rotorLetters) {
  const offsets = [];
  const letters = [...rotorLetters].reverse(); // fast -> slow
  letters.push("A", ...rotorLetters); // reflector doesn't return so use "A"
  for (const letter of letters) {
    offsets.push(letter.charCodeAt(0) - "A".charCodeAt(0));
  }
  return offsets;
}
