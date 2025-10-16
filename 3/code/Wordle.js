/*
 * File: Wordle.js
 * -----------------
 * This program implements the Wordle game.
 */
"use strict";
/**
 * GAME RULES CONSTANTS
 * ---------------------
 */
const NUM_LETTERS = 5; // The number of letters in each guess
const NUM_GUESSES = 6; // The number of guesses the player has to win

/**
 * SIZING AND POSITIONING CONSTANTS
 * --------------------------------
 */
const SECTION_SEP = 32; // The space between the grid, alert, and keyboard sections
const GUESS_MARGIN = 8; // The space around each guess square
const GWINDOW_WIDTH = 400; // The width of the GWindow

// The size of each guess square (computed to fill the entire GWINDOW_WIDTH)
const GUESS_SQUARE_SIZE =
  (GWINDOW_WIDTH - GUESS_MARGIN * 2 * NUM_LETTERS) / NUM_LETTERS;

// Height of the guess section in total
const GUESS_SECTION_HEIGHT =
  GUESS_SQUARE_SIZE * NUM_GUESSES + GUESS_MARGIN * NUM_GUESSES * 2;

// X and Y position where alerts should be centered
const ALERT_X = GWINDOW_WIDTH / 2;
const ALERT_Y = GUESS_SECTION_HEIGHT + SECTION_SEP;

// X and Y position to place the keyboard
const KEYBOARD_X = 0;
const KEYBOARD_Y = ALERT_Y + SECTION_SEP;

// GWINDOW_HEIGHT calculated to fit everything perfectly.
const GWINDOW_HEIGHT = KEYBOARD_Y + GKeyboard.getHeight(GWINDOW_WIDTH);

/**
 * STYLISTIC CONSTANTS
 * -------------------
 */
const COLORBLIND_MODE = false; // If true, uses R/G colorblind friendly colors

// Background/Border Colors
const BORDER_COLOR = "#3A3A3C"; // Color for border around guess squares
const BACKGROUND_DEFAULT_COLOR = "#121213";
const KEYBOARD_DEFAULT_COLOR = "#818384";
const BACKGROUND_CORRECT_COLOR = COLORBLIND_MODE ? "#E37E43" : "#618C55";
const BACKGROUND_FOUND_COLOR = COLORBLIND_MODE ? "#94C1F6" : "#B1A04C";
const BACKGROUND_WRONG_COLOR = "#3A3A3C";

// Text Colors
const TEXT_DEFAULT_COLOR = "#FFFFFF";
const TEXT_ALERT_COLOR = "#B05050";
const TEXT_WIN_COLOR = COLORBLIND_MODE ? "#94C1F6" : "#618C55";
const TEXT_LOSS_COLOR = "#B05050";

// Fonts
const GUESS_FONT = "700 36px HelveticaNeue";
const ALERT_FONT = "700 13px HelveticaNeue";

// Game states
const GAME_STATUS = {
  PLAYING: "PLAYING",
  ALERT: "ALERT",
  WON: "WON",
  LOST: "LOST",
};

// EMPTY ROW
const EMPTY_ROW = Array.from({ length: NUM_LETTERS }, () => ["", 2]);

/**
 * Accepts a KeyboardEvent and returns
 * the letter that was pressed, or null
 * if a letter wasn't pressed.
 */
function getKeystrokeLetter(e) {
  if (e.altKey || e.ctrlKey || e.metaKey) return null;
  const key = e.key.toLowerCase();

  if (!/^[a-z]$/.exec(key)) return null;

  return key;
}

/**
 * Accepts a KeyboardEvent and returns true
 * if that KeyboardEvent was the user pressing
 * enter (or return), and false otherwise.
 */
function isEnterKeystroke(e) {
  return (
    !e.altKey &&
    !e.ctrlKey &&
    !e.metaKey &&
    (e.code === "Enter" || e.code === "Return")
  );
}

/**
 * Accepts a KeyboardEvent and returns true
 * if that KeyboardEvent was the user pressing
 * backspace (or delete), and false otherwise.
 */
function isBackspaceKeystroke(e) {
  return (
    !e.altKey &&
    !e.ctrlKey &&
    !e.metaKey &&
    (e.code === "Backspace" || e.code === "Delete")
  );
}

/**
 * Accepts a string, and returns if it is a valid English word.
 */
function isEnglishWord(str) {
  return _DICTIONARY.has(str) || _COMMON_WORDS.has(str);
}

/**
 * Returns a random common word from the English lexicon,
 * that is NUM_LETTERS long.
 *
 * Throws an error if no such word exists.
 */
