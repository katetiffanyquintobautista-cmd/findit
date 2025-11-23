# FINDIT Testing Setup Guide

## Quick Setup for Testing

### 1. Create Test Superuser
Run this command to create an admin user for testing the dashboard:

```bash
cd school_map_project/schoolmap
python manage.py create_test_superuser
```

**Login Credentials:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@findit.com`

### 2. Create Sample Data (Optional)
To populate the dashboard with sample analytics data:

```bash
python manage.py create_sample_data
```

This creates:
- 5 sample users (student1, student2, teacher1, student3, student4)
- 5 sample buildings
- Activity logs for the past 7 days
- All with password: `password123`

### 3. Run the Development Server
```bash
python manage.py runserver
```

## Testing URLs

### Public Pages
- **Landing Page:** http://127.0.0.1:8000/
- **Login:** http://127.0.0.1:8000/login/
- **Register:** http://127.0.0.1:8000/register/

### User Pages (after login)
- **Home:** http://127.0.0.1:8000/home/
- **Profile:** http://127.0.0.1:8000/profile/
- **Settings:** http://127.0.0.1:8000/settings/

### Admin Pages (superuser only)
- **Admin Dashboard:** http://127.0.0.1:8000/admin_dashboard/
- **User Management:** http://127.0.0.1:8000/admin_dashboard/users/
- **Building Management:** http://127.0.0.1:8000/admin_dashboard/buildings/
- **Analytics:** http://127.0.0.1:8000/admin_dashboard/analytics/

## Feature Testing Checklist

### ✅ Registration with Success Popup
1. Go to `/register/`
2. Fill out student or teacher form
3. Submit form
4. **Expected:** Success popup appears
5. Click "Continue to Dashboard"
6. **Expected:** Redirected to home page

### ✅ Password Toggle
1. On login or register page
2. Click eye icon next to password field
3. **Expected:** Password visibility toggles
4. **Expected:** Icon changes and tooltip updates

### ✅ Admin Dashboard Live Analytics
1. Login as admin (admin/admin123)
2. Go to `/admin_dashboard/`
3. **Expected:** See live statistics and charts
4. Wait 30 seconds
5. **Expected:** Statistics update automatically
6. **Expected:** Activity timeline refreshes

### ✅ Mobile Responsiveness
1. Open browser developer tools
2. Switch to mobile view (375px width)
3. Test all pages
4. **Expected:** All elements stack properly
5. **Expected:** Forms are usable on mobile

## Browser Testing
Test in multiple browsers:
- Chrome
- Firefox
- Safari
- Edge

## Mobile Device Testing
Test on actual devices:
- iPhone/Android phones
- Tablets
- Different screen orientations

## Performance Testing
- Check page load times
- Monitor network requests
- Verify charts render smoothly
- Test with slow network connections

## Troubleshooting

### Common Issues:

**1. Success Popup Not Showing:**
- Check browser console for JavaScript errors
- Ensure CSRF token is present in forms
- Verify AJAX requests are working

**2. Live Analytics Not Updating:**
- Confirm user has admin privileges
- Check API endpoint accessibility
- Look for fetch errors in console

**3. Charts Not Displaying:**
- Verify Chart.js is loading
- Check data format in template
- Ensure canvas elements exist

**4. Mobile Layout Issues:**
- Clear browser cache
- Check viewport meta tag
- Test in different browsers

### Debug Commands:
```bash
# Check if migrations are applied
python manage.py showmigrations

# Create missing migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Check for errors
python manage.py check
```

## Production Considerations

Before deploying to production:

1. **Security:**
   - Change default admin password
   - Set DEBUG = False
   - Configure proper ALLOWED_HOSTS
   - Use environment variables for secrets

2. **Performance:**
   - Enable caching for dashboard API
   - Optimize database queries
   - Compress static files
   - Use CDN for Chart.js

3. **Monitoring:**
   - Set up error logging
   - Monitor API response times
   - Track user activity patterns
   - Set up alerts for system issues

## Support

If you encounter issues:
1. Check the browser console for errors
2. Review Django logs
3. Verify database connections
4. Test with sample data first
5. Check network connectivity for live updates