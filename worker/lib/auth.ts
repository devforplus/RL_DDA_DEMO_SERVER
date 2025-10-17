/**
 * 인증 토큰 관리
 * Python의 ingest_token.py 이식
 */

interface TokenPayload {
  sid: string;
  exp: number;
}

/**
 * HMAC-SHA256 기반 토큰 생성
 */
export async function signIngestToken(
  secret: string,
  sessionId: string,
  ttlSeconds: number = 3600
): Promise<string> {
  const payload: TokenPayload = {
    sid: sessionId,
    exp: Math.floor(Date.now() / 1000) + ttlSeconds,
  };

  const body = new TextEncoder().encode(JSON.stringify(payload));
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signature = await crypto.subtle.sign('HMAC', key, body);
  const combined = new Uint8Array(body.length + 1 + signature.byteLength);
  combined.set(body, 0);
  combined.set([46], body.length); // '.' character
  combined.set(new Uint8Array(signature), body.length + 1);

  // Base64 URL-safe encoding without padding
  return btoa(String.fromCharCode(...combined))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

/**
 * HMAC-SHA256 기반 토큰 검증
 */
export async function verifyIngestToken(
  secret: string,
  token: string
): Promise<TokenPayload> {
  // Add padding if needed
  const padded = token + '='.repeat((4 - (token.length % 4)) % 4);
  const decoded = atob(padded.replace(/-/g, '+').replace(/_/g, '/'));
  
  const data = new Uint8Array(decoded.length);
  for (let i = 0; i < decoded.length; i++) {
    data[i] = decoded.charCodeAt(i);
  }

  // Find the '.' separator
  let separatorIndex = -1;
  for (let i = 0; i < data.length; i++) {
    if (data[i] === 46) {
      separatorIndex = i;
      break;
    }
  }

  if (separatorIndex === -1) {
    throw new Error('Invalid token format');
  }

  const body = data.slice(0, separatorIndex);
  const signature = data.slice(separatorIndex + 1);

  // Verify signature
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['verify']
  );

  const valid = await crypto.subtle.verify('HMAC', key, signature, body);
  if (!valid) {
    throw new Error('Invalid signature');
  }

  // Parse payload
  const payloadText = new TextDecoder().decode(body);
  const payload: TokenPayload = JSON.parse(payloadText);

  // Check expiration
  if (payload.exp < Math.floor(Date.now() / 1000)) {
    throw new Error('Token expired');
  }

  return payload;
}

/**
 * Authorization 헤더에서 Bearer 토큰 추출
 */
export function extractBearerToken(authorization: string | null): string | null {
  if (!authorization) return null;
  
  const parts = authorization.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    return null;
  }
  
  return parts[1];
}

