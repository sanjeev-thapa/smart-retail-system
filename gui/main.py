from api import api

if not api.checkAuth():
    import login
else:
    import order