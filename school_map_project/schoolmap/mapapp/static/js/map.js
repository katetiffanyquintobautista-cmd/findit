// Map Interaction Functionality

// Global variables for map interaction
let currentHighlight = null;
let searchPin = null;
const mapContainer = document.querySelector('.map-container');

// Function to create a search pin with animation
function createSearchPin() {
    try {
        // Remove existing pin if any
        if (searchPin && searchPin.parentNode) {
            searchPin.remove();
        }
        
        // Get the map overlay
        const overlay = document.getElementById('mapOverlay');
        if (!overlay) {
            console.error('Map overlay not found');
            return null;
        }
        
        // Create pin element with Font Awesome icon
        searchPin = document.createElement('div');
        searchPin.className = 'search-pin';
        searchPin.innerHTML = `
            <i class="fas fa-map-marker-alt" style="font-size: 40px; color: #ff6b9e;"></i>
            <div style="position: absolute; top: 5px; left: 50%; 
                transform: translateX(-50%); width: 16px; height: 16px; 
                background: white; border-radius: 50%;">
            </div>
        `;
        
        // Style the pin container
        searchPin.style.position = 'absolute';
        searchPin.style.zIndex = '1000';
        searchPin.style.pointerEvents = 'none';
        searchPin.style.opacity = '0';
        searchPin.style.transition = 'all 0.3s ease';
        searchPin.style.willChange = 'transform, opacity';
        searchPin.style.transform = 'translate(-50%, -100%) scale(0.5)';
        searchPin.style.textShadow = '0 2px 4px rgba(0,0,0,0.2)';
        searchPin.style.textAlign = 'center';
        
        // Add pin to the overlay
        overlay.appendChild(searchPin);
        
        // Add pulsing animation
        const pulse = document.createElement('style');
        pulse.textContent = `
            @keyframes bounce {
                0% { transform: translate(-50%, -100%) scale(0.5); opacity: 0; }
                50% { transform: translate(-50%, -120%) scale(1.2); }
                70% { transform: translate(-50%, -100%) scale(0.9); }
                100% { transform: translate(-50%, -100%) scale(1); opacity: 1; }
            }
            .search-pin-enter {
                animation: bounce 0.6s ease-out forwards;
            }
            .fa-map-marker-alt {
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
            }
        `;
        document.head.appendChild(pulse);
        
        return searchPin;
    } catch (error) {
        console.error('Error creating search pin:', error);
        return null;
    }
}

// Function to position the search pin at a building
function positionSearchPin(building) {
    console.log('Positioning pin for building:', building.name);

    try {
        // Ensure pin exists
        if (!searchPin || !searchPin.parentNode) {
            if (!createSearchPin()) {
                console.error('Failed to create search pin');
                return false;
            }
        }

        // Get the map element
        const mapEl = document.getElementById('campusMap');
        if (!mapEl) {
            console.error('Map element not found');
            return false;
        }

        // Get the current transform matrix to calculate the actual position
        const currentTransform = window.getComputedStyle(mapEl).transform;
        let scale = 1, translateX = 0, translateY = 0;

        if (currentTransform !== 'none' && currentTransform !== 'matrix(1, 0, 0, 1, 0, 0)') {
            const matrix = currentTransform.match(/matrix\((.*)\)/);
            if (matrix) {
                const values = matrix[1].split(',').map(Number);
                scale = values[0]; // x scale
                translateX = values[4]; // x translation
                translateY = values[5]; // y translation
            }
        }

        // Calculate the building's center in SVG coordinates
        const svgViewBox = { width: 1440, height: 1106 };
        const buildingCenterX = building.x + (building.width / 2); // Percentage center X
        const buildingCenterY = building.y + (building.height / 2); // Percentage center Y

        // Convert to SVG pixel coordinates
        const svgPixelX = (buildingCenterX / 100) * svgViewBox.width;
        const svgPixelY = (buildingCenterY / 100) * svgViewBox.height;

        // Apply the current zoom and pan transformation
        const finalX = (svgPixelX * scale) + translateX;
        const finalY = (svgPixelY * scale) + translateY;

        console.log('Setting pin position - x:', finalX, 'y:', finalY, 'scale:', scale);

        // Apply position (pin should be centered above the building)
        searchPin.style.left = `${finalX}px`;
        searchPin.style.top = `${finalY - 40}px`; // 40px above the building center

        // Add animation class
        searchPin.classList.add('search-pin-enter');

        // Make pin visible
        searchPin.style.opacity = '1';

        // Remove animation class after it completes
        setTimeout(() => {
            if (searchPin) {
                searchPin.classList.remove('search-pin-enter');
            }
        }, 500);

        return true;
    } catch (error) {
        console.error('Error positioning search pin:', error);
        return false;
    }
}

