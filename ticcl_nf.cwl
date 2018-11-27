#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: "ticcl.nf"
hints:
  - class: DockerRequirement
    dockerPull: egpbos/lamachine:piccl

doc: |
  Run TICCL nextflow pipeline.

  Corrects OCR errors in the documents in the input directory.

requirements:
  EnvVarRequirement:
    envDef:
      LC_ALL: C.UTF-8
      LANG: C.UTF-8

inputs:
  # mandatory ticcl.nf parameters:
  input_dir:
    type: Directory
    inputBinding:
      prefix: --inputdir
  lexicon_file:
    type: File
    inputBinding:
      prefix: --lexicon
  alphabet_file:
    type: File
    inputBinding:
      prefix: --alphabet
  character_confusion_file:
    type: File
    inputBinding:
      prefix: --charconfus

  # optional ticcl.nf parameters:
  output_dir:
    type: Directory?
    inputBinding:
      prefix: --outputdir
  language:
    type: string?
    inputBinding:
      prefix: --language  
  input_extension:
    type: string?
    inputBinding:
      prefix: --extension
  input_class:
    type: string?
    inputBinding:
      prefix: --inputclass
  input_type:
    type: string?
    inputBinding:
      prefix: --inputtype
  virtual_env:
    type: Directory?
    inputBinding:
      prefix: --virtualenv
  artificial_frequency_lexicon_words:
    type: int?
    inputBinding:
      prefix: --artifrq
  levenshtein_distance:
    type: int?
    inputBinding:
      prefix: --distance
  clip_below:
    type: int?
    inputBinding:
      prefix: --clip
  corpus_frequency_file:
    type: File?
    inputBinding:
      prefix: --corpusfreqlist
 
stdout: cwl.output.json

outputs:
  out_files:
    type: File[]
