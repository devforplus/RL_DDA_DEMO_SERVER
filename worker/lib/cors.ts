/**
 * CORS 헤더 관리
 */

export interface CorsOptions {
  origins: string[];
  originRegex?: string;
}

/**
 * CORS 헤더 생성
 */
export function getCorsHeaders(origin: string | null, options: CorsOptions): HeadersInit {
  const headers: HeadersInit = {
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };

  // Origin 검증
  if (origin) {
    let allowed = false;

    // 정확한 매칭
    if (options.origins.includes(origin)) {
      allowed = true;
    }

    // 정규식 매칭
    if (!allowed && options.originRegex) {
      try {
        const regex = new RegExp(options.originRegex);
        if (regex.test(origin)) {
          allowed = true;
        }
      } catch (e) {
        console.error('Invalid CORS origin regex:', e);
      }
    }

    if (allowed) {
      headers['Access-Control-Allow-Origin'] = origin;
    }
  }

  return headers;
}

/**
 * CORS preflight 응답 생성
 */
export function createCorsPreflightResponse(origin: string | null, options: CorsOptions): Response {
  return new Response(null, {
    status: 204,
    headers: getCorsHeaders(origin, options),
  });
}

