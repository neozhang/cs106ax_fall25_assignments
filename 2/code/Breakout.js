/*
 * File: Breakout.js
 * -----------------
 * This program implements the Breakout game.
 */
"use strict";

/* Constants */
const GWINDOW_WIDTH = 360; /* Width of the graphics window      */
const GWINDOW_HEIGHT = 600; /* Height of the graphics window     */
const N_ROWS = 10; /* Number of brick rows              */
const N_COLS = 10; /* Number of brick columns           */
const BRICK_ASPECT_RATIO = 4 / 1; /* Width to height ratio of a brick  */
const BRICK_TO_BALL_RATIO = 3 / 2; /* Ratio of brick width to ball size */
const BRICK_TO_PADDLE_RATIO = 2 / 3; /* Ratio of brick to paddle width    */
const BRICK_SEP = 2; /* Separation between bricks         */
const TOP_FRACTION = 0.1; /* Fraction of window above bricks   */
const BOTTOM_FRACTION = 0.05; /* Fraction of window below paddle   */
const N_BALLS = 3; /* Number of balls in a game         */
const TIME_STEP = 10; /* Time step in milliseconds         */
const INITIAL_Y_VELOCITY = 3.0; /* Starting y velocity downward      */
const MIN_X_VELOCITY = 1.0; /* Minimum random x velocity         */
const MAX_X_VELOCITY = 3.0; /* Maximum random x velocity         */
const BRICK_COLORS = [
  "Red",
  "Orange",
  "Green",
  "Cyan",
  "Blue",
]; /* Colors for the bricks */
const POINTS_BY_ROW = [50, 40, 30, 20, 10];
const MAX_SPEED_MULTIPLIER = 2.0;
const SPEED_EXPONENT = 0.5;
const GAME_STATES = {
  WAITING: "waiting",
  PLAYING: "playing",
  WON: "won",
  LOST: "lost",
};

/* Derived constants */
const BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS;
const BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO;
const PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO;
const PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO;
const PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT;
const BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO;

/* Main program */

function Breakout() {
  // initialize the game
  const game = initializeGame();

  // initialize the graphics
  initializeGraphics(game);

  // set up event listeners
  setupEventListeners(game);
}

/* Helper functions */

/* Helper: initializedGame()
 * Initialize game variables and create graphics window
 * */
function initializeGame() {
  let gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT);
  return {
    // world
    gw,
    // game states
    remainingBalls: N_BALLS,
    remainingBricks: N_COLS * N_ROWS,
    gameState: GAME_STATES.WAITING,
    timer: null,
    clickAction: null,
    score: 0,
    paddleHitCount: 0,
    // physics
    originalVx:
      randomReal(MIN_X_VELOCITY, MAX_X_VELOCITY) * (randomChance() ? -1 : 1),
    originalVy: INITIAL_Y_VELOCITY,
    vx: 0,
    vy: 0,
    speedMultiplier: 0,
    // graphic
    paddle: null,
    ball: null,
    bricks: [],
    msg: null,
    scoreBoard: null,
  };
}

/* Helper: initializeGraphics(game)
 * Initialize graphics for the game,
 * including the paddle, ball, bricks, scoreboard, and game message.
 */
function initializeGraphics(game) {
  // display game message
  game.msg = displayGameMsg(
    "Click to start! Balls remaining: " + game.remainingBalls.toString(),
  );
  game.gw.add(game.msg);

  // render the score board
  game.scoreBoard = displayScoreBoard(game.score);
  game.gw.add(game.scoreBoard);

  // draw the ball, paddle and bricks
  game.paddle = drawPaddle();
  game.ball = drawBall();
  game.gw.add(game.paddle);
  game.gw.add(game.ball);
  game.bricks = drawBricks();
  for (const brick of game.bricks) {
    game.gw.add(brick);
  }
}

/* Helper: setupEventListeners()
 * Set up event listeners for the game
 */
function setupEventListeners(game) {
  let mouseMoveAction = (e) => {
    let newX = e.getX() - PADDLE_WIDTH / 2;
    if (newX > GWINDOW_WIDTH - PADDLE_WIDTH)
      newX = GWINDOW_WIDTH - PADDLE_WIDTH;
    if (newX < 0) newX = 0;
    game.paddle.setLocation(newX, PADDLE_Y);
  };
  game.gw.addEventListener("mousemove", mouseMoveAction);

  let mouseClickAction = () => {
    if (game.gameState === GAME_STATES.WAITING) {
      startGame(game);
    }
  };
  game.gw.addEventListener("click", mouseClickAction);
}

