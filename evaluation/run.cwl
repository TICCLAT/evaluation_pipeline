#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  gt: File
  ocr: File
outputs:
  result:
    outputSource: ocrevaluation/out_file
    type: File
steps:
  ocrevaluation:
    run: https://raw.githubusercontent.com/nlppln/ocrevaluation-docker/master/ocrevaluation.cwl
    in:
      gt: gt
      ocr: ocr
    out:
    - out_file
