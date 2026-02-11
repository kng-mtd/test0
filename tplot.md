python3 -m venv pyenv
cd pyrnv
. bin/activate

pip install tplot

with python repl

python3

https://tplot.readthedocs.io/en/latest/

import tplot
print(tplot.__version__)

fig = tplot.Figure(title='hello tplot')
fig.scatter([1, 4, 2, 5, 3])
fig.show()


with python script

line1.py
```
import sys, tplot
sys.stdout.write('\033[2J\033[H')
data = [float(x) for x in sys.stdin if x.strip()]

fig = tplot.Figure(title='line plot from stdin', xlabel='time', width=80, height=20)
fig.line(data,marker='.')
fig.show()
```

seq 10 | awk '{print int(rand()*100)}' | python3 line1.py


scatter1.py
```
import sys, tplot
sys.stdout.write('\033[2J\033[H')
data = [float(x) for x in sys.stdin if x.strip()]

fig = tplot.Figure(title='scatter plot from stdin', width=80, height=20)
fig.scatter(data, marker='o')
fig.show()
```

seq 10 | awk '{print int(rand()*100)}' | python3 scatter1.py



line2.py
```
import sys, tplot
sys.stdout.write('\033[2J\033[H')
vals=[]
header=None

for val in sys.stdin:
    if header is None:
        header=val
        continue
    vals.append(float(val))

fig = tplot.Figure(
    title='line plot from csv', ylabel=header,
    width=80, height=20
)
fig.line(vals, marker='.')
fig.show()
```

seq 10| awk 'BEGIN{print "val"} {print int(rand()*100)}' | python3 line2.py
awk -F, '{print $1}' data.csv | python3 line2.py



scatter2.py
```
import sys, tplot
sys.stdout.write('\033[2J\033[H')
x=[]
y=[]
header=None

for line in sys.stdin:
    ln=line.strip()
    if header is None:
        header=ln.split(' ')
        continue
    xi, yi=ln.split(',')
    x.append(float(xi))
    y.append(float(yi))

fig = tplot.Figure(
    title='scatter plot from csv',xlabel=header[0], ylabel=header[1],
    width=80, height=20
)
fig.scatter(x=x, y=y, marker='o')
fig.show()
```

seq 10 | awk 'BEGIN{print "x y"} {print int(rand()*100) " " int(rand()*100)}' | python3 scatter2.py

awk -F, '{print $1, $2}' data.csv | python3 scatter2.py




hbar1.py
```
import sys, tplot
sys.stdout.write('\033[2J\033[H')
lbls=[]
vals=[]
header=None

for ln in sys.stdin:
    ln=ln.strip()
    if header is None:
        header=ln.split(' ')
        continue
    lbl, val=ln.split(' ')
    lbls.append(lbl)
    vals.append(float(val))

fig = tplot.Figure(
    title='horizontal bar plot from csv',
    ylabel=header[0], xlabel=header[1],
    width=80, height=20
)

fig.hbar(y=lbls, x=vals)
fig.show()
```
import sys, tplot
sys.stdout.write('\033[2J\033[H')
x=[]
y0=[]
y1=[]
header=None

for line in sys.stdin:
    if header is None:
        header=line.strip().split(' ')
        continue
    x.append(length(x))
    ys=line.strip().split(' ')    
    y0.append(float(ys[0]))
    y1.append(float(ys[1]))
fig = tplot.Figure(
    title='2 line plot from csv', ylabel='val',
    width=80, height=20
)
fig.line(x=x, y=y0, marker='.', color='red')
fig.line(x=x, y=y1, marker='.', color='blue')
fig.show()
awk 'BEGIN{
  print "label value"
  for(i=1;i<=10;i++)
    print sprintf("%c%c%c %d", 65+int(rand()*26), 65+int(rand()*26), 65+int(rand()*26), int(rand()*100))
}' | python3 hbar1.pyimport sys, tplot
sys.stdout.write('\033[2J\033[H')
x=[]
y0=[]
y1=[]
header=None

