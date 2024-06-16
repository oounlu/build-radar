// Get Stripe publishable key
fetch("/config")
.then((result) => { return result.json(); })
.then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // new
    // Event handler
    document.querySelector("#payBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session")
    .then((result) => { return result.json(); })
    .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
        console.log(res);
    });
    });
});




// Function to switch the theme and save the preference
function switchTheme(themeName) {
    // Apply theme to the body or other elements
    document.body.className = themeName;
    // Save the preference to Local Storage
    localStorage.setItem('themePreference', themeName);
}

// Function to load the theme preference when the app starts
function loadThemePreference() {
    const themePreference = localStorage.getItem('themePreference');
    if (themePreference) {
        document.body.className = themePreference;
    }
}

// Call loadThemePreference when the application starts
document.addEventListener('DOMContentLoaded', loadThemePreference);

// Event listener for theme switch
// Assuming you have buttons with data-theme attributes
document.querySelectorAll('[data-theme]').forEach(button => {
    button.addEventListener('click', function() {
        switchTheme(this.dataset.theme);
    });
});