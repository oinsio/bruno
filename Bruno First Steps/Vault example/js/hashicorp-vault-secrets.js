/*
  Functions to get secret from Vault via HTTP.
  Bruno Safe Mode can be used.
*/
const axios = require("axios");

/**
 * Main function to get secret from Vault and extract a specific value.
 * @param {string} vaultUrl - The URL for the request.
 * @param {string} xVaultToken - The authentication token.
 * @param {string} secretName - The name of the secret to extract.
 * @returns {Promise<string|null>} - The secret value or null in case of an error.
 */
async function getVaultSecretAndExtract(vaultUrl, xVaultToken, secretName) {
  const data = await getVaultSecret(vaultUrl, xVaultToken);  // Get data from Vault
  if (data) {
    return extractSecretFromVaultResponse(data, secretName);  // Extract the secret
  }
  return null;
}

/**
 * Function to get secret from Vault via HTTP.
 * @param {string} vaultUrl - The URL for the request.
 * @param {string} xVaultToken - The authentication token.
 * @returns {Promise<Object|null>} - The secret data or null in case of an error.
 */
async function getVaultSecret(vaultUrl, xVaultToken) {
  let data = null;
  try {
    const response = await axios.get(vaultUrl, {
      headers: {
        'X-Vault-Token': xVaultToken,
      },
    });
    console.log('getVaultSecret response:', response.data);
    data = response.data;  // Save the response data
  } catch (error) {
    console.error('getVaultSecret error:', error);
  }
  return data;  // Return the data or null in case of an error
}

/**
 * Function to extract a secret from Vault response data.
 * @param {Object} data - The response data from Vault containing secrets.
 * @param {string} secretName - The name of the secret to extract.
 * @returns {string|null} - The secret value or null if not found.
 */
function extractSecretFromVaultResponse(data, secretName) {
  try {
    const secretValue = data.data.data[secretName];
    if (secretValue !== undefined) {
      return secretValue;
    } else {
      throw new Error(`Secret '${secretName}' is not found.`);
    }
  } catch (error) {
    console.error('extractSecretFromVaultResponse error:', error.message);
    return null;
  }
}

module.exports = { getVaultSecretAndExtract };
