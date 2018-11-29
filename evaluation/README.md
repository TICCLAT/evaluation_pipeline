## Evaluation of OCR quality of Dutch text

Erik Tjong Kim Sang
Netherlands eScience Center
November 2018

This directory contains the software developed for the evaluation
of the OCR quality of Dutch text. This work is part of the eScience
project [TICCLAT](https://www.esciencecenter.nl/project/ticclat).
This subtask was executed in the team sprint of 26-29 November 2018.

### Evaluation with gold standard data

The most reliable evaluation method requires the availability of
gold standard data, to enable an elaborate comparison between 
the OCR text with errors and the correct gold standard. We 
examined two strategies. The first involved 
[BLEU](https://en.wikipedia.org/wiki/BLEU), a method widely used
for evaluating machine translation results. It compared word 
ngrams in two texts. It requires that the two texts are 
sentence-aligned. In our case this means that every line in the 
texts contains a single sentence and that sentences at the same
line position belong with each other:

```sh
$ perl bleu.pl data/a0001-gold.txt data/a0001-ocr.txt
processed 3 sentences; bleu score = 0.55377
```

Bleu produces a single score between 0 and 1. Score zero indicates 
that the texts are completely different on word level. Score one
indicates that the two text are identical.

The second evaluation strategy used concerned the OCR evaluation
tool [ocrevalUAtion](https://github.com/impactcentre/ocrevalUAtion).
We downloaded the verion of NLPPLN: [ocrevaluation-docker](https://github.com/nlppln/ocrevaluation-docker)
from Github and expanded the default [run script](run.cwl). Next
we applied the script as follows:

```sh
$ cwl-runner run.cwl --gt data/a0001-gold.txt data/a0001-ocr.txt
$ grep '[WC]ER' a0001_out.html | sed 's/<[^<>]*>/ /g'
 CER  9.33 
 WER  25.19 
 WER (order independent)  23.70 
```

The program reports character error rates (CER) and word error
rates (WER)

### Evaluation without gold standard data

Often there is no gold standard data available for checking the 
quality of the text. For this scenario we examined two strategies.
First, we explored using a lexicon to check how many known words 
the OCR texts contain. Like Van Erp et al. (2018), we employed 
the [IMPACT lexicons for Dutch words and Dutch names](https://www.digitisation.eu/tools-resources/language-resources/historical-and-named-entities-lexica-of-dutch/):

```sh
$ python3 knownWords data/a0001-ocr.txt
data/a0001-ocr.txt: Known tokens: Case sensitive: 76.8% Case insensitive: 80.5%
```

The program presents two variants of the percentage of tokens in 
each text that are present in the two lexicons: a case-sensitive
count and a case-insensitive count. Only tokens that contain an
alphabetic character (a-zA-Z) are considered for these counts.

The next strategy consisted of counting the number of unique 
tokens each text contains.

# Reference

Marieke van Erp, Melvin Wevers and Hugo Huurdeman, Constructing a Recipe Web from Historical Newspapers. In: "Proceedings of the International Semantic Web Conference - ISWC 2018", Springer Verlag, pages 217-232, 2018. [PDF](https://github.com/DHLab-nl/historical-recipe-web/blob/master/constructing-recipe-web-2.pdf)

