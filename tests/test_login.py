from pytest_bdd import scenarios

from step_definitions.login_steps import *

scenarios("../features/login.feature")