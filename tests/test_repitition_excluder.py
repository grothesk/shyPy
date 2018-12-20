import pytest
import os

from shypy.decorators import RepititionsExcluder


@pytest.fixture(scope="function")
def registry_file_path(tmpdir):
    registry_file_path = os.path.join(tmpdir, 'test_registry_file')
    open(registry_file_path, 'a').close()

    yield registry_file_path

    os.remove(registry_file_path)


def test_parameter_list(registry_file_path):

    LIST = []

    version = '1.0.0'
    repex = RepititionsExcluder(registry_file_path, [version])

    @repex.exclude_repititions
    def appender(element):
        LIST.append(element)

    appender(1)
    assert LIST == [1]

    version = '1.0.1'
    repex = RepititionsExcluder(registry_file_path, [version])

    @repex.exclude_repititions
    def appender(element):
        LIST.append(element)

    appender(1)
    assert LIST == [1, 1]

    version = '1.0.0'
    repex = RepititionsExcluder(registry_file_path, [version])

    @repex.exclude_repititions
    def appender(element):
        LIST.append(element)

    appender(1)
    assert LIST == [1, 1]
    appender(0)
    assert LIST == [1, 1, 0]
