/**
 * File: Luhn.js
 * -------------
 * This program exports the isValid predicate method, which returns true
 * if and only if the number supplied as an argument could be a valid credit
 * card number according to Luhn's algorithm.
 */

"use strict";
const NUMBERS = [4460246643298726, 4460246643298627, 4460246643298727];

/* Main program */
function TestLuhnAlgorithm() {
  for (let i = 0; i < NUMBERS.length; i++) {
    console.log(
      "Account number " +
        NUMBERS[i] +
        " -> " +
        (isValid(NUMBERS[i]) ? "valid" : "invalid"),
    );
  }
}

/**
 * Function: isValid
 * -----------------
 * Returns true if and only if the supplied number
 * meets the requirements imposed by Luhn's algorithm.
 */
function isValid(number) {
  // replace the following line with the code that properly computes whether
  // the supplied number is a valid credit card number according to Luhn's algorithm.
  let sum = digitSum(number);
  if (sum % 10 == 0) {
    return true;
  } else {
    return false;
  }
}

function digitSum(n) {
  let sum = 0;
  let oddDigit = true;
  while (n > 0) {
    if (oddDigit) {
      sum += n % 10;
    } else {
      n % 10 >= 5 ? (sum += (n % 10) * 2 - 9) : (sum += (n % 10) * 2);
    }
    n = Math.floor(n / 10);
    oddDigit = !oddDigit;
  }
  return sum;
}
