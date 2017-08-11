.. author KGerring
.. filename logic
.. date = 7/24/17

=====
Logic
=====

associativity
	Within an expression containing two or more occurrences in a row of the same associative operator, the order in which the operations are performed does not matter as long as the sequence of the operands is not changed.Associativity is not the same as commutativity, which addresses whether or not the order of two operands changes the result
commutative
	In mathematics, a binary operation is commutative if changing the order of the operands does not change the result
existential_quantifification
	there is at least one
distributive
	If `x*(y+z) == (x*y) + (x*z)`
idempotence
	the property of certain operations in mathematics and computer science, that can be applied multiple times without changing the result beyond the initial application. Specifically, x ∧ x = x and x ∨ x = x for all x.
truth-preserving
	When all inputs are true, the output is true. The interpretation under which all variables are assigned a truth value of 'true' produces a truth value of 'true' as a result of disjunction.
false-preserving
	When all inputs are false, the output is false.The interpretation under which all variables are assigned a truth value of 'false' produces a truth value of 'false' as a result of disjunction.
linearity
	Another way to express this is that each variable always makes a difference in the truth-value of the operation or it never makes a difference.
	Negation, Logical biconditional, exclusive or, tautology, and contradiction are linear functions.






+++++++++++
Conjunction
+++++++++++
logical_conjunction_

- And
- commutative_
- associative_
- distributive_
- idempotent_
- monotonic
- truth-preserving
- false-preserving


=====  =====  =======
  X      Y     value
=====  =====  =======
True   True    True
True   False   False
False  True    False
False  False   False
=====  =====  =======


+++++++++++
Disjunction
+++++++++++
logical_disjunction_

- Or
- commutative_
- associative_
- distributive_
- idempotent_
- monotonic
- truth-preserving
- false-preserving
- Logical disjunction is usually short-circuited; that is, if the first (left) operand evaluates to true then the second (right) operand is not evaluated.

=====  =====  =======
  X      Y     value
=====  =====  =======
True   True    True
True   False   True
False  True    True
False  False   False
=====  =====  =======



+++++++++++++++++++++
Logical Biconditional
+++++++++++++++++++++
logical_biconditional_

- Xnor
- The biconditional of two statements is the negation of the exclusive or
- commutative_
- associative_
- truth-preserving
- `"p iff q"`
- `(x ∧ y) ∨ (¬x ∧ ¬y)`
- `(p → q) ∧ (q → p)`
- `Or(And(Not(x), Not(y)), And(x, y))`
- Equivalent
- "both or neither"
- "Biconditional introduction allows you to infer that, if B follows from A, and A follows from B, then A if and only if B."
- The only difference from material conditional is the case when the hypothesis is false but the conclusion is true. In that case, in the conditional, the result is true, yet in the biconditional the result is false

=====  =====  =======
  X      Y     value
=====  =====  =======
True   True    True
True   False   False
False  True    False
False  False   True
=====  =====  =======


++++++++++++++++++++
Material Implication
++++++++++++++++++++

material_implication_
- `Implies(x, y)`
- `if p then q; x>>y; `
- `y ∨ ¬x`
- `¬x ∨ y`
- `x SUPERSET OF y`
- `Implies(x,y)`
- `Or(Not(x), y)`
- "if p is true, then q is also true"
- P implies Q is logically equivalent to not-P or Q
- the compound p→q is logically equivalent to the negative compound: not both p and not q.

	in classical logic, the compound p→q is logically equivalent to the negative compound: not both p and not q.
	Thus the compound p→q is false if and only if both p is true and q is false.
	By the same stroke, p→q is true if and only if either p is false or q is true (or both).
	Thus → is a function from pairs of truth values of the components p, q to truth values of the compound p→q, whose truth value is entirely a function of the truth values of the components.
	Hence, this interpretation is called truth-functional.
	The compound p→q is logically equivalent also to ¬p∨q (either not p, or q (or both)), and to ¬q→¬p (if not q then not p).
	But it is not equivalent to ¬p→¬q, which is equivalent to q→p.
	if Γ ⊨ ψ  then ∅ ⊨ ( φ 1 ∧ ⋯ ∧ φ n → ψ ) for some φ 1 , … , φ n ∈ Γ .
	(This is a particular form of the deduction theorem. In words, it says that if Γ models ψ this means that ψ can be deduced just from some subset of the theorems in Γ.)

=====  =====  =======
  X      Y     value
=====  =====  =======
True   True    True
True   False   False
False  True    True
False  False   True
=====  =====  =======


++++++++++++++++++++++++
Material Non-Implication
++++++++++++++++++++++++

