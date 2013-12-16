class ParseException(Exception):
	pass

class GrammarException(ParseException):
	pass

class RootUnspecifiedException(ParseException):
	pass

class AbstractRuleException(ParseException):
	pass

def essert(condition, exception):
	if not condition:
		raise exception