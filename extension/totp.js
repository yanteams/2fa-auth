/**
 * A lightweight TOTP implementation using Web Crypto API
 */

// Base32 decoding
function base32ToBuffer(base32) {
  const base32chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
  base32 = base32.replace(/=+$/, '').toUpperCase();
  let bits = '';
  for (let i = 0; i < base32.length; i++) {
    let val = base32chars.indexOf(base32.charAt(i));
    if (val === -1) throw new Error("Invalid base32 character in key");
    bits += val.toString(2).padStart(5, '0');
  }
  let bytes = [];
  for (let i = 0; i + 8 <= bits.length; i += 8) {
    bytes.push(parseInt(bits.substr(i, 8), 2));
  }
  return new Uint8Array(bytes).buffer;
}

// Convert an integer to an 8-byte array (Counter)
function intToBuffer(num) {
  const buffer = new ArrayBuffer(8);
  const view = new DataView(buffer);
  view.setUint32(0, Math.floor(num / Math.pow(2, 32)));
  view.setUint32(4, num & 0xFFFFFFFF);
  return buffer;
}

// Generate TOTP
async function generateTOTP(secret, period = 30, digits = 6) {
  try {
    const keyBuffer = base32ToBuffer(secret);
    const key = await crypto.subtle.importKey(
      'raw',
      keyBuffer,
      { name: 'HMAC', hash: 'SHA-1' },
      false,
      ['sign']
    );

    const counter = Math.floor(Date.now() / 1000 / period);
    const counterBuffer = intToBuffer(counter);

    const signature = await crypto.subtle.sign('HMAC', key, counterBuffer);
    const hmacResult = new Uint8Array(signature);

    const offset = hmacResult[hmacResult.length - 1] & 0x0f;
    const code = (
      ((hmacResult[offset] & 0x7f) << 24) |
      ((hmacResult[offset + 1] & 0xff) << 16) |
      ((hmacResult[offset + 2] & 0xff) << 8) |
      (hmacResult[offset + 3] & 0xff)
    ) % Math.pow(10, digits);

    return code.toString().padStart(digits, '0');
  } catch (err) {
    console.error("TOTP Error:", err);
    return "ERROR";
  }
}

// Calculate remaining time
function getRemainingTime(period = 30) {
  return period - (Math.floor(Date.now() / 1000) % period);
}

window.generateTOTP = generateTOTP;
window.getRemainingTime = getRemainingTime;
