// Image Upload Functionality
function initImageUpload() {
    console.log('Initializing image upload...');
    
    const imagePreview = document.getElementById('imagePreview');
    const imageUpload = document.getElementById('imageUpload');
    
    console.log('Image preview element:', imagePreview);
    console.log('Image upload element:', imageUpload);
    
    if (!imagePreview || !imageUpload) {
        console.error('Image upload elements not found:', {
            imagePreview: !!imagePreview,
            imageUpload: !!imageUpload
        });
        return;
    }
    
    console.log('Image upload elements found, setting up event listeners...');
    
    // Handle click on upload area
    imagePreview.addEventListener('click', () => {
        imageUpload.click();
    });
    
    // Handle file selection
    imageUpload.addEventListener('change', handleFileSelect);
    
    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        imagePreview.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        imagePreview.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        imagePreview.addEventListener(eventName, unhighlight, false);
    });
    
    // Handle dropped files
    imagePreview.addEventListener('drop', handleDrop, false);
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight() {
        imagePreview.classList.add('highlight');
    }
    
    function unhighlight() {
        imagePreview.classList.remove('highlight');
    }
    
    function handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            handleFiles(files);
        }
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
    
    function handleFiles(files) {
        const file = files[0];
        
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            // Display preview
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
            imagePreview.classList.add('has-image');
        };
        reader.readAsDataURL(file);
    }
    
    console.log('Image upload initialized successfully');
}
