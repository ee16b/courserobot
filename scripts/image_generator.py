# Individual image generator
import sys

HW_NUMBER = int(sys.argv[1])
Q_NUMBER = int(sys.argv[2])
HW_PATH = sys.argv[3] + "/body.tex"

f = open(HW_PATH, 'r')
content = [n for n in f.readlines() if (not n.startswith('%') and not n.startswith('\sol') and n.strip())]

def index_containing_substring(the_list, substring):
  for i, s in enumerate(the_list):
    if substring in s:
      return i
  return -1

index_of_beginqunlist = index_containing_substring(content, 'begin{qunlist}')
index_of_endqunlist = index_containing_substring(content, 'end{qunlist}')
index_of_maketitle = index_containing_substring(content, 'maketitle')
index_of_enddoc = index_containing_substring(content, 'end{document}')

new_content = []

for i in range(index_of_beginqunlist):
  if i < index_of_maketitle:
    new_content.append(content[i])

# There may be extra empty lines, comments, etc in the qunlist section.
# So we'll find the Q'th \input{q_ line.
index_of_q_number = -1  # In theory it is (index_of_beginqunlist + Q_NUMBER)
current_q = 0
for i in range(index_of_beginqunlist+1, index_of_endqunlist):
  if "\input{q_" in content[i]:
    current_q += 1
  if current_q == Q_NUMBER:
    index_of_q_number = i
    break
assert index_of_q_number != -1, "Can't find the given question number"

new_content.append('\def\qcontributor#1{}') # Hack to disable contributor list from generating a large footer at the bottom
new_content.append('\\pagestyle{empty}') # <-- doesn't seem to do anything/work?

new_content.append(content[index_of_beginqunlist])
new_content.append('\setcounter{sparectr}{' + str(Q_NUMBER - 1) + '}')

new_content.append(content[index_of_q_number])

new_content.append(content[index_of_endqunlist])
new_content.append(content[index_of_enddoc])

with open(HW_PATH, 'w+') as f2:
  for line in new_content:
    f2.write(line + "\n")
