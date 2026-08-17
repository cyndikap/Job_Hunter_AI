export const getApiBaseUrl = () => {
  const envValue = import.meta.env.VITE_API_BASE_URL

  if (typeof envValue === 'string' && envValue.trim()) {
    return envValue.trim().replace(/\/+$/, '')
  }

  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location

    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return `${protocol}//${hostname}:8000`
    }

    return ''
  }

  return ''
}

export const buildApiUrl = (path) => {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  const baseUrl = getApiBaseUrl()

  if (!baseUrl) {
    return normalizedPath
  }

  return `${baseUrl}${normalizedPath}`
}

export const getAuthToken = () => {
  if (typeof window === 'undefined') {
    return ''
  }

  return localStorage.getItem('jobhunter_token') || ''
}

export const setAuthToken = (token) => {
  if (typeof window === 'undefined') {
    return
  }

  if (token) {
    localStorage.setItem('jobhunter_token', token)
    return
  }

  localStorage.removeItem('jobhunter_token')
}

export const apiFetch = async (path, options = {}) => {
  const token = getAuthToken()
  const response = await fetch(buildApiUrl(path), {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  })

  return response
}
