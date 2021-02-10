from .model import Search  # noqa
#from .schema import SearchSchema  # noqa

BASE_ROUTE = "search"

def register_routes(api, app, root="api"):
    from .controller import api as search_api

    api.add_namespace(search_api, path=f"/{root}/{BASE_ROUTE}")