// UI Components - Dropdowns and Notifications

// Initialize user dropdown
function initUserDropdown() {
    console.log('Initializing user dropdown...');
    
    const userDropdown = document.getElementById('userDropdown');
    const dropdownMenu = document.getElementById('dropdownMenu');
    
    console.log('User dropdown element:', userDropdown);
    console.log('Dropdown menu element:', dropdownMenu);
    
    if (!userDropdown || !dropdownMenu) {
        console.error('User dropdown elements not found:', {
            userDropdown: !!userDropdown,
            dropdownMenu: !!dropdownMenu
        });
        return;
    }
    
    console.log('User dropdown elements found, setting up event listeners...');
    
    // Hide dropdown initially (set visibility and opacity, not display)
    dropdownMenu.style.visibility = 'hidden';
    dropdownMenu.style.opacity = '0';
    dropdownMenu.style.transform = 'translateY(10px)';
    
    // Toggle dropdown on click
    userDropdown.addEventListener('click', function(e) {
        console.log('User dropdown clicked!');
        e.preventDefault();
        e.stopPropagation();
        
        // Toggle dropdown visibility
        const isHidden = dropdownMenu.style.visibility === 'hidden' || !dropdownMenu.style.visibility;
        
        if (isHidden) {
            // Show dropdown
            dropdownMenu.style.display = 'block';
            dropdownMenu.style.visibility = 'visible';
            dropdownMenu.style.opacity = '1';
            dropdownMenu.style.transform = 'translateY(0)';
        } else {
            // Hide dropdown
            dropdownMenu.style.display = 'none';
            dropdownMenu.style.visibility = 'hidden';
            dropdownMenu.style.opacity = '0';
            dropdownMenu.style.transform = 'translateY(10px)';
        }
        
        console.log('Dropdown visibility set to:', dropdownMenu.style.visibility);
        const computed = window.getComputedStyle(dropdownMenu);
        console.log('Display:', computed.display);
        console.log('Visibility:', computed.visibility);
        console.log('Opacity:', computed.opacity);
        console.log('Position:', computed.position);
        console.log('Z-Index:', computed.zIndex);
        console.log('Top:', computed.top);
        console.log('Right:', computed.right);
        console.log('Width:', computed.width);
        console.log('Height:', computed.height);
        
        // Update aria-expanded attribute
        this.setAttribute('aria-expanded', String(!isHidden));
        
        // Close other dropdowns
        document.querySelectorAll('.notification-dropdown').forEach(dropdown => {
            if (dropdown !== dropdownMenu) {
                dropdown.style.display = 'none';
            }
        });
    });
    
    // Close dropdown when clicking on a menu item
    const dropdownItems = dropdownMenu.querySelectorAll('a');
    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            dropdownMenu.style.visibility = 'hidden';
            dropdownMenu.style.opacity = '0';
            dropdownMenu.style.transform = 'translateY(10px)';
            userDropdown.setAttribute('aria-expanded', 'false');
        });
    });
    
    // Make dropdown more accessible
    userDropdown.setAttribute('aria-haspopup', 'true');
    userDropdown.setAttribute('aria-expanded', 'false');
}

// Initialize notification dropdown
function initNotificationDropdown() {
    console.log('Initializing notification dropdown...');
    
    const notificationToggle = document.getElementById('notificationToggle');
    const notificationMenu = document.getElementById('notificationMenu');
    
    console.log('Notification toggle element:', notificationToggle);
    console.log('Notification menu element:', notificationMenu);
    
    if (!notificationToggle || !notificationMenu) {
        console.error('Notification dropdown elements not found:', {
            notificationToggle: !!notificationToggle,
            notificationMenu: !!notificationMenu
        });
        return;
    }
    
    console.log('Notification dropdown elements found, setting up event listeners...');
    
    // Hide notification menu initially (set visibility and opacity, not display)
    notificationMenu.style.visibility = 'hidden';
    notificationMenu.style.opacity = '0';
    notificationMenu.style.transform = 'translateY(10px)';
    
    // Toggle notification menu on click
    notificationToggle.addEventListener('click', function(e) {
        console.log('Notification toggle clicked!');
        e.preventDefault();
        e.stopPropagation();
        
        // Toggle notification menu visibility
        const isHidden = notificationMenu.style.visibility === 'hidden' || !notificationMenu.style.visibility;
        
        if (isHidden) {
            // Show notification menu
            notificationMenu.style.display = 'block';
            notificationMenu.style.visibility = 'visible';
            notificationMenu.style.opacity = '1';
            notificationMenu.style.transform = 'translateY(0)';
        } else {
            // Hide notification menu
            notificationMenu.style.display = 'none';
            notificationMenu.style.visibility = 'hidden';
            notificationMenu.style.opacity = '0';
            notificationMenu.style.transform = 'translateY(10px)';
        }
        
        console.log('Notification menu visibility set to:', notificationMenu.style.visibility);
        
        // Close user dropdown if open
        const dropdownMenu = document.getElementById('dropdownMenu');
        if (dropdownMenu) {
            dropdownMenu.style.display = 'none';
        }
    });
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(e) {
    const dropdownMenu = document.getElementById('dropdownMenu');
    const userDropdown = document.getElementById('userDropdown');
    
    if (userDropdown && dropdownMenu) {
        if (!userDropdown.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.style.visibility = 'hidden';
            dropdownMenu.style.opacity = '0';
            dropdownMenu.style.transform = 'translateY(10px)';
            userDropdown.setAttribute('aria-expanded', 'false');
        }
    }
    
    // Handle notification dropdown
    const notificationMenu = document.getElementById('notificationMenu');
    const notificationToggle = document.getElementById('notificationToggle');
    
    if (notificationMenu && notificationToggle) {
        if (!notificationToggle.contains(e.target) && !notificationMenu.contains(e.target)) {
            notificationMenu.style.visibility = 'hidden';
            notificationMenu.style.opacity = '0';
            notificationMenu.style.transform = 'translateY(10px)';
        }
    }
});
