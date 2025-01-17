CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Your frontend development server
    # Add your production domain when deploying
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
] 