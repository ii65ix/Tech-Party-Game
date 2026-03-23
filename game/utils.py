def content_language(request):
    """Return 'ar' or 'en' for question sets based on active UI language."""
    code = getattr(request, "LANGUAGE_CODE", "") or ""
    if code.lower().startswith("ar"):
        return "ar"
    return "en"
