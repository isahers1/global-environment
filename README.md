# Automated Proof Checker

## Set up

1. Clone the repository using `git clone`
2. Install packages using pip (run `pip install -r pip-requirements.txt` in the command line)

## Codebase

The codebase we have designed seperates the elements of abstract algebra into different environments to make writing proofs a seamless experience. The main files are `proof.py,group.py,element.py,` and `logicObjects.py`. The names are pretty self explanatory, but to learn more about how each of the files work poke around some of the `__init__` calls and member functions of those files to see how they interact together. 

## Usage

There are two options to use our proof-checker, but we **highly** recommend using the first option.

+ Using our graphical user interface!
    1. Run `python gui.py` to open the interface
    2. The **Enter** button is used to enter new steps. As you type in the black text box the possible functions yoiu could call will appear below so you never make spelling errors! Warnings will appear if you attempt a step that is not valid.
    3. The **Generate Latex** will take the proof, convert it to a latex file and display the corresponding pdf inside of the GUI in real time!
    4. The **Undo** button deletes the last step you did - be careful to only use this when you need it!
+ Using our raw language in a python file
    1. Open a new file called `my_proof_name_here.py`, with a descriptive name for your proof 
    2. Create a new proof object using the `Proof` function from `proof.py`
    3. Enter the steps of your proof using the functions in `proof.py`
    4. Run the command `python my_proof_name_here.py` to see the proof steps in the console.

