import scispacy
import spacy

nlp = spacy.load("en_core_sci_lg")
text = """
No evidence of mets in the abdomen.
No significant LAP.
NC of mild dilatation of main p-duct in the pancreatic tail portion with abrupt narrowing

with abrupt narrowing (arrow) --> benign stricture > isoattenuating pancreatic cancer, cannot be excluded REC) further evaluation with PB MRI No bone mets.
atocellular 
carcinoma (HCC).
"""
doc = nlp(text)

print(list(doc.sents))

print(doc.ents)