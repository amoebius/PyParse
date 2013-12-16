# TODO:
# ..............................................
# HANDLE SUBCLASSING EXISTING GRAMMARS:
#  - As such, "Grammar" is the empty grammar class
#  - Subclasses extend on previous definitions, unless decorated to indicate override?
#    - This should be handled by override vs. extend by default
# Allow two methods for "or-ing":
#  - Implement @extends, so if a previous local exists it sticks everything into a list
#  - Just allow them to give a list of classes as representing a single "node", ^ which will tie in nicely
#  -- Create a Rule('production', evaluate(*args)) metaclass that will create rules for you?
# Defaults for rule evaluation:
#  - def __call__(self): return evaluate(*self.children)
#  - def evaluate(child): return child()
# The class representing the grammar should specify the root rule at the start of its docstring.
#  - A rule name can be specified when calling the class, and is required if a default rule is neglected.
# Single space = optional whitespace, double space = compulsory whitespace
# < > = production rule, " " or ' ' = exact match string, r" " or r' ' = regular expression match (consuming, and only one match will be tried)
# For regular expressions:
#  - The child "node" will be a tuple of the groups if there are matched groups, the matched group if there is a single such group,
#    or if there are no groups then the text will be consumed but not placed as a child node.
# Differentiate types of nodes:
#  - RegexNode vs. Node ?  (so that strings aren't regex by default)
# ..............................................
# Where does checking if rules/grammars are abstract go?
# ..............................................

# DONE:
# ..............................................
# ~ nothing ~
# ..............................................

from parseexception import essert, ParseException, GrammarException, RootUnspecifiedException, AbstractRuleException

# EVILHAX:
import inspect

def overrides(cls):
	try:
		del cls.__rule_previous
	except AttributeError:
		raise ParseException('Rule named "%s" already overwritten.' % cls.__name__)
	return cls

# ------------------------------------
# Returns the local variable with name "name" from the scope that called the caller, or
# 'None' if no such variable was defined in local scope.
def getPreviousLocal(name):
	
	# Get the current stack frame:
	frame = inspect.currentframe()

	try:
		# Get the local variable from the frame before the caller's frame:
		local = frame.f_back.f_back.f_locals.get(name, None)
		return local

	except Exception:
		# Alert of any exceptions:
		raise RuntimeError("Unable to check locals for existing rule.")

	finally:
		# Clean up frame hacks:
		del frame

# ------------------------------------

# /EVILHAX


class GrammarType(type):
	def __init__(cls, name, bases, attributes):
		super(GrammarType, cls).__init__(name, bases, attributes)
		# TODO:
		# - Build lists of nodes
		# - Parse root node from docstring
		# - Import things from bases
		# - Check for cycles
		

class Grammar(object):
	__metaclass__ = GrammarType
	def __init__(self, text, root = None):
		#TODO:  Parse the text based off the grammar!
		if root is None:
			try:
				root = self.__doc__
			except AttributeError:
				raise RootUnspecifiedException('A root production was not specified, and no default was found in grammar definitions.')
		
		# Create a default rule if a string production is given:
		if type(root) is str:
			root = Rule.create('__root__', root)
		# use the root production and go on...
		

class RuleType(type):
	def __new__(mcls, name, bases, attributes):
		
		previous = getPreviousLocal(name)
		if type(previous) is not RuleType:
			previous = None
		attributes['__rule_previous'] = previous

		# TODO:  Handle exceptions
		return super(RuleType, mcls).__new__(mcls, name, bases, attributes)

	def __init__(cls, name, bases, attributes):
		super(RuleType, cls).__init__(name, bases, attributes)
		# TODO:  Are __rule_next, __rule_first or other linked-list attributes useful/required?
		# TODO:  Parse docstrings

		# TODO:  How am I going to handle missing / invalid docstrings?
		#   - Missing docstrings manifest as __doc__ == None
		#   - This is an ACCEPTABLE thing
		#   - Mark the node "abstract" though!!!
		#     - Perhaps just don't parse, and have the Rule class check for the parsed version in __init__

class Rule(object):
	__metaclass__ = RuleType

	def __call__(self):
		return evaluate(*map(lambda x: x(), self.children))

	@staticmethod
	def evaluate(child):
		return child

	# Creates a rule from given parameters:
	@staticmethod
	def create(name, production, evaluator = lambda child: child, call = __call__):
		return RuleType(name, (Rule,), {
				'__doc__': production,
				'evaluate': staticmethod(evaluator),
				'__call__': call,
			})
	
	# Wraps a captured regular expression.  See TODOs for desired behaviour, but __call__ should "evaluate" it.
	# For now, just extend standard strings to return themselves on call!  Beautiful:
	class Regex(str):
		def __call__(self):
			return self