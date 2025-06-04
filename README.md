# Matrix

Python project I created for myself, to dont calculate matrices by myself :)

## Usage

You can import Matrix from this project to use it in your calculations or run matrix.py with:

```sh
python3 matrix.py somefile.txt
```

If you dont provide file, will open tmp file where you can write instructions:

```sh
python3 matrix.py
```

This will make matrix.py to try to interpretate input file and make calculations. Syntax is same as python code, To print matrix you can use print() or show(). Example of instruction file: 

```py
A = Matrix(
  [1, 2, 3],
  [1, 2, 3],
  [1, 2, 3]
)

B = Matrix(
  [1, 2, 3],
  [1, 2, 3],
  [1, 2, 3]
)

C = A + B

C.transpose()

show(C)
```
