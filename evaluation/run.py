#!/usr/bin/env python3
"""
    run.py: run ocrevaluation-docker
    usage: run.py
    code source: https://github.com/nlppln/ocrevaluation-docker
    20181127 erikt(at)xs4all.nl
"""

from nlppln import WorkflowGenerator

with WorkflowGenerator() as wf:
        wf.load(step_file='https://raw.githubusercontent.com/nlppln/ocrevaluation-docker/master/ocrevaluation.cwl')

	# add workflow inputs
        gt = wf.add_input(gt="File")
        ocr =  wf.add_input(ocr="File")
	# add data processing steps

	# to run the ocrevalUAtion tool for a single file:
        out_file = wf.ocrevaluation(gt=gt, ocr=ocr)

	# or for a list of gt and ocr files:
        # out_files = wf.ocrevaluation(gt=gt_files, ocr=ocr_files, scatter=['gt', 'ocr'], scatter_method='dotproduct')

	# add more processing tools
	# add workflow outputs
        wf.add_outputs(result=out_file)
	# save workflow to file
        wf.save("run.cwl",mode="rel")
