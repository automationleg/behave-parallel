# Behave-Parallel
Script supporting to run Python Behave test features in parallel.  

#### Installation
1. Extract the `behave_parallel.py` and place it in a behave test project folder. Example project structure:
```
    .
    ├── LICENSE
    ├── README.md
    ├── behave_parallel.py
    ├── features
        ├── feature1.feature
        ├── feature2.feature
        ├── feature3.feature
        └── steps
            └── example_steps.py

```
   
2. Initial check
```bash
python behave_parallel.py --help
```
It will print out the following help:
```bash
usage: Run python behave test scenarios in parallel. Example execution with behave parameters:
"python behave_parallel.py --suite features/tests/smoke -f allure_behave.formatter:AllureFormatter -o test-results"
       [-h] [--suite SUITE] [--processes PROCESSES] [--tags TAGS]

optional arguments:
  -h, --help            show this help message and exit
  --suite SUITE, -s SUITE
                        Please specify the suite(directory with feature files) you want to run. Default directory is "features"
  --processes PROCESSES, -p PROCESSES
                        Maximum number of processes. Default = 4
  --tags TAGS, -t TAGS  Please specify behave tags to run
```   

#### Usage
1. To run tests in parallel, use `behave_parallel.py` script instead of standard `behave`.
Example execution that can be tried with included sample tests
```bash
python behave_parallel.py --processes 4 --tags=@example --tags=~@skip -f pretty
```
Will run all 3 feature files in parallel only for `@example` tags and excluding `@skip` tags and using pretty formatter

Script creates `multiprocessing_features.log` logfile storing: feature name, start time, end time and duration of execution

### Limitations
Current version of the script doesn't support parallel execution of scenarios - only features are supported to 
run in parallel.
However, running BDD features in parallel has some pros actually:
* setup/teardown done on a feature level can be used without a risk that it is going to be executed every time in case 
  of parallel scenario run
* scenarios defined in feature files can be dependent(but, I don't think it's usually a good practice)


### Credits
[Step Up Automation](https://stepupautomation.wordpress.com/2019/03/28/execute-tests-in-parallel-with-behave-bdd/) - Initial source of the script. However, that didn't work well for my needs