function getRandomWord() {
  const nLetterWords = [..._COMMON_WORDS].filter(
    (word) => word.length === NUM_LETTERS,
  );

  if (nLetterWords.length === 0) {
    throw new Error(
      `The list of common words does not have any words that are ${NUM_LETTERS} long!`,
    );
  }

  return nLetterWords[randomInteger(0, nLetterWords.length)];
}

/**
 * Main function that initializes and runs the Wordle game.
 * Sets up the game window, graphics, and event listeners.
 */
function Wordle() {
  // initialize the game
  let game = initializeGame();

  // initialize graphics
  let gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT);
  let gameView = initializeView(game);
  gw.add(gameView.grid);
  gw.add(gameView.alert);
  gw.add(gameView.keyboard);

  // setup event listeners
  setEventListeners(gw, game, gameView);
}

/**
 * Initializes a new game with default state.
 * Returns a game object with playing status and empty progress.
 */
function initializeGame() {
  let game = {
    status: GAME_STATUS.PLAYING,
    secret: getRandomWord().toUpperCase(),
    guessedRows: [],
    guessInProgress: "",
    foundLetters: "",
    correctLetters: "",
    wrongLetters: "",
  };
  return game;
}

/**
 * Initializes the game view with grid, alert, and keyboard.
 * Returns a view object containing all UI components.
 */
function initializeView(game) {
  let gameView = {
    grid: drawEmptyGrid(),
    alert: drawAlert(
      "Type or click on the keyboard to start. Good luck!",
      game.status,
    ),
    keyboard: GKeyboard(
      KEYBOARD_X,
      KEYBOARD_Y,
      GWINDOW_WIDTH,
      TEXT_DEFAULT_COLOR,
      KEYBOARD_DEFAULT_COLOR,
    ),
    currentRow: 0,
    currentColumn: 0,
  };
  return gameView;
}

/**
 * Initializes event listeners for the game view.
 */
function setEventListeners(gw, game, gameView) {
  function keyClickAction(e) {
    if (game.status !== GAME_STATUS.PLAYING && game.status !== GAME_STATUS.ALERT) {
      return; // early return to block keyclicks on non-playing status
    }
    if (e) {
      // guard against edge cases
      let letter = e.toUpperCase();
      if (game.status === GAME_STATUS.ALERT) {
        game.status = GAME_STATUS.PLAYING;
        updateAlert("", game.status, gw, gameView);
      }
      if (game.guessInProgress.length < NUM_LETTERS) {
        game.guessInProgress += letter;
        // render the current row
        let row = createRow(game.guessInProgress);
        let rowView = drawRow(row, gameView.currentRow, gameView.grid);
        gameView.currentColumn += 1;
      }
    }
  }

  function enterAction() {
    if (game.status === GAME_STATUS.PLAYING || game.status === GAME_STATUS.ALERT) {
      let guess = game.guessInProgress.trim();
      if (guess.length < NUM_LETTERS) {
        game.status = GAME_STATUS.ALERT;
        updateAlert(
          `You guessed ${guess} but it's too short.`,
          game.status,
          gw,
          gameView,
        );
      } else if (!isEnglishWord(guess.toLowerCase())) {
        game.status = GAME_STATUS.ALERT;
        updateAlert(
          `You guessed ${guess} but it's not an English word.`,
          game.status,
          gw,
          gameView,
        );
      } else {
        // update the grid
        let row = createRow(guess, game.secret); // create the model for the new row
        let rowView = drawRow(row, gameView.currentRow, gameView.grid); // create the view for the new row
        game.guessedRows.push(row); // submit the current row

        // check win / lose
        if (game.guessInProgress === game.secret) {
          game.status = GAME_STATUS.WON;
          updateAlert(
            `You won! The secret word is ${game.secret}. Press Enter to restart.`,
            game.status,
            gw,
            gameView,
          );
        } else if (gameView.currentRow === NUM_GUESSES - 1) {
          game.status = GAME_STATUS.LOST;
          updateAlert(
            `You lost! The secret word is ${game.secret}. Press Enter to restart.`,
            game.status,
            gw,
            gameView,
          );
        } else {
          gameView.currentRow += 1; // move the cursor row
          gameView.currentColumn = 0; // reset the cursor column
          game = saveGuessToGame(row, game);
          updateKeyColor(gameView.keyboard, game); // update keyboard colors
          updateAlert("Keep guessing!", game.status, gw, gameView);
        }
        // reset, clean up and move on
        game.guessInProgress = ""; // reset the string
      }
    } else {
      resetGame(gw, game, gameView);
    }
  }

  function backspaceAction() {
    if (game.status !== GAME_STATUS.PLAYING && game.status !== GAME_STATUS.ALERT) {
      return;
    }
    if (gameView.currentColumn > 0) {
      if (game.status === GAME_STATUS.ALERT) {
        game.status = GAME_STATUS.PLAYING;
        updateAlert("", game.status, gw, gameView);
      }
      game.guessInProgress = game.guessInProgress.substring(
        0,
        gameView.currentColumn - 1,
      ) + game.guessInProgress.substring(gameView.currentColumn); // remove character at currentColumn - 1
      gameView.currentColumn -= 1; // move the cursor back by 1
      // redraw the current row
      let row = createRow(game.guessInProgress);
      let rowView = drawRow(row, gameView.currentRow, gameView.grid);
    }
  }

  function keyDownAction(e) {
    let key = getKeystrokeLetter(e);
    if (isEnterKeystroke(e)) {
      enterAction();
    } else if (isBackspaceKeystroke(e)) {
      backspaceAction();
    } else {
      keyClickAction(key);
    }
  }

  gameView.keyboard.addEventListener("keyclick", keyClickAction);
  gameView.keyboard.addEventListener("enter", enterAction);
  gameView.keyboard.addEventListener("backspace", backspaceAction);
  gw.addEventListener("keydown", keyDownAction);
}

