document.getElementById('logout-button').addEventListener('click', function() {
    document.getElementById('logout-modal').style.display = 'block';
});

document.getElementById('close-button').addEventListener('click', function() {
    document.getElementById('logout-modal').style.display = 'none';
});

document.getElementById('confirm-logout').addEventListener('click', function() {
    // Redirect to logout URL
    window.location.href = 'your-logout-url';
});
