// Global variables
let searchInput, voiceSearchBtn, suggestionsDropdown, debounceTimer;

// Use the global buildings array from buildings.js
// Make sure buildings.js is loaded before this script in your HTML
const buildings = window.buildings || [];

// Utility function to escape special regex characters
function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Highlight matching text in search results
function highlightMatch(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
}

// Find matching buildings based on query
function findMatchingBuildings(query) {
    if (!query || !buildings) return [];
    query = query.toLowerCase().trim();
    return buildings.filter(building => 
        (building.name && building.name.toLowerCase().includes(query)) ||
        (building.description && building.description.toLowerCase().includes(query)) ||
        (building.category && building.category.toLowerCase().includes(query))
    );
}

// Show suggestions in dropdown
function showSuggestions(matches, query) {
    if (!suggestionsDropdown) {
        console.error('Suggestions dropdown element not found');
        return;
    }
    
    // Clear previous suggestions and reset active index
    suggestionsDropdown.innerHTML = '';
    activeSuggestionIndex = -1;
    
    if (!matches || matches.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'suggestion-item';
        noResults.textContent = 'No results found';
        noResults.style.padding = '12px 16px';
        noResults.style.color = '#666';
        noResults.style.cursor = 'default';
        suggestionsDropdown.appendChild(noResults);
        suggestionsDropdown.classList.add('show');
        return;
    }
    
    // Add new suggestions
    matches.slice(0, 5).forEach((building) => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.setAttribute('data-name', building.name);
        item.setAttribute('tabindex', '0');
        
        // Show only the building name
        item.textContent = building.name;
        
        // Handle click on suggestion
        item.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            searchInput.value = building.name;
            searchInput.focus();
            hideSuggestions();
            performSearch(building.name);
        });
        
        // Handle keyboard navigation for individual items
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                searchInput.value = building.name;
                searchInput.focus();
                hideSuggestions();
                performSearch(building.name);
            }
        });
        
        // Hover effects
        item.addEventListener('mouseenter', () => {
            const index = Array.from(suggestionsDropdown.children).indexOf(item);
            if (index !== -1) {
                activeSuggestionIndex = index;
                updateActiveSuggestion();
            }
        });
        
        suggestionsDropdown.appendChild(item);
    });
    
    // Ensure the dropdown is properly positioned
    const searchBar = searchInput.closest('.search-bar');
    if (searchBar) {
        // Position the dropdown relative to the search bar
        searchBar.style.position = 'relative';
        suggestionsDropdown.style.position = 'absolute';
        suggestionsDropdown.style.top = 'calc(100% + 5px)';
        suggestionsDropdown.style.left = '0';
        suggestionsDropdown.style.width = '100%';
    }
    
    // Show the dropdown
    suggestionsDropdown.style.display = 'block';
    suggestionsDropdown.classList.add('show');
}

// Hide suggestions dropdown
function hideSuggestions() {
    if (suggestionsDropdown) {
        suggestionsDropdown.classList.remove('show');
        suggestionsDropdown.style.display = 'none';
    }
}

// Perform search and update UI
function performSearch(query) {
    if (!query || !searchInput) return;
    
    // Trim and update input
    query = query.trim();
    searchInput.value = query;
    
    // Find matching buildings
    const matches = findMatchingBuildings(query);
    
    if (matches.length > 0) {
        const building = matches[0];
        
        // Remove any existing pin and highlight first
        if (window.removeSearchPin) {
            window.removeSearchPin();
        }
        
        // Use the positionSearchPin function which now handles zooming
        if (window.positionSearchPin) {
            window.positionSearchPin(building);
        }
        
        // Add a class to the map container to indicate a search is active
        const mapContainer = document.querySelector('.map-container');
        if (mapContainer) {
            mapContainer.classList.add('search-active');
            
            // Remove the class after animation completes
            setTimeout(() => {
                mapContainer.classList.remove('search-active');
            }, 5000);
        }
    } else {
        // If no matches, remove any existing pin and highlight
        if (window.removeSearchPin) {
            window.removeSearchPin();
        }
        
        // Remove any existing highlights
        const existingHighlights = document.querySelectorAll('.building-highlight');
        existingHighlights.forEach(el => el.remove());
        
        // Show no results message
        alert('No matching buildings found.');
    }
    
    // Hide suggestions
    hideSuggestions();
}

