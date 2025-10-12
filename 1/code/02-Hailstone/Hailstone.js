/*
 * File: Hailstone.js
 * ------------------
 * This program displays the Hailstone sequence for a number.
 */
"use strict";

function TestHailstone() {
  console.log(
    "Use this expression evaluator to ensure your hailstone implementation works.",
  );
  evaluateExpressions();
}

/*
 * Function: hailstone
 * -------------------
 * Accepts the supplied number and prints the sequence of numbers that lead the original
 * number down to 1 (along with information about how the intermediate numbers were computed).
 */
function hailstone(n) {
  let msg = "";
  let step = 0;
  while (n != 1) {
    if (n % 2 == 0) {
      n = n / 2;
      msg += n * 2 + " is even, so I take half: " + n + "<br />";
      step++;
    } else {
      n = n * 3 + 1;
      msg += (n - 1) / 3 + " is odd, so I make 3n+ 1: " + n + "<br />";
      step++;
    }
  }
  msg += "The process took " + step + " steps to reach 1.";
  return msg;
}
