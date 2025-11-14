/**
 * File: match-the-flag.js
 * -----------------------
 * Defines the controller for the MatchTheFlag application.
 */
"use strict";

function BootstrapMatchTheFlag() {

   /*
    * Function: shuffle
    * -----------------
    * Generically shuffles the supplied array so
    * that any single permutation of the elements
    * is equally likely.
    */
   function shuffle(array) {
      for (let lh = 0; lh < array.length; lh++) {
         let rh = lh + Math.floor(Math.random() * (array.length - lh));
         let temp = array[rh];
         array[rh] = array[lh];
         array[lh] = temp;
      }    
   }
}

/* Execute the above function when the DOM tree is fully loaded. */
document.addEventListener("DOMContentLoaded", BootstrapMatchTheFlag);