// Function to remove search pin with animation
function removeSearchPin() {
    if (searchPin && searchPin.parentNode) {
        searchPin.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        searchPin.style.opacity = '0';
        searchPin.style.transform = 'translate(-50%, -100%) scale(0.5)';
        
        // Remove after animation completes
        setTimeout(() => {
            if (searchPin && searchPin.parentNode) {
                searchPin.remove();
                searchPin = null;
            }
        }, 300);
    }
}

// Function to highlight a building by name
function highlightBuilding(buildingName) {
    // Remove highlight from current building if any
    if (currentHighlight) {
        currentHighlight.style.boxShadow = 'none';
        currentHighlight.style.zIndex = '1';
    }
    
    // Find all building elements
    const buildings = document.querySelectorAll('.map-area');
    let found = false;
    
    // Find and highlight the building
    buildings.forEach(building => {
        const title = building.getAttribute('data-building-name');
        if (title && title.toLowerCase() === buildingName.toLowerCase()) {
            building.style.boxShadow = '0 0 15px 5px rgba(255, 215, 0, 0.7)';
            building.style.zIndex = '10';
            building.style.transition = 'box-shadow 0.5s ease';
            currentHighlight = building;
            found = true;
        }
    });
    
    return found;
}

// Function to smoothly zoom to a building
function zoomToBuilding(buildingName) {
    console.log('Zooming to building:', buildingName);

    // Find the building in the buildings data
    const buildings = window.buildingsData || [];
    const building = buildings.find(b => b.name.toLowerCase() === buildingName.toLowerCase());

    if (!building) {
        console.error('Building not found:', buildingName);
        return false;
    }

    // Get the map element
    const map = document.getElementById('campusMap');
    if (!map) {
        console.error('Map element not found');
        return false;
    }

    // Get the map container
    const container = document.querySelector('.map-container');
    if (!container) {
        console.error('Map container not found');
        return false;
    }

    // Get container dimensions
    const containerRect = container.getBoundingClientRect();

    // SVG viewBox dimensions (must match the SVG file)
    const svgViewBox = { width: 1440, height: 1106 };

    // Building dimensions in SVG pixels (convert from percentages)
    const buildingSvgWidth = (building.width / 100) * svgViewBox.width;
    const buildingSvgHeight = (building.height / 100) * svgViewBox.height;

    // Building center in SVG pixels
    const buildingCenterSvgX = (building.x / 100) * svgViewBox.width + (buildingSvgWidth / 2);
    const buildingCenterSvgY = (building.y / 100) * svgViewBox.height + (buildingSvgHeight / 2);

    // Calculate zoom level to show the building nicely
    const padding = 0.3; // 30% padding around the building
    const zoomX = (containerRect.width * (1 - padding)) / buildingSvgWidth;
    const zoomY = (containerRect.height * (1 - padding)) / buildingSvgHeight;
    const newScale = Math.min(zoomX, zoomY, 4); // Cap at 4x zoom

    // Calculate translation to center the building
    const containerCenterX = containerRect.width / 2;
    const containerCenterY = containerRect.height / 2;

    // Translation needed to center the building at the new scale
    const translateX = containerCenterX - (buildingCenterSvgX * newScale);
    const translateY = containerCenterY - (buildingCenterSvgY * newScale);

    console.log('Zooming to building:', {
        building: buildingName,
        svgCenter: { x: buildingCenterSvgX, y: buildingCenterSvgY },
        containerCenter: { x: containerCenterX, y: containerCenterY },
        scale: newScale,
        translate: { x: translateX, y: translateY }
    });

    // Apply the transform with smooth transition
    map.style.transition = 'transform 1s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
    map.style.transformOrigin = '0 0';
    map.style.transform = `matrix(${newScale}, 0, 0, ${newScale}, ${translateX}, ${translateY})`;

    // Highlight the building after zoom
    setTimeout(() => {
        const buildingElement = document.querySelector(`.map-area[data-building-name="${building.name}"]`);
        if (buildingElement) {
            buildingElement.style.zIndex = '1000';
            buildingElement.style.boxShadow = '0 0 0 3px rgba(255, 200, 0, 0.8)';
            buildingElement.style.transition = 'all 0.3s ease';

            // Reset highlight after a few seconds
            setTimeout(() => {
                if (buildingElement) {
                    buildingElement.style.zIndex = '';
                    buildingElement.style.boxShadow = '';
                }
            }, 3000);
        }

        // Position search pin if needed
        if (typeof positionSearchPin === 'function') {
            positionSearchPin(building);
        }
    }, 1000);

    return true;
}

