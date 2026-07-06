// habitos-frontend/src/apiFetch.js

const API_URL = import.meta.env.VITE_API_URL

async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('token')

    const headers = {
        'Content-Type': 'application/json',
        ...(token && {'Authorization': `Bearer ${token}`}),
        ...options.headers
    }

    const response = await fetch(url, {
        ...options,
        headers
    })

    if (response.status === 401) {
        localStorage.removeItem('token')
    }

    return response
}

export default apiFetch