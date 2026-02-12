function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to post a review.');
        window.location.href = 'login.html';
    }
    return token;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function submitReview(token, placeId, reviewText, reviewRating) {
    /* التعديل 1: الرابط الديناميكي لبيئة Codespaces */
    let baseUrl = window.location.origin.replace('-3000', '-5000').replace('-8080', '-5000');
    if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
        baseUrl = 'http://127.0.0.1:5000';
    }
    
    // تأكد من أن المسار يطابق الـ API الخاص بك لإنشاء تقييم
    const API_URL = `${baseUrl}/api/v1/reviews/`;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            /* التعديل 2: مطابقة الحقول مع قاعدة البيانات (text بدلاً من comment)
               وإرسال الـ place_id ضمن الجسم (Body)
            */
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: reviewRating
            })
        });

        if (response.ok) {
            alert('Review submitted successfully! Returning to place details...');
            // العودة لصفحة التفاصيل لرؤية التقييم الجديد
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const data = await response.json().catch(() => ({}));
            alert('Failed to submit review: ' + (data.msg || data.message || 'Error occurred'));
        }
    } catch (error) {
        console.error('Submission Error:', error);
        alert('Connection error: Could not reach the server.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    const reviewForm = document.getElementById('review-form');

    if (!placeId) {
        alert('No place selected.');
        window.location.href = 'index.html';
        return;
    }

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value.trim();
            const reviewRating = parseInt(document.getElementById('review-rating').value);

            if (!reviewText || isNaN(reviewRating)) {
                alert('Please provide a comment and a rating.');
                return;
            }

            if (reviewRating < 1 || reviewRating > 5) {
                alert('Rating must be between 1 and 5.');
                return;
            }

            await submitReview(token, placeId, reviewText, reviewRating);
        });
    }
});
