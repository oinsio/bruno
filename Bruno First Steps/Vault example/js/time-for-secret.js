/*
  Functions to check if it is time to get secrets from a secret manager.
*/
const intervalToReGetSecrets = 1;  // Interval in minutes to re-get secrets

/**
 * Function to check if it is time to get secrets from a secret manager.
 * @param arr - The array to check for empty strings.
 * @param time - The time to check if enough time has passed from now.
 * @returns {boolean} - True if it is time to get secrets, false otherwise.
 */
function isTimeToGetSecret(arr, time) {
    // Check if the array has an empty string
    if (hasEmptyString(arr)) return true;
    // Check if enough time has passed from now
    return isEnoughTimePassedFromNow(time, intervalToReGetSecrets);
}

/**
 * Function to check if the array has an empty string.
 * @param arr - The array to check for empty strings.
 * @returns {boolean} - True if the array has an empty string, false otherwise.
 */
function hasEmptyString(arr) {
    // Check each string in the array
    for (let str of arr) {
        // If the string is empty, return true
        if (!str) return true;
    }
    // If no empty string is found, return false
    return false;
}

/**
 * Function to check if enough time has passed from now.
 * @param time - The time to check if enough time has passed from now.
 * @param minutes - The number of minutes to check.
 * @returns {boolean} - True if enough time has passed, false otherwise.
 */
function isEnoughTimePassedFromNow(time, minutes) {
    // Get the current time in milliseconds
    const now = Date.now();
    // Get the time in milliseconds from the time parameter
    const timeInMs = new Date(time).getTime();
    // Calculate the difference in minutes
    const diffInMinutes = (now - timeInMs) / (1000 * 60);
    // Return true if the difference is greater than the minutes parameter
    return diffInMinutes >= minutes;
}

module.exports = { isTimeToGetSecret };
