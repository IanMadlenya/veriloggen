FROM ubuntu:16.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install build-essential -y
RUN apt-get install git -y
RUN apt-get install python python-pip python3 python3-pip -y
RUN apt-get install iverilog gtkwave -y
RUN apt-get install python-pygraphviz -y
RUN pip install jinja2
RUN pip3 install jinja2
RUN pip install pyverilog
RUN pip3 install pyverilog
RUN pip install ipgen
RUN pip3 install ipgen
RUN mkdir /home/veriloggen/
WORKDIR "/home/veriloggen"
RUN git clone https://github.com/PyHDI/veriloggen.git
RUN cd veriloggen && python setup.py install && cd ../
RUN cd veriloggen && python3 setup.py install && cd ../
