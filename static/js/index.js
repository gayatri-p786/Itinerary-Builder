

    document.getElementById('add-itinerary-btn').addEventListener('click', function() {
        window.location.href = "/add_itinerary";
    });

    document.querySelectorAll('.edit-itinerary-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            console.log("id:",id);
            window.location.href = `/edit_itinerary/${id}`;
        });
    });

    document.querySelectorAll('.delete-itinerary-btn').forEach(function(button) {
        button.addEventListener('click', async function() {
            const id = this.getAttribute('data-id');
            const response = await fetch(`/delete_itinerary/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Failed to delete itinerary');
            }
        });
    });