for line in sys.stdin:
    if header is None:
        header=line.strip().split(' ')
        continue
    x.append(length(x))
    ys=line.strip().split(' ')    
    y0.append(float(ys[0]))
    y1.append(float(ys[1]))
fig = tplot.Figure(
    title='2 line plot from csv', ylabel='val',
    width=80, height=20
)
fig.line(x=x, y=y0, marker='.', color='red')
fig.line(x=x, y=y1, marker='.', color='blue')
fig.show()

awk -F, '{print $1, $2}' data.csv | python3 hbar1.py




line3.py
```
import sys, tplot
sys.stdout.write('\033[2J\033[H')
y0=[]
y1=[]
header=None

for line in sys.stdin:
    if header is None:
        header=line.strip().split(' ')
        continue
    ys=line.strip().split(' ')
    y0.append(float(ys[0]))
    y1.append(float(ys[1]))
fig = tplot.Figure(
    title='2 line plot from csv', ylabel='val',
    width=80, height=20,
    legendloc='topright'
)
fig.line(y0, marker='.', color='red', label=header[0])
fig.line(y1, marker='.', color='blue', label=header[1])
fig.show()
```

seq 10 | awk 'BEGIN{print "x1 x2"} {print int(rand()*100) " " int(rand()*100)}' | python3 line3.py

awk -F, '{print $1, $2}' data.csv | python3 scatter2.py




while true; do
  echo "$(date +%M:%S.%1N),$((RANDOM%100))" >> log.csv
  sleep 1 
done &

jobs
kill %1

last10.py
```
import sys
from collections import deque
buf=deque(maxlen=10)

for ln in sys.stdin:
    buf.append(ln.rstrip())
    sys.stdout.write('\033[2J\033[H')
    for row in buf:
        t, val=row.split(',')
        print(t, val)
```

tail -f log.csv | python3 last10.py

scatterlast10.py
```
import sys, tplot
from collections import deque

buf0=deque(maxlen=10)
buf1=deque(maxlen=10)
fig = tplot.Figure(title='plot from log.csv', xlabel='time', ylabel='value', width=80, height=20)

for ln in sys.stdin:
    t, val=ln.rstrip().split(',')
    buf0.append(t[-4:])
    buf1.append(float(val))
    sys.stdout.write('\033[2J\033[H')
    fig.line(x=buf0, y=buf1, marker='o')
    fig.show()

```

tail -f log.csv | python3 scatterlast10.py




duckdb

copy (
	select * from read_csv('penguins.csv', nullstr=['NA', 'null', 'NULL']))
to 'penguins1.csv' with(header);

from penguins1.csv;

sqlite3 db.sqlite "select val from t" | python3 line.py
duckdb -csv -c "select value from tbl" db.duckdb | tplot
awk -F, '{print $4,$5,$5,$6}' penguins1.csv | head -n5

duckdb -csv -c '
select bill_length_mm, bill_depth_mm from penguins1.csv
where bill_length_mm is not null and bill_depth_mm is not null limit 10;
' | awk -F, '{print $1,$2}' | python3 scatter2.py


duckdb -csv <<EOF | awk -F, '{print $1,$2}' | python3 scatter2.py
select bill_length_mm, bill_depth_mm from 'penguins1.csv'
where bill_length_mm is not null and bill_depth_mm is not null limit 10;
EOF

duckdb -csv <<EOF | awk -F, '{print $1,$2}' | python3 scatter2.py
select bill_length_mm, bill_depth_mm from 'penguins1.csv'
where sex='male' and bill_length_mm is not null and bill_depth_mm is not null;
EOF

duckdb -csv <<EOF | awk -F, '{print $1,$2}' | python3 scatter2.py
select bill_length_mm, bill_depth_mm from 'penguins1.csv'
where sex='female' and bill_length_mm is not null and bill_depth_mm is not null;
EOF

