// Search functionality with dropdown suggestions
let currentHighlightIndex = -1;
let filteredBuildings = [];

function performSearch(searchTerm) {
    if (!searchTerm) return;
    
    const buildings = window.buildings || window.buildingsData;
    if (!buildings) return;
    
    searchTerm = searchTerm.toLowerCase();
    const result = buildings.find(b => b.name.toLowerCase().includes(searchTerm));
    
    if (result) {
        // Zoom and center the map on the building
        if (window.map) {
            map.setView(result.coordinates, 20);
            
            // Add a temporary marker
            const marker = L.marker(result.coordinates).addTo(map);
            marker.bindPopup(`<b>${result.name}</b><br>${result.description}`).openPopup();
            
            // Remove marker after delay
            setTimeout(() => map.removeLayer(marker), 5000);
        }
        
        // Hide suggestions after selection
        hideSuggestions();
    } else {
        alert("Building not found!");
    }
}

function showSuggestions(searchTerm) {
    const dropdown = document.getElementById('suggestionsDropdown');
    if (!dropdown) return;
    
    // Ensure buildings data is available
    if (!window.buildings && !window.buildingsData) {
        console.log('Buildings data not loaded yet');
        return;
    }
    
    const buildings = window.buildings || window.buildingsData;
    if (!buildings) return;
    
    if (!searchTerm.trim()) {
        hideSuggestions();
        return;
    }
    
    // Filter buildings based on search term
    filteredBuildings = buildings.filter(building => 
        building.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    if (filteredBuildings.length === 0) {
        hideSuggestions();
        return;
    }
    
    // Create suggestion items
    dropdown.innerHTML = '';
    filteredBuildings.forEach((building, index) => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.innerHTML = `
            <i class="fas fa-${building.icon || 'building'}"></i>
            <div class="suggestion-content">
                <div class="suggestion-title">${highlightMatch(building.name, searchTerm)}</div>
                <div class="suggestion-category">${building.category}</div>
            </div>
        `;
        
        item.addEventListener('click', () => {
            document.getElementById('locationSearch').value = building.name;
            performSearch(building.name);
        });
        
        dropdown.appendChild(item);
    });
    
    dropdown.classList.add('show');
    currentHighlightIndex = -1;
}

function hideSuggestions() {
    const dropdown = document.getElementById('suggestionsDropdown');
    if (dropdown) {
        dropdown.classList.remove('show');
        dropdown.innerHTML = '';
    }
    currentHighlightIndex = -1;
    filteredBuildings = [];
}

function highlightMatch(text, searchTerm) {
    if (!searchTerm) return text;
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
}

function navigateSuggestions(direction) {
    const items = document.querySelectorAll('.suggestion-item');
    if (items.length === 0) return;
    
    // Remove current highlight
    if (currentHighlightIndex >= 0) {
        items[currentHighlightIndex].classList.remove('highlighted');
    }
    
    // Update index
    if (direction === 'down') {
        currentHighlightIndex = (currentHighlightIndex + 1) % items.length;
    } else if (direction === 'up') {
        currentHighlightIndex = currentHighlightIndex <= 0 ? items.length - 1 : currentHighlightIndex - 1;
    }
    
    // Add new highlight
    items[currentHighlightIndex].classList.add('highlighted');
    
    // Update input with highlighted suggestion
    const highlightedBuilding = filteredBuildings[currentHighlightIndex];
    if (highlightedBuilding) {
        document.getElementById('locationSearch').value = highlightedBuilding.name;
    }
}

// Voice search functionality
function initVoiceSearch() {
    const voiceSearchBtn = document.getElementById('voiceSearchBtn');
    if (!voiceSearchBtn) return;
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn('Speech Recognition not supported');
        voiceSearchBtn.style.display = 'none';
        return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    voiceSearchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        if (voiceSearchBtn.classList.contains('listening')) {
            recognition.stop();
            return;
        }
        
        voiceSearchBtn.classList.add('listening');
        recognition.start();
    });
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const searchInput = document.getElementById('locationSearch');
        if (searchInput) {
            searchInput.value = transcript;
            performSearch(transcript);
        }
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        voiceSearchBtn.classList.remove('listening');
    };
    
    recognition.onend = function() {
        voiceSearchBtn.classList.remove('listening');
    };
}

// Initialize search functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('locationSearch');
    const searchForm = document.getElementById('searchForm');
    
    if (searchInput) {
        // Show suggestions as user types
        searchInput.addEventListener('input', function(e) {
            showSuggestions(e.target.value);
        });
        
        // Handle keyboard navigation
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                navigateSuggestions('down');
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                navigateSuggestions('up');
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (currentHighlightIndex >= 0) {
                    const selectedBuilding = filteredBuildings[currentHighlightIndex];
                    performSearch(selectedBuilding.name);
                } else {
                    performSearch(searchInput.value.trim());
                }
            } else if (e.key === 'Escape') {
                hideSuggestions();
            }
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !document.getElementById('suggestionsDropdown').contains(e.target)) {
                hideSuggestions();
            }
        });
    }
    
    // Handle form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchTerm = searchInput.value.trim();
            if (searchTerm) {
                performSearch(searchTerm);
            }
        });
    }
    
    // Initialize voice search
    initVoiceSearch();
});