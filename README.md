## Modelstorage

A Django storage backend that stores files as models in the DB. For obvious reasons, it is only useful for testing with small files, as the content of files is stored in memory.

I had found several snippets on the web (on many of which this work is based), but all of them required creating tables by hand. Instead, this app uses the ORM and is more straightforward, at the cost of higher overhead.

## Installation

1. Add 'modelstorage' to your INSTALLED_APPS setting:

    INSTALLED_APPS = (
        ...
        'polls',
    )

2. Optionally, configure the base URL for files served from the DB (the default is '/dbfiles/'):

	MODELSTORAGE_BASEURL = '/myfiles/'

3. Wire the provided view into your project's urls.py at the base URL:

	from modelstorage.views import dbfile_view

	url(r'^dbfiles/(?P<filename>.+)',
        dbfile_view,
        name = 'dbfile_view'
    ),

4. Optionally, set ModelStorage as the default storage backend in settings.py:

	DEFAULT_FILE_STORAGE = 'modelstorage.storage.ModelStorage'
	
5. Migrate the DB to create the model.
