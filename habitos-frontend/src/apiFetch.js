// habitos-frontend/src/apiFetch.js

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