// Highlight a building on the map
function highlightBuilding(buildingName) {
    if (!window.map) return;
    
    // Remove previous highlight if exists
    if (window.currentHighlight) {
        // Remove any existing highlight elements
        const existingHighlights = document.querySelectorAll('.building-highlight');
        existingHighlights.forEach(el => el.remove());
        
        // Remove any existing highlight layers and sources
        if (window.map.getLayer('highlight')) {
            window.map.removeLayer('highlight');
        }
        if (window.map.getSource('highlight')) {
            window.map.removeSource('highlight');
        }
    }
    
    // Find the building in our data
    const building = buildings.find(b => b.name === buildingName);
    if (!building || !building.coordinates) return;
    
    // Create a pulsing highlight effect
    const highlight = document.createElement('div');
    highlight.className = 'building-highlight';
    highlight.style.position = 'absolute';
    highlight.style.width = building.width + '%';
    highlight.style.height = building.height + '%';
    highlight.style.left = building.x + '%';
    highlight.style.top = building.y + '%';
    highlight.style.backgroundColor = 'rgba(255, 107, 158, 0.2)';
    highlight.style.border = '2px dashed #ff6b9e';
    highlight.style.borderRadius = '8px';
    highlight.style.pointerEvents = 'none';
    highlight.style.zIndex = '5';
    highlight.style.animation = 'pulse 2s infinite';
    
    // Add the highlight to the map overlay
    const mapOverlay = document.getElementById('mapOverlay');
    if (mapOverlay) {
        mapOverlay.appendChild(highlight);
    }
    
    // Add a pulsing marker at the building's center
    if (window.map) {
        const marker = document.createElement('div');
        marker.className = 'pulse-marker';
        marker.style.width = '20px';
        marker.style.height = '20px';
        marker.style.background = '#ff6b9e';
        marker.style.borderRadius = '50%';
        marker.style.position = 'absolute';
        marker.style.transform = 'translate(-50%, -50%)';
        marker.style.zIndex = '10';
        
        // Position the marker at the building's center
        const markerX = building.x + (building.width / 2);
        const markerY = building.y + (building.height / 2);
        marker.style.left = markerX + '%';
        marker.style.top = markerY + '%';
        
        // Add the marker to the overlay
        mapOverlay.appendChild(marker);
        
        // Remove the marker after animation completes
        setTimeout(() => {
            if (marker.parentNode) {
                marker.remove();
            }
        }, 5000);
    }
    
    // Add circle layer to highlight the building
    window.map.addLayer({
        id: 'highlight-circle',
        type: 'circle',
        source: 'highlight',
        paint: {
            'circle-radius': 15,
            'circle-color': '#ff6b9e',
            'circle-opacity': 0.5,
            'circle-stroke-width': 2,
            'circle-stroke-color': '#fff'
        }
    });
    
    // Store reference to current highlight
    window.currentHighlight = buildingName;
}

// Zoom to a specific building on the map
function zoomToBuilding(buildingName) {
    if (!window.map) return;
    
    const building = buildings.find(b => b.name === buildingName);
    if (!building || !building.coordinates) return;
    
    window.map.flyTo({
        center: building.coordinates,
        zoom: 18,
        essential: true
    });
}

// Initialize voice search
function initVoiceSearch() {
    if (!('webkitSpeechRecognition' in window) || !voiceSearchBtn) {
        voiceSearchBtn.style.display = 'none';
        return;
    }
    
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    voiceSearchBtn.addEventListener('click', () => {
        try {
            recognition.start();
            voiceSearchBtn.classList.add('listening');
            searchInput.placeholder = 'Listening...';
        } catch (error) {
            console.error('Error starting voice recognition:', error);
            voiceSearchBtn.classList.remove('listening');
            searchInput.placeholder = 'Search for a location...';
        }
    });
    
    recognition.onresult = (event) => {
        if (event.results && event.results.length > 0) {
            const transcript = event.results[0][0].transcript.trim();
            console.log('Voice recognition result:', transcript);
            
            // Update the search input
            searchInput.value = transcript;
            
            // Trigger the input event to show suggestions
            const inputEvent = new Event('input', {
                bubbles: true,
                cancelable: true,
            });
            searchInput.dispatchEvent(inputEvent);
            
            // Perform the search
            performSearch(transcript);
            
            // Focus the input to show keyboard if needed
            searchInput.focus();
        }
        
        voiceSearchBtn.classList.remove('listening');
        searchInput.placeholder = 'Search for a location...';
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        voiceSearchBtn.classList.remove('listening');
        searchInput.placeholder = 'Search for a location...';
        
        // Show error to user
        if (event.error === 'not-allowed') {
            alert('Please allow microphone access to use voice search.');
        } else if (event.error === 'audio-capture') {
            alert('No microphone was found. Please ensure your microphone is connected.');
        } else {
            alert('Error occurred with voice recognition. Please try again.');
        }
        voiceSearchBtn.classList.remove('listening');
        searchInput.placeholder = 'Search for a location...';
    };
    
    recognition.onend = () => {
        voiceSearchBtn.classList.remove('listening');
        searchInput.placeholder = 'Search for a location...';
    };
}

