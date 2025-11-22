// Global variables
let searchInput, voiceSearchBtn, suggestionsDropdown, debounceTimer;
let activeSuggestionIndex = -1;
let suggestionItems = [];
let buildings = [];

// Expose functions to global scope
window.searchFunctions = {
    performSearch: null,
    initSearch: null,
    findMatchingBuildings: null,
    showSuggestions: null,
    hideSuggestions: null
};

// Load buildings data when the document is ready
function loadBuildingsData() {
    if (typeof window.buildingsData !== 'undefined') {
        buildings = window.buildingsData;
        console.log('Buildings data loaded successfully:', buildings.length, 'buildings');
        // Initialize search after buildings are loaded
        initSearch();
    } else {
        console.error('Buildings data not found. Make sure buildings.js is loaded before search_fixed.js');
    }
}

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
window.searchFunctions.findMatchingBuildings = function(query) {
    if (!query) return [];
    const regex = new RegExp(escapeRegex(query), 'i');
    return buildings.filter(building => 
        regex.test(building.name) || 
        regex.test(building.description) ||
        regex.test(building.category)
    );
}

// Show suggestions in dropdown
window.searchFunctions.showSuggestions = function(matches, query) {
    if (!suggestionsDropdown) return;
    
    if (matches.length === 0) {
        suggestionsDropdown.innerHTML = '<div class="suggestion-item no-results">No results found</div>';
    } else {
        suggestionsDropdown.innerHTML = matches.map(building => `
            <div class="suggestion-item" data-name="${building.name}" data-building='${JSON.stringify(building)}'>
                <i class="fas fa-${building.icon}"></i>
                <div class="suggestion-text">
                    <div class="suggestion-title">${highlightMatch(building.name, query)}</div>
                    <div class="suggestion-category">${building.category}</div>
                </div>
            </div>
        `).join('');
        
        // Add click handlers to suggestions
        document.querySelectorAll('.suggestion-item').forEach((item) => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                const buildingData = JSON.parse(item.getAttribute('data-building'));
                searchInput.value = buildingData.name;
                performSearch(buildingData.name);
                hideSuggestions();
            });
        });
    }
    
    suggestionsDropdown.style.display = 'block';
    suggestionsDropdown.classList.add('show');
}

// Hide suggestions dropdown
window.searchFunctions.hideSuggestions = function() {
    if (suggestionsDropdown) {
        suggestionsDropdown.classList.remove('show');
        suggestionsDropdown.style.display = 'none';
        activeSuggestionIndex = -1;
    }
}

// Perform search and update UI
window.searchFunctions.performSearch = function(query) {
    try {
        if (!query || !searchInput) return;
        
        // Trim and update input
        query = query.trim();
        searchInput.value = query;
        
        // Find matching buildings
        const matches = findMatchingBuildings(query);
        
        if (matches.length > 0) {
            const building = matches[0];
            
            // Remove any existing pin first
            if (window.removeSearchPin) {
                window.removeSearchPin();
            }
            
            // Highlight the building immediately
            if (window.highlightBuilding) {
                window.highlightBuilding(building.name);
            }
            
            // Zoom to the building on the map
            if (building.coordinates) {
                // Try to use map if available
                const map = window.getMap ? window.getMap() : null;
                
                if (map && typeof map.flyTo === 'function') {
                    map.flyTo({
                        center: building.coordinates,
                        zoom: 18,
                        essential: true
                    });
                    
                    // Add a small delay to ensure the map has finished animating
                    setTimeout(() => {
                        if (window.positionSearchPin) {
                            window.positionSearchPin(building);
                        }
                    }, 800);
                } else if (window.zoomToBuilding) {
                    // Use the zoomToBuilding function if available
                    window.zoomToBuilding(building.name);
                    // Position the pin after a delay
                    setTimeout(() => {
                        if (window.positionSearchPin) {
                            window.positionSearchPin(building);
                        }
                    }, 500);
                } else {
                    // Fallback to just positioning the pin if map is not available
                    console.log('Map functions not available, positioning pin directly');
                    if (window.positionSearchPin) {
                        // Give a small delay to ensure the building is highlighted
                        setTimeout(() => window.positionSearchPin(building), 300);
                    }
                }
            }
        } else {
            // If no matches, remove any existing pin
            if (window.removeSearchPin) {
                window.removeSearchPin();
            }
        }
        
        // Hide suggestions
        hideSuggestions();
    } catch (error) {
        console.error('Error performing search:', error);
    }
}

