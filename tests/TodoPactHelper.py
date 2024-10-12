import subprocess
from pact_test import PactHelper


class TodoPactHelper(PactHelper):
    process = None

    def setup(self):
        self.process = subprocess.Popen('poetry run todo-backend', shell=True)

    def tear_down(self):
        self.process.kill()