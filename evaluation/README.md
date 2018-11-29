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

counting lexicon words

counting unique words

# Reference

Marieke van Erp, Melvin Wevers and Hugo Huurdeman, Constructing a Recipe Web from Historical Newspapers. In: "Proceedings of the International Semantic Web Conference - ISWC 2018", Springer Verlag, pages 217-232, 2018.

