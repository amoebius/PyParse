PyParse
=======

A module to easily define and evaluate programming langauges in a pythonic setting.

Foremost, through some metaclass magic, grammars are defined with nice syntax:

```python
# Matches a series of balanced parentheses and brackets, with optional whitespace:
class MyGrammar(Grammar):
    " <Group> "
    
    # A production rule definition is in the form of a class definition, the docstring representing the production:
    class Group(Rule):
    	"'(' <Group> ')'" # Single spaces are optional whitespace
    
    # Rule names are automatically overloaded, unless "@overrides" is applied to a class definition.
    # This means that the first matching rule is chosen:
    class Group(Rule):
    	"'[' <Group> ']'"

    # Base node:
    class Group(Rule):
    	""

try:
	# Build a parse tree, and just ignore the result for now:
    MyGrammar('(([] ) \n )')
    
    print "Valid."

except ParseException:
	print "Invalid."
```

Secondly, through a hopefully smooth interface, a parse tree can be evaluated:

```python
class SimpleCalculator(Grammar):
    " <Add> "

    # Matches a number:
    class Number(Rule):
        "r'([0-9]+)'" # Regular expressions are allowed, with matched groups retained.

        # This allows the node to be evaluated:
        @staticmethod
        def evaluate(matchedString):
            return int(matchedString)

        # NB:  Alternatively, one could use 'evaluate = staticmethod(int)'


    class Add(Rule):
        "<Multiply> '+' <Add>" # Recursive definition

        @staticmethod
        def evaluate(left, right):
            return left + right

    class Add(Rule):
        "<Multiply>" # Base case
        # NB:  Default evaluation will return a single child for us

    class Multiply(Rule):
        r"<Number> r'x|\*' <Multiply>" # Regular expression allows 'x' or '*', without capturing them.

        evaluate = staticmethod(lambda left, right: left * right)

    class Multiply(Rule):
        "<Number>"

    # Done!

expression = raw_input("Enter expression: ")
try:
    parsed = SimpleCalculator(expression)
    result = parsed()
    print ">>", result

except ParseException:
    print "Invalid expression."
```

The entire method of evaluation is customisable and can be user-defined, so long as the root node is callable.  Awesome.

Thirdly, all forms of class inheritance should behave as expected - allowing you to inherit the functionality of rules and grammars.

```python
class FloatCalculator(SimpleCalculator):
    # Root node specification is inherited.

    # Override the old integer number definition:
    @overrides
    class Number(Rule):
        r'r"(-?[0-9]+|-?[0-9]+\.[0-9]*)"' # Don't judge me on my regexes - it works.
        evaluate = staticmethod(float)

    # Done.

class BracketCalculator(FloatCalculator):

    # We can hackily add brackets by extending the existing definition of a number:
    class Number(Rule):
        "'(' <Add> ')'"

    # Quite easily done.
```

That's enough of examples of the interface, which may be documented properly after it's actually implemented.  As it doesn't yet exist.  Nevertheless, the calculator example will be eventually fleshed out more in a file that isn't the 'readme'.

Currently written to work with Python 2.7, though 3.x appears to add a new metaclass method '__prepare__' that would make things considerably less hacky than they currently are...  Regardless, the interface exposed to the end user is very clean, if I might claim so.

TODO:
- Implementing said features:
 - Lexing rule definitions.
 - Parsing strings from these definitions.
 - Making inheritance work and dealing with the existence of 'abstract' Rules and Grammars.
 - Hacky metaclass things to package the nodes in a nice format.
- Examples:
 - A calculator, applying the entire interface.
 - A programming language would be nice too.  I hesitate to try python though...
- i.e. everything yet to be implemented.