# evaluation_pipeline
Evaluation pipeline for TICCL(AT)

## 26 November 2018 sprint plan
![26 November 2018 sprint plan](sprint_plan_20181126.jpg)

# TICCL runner

## Run ticcl_nf.cwl on Ponyland

### Setup virtualenv (as recommended by cwltool docs)

```sh
mkdir envs
cd envs
virtualenv -p python3 cwltool
source cwltool/bin/activate
```

### Install cwltool

```sh
pip install cwlref-runner
```

### Run TICCL

```sh
cwl-runner ticcl_nf.cwl --lexicon_file=/vol/customopt/lamachine16.dev/src/PICCL/data/int/nld/nuTICCL.OldandINLlexandINLNamesAspell.v2.COL1.tsv --input_dir=/vol/bigdata/corpora/SoNaR500.Curated/SONAR500/DATA/WR-P-E-E_newsletters/ --alphabet_file=/vol/customopt/lamachine16.dev/src/PICCL/data/int/nld/nld.aspell.dict.lc.chars --character_confusion_file=/vol/customopt/lamachine16.dev/src/PICCL/data/int/nld/nld.aspell.dict.c20.d2.confusion
```


## Run on LaMachine Docker image with PICCL

```sh
docker run -p 8080:80 -t -i -v $PWD:/data egpbos/lamachine:piccl
```

There you can then run all the TICCL-tools separately, or run them using the Nextflow script ticcl.nf.

To build and upload the image to Dockerhub (in directory with Dockerfile) do:
```sh
docker build -t egpbos/lamachine:piccl .
docker push egpbos/lamachine:piccl
```

## Run using