// Initialize the search functionality
window.searchFunctions.initSearch = function() {
    console.log('Initializing search...');
    
    // Initialize elements
    searchInput = document.getElementById('locationSearch');
    voiceSearchBtn = document.getElementById('voiceSearchBtn');
    suggestionsDropdown = document.getElementById('suggestionsDropdown');
    
    if (!searchInput || !suggestionsDropdown) {
        console.error('Required elements not found in the DOM');
        return;
    }
    
    console.log('Search elements found:', { searchInput, suggestionsDropdown });
    
    // Input event handler with debounce
    let debounceTimer;
    searchInput.addEventListener('input', function(e) {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();
        
        if (query.length === 0) {
            hideSuggestions();
            return;
        }
        
        debounceTimer = setTimeout(() => {
            const matches = findMatchingBuildings(query);
            showSuggestions(matches, query);
        }, 300);
    });
    
    // Handle form submission
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (query) {
                performSearch(query);
                hideSuggestions();
            }
        });
    }
    
    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        // Handle Enter key
        if (e.key === 'Enter') {
            e.preventDefault();
            const activeItem = document.querySelector('.suggestion-item.active');
            if (activeItem && suggestionsDropdown.classList.contains('show')) {
                // If there's an active suggestion, use it
                const buildingData = JSON.parse(activeItem.getAttribute('data-building'));
                searchInput.value = buildingData.name;
                performSearch(buildingData.name);
            } else {
                // Otherwise, search for the current input
                performSearch(this.value.trim());
            }
            hideSuggestions();
            return;
        }
        
        // Only process other keys if dropdown is visible
        if (!suggestionsDropdown.classList.contains('show')) return;
        
        suggestionItems = Array.from(document.querySelectorAll('.suggestion-item:not(.no-results)'));
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                activeSuggestionIndex = Math.min(activeSuggestionIndex + 1, suggestionItems.length - 1);
                updateActiveSuggestion();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                activeSuggestionIndex = Math.max(activeSuggestionIndex - 1, -1);
                updateActiveSuggestion();
                break;
                
            case 'Escape':
                e.preventDefault();
                hideSuggestions();
                break;
        }
    });
    
    // Update active suggestion in dropdown
    function updateActiveSuggestion() {
        suggestionItems.forEach((item, index) => {
            if (index === activeSuggestionIndex) {
                item.classList.add('active');
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                item.classList.remove('active');
            }
        });
    }
    
    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsDropdown.contains(e.target)) {
            hideSuggestions();
        }
    });
    
    console.log('Search initialized successfully');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadBuildingsData);
} else {
    loadBuildingsData();
}

// Expose performSearch globally for HTML form
window.performSearch = function(query) {
    if (window.searchFunctions && window.searchFunctions.performSearch) {
        return window.searchFunctions.performSearch(query);
    } else {
        console.error('Search functions not initialized yet');
        // Try to initialize and retry
        if (window.searchFunctions && window.searchFunctions.initSearch) {
            window.searchFunctions.initSearch();
            if (window.searchFunctions.performSearch) {
                return window.searchFunctions.performSearch(query);
            }
        }
        return false;
    }
};

// Expose necessary functions to the global scope
if (typeof window !== 'undefined') {
    window.performSearch = performSearch;
    window.findMatchingBuildings = findMatchingBuildings;
    window.highlightBuilding = highlightBuilding;
    window.zoomToBuilding = zoomToBuilding;
}
