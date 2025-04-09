def pytest_addoption(parser):
    parser.addoption("--use-mock", action="store_true", help="Use mock API client")

