shyPy
=====

.. image:: https://travis-ci.org/grothesk/shyPy.svg?branch=master
    :target: https://travis-ci.org/grothesk/shyPy

A shy Python package with things I secretly like to use.

Installation
------------

You can install shyPy like this:

.. code-block:: bash

    pip install git+https://github.com/grothesk/shypy

NeoCache
--------
Imagine the following use case:
app tracking events are collected in a database. Statistics and plots according to the data available in the database
are provided via a Flask app. The database queries are quite time-consuming. The data should be updated regularly, but
do not have to be available in real time. In this case, NeoCache can help to avoid users being confronted with long
loading times.

With NeoCache.register() functions can be added to a caching mechanism. At the same time, the NeoCache object remembers
these functions in order to update the cache via NeoCache.update() on demand.

Register functions like this:

.. code-block:: python

    #functions.py
    from shypy.caching import NeoCache


    daily_update = NeoCache(context='daily')
    weekly_update = NeoCache(context='weekly')


    @daily_update.register()
    def get_daily_active_user():
        ...
        return data


    @daily_update.register()
    def get_daily_new_user():
        ...
        return data


    @weekly_update.register()
    def get_weekly_report():
        ...
        return data


Add update functions to Flask's cli commands like this:

.. code-block:: python

    #cli_commands.py
    from somewhere import app
    from anywhere.functions import daily_update, weekly_update


    @app.cli.command()
    def update_cache_daily():
        daily_update.update()


    @app.cli.command()
    def update_cache_weekly():
        weekly_update.update()

Finally, only the following two steps are left: integrating the functions into the app and creating the cron
jobs for calling the update functions.

Please note: to keep the API simple, NeoCache only allows the registration of functions without input arguments.
This also avoids having to persist the used input parameters for the cache update. Sometimes it may therefore necessary
to write a wrapper function.

RepititionsExcluder
----------

Imagine the following situation: You have a large amount of files with raw data. Via an ETL process you transfer the
data periodically into a data warehouse. Since the ETL process is very complex and demanding, you want to make sure that
you only feed each file to the process once. On the other hand, you want to process the data again when
the ETL process has been revised. This scenario could be implemented with the **RepititionsExcluder** as follows:

.. code-block:: python

    from shypy.decorators import RepititionsExcluder


    ETL_VERSION = '1.0.0'
    REGISTRY_FILE_PATH = 'registry.txt'


    repex = RepititionsExcluder(REGISTRY_FILE_PATH, [ETL_VERSION])


    @repex.exclude_repititions
    def process_data(file_path):
        ...


    for f in file_paths:
        process_data(f)

In this example, **process_data** would only be executed if **f** had not yet been processed for **ETL_VERSION** '1.0.0'.


