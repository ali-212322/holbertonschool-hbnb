function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getBaseUrl() {
    const { origin } = window.location;
    if (origin.includes('github.dev') || origin.includes('app.github.dev')) {
        return origin.replace(/-(3000|5500|8080)\./, '-5000.');
    }
    return 'http://127.0.0.1:5000';
}

// دالة لجلب اسم المكان لعرضه في العنوان (تحسين UX)
async function fetchPlaceName(token, placeId) {
    const API_URL = `${getBaseUrl()}/api/v1/places/${placeId}`;
    try {
        const response = await fetch(API_URL, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const data = await response.json();
            const header = document.getElementById('place-name-header');
            if (header) header.textContent = `Reviewing: ${data.title || data.name}`;
        }
    } catch (error) {
        console.error('Error fetching place name:', error);
    }
}

async function submitReview(token, placeId, reviewText, reviewRating) {
    const API_URL = `${getBaseUrl()}/api/v1/reviews/`;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(reviewRating)
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const data = await response.json().catch(() => ({}));
            alert('Failed: ' + (data.msg || data.message || 'Error occurred'));
        }
    } catch (error) {
        alert('Connection error.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html'; // حماية الصفحة
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const placeId = params.get('id');
    const reviewForm = document.getElementById('review-form');

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    // جلب اسم المكان ليظهر في الـ Header كما في الديزاين
    fetchPlaceName(token, placeId);

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('review-text').value;
            const rating = document.getElementById('review-rating').value;

            await submitReview(token, placeId, text, rating);
        });
    }
});
