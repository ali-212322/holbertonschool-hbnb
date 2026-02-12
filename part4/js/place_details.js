function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    /* التعديل 1: الرابط الديناميكي لبيئة Codespaces */
    let baseUrl = window.location.origin.replace('-3000', '-5000').replace('-8080', '-5000');
    if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
        baseUrl = 'http://127.0.0.1:5000';
    }
    
    const API_URL = `${baseUrl}/api/v1/places/${placeId}`;

    try {
        const response = await fetch(API_URL, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaceDetails(data);
        } else {
            console.error('Failed to fetch place details');
            alert('Place details not found.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;
    container.innerHTML = '';

    /* التعديل 2: مواءمة المسميات (title بدلاً من name) */
    const info = document.createElement('div');
    info.className = 'place-info-section';
    
    // معالجة المرافق (Amenities) إذا كانت قائمة من الكائنات أو نصوص
    const amenitiesList = place.amenities && place.amenities.length > 0 
        ? place.amenities.map(a => typeof a === 'object' ? a.name : a).join(', ')
        : 'No amenities listed';

    info.innerHTML = `
        <h1>${place.title || place.name}</h1>
        <div class="place-meta">
            <p><strong>Host ID:</strong> ${place.owner_id || 'Unknown'}</p>
            <p><strong>Price per night:</strong> $${place.price}</p>
        </div>
        <div class="place-description">
            <h3>Description</h3>
            <p>${place.description || 'No description provided.'}</p>
        </div>
        <div class="place-amenities">
            <h3>Amenities</h3>
            <p>${amenitiesList}</p>
        </div>
    `;
    container.appendChild(info);

    /* التعديل 3: مواءمة عرض التقييمات (Reviews) */
    const reviewsHeader = document.createElement('h3');
    reviewsHeader.innerText = 'Reviews';
    container.appendChild(reviewsHeader);

    const reviewsSection = document.createElement('div');
    reviewsSection.className = 'reviews-container';

    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('article');
            reviewCard.className = 'review-card';
            // نستخدم review.text و review.rating كما حقناها في SQL
            reviewCard.innerHTML = `
                <div class="review-header">
                    <span class="user-name">User ID: ${review.user_id}</span>
                    <span class="rating">⭐ ${review.rating}/5</span>
                </div>
                <p class="review-text">"${review.text || review.comment}"</p>
            `;
            reviewsSection.appendChild(reviewCard);
        });
    } else {
        reviewsSection.innerHTML = '<p class="no-reviews">No reviews for this place yet.</p>';
    }
    container.appendChild(reviewsSection);
}

function checkAuthentication(placeId) {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const loginLink = document.getElementById('login-link');

    // جلب البيانات دائماً، ولكن التحكم في ظهور نموذج إضافة تقييم
    if (token) {
        if (addReviewSection) addReviewSection.style.display = 'block';
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaceDetails(token, placeId);
    } else {
        if (addReviewSection) addReviewSection.style.display = 'none';
        if (loginLink) loginLink.style.display = 'block';
        // حتى لو لم يسجل دخول، نحاول جلب البيانات (حسب سياسة الـ API لديك)
        fetchPlaceDetails(null, placeId);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        checkAuthentication(placeId);
    } else {
        window.location.href = 'index.html';
    }
});
