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



#cli_commands.py
from somewhere import app
from anywhere.functions import daily_update, weekly_update


@app.cli.command()
def update_cache_daily():
    daily_update.update()


@app.cli.command()
def update_cache_weekly():
    weekly_update.update()


