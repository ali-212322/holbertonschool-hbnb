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
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaceDetails(data);
        } else {
            alert('Failed to fetch place details: ' + response.statusText);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    container.innerHTML = '';

    const info = document.createElement('div');
    info.className = 'place-info';
    info.innerHTML = `
        <h2>${place.name}</h2>
        <p><strong>Price:</strong> $${place.price}</p>
        <p><strong>Description:</strong> ${place.description || ''}</p>
        <p><strong>Amenities:</strong> ${place.amenities?.join(', ') || 'None'}</p>
    `;
    container.appendChild(info);

    const reviewsSection = document.createElement('section');
    reviewsSection.className = 'reviews';
    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('article');
            reviewCard.className = 'review-card';
            reviewCard.innerHTML = `
                <p>${review.comment}</p>
                <p><strong>User:</strong> ${review.user_name}</p>
                <p><strong>Rating:</strong> ${review.rating}</p>
            `;
            reviewsSection.appendChild(reviewCard);
        });
    } else {
        reviewsSection.innerHTML = '<p>No reviews yet.</p>';
    }
    container.appendChild(reviewsSection);
}

function checkAuthentication(placeId) {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        addReviewSection.style.display = 'none';
        loginLink.style.display = 'block';
    } else {
        addReviewSection.style.display = 'block';
        loginLink.style.display = 'none';
        fetchPlaceDetails(token, placeId);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    checkAuthentication(placeId);
});
