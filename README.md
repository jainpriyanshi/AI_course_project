# AI_course_project
### Run Instruction
To run these Project
> pip3 install requirements.txt \
> python3 query.py "your_search_question"

Example : python3 query.py " What does backprop mean? Is the backprop term basically the same as backpropagation or does it have a different meaning?"

You can try running query.py on 
1)  What does backprop mean? Is the backprop term basically the same as backpropagation or does it have a different meaning?
2) I've heard a lot of people working on VR talk about scanline racing and that it's supposed to help improve latency for motion-to-photon. However, it isn't clear to me how this can be done with OpenGL. Could someone explain how scanline racing works, and how it can be implemented on modern GPUs

To complete the whole Installation Process
1) Download the zip under zip folder in code directory
>  [cs.meta.stackexchange.com.7z](https://archive.org/download/stackexchange/cs.meta.stackexchange.com.7z)  \
>  [cs.stackexchange.com.7z](https://archive.org/download/stackexchange/cs.stackexchange.com.7z)\
> [datascience.meta.stackexchange.com.7z](https://archive.org/download/stackexchange/datascience.meta.stackexchange.com.7z)\
> [datascience.stackexchange.com.7z](https://archive.org/download/stackexchange/datascience.stackexchange.com.7z)\
> [ai.meta.stackexchange.com.7z](https://archive.org/download/stackexchange/ai.meta.stackexchange.com.7z)\
> [ai.stackexchange.com.7z](https://archive.org/download/stackexchange/ai.stackexchange.com.7z)\
> [computergraphics.meta.stackexchange.com.7z](https://archive.org/download/stackexchange/computergraphics.meta.stackexchange.com.7z)\
> [computergraphics.stackexchange.com.7z](https://archive.org/download/stackexchange/computergraphics.stackexchange.com.7z)\
2) Unzip these zip files and store Posts.xml in each zip under xml directory with th nameof their data
> Content of ./code/xml \
> AI.xml \
> AImeta.xml \
> CS.xml \
> CSmeta.xml \
> DataScience.xml \
> DataSciencemeta.xml \
> ComputerGraphics.xml \
> ComputerGraphicsmeta.xml \
3) Create a folder named csv in Project directory
4) Run
> python3 parser.py \
> python3 datacleaner.py \
> python3 merge.py \
> python3 query.py "your_question"