/* Helper: startGame()
 * Initialize game variables and create graphics window
 */

function startGame(game) {
  game.gameState = GAME_STATES.PLAYING;
  game.gw.remove(game.msg);
  game.paddleHitCount = 0; // reset the paddle hit count for the ball
  game.vx = game.originalVx;
  game.vy = game.originalVy;
  let step = function () {
    game.ball.move(game.vx, game.vy);
    checkWallCollision(game);
    checkBallCollision(game);
    checkBallDrop(game);
  };
  game.timer = setInterval(step, TIME_STEP);
}

/* Helper: checkWallCollision(game)
 * Checks for collision between the ball and the walls.
 * If a collision is detected, the ball's velocity is updated accordingly.
 */
function checkWallCollision(game) {
  let ball = game.ball;
  if (ball.getX() > GWINDOW_WIDTH - BALL_SIZE || ball.getX() < 0) {
    game.vx = -1 * game.vx;
  }
  if (ball.getY() < 0) {
    game.vy = -1 * game.vy;
  }
}

/* Helper: checkBallCollision(game)
 * Checks for collision between the ball and the game objects.
 * If a collision is detected, the ball's velocity is updated accordingly.
 */
function checkBallCollision(game) {
  let ball = game.ball;
  let collider = getCollidingObject(game.gw, ball);
  if (collider && collider !== ball) {
    if (collider === game.paddle) {
      game.paddleHitCount += 1;
      let collideSide = getCollideSide(ball, collider);
      let speedMultiplier = Math.min(
        1 + game.paddleHitCount / 100,
        MAX_SPEED_MULTIPLIER,
      );
      switch (collideSide) {
        case "top":
          game.vy = -1 * game.vy * speedMultiplier;
          ball.setLocation(ball.getX(), game.paddle.getY() - BALL_SIZE);
          break;
        case "bottom":
          game.vy = -1 * game.vy * speedMultiplier;
          ball.setLocation(
            ball.getX(),
            game.paddle.getY() + game.paddle.getHeight(),
          );
          break;
        case "left":
          game.vx = -1 * game.vx * speedMultiplier;
          ball.setLocation(game.paddle.getX() - BALL_SIZE, ball.getY());
          break;
        case "right":
          game.vx = -1 * game.vx * speedMultiplier;
          ball.setLocation(
            game.paddle.getX() + game.paddle.getWidth(),
            ball.getY(),
          );
          break;
      }
    } else if (game.bricks.includes(collider)) {
      game.gw.remove(collider);
      game.score += getPointsForCollision(collider);
      game.gw.remove(game.scoreBoard);
      game.scoreBoard = displayScoreBoard(game.score);
      game.gw.add(game.scoreBoard);
      game.remainingBricks -= 1;
      // all bricks cleared
      if (game.remainingBricks === 0) {
        game.gameState = GAME_STATES.WON;
        game.msg = displayGameMsg(
          "You win! Balls remaining: " + game.remainingBalls,
        );
        game.gw.add(game.msg);
        //clean up
        game.gw.remove(ball);
        clearInterval(game.timer);
      } else if (collider !== game.scoreBoard) {
        game.vy = -1 * game.vy;
      }
    }
  }
}

/* Helper: checkBallDrop(game) */
function checkBallDrop(game) {
  let ball = game.ball;
  if (ball.getY() + BALL_SIZE >= game.gw.getHeight()) {
    game.remainingBalls -= 1;
    if (game.remainingBalls === 0) {
      game.gameState = GAME_STATES.LOST;
      game.msg = displayGameMsg(
        "Game over! Bricks remaining: " + game.remainingBricks,
      );
      game.gw.add(game.msg);
      //clean up
      game.gw.remove(ball);
      clearInterval(game.timer);
    } else {
      ball.setLocation(
        (game.gw.getWidth() - BALL_SIZE) / 2,
        (game.gw.getHeight() - BALL_SIZE) / 2,
      );
      game.gameState = GAME_STATES.WAITING;
      clearInterval(game.timer);
      game.vy = 0;
      game.vx = 0;
    }
  }
}

/* Helper: drawBricks()
 * Creates and returns an array of brick rectangles arranged in a grid at the top of the graphics window.
 * Bricks are drawn in N_COLS columns and N_ROWS rows, with alternating colors from BRICK_COLORS.
 * Each brick is filled and positioned with specified separation.
 */
