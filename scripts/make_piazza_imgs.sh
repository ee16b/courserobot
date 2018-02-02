#!/bin/bash

set -ex

function make_piazza_imgs {
  # argument 1: homework number
  # argument 2: homework location
  # argument 3: path to scripts folder
  # argument 4: path to hw_pics folder
  script_dir="$3"
  hw_pics_dir="$4"

  cd $2/$1
  mkdir -p screenshots

  for i in `seq 1 $(python3 $script_dir/hw_get_num_questions.py $1)`;
    do
      cp body.tex body_temp.tex
      python3 $script_dir/image_generator.py $1 $i $2/$1
      pdflatex -interaction=batchmode prob$1.tex
      pdflatex -interaction=batchmode prob$1.tex
      mv prob$1.pdf screenshots/prob$1q$i.pdf
      mv body_temp.tex body.tex
      convert -density 350 -resize 1000x -trim -append "screenshots/prob$1q$i.pdf" "screenshots/prob$i.png"
    done

  rm -f screenshots/*.pdf *.annotations *.aux *.log *.out
  rm -rf $hw_pics_dir
  mv screenshots $hw_pics_dir

}

make_piazza_imgs $1 $2 $3 $4
