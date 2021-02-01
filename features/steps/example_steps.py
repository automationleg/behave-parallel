from behave import step
from random import randint
import time


@step("I have a scenario setup that takes between {a:d} and {b:d} seconds")
def step_impl(context, a, b):
    context.start_time = time.monotonic()
    time.sleep(randint(a, b))


@step("I print the time it took for this setup")
def step_impl(context):
    print(f'Setup step took: {time.monotonic() - context.start_time} seconds')