document.getElementById('add-destination').addEventListener('click', function () {
    const destinationsContainer = document.getElementById('destinations-container');
    const destinationDiv = document.createElement('div');
    destinationDiv.classList.add('destination');
    destinationDiv.innerHTML = `
        <input type="text" class="destination-name" name="destination" placeholder="Destination Name" required>
        <input type="text" class="activities" name="activities" placeholder="Activities (comma separated)">
        <button type="button" class="remove-destination"><i class="fas fa-times"></i></button>
    `;
    destinationsContainer.appendChild(destinationDiv);

    // Add event listener to the remove button
    destinationDiv.querySelector('.remove-destination').addEventListener('click', function () {
        destinationsContainer.removeChild(destinationDiv);
    });
});

document.querySelectorAll('.remove-destination').forEach(function (button) {
    button.addEventListener('click', function () {
        const destinationDiv = button.closest('.destination');
        destinationDiv.parentElement.removeChild(destinationDiv);
    });
});

document.getElementById('edit-itinerary-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const id = document.getElementById('itinerary-id').value;
    const name = document.getElementById('itinerary-name').value;
    const destinations = [];

    document.querySelectorAll('.destination').forEach(function (destination) {
        const destinationName = destination.querySelector('.destination-name').value;
        const activities = destination.querySelector('.activities').value.split(',').map(activity => activity.trim());
        destinations.push({ name: destinationName, activities: activities });
    });

    const response = await fetch('/edit_itinerary/' + id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, destinations: destinations })
    });

    if (response.ok) {
        window.location.href = '/';
    } else {
        console.error('Failed to edit itinerary');
    }
});
