from pyparse import Grammar, Rule, overrides


class Calculator(Grammar):
	' <Add> '

	class Add(Rule):
		'<Multiply> "+" <Add>'
		def __call__(self):
			return self.children[0]() + self.children[1]()

	Add = Rule.create('Add', '<Multiply>')

	class Multiply(Rule):
		r'<Number> r"\*|x" <Multiply>'
		
		@staticmethod
		def evaluate(left, right):
			return left * right

	class Multiply(Rule):
		'<Number>'

	class Number(Rule):
		r'r"(-?[0-9]+)"'
		evaluate = staticmethod(int)


class ExtendedCalculator(Calculator):
	
	@overrides
	class Number(Rule):
		r'r"(-?[0-9]+|-?[0-9]+\.[0-9]*)"'
		evaluate = staticmethod(float)

	class Number(Rule):
		'"(" <Add> ")"'