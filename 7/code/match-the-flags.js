/**
 * File: match-the-flag.js
 * -----------------------
 * Defines the controller for the MatchTheFlag application.
 */
"use strict";

function BootstrapMatchTheFlag() {
  let revealedFlagIds = [];
  let matchedFlagsIds = [];
  let boardDiv = document.getElementById("board");
  let msgDiv = document.getElementById("message");

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

  // initialize the flag array
  function initFlags() {
    let flags = [];
    for (const country of COUNTRIES) {
      flags.push(country);
      flags.push(country);
    }
    shuffle(flags);
    return flags;
  }

  // creating flags in the div
  function createFlags() {
    let flags = initFlags();
    for (let i = 0; i < flags.length; i++) {
      let flagNode = document.createElement("img");
      let flag = flags[i];
      flagNode.setAttribute("src", COVER_IMAGE);
      flagNode.setAttribute("data-country-name", flag);
      flagNode.setAttribute(
        "data-country-image",
        "images/" + flag.toLowerCase() + ".png",
      );
      flagNode.id = "flag-" + i;
      boardDiv.appendChild(flagNode);
      flagNode.addEventListener("click", handleImgClick);
    }
  }

  // handling mouse click events on img nodes
  function handleImgClick(e) {
    let node = e.currentTarget;
    let currentImg = node.getAttribute("src");
    let flagImg = node.getAttribute("data-country-image");

    if (revealedFlagIds.length < 2) {
      if (currentImg === COVER_IMAGE) {
        node.setAttribute("src", flagImg);
        revealedFlagIds.push(node.id);
      } else if (currentImg !== MATCHED_IMAGE) {
        // then this must be a revealed country flag -> COVER_IMAGE
        node.setAttribute("src", COVER_IMAGE);
        let index = revealedFlagIds.indexOf(node.id);
        revealedFlagIds.splice(index, 1);
      }
      if (revealedFlagIds.length == 2) {
        setTimeout(handleFlagMatch, DELAY);
      }
    }
  }

  function handleFlagMatch() {
    let firstFlag = document.getElementById(revealedFlagIds[0]);
    let secondFlag = document.getElementById(revealedFlagIds[1]);
    if (
      firstFlag.getAttribute("data-country-image") ===
      secondFlag.getAttribute("data-country-image")
    ) {
      firstFlag.setAttribute("src", MATCHED_IMAGE);
      secondFlag.setAttribute("src", MATCHED_IMAGE);
      matchedFlagsIds.push([firstFlag.id, secondFlag.id]);
      if (matchedFlagsIds.length === NUM_COUNTRIES) {
        updateMessage("All flags are matched!");
      } else {
        updateMessage(
          firstFlag.getAttribute("data-country-name") + " flags are matched!",
        );
      }
    } else {
      firstFlag.setAttribute("src", COVER_IMAGE);
      secondFlag.setAttribute("src", COVER_IMAGE);
    }
    revealedFlagIds = [];
  }

  // HELPER: update the message div
  function updateMessage(msg) {
    let textNode = document.createTextNode(msg);
    while (msgDiv.childNodes.length > 0) {
      msgDiv.removeChild(msgDiv.lastChild);
    }
    msgDiv.appendChild(textNode);
  }

  // create the flags and start the game
  createFlags();
}

/* Execute the above function when the DOM tree is fully loaded. */
document.addEventListener("DOMContentLoaded", BootstrapMatchTheFlag);
