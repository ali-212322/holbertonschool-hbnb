function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (!token) {
        // التعليمات الصارمة: إعادة التوجيه للوجن إذا لم يكن مسجلاً
        window.location.href = 'login.html';
        return;
    } else {
        if (loginLink) {
            loginLink.textContent = 'Logout'; // تغيير النص ليصبح تسجيل خروج
            loginLink.href = '#';
            loginLink.addEventListener('click', () => {
                document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                window.location.reload();
            });
        }
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    let baseUrl = window.location.origin.replace('-3000', '-5000').replace('-8080', '-5000');
    if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
        baseUrl = 'http://127.0.0.1:5000';
    }
    
    const API_URL = `${baseUrl}/api/v1/places/`;

    try {
        const response = await fetch(API_URL, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else if (response.status === 401) {
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price;
        
        const displayTitle = place.title || place.name || 'No Title';
        
        // التعديل ليطابق صورة img_index.png بالضبط
        card.innerHTML = `
            <h2>${displayTitle}</h2>
            <p>Price per night: $${place.price}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', checkAuthentication);

// منطق الفلترة (كما هو في كودك فهو يعمل بشكل رائع)
document.getElementById('price-filter')?.addEventListener('change', (event) => {
    const selected = event.target.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        if (selected === 'all' || price <= parseFloat(selected)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});
