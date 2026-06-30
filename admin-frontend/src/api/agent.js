const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

function getToken() {
  return localStorage.getItem('community_access_token') || ''
}

async function refreshToken() {
  const refresh = localStorage.getItem('community_refresh_token')
  if (!refresh) return null
  try {
    const res = await fetch(`${API_BASE}/community/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refresh }),
    })
    if (!res.ok) return null
    const data = await res.json()
    localStorage.setItem('community_access_token', data.access_token)
    if (data.refresh_token) {
      localStorage.setItem('community_refresh_token', data.refresh_token)
    }
    return data.access_token
  } catch {
    return null
  }
}

async function doFetch(messages, token) {
  return fetch(`${API_BASE}/community/agent/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ messages }),
  })
}

export async function* streamAgentChat(messages) {
  let token = getToken()
  let res = await doFetch(messages, token)

  if (res.status === 401 || res.status === 403) {
    const newToken = await refreshToken()
    if (newToken) {
      token = newToken
      res = await doFetch(messages, token)
    }
  }

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          yield JSON.parse(line.slice(6))
        } catch {
          // skip malformed
        }
      }
    }
  }
}
