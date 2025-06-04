# Matrix

Python project I created for myself, to dont calculate matrices by myself :)

## Usage

You can import Matrix from this project to use it in your calculations or run matrix.py with:

```sh
python3 matrix.py somefile.txt
```

This will make matrix.py to try to interpretate input file and make calculations, printing them to stdout. Syntax is like python code, Example of instruction file: 

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
```
