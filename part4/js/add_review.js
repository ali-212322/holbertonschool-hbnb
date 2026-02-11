function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function submitReview(token, placeId, reviewText, reviewRating) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                comment: reviewText,
                rating: reviewRating
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-form').reset();
        } else {
            const data = await response.json();
            alert('Failed to submit review: ' + (data.message || response.statusText));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value.trim();
            const reviewRating = parseInt(document.getElementById('review-rating').value);

            if (!reviewText || !reviewRating) {
                alert('Please fill in all fields.');
                return;
            }

            await submitReview(token, placeId, reviewText, reviewRating);
        });
    }
});
