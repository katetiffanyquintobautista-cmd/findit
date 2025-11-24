# Setup script for local development
# Run this script in PowerShell (right-click -> Run with PowerShell)

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path -Path .env)) {
    Write-Host "Creating .env file from .env.example..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    
    # Generate a secure secret key
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | ForEach-Object {[char]$_})
    (Get-Content .env) -replace 'SECRET_KEY=.*', "SECRET_KEY=$secretKey" | Set-Content .env
    
    Write-Host ""
    Write-Host "IMPORTANT: Please edit the .env file and update the following:" -ForegroundColor Yellow
    Write-Host "- CLOUDINARY_CLOUD_NAME" -ForegroundColor Yellow
    Write-Host "- CLOUDINARY_API_KEY" -ForegroundColor Yellow
    Write-Host "- CLOUDINARY_API_SECRET" -ForegroundColor Yellow
    Write-Host "- Other environment-specific settings" -ForegroundColor Yellow
    Write-Host ""
}

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Cyan
python manage.py migrate

# Create superuser if needed
$createSuperuser = Read-Host "Do you want to create a superuser? (y/n)"
if ($createSuperuser -eq 'y') {
    python manage.py createsuperuser
}

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Cyan
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To start the development server, run:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate"
Write-Host "  python manage.py runserver"
Write-Host ""
