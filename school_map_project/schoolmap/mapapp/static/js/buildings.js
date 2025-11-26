const svgToPercent = (x, y, width, height) => ({
x: (x / 1440) * 100,
y: (y / 1106) * 100,
width: (width / 1440) * 100,
height: (height / 1106) * 100
});

const buildDetails = (gradeLevels, sections, extraInfo) => ({
gradeLevels,
sections,
extraInfo
});

window.buildings = window.buildingsData = [
{
name: 'Library',
category: 'Facilities',
icon: 'book',
description: 'School library with study areas and reading materials.',
coordinates: [11.551417, 124.416917], // swapped lat,lng
details: buildDetails(['All Grade Levels'], ['Research Nook', 'Quiet Study'], 'Multi-level stacks and collaborative study pods.'),
...svgToPercent(722, 577, 86, 34)
},
{
name: 'Admin Office',
category: 'Administrative',
icon: 'university',
description: 'Administrative offices and staff rooms.',
coordinates: [11.552500, 124.417194],
details: buildDetails(['All Grades'], ["Principal's Office", 'Registrar'], 'Handles enrollment, records management, and overall campus coordination.'),
...svgToPercent(1046, 139, 106, 71)
},
{
name: 'Caregiving',
category: 'Academic',
icon: 'user-nurse',
description: 'Caregiving classrooms for students.',
coordinates: [11.551083, 124.417],
details: buildDetails(['Grades 11-12'], ['Caregiving Sections'], 'Practical caregiving competency training.'),
...svgToPercent(912, 159, 80, 67)
},
{
name: 'Junior High / Canteen / Clinic',
category: 'Academic',
icon: 'school',
description: 'Junior High classrooms, canteen, and clinic.',
coordinates: [11.551917, 124.416778],
details: buildDetails(['Grades 7-10'], ['Classrooms & Services'], 'Multiple sections and student support services.'),
...svgToPercent(870, 161, 70, 40)
},
{
name: 'Food Processing 1',
category: 'Academic',
icon: 'utensils',
description: 'Food Processing lab 1.',
coordinates: [11.551528, 124.416556],
details: buildDetails(['Grade 10'], ['Lab 1'], 'Hands-on culinary and food processing skills.'),
...svgToPercent(645, 138, 22, 71)
},
{
name: 'Food Processing 2',
category: 'Academic',
icon: 'utensils',
description: 'Food Processing lab 2.',
coordinates: [11.551528, 124.416444],
details: buildDetails(['Grade 10'], ['Lab 2'], 'Hands-on culinary and food processing skills.'),
...svgToPercent(587, 138, 23, 71)
},
{
name: 'Canteen 2',
category: 'Facilities',
icon: 'utensils',
description: 'Secondary canteen for students.',
coordinates: [11.551417, 124.416361],
details: buildDetails(['All Grades'], ['Cafeteria'], 'Secondary cafeteria near exit.'),
...svgToPercent(645, 117, 35, 30)
}
// Continue adding more buildings with same structure
];

// Simple search and zoom function using Leaflet
window.performSearch = (searchTerm) => {
    const map = window.campusMap; // your Leaflet map instance
    const markerLayer = window.buildingMarkers || L.layerGroup().addTo(map);

    const result = window.buildings.find(
        (b) => b.name.toLowerCase() === searchTerm.toLowerCase()
    );
    if (!result) {
        alert('Building not found.');
        return;
    }

    // Clear existing markers
    markerLayer.clearLayers();

    L.marker([result.coordinates[0], result.coordinates[1]], {
        icon: L.icon({
            iconUrl: '/static/icons/pink-marker.png', // your pink icon path
            iconSize: [30, 30],
            iconAnchor: [15, 30]
        })
    })
        .addTo(markerLayer)
        .bindPopup(`<strong>${result.name}</strong><br>${result.description}`)
        .openPopup();

    map.setView([result.coordinates[0], result.coordinates[1]], 19); // zoom in
    window.buildingMarkers = markerLayer;
};