// Initialize the search functionality
function initSearch() {
    console.log('Initializing search...');
    
    // Initialize elements
    searchInput = document.getElementById('locationSearch');
    voiceSearchBtn = document.getElementById('voiceSearchBtn');
    suggestionsDropdown = document.getElementById('suggestionsDropdown');
    
    if (!searchInput || !suggestionsDropdown) {
        console.error('Required elements not found in the DOM');
        return false;
    }
    
    console.log('Search elements found:', { searchInput, suggestionsDropdown });
    return true;
    
    console.log('Setting up search event listeners...');
    
    // Set up event listeners
    searchInput.addEventListener('input', function(e) {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();
        
        if (query.length === 0) {
            hideSuggestions();
            return;
        }
        
        debounceTimer = setTimeout(() => {
            try {
                const matches = findMatchingBuildings(query);
                console.log('Found matches:', matches);
                showSuggestions(matches, query);
            } catch (error) {
                console.error('Error in search input handler:', error);
            }
        }, 300);
    });
    
    // Track active suggestion index
    let activeSuggestionIndex = -1;
    let suggestionItems = [];

    // Handle keyboard navigation in search input
    searchInput.addEventListener('keydown', function(e) {
        console.log('Key pressed:', e.key);
        
        // Always process Enter key, even if dropdown is not visible
        if (e.key === 'Enter') {
            console.log('Enter key pressed, performing search...');
            e.preventDefault();
            const query = this.value.trim();
            console.log('Search query:', query);
            performSearch(query);
            hideSuggestions();
            return;
        }

        // Only process other keys if dropdown is visible
        if (!suggestionsDropdown.classList.contains('show')) return;
        
        suggestionItems = Array.from(document.querySelectorAll('.suggestion-item'));
        console.log('Suggestions found:', suggestionItems.length);
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                activeSuggestionIndex = Math.min(activeSuggestionIndex + 1, suggestionItems.length - 1);
                console.log('ArrowDown - New index:', activeSuggestionIndex);
                updateActiveSuggestion();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                activeSuggestionIndex = Math.max(activeSuggestionIndex - 1, -1);
                console.log('ArrowUp - New index:', activeSuggestionIndex);
                updateActiveSuggestion();
                break;
                
            case 'Enter':
                e.preventDefault();
                console.log('Enter key in dropdown - Active index:', activeSuggestionIndex);
                if (activeSuggestionIndex >= 0 && suggestionItems[activeSuggestionIndex]) {
                    const buildingName = suggestionItems[activeSuggestionIndex].getAttribute('data-name');
                    console.log('Selecting building:', buildingName);
                    searchInput.value = buildingName;
                    performSearch(buildingName);
                    hideSuggestions();
                } else {
                    console.log('No active suggestion, performing search with input value');
                    performSearch(searchInput.value.trim());
                }
                break;
                
            case 'Escape':
                e.preventDefault();
                console.log('Escape key pressed, hiding suggestions');
                hideSuggestions();
                break;
        }
    });
    
    // Update active suggestion in the dropdown
    function updateActiveSuggestion() {
        suggestionItems.forEach((item, index) => {
            if (index === activeSuggestionIndex) {
                item.classList.add('active');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('active');
            }
        });
        
        // Reset to input value if no suggestion is selected
        if (activeSuggestionIndex === -1) {
            searchInput.value = searchInput.value; // Keep current value
        }
    }
    
    // Handle click outside to close suggestions
    document.addEventListener('click', function(e) {
        if (searchInput && suggestionsDropdown && 
            !searchInput.contains(e.target) && 
            !suggestionsDropdown.contains(e.target)) {
            hideSuggestions();
        }
    });
    
    // Handle focus on search input
    searchInput.addEventListener('focus', function() {
        activeSuggestionIndex = -1; // Reset active suggestion
        const query = this.value.trim();
        if (query) {
            try {
                const matches = findMatchingBuildings(query);
                showSuggestions(matches, query);
            } catch (error) {
                console.error('Error showing suggestions on focus:', error);
            }
        }
    });
    
    // Reset active suggestion when clicking on input
    searchInput.addEventListener('click', function() {
        activeSuggestionIndex = -1;
        updateActiveSuggestion();
    });
    
    // Initialize voice search if available
    if (voiceSearchBtn) {
        initVoiceSearch();
    }
    
    console.log('Search functionality initialized');
}

// Add pulse animation to the page
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 0.7;
            box-shadow: 0 0 0 0 rgba(255, 107, 158, 0.7);
        }
        70% {
            transform: scale(1.5);
            opacity: 0;
            box-shadow: 0 0 0 10px rgba(255, 107, 158, 0);
        }
        100% {
            transform: scale(1);
            opacity: 0;
            box-shadow: 0 0 0 0 rgba(255, 107, 158, 0);
        }
    }
    
    .pulse-marker {
        animation: pulse 2s infinite;
    }
    
    .search-active #campusMap {
        transition: transform 0.5s ease;
    }
`;
document.head.appendChild(style);

// Expose necessary functions to the global scope
if (typeof window !== 'undefined') {
    window.performSearch = performSearch;
    window.findMatchingBuildings = findMatchingBuildings;
    window.highlightBuilding = highlightBuilding;
    window.zoomToBuilding = zoomToBuilding;
    window.initSearch = initSearch;
    window.initVoiceSearch = initVoiceSearch;
    window.buildings = buildings;
}
