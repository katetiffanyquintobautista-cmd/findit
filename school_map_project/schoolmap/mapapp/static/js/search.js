// Global variables
let searchInput, voiceSearchBtn, suggestionsDropdown, debounceTimer;

// Import buildings data from shared file
let buildings = [];

// Load buildings data when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    // This will be populated from the shared buildings.js file
    // Make sure buildings.js is loaded before search.js in your HTML
    if (typeof window.buildingsData !== 'undefined') {
        buildings = window.buildingsData;
    } else {
        console.error('Buildings data not found. Make sure buildings.js is loaded before search.js');
    }
});

// Find matching buildings based on query
function findMatchingBuildings(query) {
    if (!query || query.trim().length === 0) return [];
    
    const searchTerm = query.toLowerCase().trim();
    console.log('Searching for:', searchTerm);
    
    if (buildings.length === 0) {
        console.error('Buildings data not loaded yet');
        return [];
    }
    
    return buildings.filter(building => {
        // Search in name, description, and category
        return (
            building.name.toLowerCase().includes(searchTerm) ||
            (building.description && building.description.toLowerCase().includes(searchTerm)) ||
            (building.category && building.category.toLowerCase().includes(searchTerm))
        );
    }).sort((a, b) => {
        // Sort by match in name first, then description, then category
        const aNameMatch = a.name.toLowerCase().includes(searchTerm);
        const bNameMatch = b.name.toLowerCase().includes(searchTerm);
        
        if (aNameMatch && !bNameMatch) return -1;
        if (!aNameMatch && bNameMatch) return 1;
        
        // For partial matches, prefer matches that start with the search term
        const aStartsWith = a.name.toLowerCase().startsWith(searchTerm);
        const bStartsWith = b.name.toLowerCase().startsWith(searchTerm);
        
        if (aStartsWith && !bStartsWith) return -1;
        if (!aStartsWith && bStartsWith) return 1;
        
        const aDescMatch = a.description && a.description.toLowerCase().includes(searchTerm);
        const bDescMatch = b.description && b.description.toLowerCase().includes(searchTerm);
        
        if (aDescMatch && !bDescMatch) return -1;
        if (!aDescMatch && bDescMatch) return 1;
        
        // Finally, sort alphabetically
        return a.name.localeCompare(b.name);
    });
}

// Show suggestions in dropdown
function showSuggestions(matches, query) {
    console.log('Showing suggestions for query:', query, 'Matches:', matches);
    
    if (!suggestionsDropdown) {
        console.error('Suggestions dropdown element not found');
        return;
    }
    
    // Clear previous suggestions
    suggestionsDropdown.innerHTML = '';
    
    if (!matches || matches.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'suggestion-item';
        noResults.textContent = 'No results found';
        noResults.style.padding = '12px 16px';
        noResults.style.color = '#666';
        suggestionsDropdown.appendChild(noResults);
        suggestionsDropdown.style.display = 'block';
        return;
    }
    
    // Add new suggestions
    matches.slice(0, 5).forEach((building) => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.setAttribute('data-name', building.name);
        item.setAttribute('tabindex', '0');
        item.style.padding = '12px 16px';
        item.style.cursor = 'pointer';
        item.style.display = 'flex';
        item.style.alignItems = 'center';
        item.style.gap = '12px';
        item.style.transition = 'background-color 0.2s';
        
        // Highlight matching text in the name
        const highlightedName = highlightMatch(building.name, query);
        const description = building.description || '';
        const highlightedDesc = highlightMatch(description, query);
        
        // Create icon
        const icon = document.createElement('i');
        icon.className = `fas fa-${building.icon || 'map-marker-alt'}`;
        icon.style.color = '#6b7280';
        icon.style.width = '20px';
        icon.style.textAlign = 'center';
        
        // Create content container
        const content = document.createElement('div');
        content.style.flex = '1';
        content.style.minWidth = '0'; // Ensure text truncation works
        
        // Create name element
        const nameElement = document.createElement('div');
        nameElement.style.fontWeight = '500';
        nameElement.style.color = '#1f2937';
        nameElement.style.marginBottom = '2px';
        nameElement.innerHTML = highlightedName;
        
        // Create description element
        const descElement = document.createElement('div');
        descElement.style.fontSize = '0.85rem';
        descElement.style.color = '#6b7280';
        descElement.style.whiteSpace = 'nowrap';
        descElement.style.overflow = 'hidden';
        descElement.style.textOverflow = 'ellipsis';
        descElement.innerHTML = highlightedDesc || '&nbsp;';
        
        // Assemble the elements
        content.appendChild(nameElement);
        content.appendChild(descElement);
        
        item.appendChild(icon);
        item.appendChild(content);
        
        // Add hover effect
        item.addEventListener('mouseenter', () => {
            item.style.backgroundColor = '#f9fafb';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.backgroundColor = '';
        });
        
        // Handle click
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            if (searchInput) {
                searchInput.value = building.name;
                performSearch(building.name);
            }
            hideSuggestions();
        });
        
        // Handle keyboard navigation
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                if (searchInput) {
                    searchInput.value = building.name;
                    performSearch(building.name);
                }
                hideSuggestions();
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                const next = item.nextElementSibling || item.parentNode.firstElementChild;
                if (next) next.focus();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prev = item.previousElementSibling || item.parentNode.lastElementChild;
                if (prev) prev.focus();
            } else if (e.key === 'Escape') {
                hideSuggestions();
                if (searchInput) searchInput.focus();
            }
        });
        item.style.transition = 'background-color 0.2s';
        
        // Name element was already created above
        const name = document.createElement('span');
        name.innerHTML = highlightMatch(building.name, query);
        
        item.appendChild(icon);
        item.appendChild(name);
        
        // Hover effects
        item.addEventListener('mouseenter', function() {
            item.style.backgroundColor = '#f5f8ff';
        });
        
        item.addEventListener('mouseleave', function() {
            item.style.backgroundColor = 'transparent';
        });
        
        // Click handler
        item.addEventListener('click', function() {
            if (searchInput) {
                searchInput.value = building.name;
                performSearch(building.name);
                searchInput.focus();
            }
        });
        
        // Keyboard navigation
        item.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                searchInput.value = building.name;
                performSearch(building.name);
                searchInput.focus();
            }
        });
        
        suggestionsDropdown.appendChild(item);
    });
    
    // Style the dropdown
    suggestionsDropdown.style.display = 'block';
    suggestionsDropdown.style.position = 'absolute';
    suggestionsDropdown.style.top = '100%';
    suggestionsDropdown.style.left = '0';
    suggestionsDropdown.style.right = '0';
    suggestionsDropdown.style.background = 'white';
    suggestionsDropdown.style.border = '1px solid #ddd';
    suggestionsDropdown.style.borderTop = 'none';
    suggestionsDropdown.style.borderRadius = '0 0 8px 8px';
    suggestionsDropdown.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    suggestionsDropdown.style.zIndex = '1000';
    suggestionsDropdown.style.maxHeight = '300px';
    suggestionsDropdown.style.overflowY = 'auto';
}