/**
 * Draws an empty grid of guess squares.
 * Populates the provided grid compound with empty rows.
 */
function drawEmptyGrid() {
  let gridCompound = GCompound();
  for (let i = 0; i < NUM_GUESSES; i++) {
    gridCompound.add(drawRow(EMPTY_ROW, i, gridCompound));
  }
  return gridCompound;
}

/**
 * Creates a row model with letters and color codes.
 * Returns an array of [letter, color] pairs for display.
 */
function createRow(guess, secret) {
  let row = [];
  let colorCodes = [];
  if (secret) {
    colorCodes = checkGuessWithSecret(guess, secret);
  } else {
    colorCodes = [2, 2, 2, 2, 2]; // use the value 2 for normal color
  }
  for (let i = 0; i < NUM_LETTERS; i++) {
    if (guess) {
      let currentletter = guess.substring(i, i + 1);
      row.push([currentletter, colorCodes[i]]);
    } else {
      row = EMPTY_ROW;
    }
  }
  return row;
}

/**
 * Draws a single row of guess squares.
 * Returns a compound object with positioned squares.
 */
function drawRow(row, currentRow, gridCompound) {
  let rowCompound = GCompound();
  for (let i = 0; i < row.length; i++) {
    let square = drawGuessSquare(row[i][0], row[i][1]);
    rowCompound.add(square, (GUESS_SQUARE_SIZE + GUESS_MARGIN * 2) * i, 0);
  }
  if (gridCompound !== undefined) {
    gridCompound.add(
      rowCompound,
      GUESS_MARGIN,
      GUESS_MARGIN + (GUESS_SQUARE_SIZE + GUESS_MARGIN * 2) * currentRow,
    );
  }
  return rowCompound;
}

/**
 * Draws a single guess square with letter and color.
 * Returns a compound object with background and text.
 */
function drawGuessSquare(letter, color) {
  let square = GCompound();
  let squareBox = GRect(0, 0, GUESS_SQUARE_SIZE, GUESS_SQUARE_SIZE);
  squareBox.setFilled(true);
  squareBox.setColor(BORDER_COLOR);
  switch (color) {
    case -1:
      squareBox.setFillColor(BACKGROUND_WRONG_COLOR);
      break;
    case 0:
      squareBox.setFillColor(BACKGROUND_FOUND_COLOR);
      break;
    case 1:
      squareBox.setFillColor(BACKGROUND_CORRECT_COLOR);
      break;
    default:
      squareBox.setFillColor(BACKGROUND_DEFAULT_COLOR);
  }
  let squareText = GLabel(letter.toUpperCase());
  squareText.setFont(GUESS_FONT);
  squareText.setColor(TEXT_DEFAULT_COLOR);
  square.add(squareBox);
  square.add(
    squareText,
    (GUESS_SQUARE_SIZE - squareText.getWidth()) / 2,
    GUESS_SQUARE_SIZE - squareText.getAscent() + 8,
  );
  return square;
}

/**
 * Draws an alert message with appropriate color.
 * Returns a centered label based on game status.
 */