material_nonimplication_
- negation of material implication
- `Not(Implies(y,x))`
- `y ∧ ¬x`
- `~(x<<y)`
- `⊅` `NOT A SUPERSET OF`
- Unicode 8603
- "p but not q."
- falsehood-preserving
- is true only if x is true and y is false


=====  =====  =======
  X      Y     value
=====  =====  =======
True   True    False
True   False   False
False  True    True
False  False   False
=====  =====  =======



++++++++++++
Joint Denial
++++++++++++

nor_
- Nor
- `Not(Or(x,y))`
- It evaluates its arguments in order, giving False immediately if any of them are True, and True if they are all False.
- Returns False if any argument is True
- Returns True if all arguments are False

- *not* truth-preserving
- false-preserving
- linear
- monotonic
- self-dual
- The logical NOR ↓ is the negation of the disjunction
- `P ↓ Q  ⇔ ¬(P ∨ Q)
- True *only* if *both* are False
-  true if and only if both operands are false. In other words, it produces a value of false if and only if at least one operand is true
- `P ∧ Q  ⇔ ( P ↓ P )↓( Q ↓ Q )`
- `P ∨ Q  ⇔ ( P ↓ Q )↓( P ↓ Q )`
- `P → Q  ⇔ (( P ↓ P ) ↓ Q) ↓ (( P ↓ P ) ↓ Q)`
- `¬ P ⇔ P ↓ P`
=====  =====  =======
X      Y      value
=====  =====  =======
True   True   False
True   False  False
False  True   False
False  False  True
=====  =====  =======

++++++++++++++++++++++++
Converse Non-Implication
++++++++++++++++++++++++

converse_nonimplication_
- `Not(Implies(x,y))`
- `x ∧ ¬y`
- `~(x>>y)`
- Unicode 8836
- 'LEFTWARDS ARROW WITH STROKE'
- "It is not the case that B implies A"
- falsehood-preserving
- non-associative
- the negation of the converse of implication
- Implication q → p is the dual of Converse Nonimplication  q ↚ p

=====  =====  =======
  X      Y     value
=====  =====  =======
True   True    False
True   False   True
False  True    False
False  False   False
=====  =====  =======


+++++++++++++++++++++
Exclusive Disjunction
+++++++++++++++++++++

xor_
- Xor
- `CIRCLED PLUS` or `XOR` for symbol
- bitwise is `^`
- True only when the outputs are different
- opposite of `logical biconditional`
- `(x ∧ ¬y) ∨ (y ∧ ¬x)`
- is true only when an odd number of inputs is true
- is false whenever an even number of inputs are true
- commutative_
- associative_
- falsehood-preserving: When all inputs are false, the output is false.

=====  =====  =======
  X      Y     value
=====  =====  =======
False  False   False
False  True    True
True   False   True
True   True    False
=====  =====  =======






++++++++++++++++++
Alternative Denial
++++++++++++++++++
nand_
- Nand
- `¬x | ¬y`
- `Or(Not(x), Not(y))`
- It produces a value of true, if — and only if — at least one of the propositions is false.
- functionally complete

=====  =====  =======
  X      Y     value
=====  =====  =======
True   True    False
True   False   True
False  True    True
False  False   True
=====  =====  =======

-----

.. _logical_biconditional: https://en.wikipedia.org/wiki/Logical_biconditional
.. _nand: https://en.wikipedia.org/wiki/Sheffer_stroke
.. _xor: https://en.wikipedia.org/wiki/Exclusive_or
.. _nor: https://en.wikipedia.org/wiki/Logical_NOR
.. _material_implication: https://en.wikipedia.org/wiki/Material_conditional
.. _logical_disjunction: https://en.wikipedia.org/wiki/Logical_disjunction
.. _logical_conjunction: https://en.wikipedia.org/wiki/Logical_conjunction
.. _material_nonimplication: https://en.wikipedia.org/wiki/Material_nonimplication
.. _converse_nonimplication: https://en.wikipedia.org/wiki/Converse_nonimplication
.. _commutative: https://en.wikipedia.org/wiki/Commutative_property
.. _associative: https://en.wikipedia.org/wiki/Associative_property
.. _distributive: https://en.wikipedia.org/wiki/Distributive_property
.. _idempotent: https://en.wikipedia.org/wiki/Idempotence
.. _parser: https://raw.githubusercontent.com/IvanGryzov/LogicParser/master/parser.py
.. _logicparser: https://raw.githubusercontent.com/gehaxelt/Python-LogicParser/master/logicparser.py


.. |date| date:: %Y-%m-%dT%H:%M:%S

.. [#] This document was generated |date| .
