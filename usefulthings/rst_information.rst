.. author KGerring
.. filename rst_information
.. date = 5/8/17

=====
Title
=====

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+---------------------+




Here is a citation reference: [CIT2002]_.

[2]_ will be "2" (manually numbered)

[#]_ will be "3" (anonymous auto-numbered)

[#label]_ will be "1" (labeled auto-numbered). ``[#label]_``

[#note]_ is a note

note_ is a note as well


.. [CIT2002] This is the citation.  It's just like a footnote, except the label is textual.

.. [2] This footnote is labeled manually, so its number is fixed.

.. [#label] This autonumber-labeled footnote will be labeled "1".
   It is the first auto-numbered footnote and no other footnote
   with label "1" exists.  The order of the footnotes is used to
   determine numbering, not the order of the footnote references.

.. [#] This footnote will be labeled "3".  It is the second
   auto-numbered footnote, but footnote label "2" is already used.

.. [#note] This is the footnote labeled "note".

.. |date| date:: %Y-%m-%dT%H:%M:%S

.. [#] This document was generated |date| .
