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
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            alert('Failed to fetch places: ' + response.statusText);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price;
        card.innerHTML = `
            <h2>${place.name}</h2>
            <p>Price per night: $${place.price}</p>
            <p>${place.description || ''}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    const priceFilter = document.getElementById('price-filter');
    priceFilter.addEventListener('change', (event) => {
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
});
