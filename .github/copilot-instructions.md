Activate the python venv before running any python commands:
`source .venv/Scripts/activate`

We only use the `unittest` framework for tests. DO NOT USE `pytest` or any other testing framework. Test files are always called `*_test.py` and are located next to the file they are testing.

Absolutely NO fallback logic is allowed. If we have fallback code, we are potentially creating information that is not there. People will be acting on this information and if we have created something from nothing, then it is really bad. We simply cannot do this.

"Don't cheat the grind" means facing the real engineering challenge head-on instead of taking shortcuts that avoid the core problem. When we encounter complex, messy real-world data, the right approach is to build robust logic that handles the complexity, not to sanitize the test data to make our job easier. True engineering excellence comes from wrestling with the actual constraints and edge cases, building systems that work with the data as it actually exists rather than as we wish it existed.

We don't cheat the grind.