function drawBricks() {
  let bricks = [];
  for (let i = 0; i < N_COLS; i++) {
    for (let j = 0; j < N_ROWS; j++) {
      let brick = GRect(0, 0, BRICK_WIDTH, BRICK_HEIGHT);
      brick.setLocation(
        BRICK_SEP + i * (BRICK_WIDTH + BRICK_SEP),
        TOP_FRACTION * GWINDOW_HEIGHT + j * (BRICK_HEIGHT + BRICK_SEP),
      );
      let color = BRICK_COLORS[Math.floor((j / 2) % 5)];
      brick.setFilled(true);
      brick.setColor(color);
      bricks.push(brick);
    }
  }
  return bricks;
}

/* Helper: drawPaddle()
 * Creates and configures a rectangular paddle graphic for a game window.
 */
function drawPaddle() {
  let paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT);
  paddle.setLocation((GWINDOW_WIDTH - PADDLE_WIDTH) / 2, PADDLE_Y);
  paddle.setFilled(true);
  paddle.setColor("Black");
  return paddle;
}

/* Helper: drawBall()
 * Creates and returns a filled oval representing a ball, centered in the graphics window.
 */
function drawBall() {
  let x0 = (GWINDOW_WIDTH - BALL_SIZE) / 2;
  let y0 = (GWINDOW_HEIGHT - BALL_SIZE) / 2;
  let ball = GOval(x0, y0, BALL_SIZE, BALL_SIZE);
  ball.setFilled(true);
  return ball;
}

/* Helper: displayScoreBoard(score)
 * Creates and returns a graphical label displaying the current score.
 */
function displayScoreBoard(score) {
  let scoreBoard = GLabel("Score: " + score.toString(), 5, 15);
  return scoreBoard;
}

/* Helper: getCollidingObject(tw, ball)
 * Checks the four corners of the ball for collisions with elements in the game world.
 * Returns the first colliding element found, or null if no collision.
 */
function getCollidingObject(gw, ball) {
  let corners = [
    [ball.getX(), ball.getY()],
    [ball.getX() + BALL_SIZE, ball.getY()],
    [ball.getX(), ball.getY() + BALL_SIZE],
    [ball.getX() + BALL_SIZE, ball.getY() + BALL_SIZE],
  ];

  let collider = null;

  for (let i = 0; i < 4; i++) {
    collider = gw.getElementAt(corners[i][0], corners[i][1]);
    if (collider == null) {
      continue;
    } else {
      return collider;
    }
  }
  return collider;
}

/* Helper: displayGameMsg(msg);
 * Displays a centered message label in the game window.
 * */

function displayGameMsg(msg) {
  let label = GLabel(msg);
  let x = (GWINDOW_WIDTH - label.getWidth()) / 2;
  let y = (GWINDOW_HEIGHT - label.getHeight()) / 2 - 50;
  label.setLocation(x, y);

  return label;
}

/* Helper: getCollideSide(ball, collider);
 * Determines the side of the collider that the ball has collided with based on overlap distances.
 */

function getCollideSide(ball, collider) {
  // Get ball bounds
  let ballLeft = ball.getX();
  let ballRight = ball.getX() + BALL_SIZE;
  let ballTop = ball.getY();
  let ballBottom = ball.getY() + BALL_SIZE;

  // Paddle bounds
  let colliderLeft = collider.getX(); // Assuming paddle has getX(), getY(), getWidth(), etc.
  let colliderRight = colliderLeft + collider.getWidth();
  let colliderTop = collider.getY();
  let colliderBottom = colliderTop + collider.getHeight();

  // Calculate overlap distances (positive = overlap amount)
  let overlapLeft = ballRight - colliderLeft;
  let overlapRight = colliderRight - ballLeft;
  let overlapTop = ballBottom - colliderTop;
  let overlapBottom = colliderBottom - ballTop;

  // Find the smallest overlap to determine hit side
  let m = Math.min(overlapLeft, overlapRight, overlapTop, overlapBottom);
  if (m === overlapTop) {
    return "top";
  } else if (m === overlapBottom) {
    return "bottom";
  } else if (m === overlapLeft) {
    return "left";
  } else if (m === overlapRight) {
    return "right";
  }
}

/* Helper: getPointsForCollision(collider)
 * Calculates points awarded for colliding with a brick based on its vertical position.
 * Higher rows (closer to the top) yield more points according to the POINTS_BY_ROW.
 */

function getPointsForCollision(collider) {
  let points =
    POINTS_BY_ROW[
      Math.floor(
        (collider.getY() - TOP_FRACTION * GWINDOW_HEIGHT) /
          (BRICK_HEIGHT + BRICK_SEP) /
          2,
      )
    ];
  return points;
}
