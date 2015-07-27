# packing-pythagorean-triangles
This project is an attempt to pack congruent Pythagorean triangles into a rectangle written in Python 3. It came about as my answer to [this awesome challenge on the Code Golf Stack Exchange](http://codegolf.stackexchange.com/questions/51728/stacking-pythagorean-triangles/53843#53843).

## Usage
To run the code, do:
```
$ python3 pythtriples.py
```

After inputting the dimensions for the rectangle, the code will output a list of triangles, represented by the coordinates of their vertices.

Example output for 100x100 rectangle:
```
[[50, 50], [53, 50], [50, 54]]
[[53, 50], [50, 54], [62.6, 57.2]]
[[53, 50], [62.6, 57.2], [58.4, 42.8]]
[[62.6, 57.2], [58.4, 42.8], [81.8, 51.6]]
[[62.6, 57.2], [81.8, 51.6], [72.2, 64.4]]
[[58.4, 42.8], [81.8, 51.6], [82.33088000000001, 44.62016]]
[[62.6, 57.2], [72.2, 64.4], [41.599999999999994, 85.2]]
[[58.4, 42.8], [82.33088000000001, 44.62016], [59.765119999999996, 24.8518
[[82.33088000000001, 44.62016], [59.765119999999996, 24.851839999999996], 
9 triangles placed in 0.007 seconds.
```

You can also call the `matplotlib_graph()` function after `build_all_triangles()` to graph the output with matplotlib. Some example outputs:

1000x1000 with 109 triangles:
![1000x1000](http://i.stack.imgur.com/iyNWb.png)

10000x10000 with 724 triangles:
![10000x10000](http://i.stack.imgur.com/43Zzh.png)
