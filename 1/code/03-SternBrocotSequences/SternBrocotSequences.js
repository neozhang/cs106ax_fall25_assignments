/*
 * File: SternBrocotSequences.js
 * -----------------------------
 * Exports a function that generates Stern-Brocot sequences for
 * arbitrary real numbers between 0 and 1.
 */

"use strict";

function TestSternBrocotSequences() {
  console.log("sbs(0.5) -> " + sbs(0.5));
  console.log("sbs(0.125) -> " + sbs(0.125));
  console.log("sbs(0.65) -> " + sbs(0.65));
  console.log("sbs(Math.E - 2) -> " + sbs(Math.E - 2));
  console.log("sbs(Math.PI - 3) -> " + sbs(Math.PI - 3));
  console.log("sbs(Math.PI - 3, 100) -> " + sbs(Math.PI - 3, 100));
  console.log("");
  console.log(
    "Now use the console to test the function for arbitrary positive numbers.",
  );
  evaluateExpressions();
}

/*
 * Function: sbs
 * -------------
 * Accepts the provided number and an optional max length and returns
 * the Stern-Brocot sequence best representing it.  We assume the supplied
 * number is between 0 and 1, and that max, if supplied, is a reasonably small
 * (in the hundreds).
 */

/*
 * Notes
 * -----
 * 1. The route string can be reversed to trace back to the original point "1/2".
 * 2. The route string can be used to find the position of a node in the tree:
 * 2.1 Depth: The length of the route string -1 -> the depth in the tree (1/2 -> depth 0; 0/1 and 1/1 -> depth -1).
 * 2.2 Offset: Think L as 0 and R as 1. LLR -> 001 (binary) -> 1 (decimal) -> 1+1=2nd item (horizontal offset).
 * 3. To compute the value of a node, it is required to find the left and right ancestor:
 * 3.1 Move from right to left on the route string.
 * 3.2 The first letter provides one ancestor (depth - 1, or remove the last letter on the route string, on the opposite direction).
 * 3.3 Move onto the next letter. If it's the same letter, skip. Move onto the next letter.
 * 3.4 For routes of all "L", use "0/1" as the Left Ancestor. For routes of all "R", use "1/1" as the Right Ancestor.
 */

const DEFAULT_MAX_LENGTH = 500;
function sbs(num, max) {
  if (max === undefined) max = DEFAULT_MAX_LENGTH; // second argument is missing? use 500 as a default
  let left = [0, 1];
  let right = [1, 1];
  let cur = [1, 2];
  let route = "";
  for (let level = 0; level < max; level++) {
    if (num == cur[0] / cur[1]) {
      return compressRoute(route);
    }
    if (num > cur[0] / cur[1]) {
      route += "R"; // move right;
      left = cur; // set new left bound
    } else {
      route += "L"; // move left;
      right = cur; // set new right bound
    }
    cur = [left[0] + right[0], left[1] + right[1]];
  }
  return compressRoute(route);
}

function compressRoute(route) {
  // LLRLRRRRRLL -> L2 R L R5 L2
  if (!route || route.length === 0) return "";

  let compressed = [];
  let count = 1;
  for (let i = 1; i <= route.length; i++) {
    if (route[i] === route[i - 1]) {
      count++;
    } else {
      if (count === 1) {
        compressed.push(route[i - 1]);
      } else {
        compressed.push(route[i - 1] + count.toString());
      }
      count = 1;
    }
  }
  return compressed.join(" ");
}
