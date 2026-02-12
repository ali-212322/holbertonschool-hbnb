// دالة مساعدة لتحويل الرقم إلى نجوم ★
function getStarRating(rating) {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

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
    let baseUrl = window.location.origin.replace('-3000', '-5000').replace('-8080', '-5000');
    if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
        baseUrl = 'http://127.0.0.1:5000';
    }
    
    const API_URL = `${baseUrl}/api/v1/places/${placeId}`;

    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(API_URL, { headers });

        if (response.ok) {
            const data = await response.json();
            displayPlaceDetails(data);
        } else {
            window.location.href = 'index.html';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;
    container.innerHTML = '';

    const amenitiesList = place.amenities && place.amenities.length > 0 
        ? place.amenities.map(a => typeof a === 'object' ? a.name : a).join(', ')
        : 'None';

    // إنشاء قسم المعلومات الأساسية (مطابق لـ img_place.png)
    const infoSection = document.createElement('div');
    infoSection.className = 'card place-details-card';
    infoSection.innerHTML = `
        <h1>${place.title || place.name}</h1>
        <div class="place-meta">
            <p><strong>Host:</strong> ${place.host_name || 'Owner'}</p>
            <p><strong>Price per night:</strong> $${place.price}</p>
        </div>
        <div class="place-description">
            <p>${place.description || 'No description provided.'}</p>
        </div>
        <div class="place-amenities">
            <p><strong>Amenities:</strong> ${amenitiesList}</p>
        </div>
    `;
    container.appendChild(infoSection);

    // قسم التقييمات
    const reviewsTitle = document.createElement('h2');
    reviewsTitle.innerText = 'Reviews';
    reviewsTitle.className = 'section-title';
    container.appendChild(reviewsTitle);

    const reviewsContainer = document.createElement('div');
    reviewsContainer.className = 'reviews-list';

    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'card review-card';
            reviewCard.innerHTML = `
                <p><strong>${review.user_name || 'User'}:</strong></p>
                <p class="rating-stars">${getStarRating(review.rating)}</p>
                <p class="review-text">${review.text || review.comment}</p>
            `;
            reviewsContainer.appendChild(reviewCard);
        });
    } else {
        reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
    }
    container.appendChild(reviewsContainer);
}

document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    
    if (placeId) {
        fetchPlaceDetails(token, placeId);
        
        // إظهار قسم إضافة التقييم فقط إذا كان هناك توكن
        if (token && addReviewSection) {
            addReviewSection.style.display = 'block';
            // تحديث رابط الزر إذا كنت تستخدم صفحة منفصلة
            const submitBtn = document.getElementById('submit-review');
            if (submitBtn) {
                submitBtn.onclick = () => window.location.href = `add_review.html?id=${placeId}`;
            }
        }
    } else {
        window.location.href = 'index.html';
    }
});