// Function to reset map view
function resetMapView() {
    const map = document.getElementById('campusMap');
    if (map) {
        // Reset transform with smooth animation
        map.style.transition = 'transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        map.style.transform = 'matrix(1, 0, 0, 1, 0, 0)'; // Identity matrix (no transform)

        // Remove highlight if any
        if (currentHighlight) {
            currentHighlight.style.boxShadow = 'none';
            currentHighlight.style.zIndex = '1';
            currentHighlight = null;
        }

        // Remove search pin if any
        if (typeof removeSearchPin === 'function') {
            removeSearchPin();
        }

        // Reset transition after animation completes
        setTimeout(() => {
            if (map) {
                map.style.transition = 'transform 0.3s ease';
            }
        }, 800);
    }
}

// Global map variable (reuse existing instance if script evaluated twice)
let map = window.campusMap || null;

// Make functions and map globally available
window.highlightBuilding = highlightBuilding;
window.zoomToBuilding = zoomToBuilding;
window.resetMapView = resetMapView;
window.positionSearchPin = positionSearchPin;
window.removeSearchPin = removeSearchPin;
window.getMap = () => map; // Getter function for the map

function initMap() {
    console.log('Initializing map...');
    
    const campusMap = document.getElementById('campusMap');
    const mapPopup = document.getElementById('mapPopup');
    const popupTitle = document.getElementById('popupTitle');
    const popupContent = document.getElementById('popupContent');
    const closePopup = document.getElementById('closePopup');
    
    if (!campusMap || !mapPopup) {
        console.warn('Map elements not found');
        return;
    }
    
    console.log('Map elements found, setting up event listeners...');

    // Store reference globally so other scripts can access without redeclaring
    window.campusMap = campusMap;
    
    // Use the shared buildings data
    const buildings = window.buildingsData || [];
    
    if (buildings.length === 0) {
        console.error('Buildings data not loaded. Make sure buildings.js is loaded before map.js');
        return; // Exit if no buildings data is available
    }
    
    // Create clickable areas on the map
    const mapOverlay = document.getElementById('mapOverlay');
    
    if (mapOverlay) {
        buildings.forEach(building => {
            const area = document.createElement('div');
            area.className = 'map-area';
            area.setAttribute('data-building-name', building.name);
            area.style.position = 'absolute';
            area.style.left = building.x + '%';
            area.style.top = building.y + '%';
            area.style.width = building.width + '%';
            area.style.height = building.height + '%';
            area.style.cursor = 'pointer';
            // Use custom colors if defined, otherwise use default
            const defaultBg = 'rgba(255, 107, 158, 0.2)';
            const defaultBorder = 'rgba(255, 107, 158, 0.5)';
            const hoverBg = building.color || 'rgba(255, 107, 158, 0.4)';
            const defaultHoverBg = 'rgba(255, 107, 158, 0.4)';
            
            area.style.backgroundColor = building.color || defaultBg;
            area.style.border = `2px solid ${building.borderColor || defaultBorder}`;
            area.style.borderRadius = '8px';
            area.style.transition = 'all 0.3s ease';
            
            // Hover effect
            area.addEventListener('mouseenter', function() {
                this.style.backgroundColor = hoverBg;
                this.style.transform = 'scale(1.05)';
            });
            
            area.addEventListener('mouseleave', function() {
                this.style.backgroundColor = building.color || defaultBg;
                this.style.transform = 'scale(1)';
            });
            
            // Click to show popup
            area.addEventListener('click', function(e) {
                e.stopPropagation();
                if (!window.searchActive) {
                    showPopup(building, e);
                }
            });
            
            mapOverlay.appendChild(area);
        });
    }
    
    // Show popup function
    function showPopup(building, event) {
        console.log('Showing popup for:', building.name);
        const encodedName = encodeURIComponent(building.name);
        
        popupTitle.textContent = building.name;
        popupContent.innerHTML = `
            <div style="padding-top: 4px;">
                <button onclick="viewBuildingDetails('${encodedName}')" style="
                    background: linear-gradient(135deg, #ff6b9e 0%, #a78bfa 100%);
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-weight: 500;
                    width: 100%;
                    margin-top: 5px;
                ">
                    <i class="fas fa-info-circle"></i> View Details
                </button>
            </div>
        `;
        
        // Get the clicked area's position and dimensions
        const mapRect = campusMap.getBoundingClientRect();
        const containerRect = campusMap.parentElement.getBoundingClientRect();
        
        // Calculate the center of the building
        const buildingCenterX = (building.x + (building.width / 2)) * (mapRect.width / 100);
        const buildingCenterY = (building.y + (building.height / 2)) * (mapRect.height / 100);
        
        // Show popup temporarily to get its dimensions
        mapPopup.style.display = 'block';
        mapPopup.style.visibility = 'hidden';
        const popupRect = mapPopup.getBoundingClientRect();
        mapPopup.style.visibility = 'visible';
        
        // Position the popup centered above the building
        let x = buildingCenterX - (popupRect.width / 2);
        let y = buildingCenterY - popupRect.height - 10; // 10px above the building
        
        // Adjust if popup goes off the left/right edges
        if (x < 10) x = 10;
        if (x + popupRect.width > mapRect.width - 10) {
            x = mapRect.width - popupRect.width - 10;
        }
        
        // If popup would go above the viewport, show it below the building instead
        if (y < 10) {
            y = buildingCenterY + building.height * (mapRect.height / 100) + 10;
        }
        
        // Apply the calculated position
        mapPopup.style.left = x + 'px';
        mapPopup.style.top = y + 'px';
        
        // Animate popup
        mapPopup.style.opacity = '0';
        mapPopup.style.transform = 'translateY(10px)';
        setTimeout(() => {
            mapPopup.style.transition = 'all 0.3s ease';
            mapPopup.style.opacity = '1';
            mapPopup.style.transform = 'translateY(0)';
        }, 10);
    }
    
    // Allow other scripts (like search) to open the popup programmatically
    window.showBuildingPopup = function(buildingName) {
        if (!Array.isArray(buildings)) return;
        const building = buildings.find(b => b.name === buildingName);
        if (building) {
            showPopup(building);
        } else {
            console.warn('Building not found for popup:', buildingName);
        }
    };

    window.viewBuildingDetails = function(encodedBuildingName) {
        const decodedName = decodeURIComponent(encodedBuildingName || '');
        const target = `/details/?building=${encodeURIComponent(decodedName)}`;
        window.location.href = target;
    };

    // Close popup
    if (closePopup) {
        closePopup.addEventListener('click', function() {
            mapPopup.style.display = 'none';
            // Reset map view when popup is closed
            if (typeof resetMapView === 'function') {
                resetMapView();
            }
        });
    }
    
    // Close popup when clicking outside
    document.addEventListener('click', function(e) {
        if (!mapPopup.contains(e.target) && !e.target.classList.contains('map-area')) {
            mapPopup.style.display = 'none';
            // Reset map view when clicking outside popup
            if (typeof resetMapView === 'function') {
                resetMapView();
            }
        }
    });
    
    console.log('Map initialized successfully with', buildings.length, 'buildings');
    
    // Add click handler to reset view when clicking on the map background
    mapOverlay.addEventListener('click', function(e) {
        if (e.target === mapOverlay) {
            resetMapView();
        }
    });
}

// Get directions function
function getDirections(buildingName) {
    console.log('Getting directions to:', buildingName);
    alert('Directions to ' + buildingName + ' will be shown here.\n\nThis feature can be integrated with a routing system.');
    // You can integrate with a real routing/pathfinding system here
}
