shyPy
=====

A shy Python package with things I secretly like to use.

Installation
------------

...


Decorators
----------

shyPy contains the following classes for providing decorators:

- RepititionsExcluder
- CheckRaiser

Imagine the following situation: You have a large amount of files with raw data. With an ETL process you transfer the
data periodically into a data warehouse. Since the ETL process is very complex and demanding, you want to make sure that
you only feed each file to the process once. On the other hand, you want to edit the already processed data again when
the ETL process has been revised. This scenario could be implemented with the RepititionsExcluder as follows:

.. code-block:: python
    from shypy.decorators import RepititionsExcluder


    ETL_VERSION = '1.0.0'
    REGISTRY_FILE_PATH = 'registry.txt


    repex = RepititionsExcluder(REGISTRY_FILE_PATH, [ETL_VERSION])

    @repex.exclude_repititions
    def process_data(file_path):
        ...


    for f in file_paths:
        process_data(f)

In this example, process_data would only be executed if f had not yet been processed for ETL_VERSION '1.0.0'.