function drawAlert(text, gameStatus) {
  let alert = GLabel(text, ALERT_X, ALERT_Y);
  alert.setTextAlign("center");
  alert.setFont(ALERT_FONT);
  if (gameStatus === GAME_STATUS.WON) {
    alert.setColor(TEXT_WIN_COLOR);
  } else if (gameStatus === GAME_STATUS.LOST) {
    alert.setColor(TEXT_LOSS_COLOR);
  } else if (gameStatus === GAME_STATUS.ALERT) {
    alert.setColor(TEXT_ALERT_COLOR);
  } else {
    alert.setColor(TEXT_DEFAULT_COLOR);
  }
  return alert;
}

/**
 * Updates keyboard key colors based on game state.
 * Modifies keyboard appearance for found, correct, and wrong letters.
 */
function updateKeyColor(keyboard, game) {
  for (let i = 0; i < game.foundLetters.length; i++) {
    let letter = game.foundLetters.substring(i, i + 1);
    keyboard.setKeyColor(letter, BACKGROUND_FOUND_COLOR);
  }
  for (let i = 0; i < game.correctLetters.length; i++) {
    let letter = game.correctLetters.substring(i, i + 1);
    keyboard.setKeyColor(letter, BACKGROUND_CORRECT_COLOR);
  }
  for (let i = 0; i < game.wrongLetters.length; i++) {
    let letter = game.wrongLetters.substring(i, i + 1);
    keyboard.setKeyColor(letter, BACKGROUND_WRONG_COLOR);
  }
}

/**
 * Checks a guess against the secret word.
 * Returns array with 1 for exact match, 0 for wrong position, -1 for not found.
 */
function checkGuessWithSecret(guess, secret) {
  let match = [];
  let matchedPos = 0;
  for (let i = 0; i < guess.length; i++) {
    let currentLetter = guess.substring(i, i + 1);
    matchedPos = secret.indexOf(currentLetter);
    if (matchedPos === -1) {
      match.push(-1);
    } else if (matchedPos === i) {
      match.push(1);
    } else {
      match.push(0);
    }
  }
  return match;
}

/**
 * Saves guess results to game state.
 * Updates found, correct, and wrong letter tracking.
 */
function saveGuessToGame(row, game) {
  for (let i = 0; i < row.length; i++) {
    let letter = row[i][0];
    let color = row[i][1];
    if (color > 1) continue;
    if (color === 1) {
      game.foundLetters = game.foundLetters.split(letter).join(""); // remove this letter from foundLetters
      game.correctLetters += letter; // add this letter to correctLetters
    } else if (color === 0) {
      game.foundLetters += letter; // add this letter to foundLetters
    } else if (color === -1) {
      game.wrongLetters += letter; // add this letter to wrongLetters
    }
  }
  return game;
}

/**
 * Updates the alert message with the given message and game status.
 */
function updateAlert(message, gameStatus, gw, gameView) {
  gw.remove(gameView.alert);
  gameView.alert = drawAlert(message, gameStatus);
  gw.add(gameView.alert);
}

/**
 * Extension: Enter key to restart game when game is won or lost
 */
function resetGame(gw, game, gameView) {
  if (game.status === GAME_STATUS.WON || game.status === GAME_STATUS.LOST) {
    // Remove old UI
    gw.remove(gameView.grid);
    gw.remove(gameView.alert);

    // Reinitialize game state
    const newGame = initializeGame();
    game.status = newGame.status;
    game.secret = newGame.secret;
    game.guessedRows = newGame.guessedRows;
    game.guessInProgress = newGame.guessInProgress;
    game.foundLetters = newGame.foundLetters;
    game.correctLetters = newGame.correctLetters;
    game.wrongLetters = newGame.wrongLetters;

    // Reset view state
    gameView.currentRow = 0;
    gameView.currentColumn = 0;
    gameView.grid = drawEmptyGrid();
    gameView.alert = drawAlert(
      "Type or click on the keyboard to start. Good luck!",
      game.status,
    );

    // Reset the keyboard colors
    resetAllColors(gameView.keyboard);

    // Add back the new UI
    gw.add(gameView.grid);
    gw.add(gameView.alert);
  }
}


/**
 * Resets all keyboard key colors to the default color.
 */
function resetAllColors(keyboard) {
  let keys = "QWERTYUIOPASDFGHJKLZXCVBNM";
  for (let i = 0; i < keys.length; i++) {
    keyboard.setKeyColor(keys[i], KEYBOARD_DEFAULT_COLOR);
  }
}