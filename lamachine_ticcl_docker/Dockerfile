FROM proycon/lamachine:latest
LABEL maintainer="Patrick Bos <p.bos@esciencecenter.nl>"
LABEL description="LaMachine distribution with TICCL preinstalled."

RUN lamachine-add piccl
RUN lamachine-add nextflow
RUN /bin/bash -c "source lamachine-activate; lamachine-update --noninteractive"

CMD /bin/bash
