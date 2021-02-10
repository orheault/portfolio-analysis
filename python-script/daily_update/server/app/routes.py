def register_routes(api, app, root="api"):
    from app.search import register_routes as attach_search

    # Add routes
    attach_search(api, app)