// Hide suggestions dropdown
function hideSuggestions() {
    if (suggestionsDropdown) {
        suggestionsDropdown.style.display = 'none';
        suggestionsDropdown.innerHTML = '';
    }
}

// Highlight matching text in search results
function highlightMatch(text, query) {
    if (!query) return text;
    
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<span style="font-weight:bold;color:#1e88e5">$1</span>');
}

// Utility function to escape special regex characters
function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Global variable to store the current marker
let currentMarker = null;

// Perform search
function performSearch(query) {
    if (!query) return;
    
    query = query.trim();
    console.log('Performing search for:', query);
    
    const matches = findMatchingBuildings(query);
    console.log('Search results:', matches);
    
    if (matches.length > 0) {
        const building = matches[0];
        
        // Update the search input with the full building name
        if (searchInput) {
            searchInput.value = building.name;
        }
        
        // Get the map instance
        const map = window.map;
        if (!map) {
            console.error('Map not initialized');
            return;
        }
        
        // Remove existing marker if any
        if (currentMarker) {
            map.removeLayer(currentMarker);
            currentMarker = null;
        }
        
        // Create a custom pink marker icon
        const pinkIcon = L.divIcon({
            className: 'pink-marker',
            html: '<i class="fas fa-map-marker-alt" style="font-size: 40px; color: #ff6b9e; text-shadow: 0 2px 4px rgba(0,0,0,0.2);"></i>',
            iconSize: [40, 40],
            iconAnchor: [20, 40],
            popupAnchor: [0, -40]
        });
        
        // Add marker to the map
        if (building.coordinates && Array.isArray(building.coordinates) && building.coordinates.length === 2) {
            const [lng, lat] = building.coordinates;
            currentMarker = L.marker([lat, lng], { icon: pinkIcon })
                .addTo(map)
                .bindPopup(`<b>${building.name}</b><br>${building.description || ''}`)
                .openPopup();
            
            // Zoom to the building with some padding
            map.flyTo([lat, lng], 18, {
                duration: 1,
                easeLinearity: 0.25,
                animate: true
            });
            
            // Show popup after animation
            setTimeout(() => {
                currentMarker.openPopup();
            }, 1000);
        }
    } else {
        // If no matches found, remove any existing marker
        if (currentMarker) {
            window.map.removeLayer(currentMarker);
            currentMarker = null;
        }
        alert('No matching building found.');
    }
    
    hideSuggestions();
}

// Voice search functionality
function initVoiceSearch() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn('Speech Recognition not supported');
        if (voiceSearchBtn) {
            voiceSearchBtn.style.display = 'none';
        }
        return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    voiceSearchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        try {
            if (voiceSearchBtn.classList.contains('listening')) {
                if (window.recognition) {
                    window.recognition.stop();
                }
                voiceSearchBtn.classList.remove('listening');
                return;
            }
            
            // Start voice recognition logic here
            voiceSearchBtn.classList.add('listening');
            
            // Initialize speech recognition if not already done
            if (!window.recognition) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    throw new Error('Speech recognition not supported in this browser');
                }
                
                window.recognition = new SpeechRecognition();
                window.recognition.continuous = false;
                window.recognition.interimResults = false;
                
                window.recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    searchInput.value = transcript;
                    performSearch(transcript);
                };
                
                window.recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    voiceSearchBtn.classList.remove('listening');
                };
                
                window.recognition.onend = function() {
                    voiceSearchBtn.classList.remove('listening');
                };
            }
            
            window.recognition.start();
            
        } catch (error) {
            console.error('Error in voice search:', error);
            
            // Reset UI on error
            const currentVoiceBtn = document.getElementById('voiceSearchBtn');
            if (currentVoiceBtn) {
                currentVoiceBtn.classList.remove('listening');
                currentVoiceBtn.disabled = false;
            }
            
            const currentSearchInput = document.getElementById('searchInput');
            if (currentSearchInput) {
                currentSearchInput.placeholder = 'Search for a location...';
            }
            
            console.error('Error initializing voice recognition:', error);
            alert('Error initializing voice recognition. Please try again.');
        }
    });
}
