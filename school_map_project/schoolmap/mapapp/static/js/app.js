// Main application initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded, initializing components...');
    
    // Apply theme on page load
    // Priority: 1. data-theme attribute (from server), 2. localStorage
    const htmlElement = document.documentElement;
    const serverTheme = htmlElement.getAttribute('data-theme');
    const savedTheme = localStorage.getItem('theme');
    
    const themeToApply = serverTheme || savedTheme || 'light';
    console.log('=== THEME DEBUG ===');
    console.log('Server theme (data-theme):', serverTheme);
    console.log('LocalStorage theme:', savedTheme);
    console.log('Theme to apply:', themeToApply);
    console.log('==================');
    applyTheme(themeToApply);
    
    // Apply saved font size
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        applyFontSize(savedFontSize);
    }
    
    // Handle logo image fallback
    const logoImage = document.getElementById('logoImage');
    if (logoImage) {
        logoImage.onerror = function() {
            this.onerror = null;
            this.src = this.getAttribute('data-fallback');
        };
    }
    
    // Initialize all components
    initializeApp();
});

// Apply theme function
function applyTheme(theme) {
    console.log('applyTheme called with:', theme);
    const root = document.documentElement;
    const body = document.body;
    
    if (theme === 'dark') {
        root.style.setProperty('--bg-color', '#1e293b', 'important');
        root.style.setProperty('--text-color', '#f8fafc', 'important');
        root.style.setProperty('--card-bg', '#334155', 'important');
        root.style.setProperty('--primary-color', '#a78bfa', 'important');
        root.style.setProperty('--accent-color', '#a78bfa', 'important');
        root.style.backgroundColor = '#1e293b';
        root.style.color = '#f8fafc';
        if (body) {
            body.style.backgroundColor = '#1e293b';
            body.style.color = '#f8fafc';
        }
        console.log('Dark theme applied');
    } else if (theme === 'light') {
        root.style.setProperty('--bg-color', '#fff0f5', 'important');
        root.style.setProperty('--text-color', '#1e293b', 'important');
        root.style.setProperty('--card-bg', '#ffffff', 'important');
        root.style.setProperty('--primary-color', '#ff6b9e', 'important');
        root.style.setProperty('--accent-color', '#ff6b9e', 'important');
        root.style.backgroundColor = '#fff0f5';
        root.style.color = '#1e293b';
        if (body) {
            body.style.backgroundColor = '#fff0f5';
            body.style.color = '#1e293b';
        }
        console.log('Light theme applied');
    } else if (theme === 'sunset') {
        // Sunset theme - warm orange, amber, and coral tones
        root.style.setProperty('--bg-color', '#fff7ed', 'important');  // Orange-50 (very light orange)
        root.style.setProperty('--text-color', '#7c2d12', 'important');  // Orange-900 (dark orange-brown)
        root.style.setProperty('--card-bg', '#ffedd5', 'important');  // Orange-100 (light peach)
        root.style.setProperty('--primary-color', '#f97316', 'important');  // Orange-500 (vibrant orange)
        root.style.setProperty('--accent-color', '#fb923c', 'important');  // Orange-400 (bright orange)
        root.style.setProperty('--secondary-color', '#fdba74', 'important');  // Orange-300 (light orange)
        root.style.backgroundColor = '#fff7ed';
        root.style.color = '#7c2d12';
        if (body) {
            body.style.backgroundColor = '#fff7ed';
            body.style.color = '#7c2d12';
        }
        console.log('Sunset theme applied');
    }
    
    root.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    console.log('Theme applied - Background should be:', root.style.backgroundColor);
}

// Apply font size function
function applyFontSize(size) {
    const validSizes = ['small', 'medium', 'large'];
    if (!validSizes.includes(size)) return;
    
    let fontSize;
    switch(size) {
        case 'small':
            fontSize = '14px';
            break;
        case 'medium':
            fontSize = '16px';
            break;
        case 'large':
            fontSize = '18px';
            break;
    }
    
    document.documentElement.style.setProperty('--font-size', fontSize);
    localStorage.setItem('fontSize', size);
}

// Main initialization function
function initializeApp() {
    console.log('Initializing application components...');
    
    try {
        console.log('Initializing search...');
        if (typeof initSearch === 'function') {
            initSearch();
        }
        
        console.log('Initializing image upload...');
        if (typeof initImageUpload === 'function') {
            initImageUpload();
        }
        
        console.log('Initializing user dropdown...');
        if (typeof initUserDropdown === 'function') {
            initUserDropdown();
        }
        
        console.log('Initializing notification dropdown...');
        if (typeof initNotificationDropdown === 'function') {
            initNotificationDropdown();
        }
        
        console.log('Initializing map...');
        if (typeof initMap === 'function') {
            initMap();
        }
        
        console.log('All components initialized successfully');
    } catch (error) {
        console.error('Error initializing components:', error);
    }
}
