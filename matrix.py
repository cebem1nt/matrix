from fractions import Fraction
import sys, os, subprocess

# The scariest code of the universe ....

type Number = int | float
type Index = int | tuple[int]
type Row = list[Number]

class Matrix:
    """
    2D Matrix implementation. 
        - Takes rows only instead of default [[], [], []]
        - To access row & column use [i, j] instead of [i][j] 
        - Optionally, instead of rows you can provide a matrix
        - If no matrix provided, you should pass x, y as dimensions of a matrix
        - You can set is_fractions to True, so each number will be calculated as fraction
    """

    def __init__(self, *rows: Row, matrix: list[Row] = None, 
                 is_fractions = False,
                 x: Index = None, 
                 y: Index = None ):

        self.is_fractions = is_fractions

        if matrix: 
            self._matrix = matrix
        else:
            self._matrix = list(rows)
       
        if not self._matrix:
            if not x or not y:
                raise ValueError("You should provide matrix dimensions (x, y)")

            self.rows = x
            self.columns = y
            self._matrix = [ 
                [0 for _ in range(y)] for _ in range(x)
            ]

        else:
            self.rows = len(self._matrix)
            self.columns = len(self._matrix[0])


        if any(len(r) != self.columns for r in self._matrix):
            raise ValueError("Invalid matrix dimensions")

        if is_fractions:
            self.to_fraction_matrix()

    def __str__(self):
        string = "\n"

        for row in self:
            for item in row:
                string += str(item) + " "
            string += "\n"

        return string

    def __eq__(self, other):
        return self._matrix == other._matrix

    def __getitem__(self, index: Index):
        if isinstance(index, int):
            return self._matrix[index]

        elif isinstance(index, tuple) and len(index) == 2:
            i, j = index
            return self._matrix[i][j]

        else:
            raise IndexError("Invalid index")

    def __setitem__(self, index: Index, value: Number):
        if (self.is_fractions):
            value = Fraction(value)

        if isinstance(index, int):
            self._matrix[index] = value

        elif isinstance(index, tuple) and len(index) == 2:
            i, j = index
            self._matrix[i][j] = value

        else:
            raise IndexError("Invalid index")

    def __iter__(self):
        for row in self._matrix:
            yield row

    def __add__(self, other):
        if not has_same_dimensions(self, other):
            raise AssertionError("Matrixes don't have same dimensions")

        result_matrix = []

        for i in range(self.rows):
            row = []

            for j in range(self.columns):
                row.append(self[i, j] + other[i, j])

            result_matrix.append(row)
        
        return Matrix(matrix=result_matrix)

    def __sub__(self, other):
        if not has_same_dimensions(self, other):
            raise AssertionError("Matrixes don't have same dimensions")

        result_matrix = []

        for i in range(self.rows):
            row = []
            
            for j in range(self.columns):
                row.append(self[i, j] - other[i, j])

            result_matrix.append(row)
        
        return Matrix(matrix=result_matrix)

    def __mul__(self, other):
        result_matrix = []

        if isinstance(other, (int, float)):
            for row in self:
                new_row = []

                for x in row:
                    new_row.append(x * other)
                result_matrix.append(new_row)

        else:
            if self.columns != other.rows:
                raise AssertionError("Matrices don't have compatible dimensions")
            
            for i in range(self.rows):
                row = []

                for j in range(other.columns):
                    summed = 0

                    for k in range(self.columns):
                        summed += self[i, k] + other[k, j]
                    row.append(summed)

                result_matrix.append(row)

        return Matrix(matrix=result_matrix)

    def __rmul__(self, other):
        return self.__mul__(other)

    # Elementary operations:

    def swap_rows(self, R1: int, 
                        R2: int):

        """Swaps first row with second row"""

        self[R1], self[R2] = self[R2], self[R1]


    def multiply_row(self, R: int, 
                           factor: Number = 1):

        """Multiplies given row by a factor"""

        self[R] = [x * factor for x in self[R]]


    def add_rows(self, R1: int, 
                       R2: int, 
                       factor: Number =1):

        """Adds elements of R2 to R1"""

        modified_row = []

        for x1, x2 in zip(self[R1], self[R2]):
            modified_row.append(x1 + factor*x2)

        self[R1] = modified_row

    def is_sqare_matrix(self) -> bool:
        return self.rows == self.columns 

    def transpose(self):
        transposed = []

        for j in range(self.columns):
            row = []

            for i in range(self.rows):
                row.append(self[i, j])

            transposed.append(row)
            
        self._matrix = transposed
        self.columns, self.rows = self.rows, self.columns

    def to_fraction_matrix(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self[i, j] = Fraction(self[i, j])

# Helping / lib functions

def has_same_dimensions(original: Matrix, other: Matrix) -> bool:
    return (original.columns == other.columns) and \
            (original.rows == other.rows) 

def __choose_expansion_row(A: Matrix):
    best_row = 0
    best_zero_count = -1

    n = A.rows

    for i in range(n):
        zero_count = sum(1 for x in A[i] if x == 0)

        if zero_count > best_zero_count:
            best_zero_count = zero_count
            best_row = i

    return best_row


def __minor_matrix(A: Matrix, 
                   row: int, 
                   col: int):

    return Matrix(
        matrix=[ 
            [A[i, j] for j in range(A.rows) if j != col]
            for i in range(A.rows) if i != row 
        ]
    )

def det(A: Matrix) -> Number:
    """
    Determinant of a matrix using Laplace expansion algorithm (simple)
    """

    if not A.is_sqare_matrix(): 
        raise ValueError(f"Given matrix {A} is not square matrix")

    n = A.rows

    if n == 1:
        # Base case
        return A[0, 0];
    elif n == 2:
        # 2x2 submatrix case
        # just do a*d - b*c
        return (A[0, 0] * A[1, 1]) - (A[0, 1] * A[1, 0])

    r = __choose_expansion_row(A)
    res = 0
    sign = 1

    for j in range(n):
        a = A[r, j]
    
        if a == 0:
            sign = -sign
            continue
            
        M = __minor_matrix(A, r, j)
        res += sign * a * det(M)
        sign = -sign

    return res


def inverse(matrix: Matrix, is_fractions=False) -> Matrix:
    """ 
    Implementation of matrix inversion using Gauss elimination
        - Returns new inversed matrix
        - Won't work with 0s on main diagonal
        - Optionally will return matrix with fractions
    """

    n = matrix.rows

    if not matrix.is_sqare_matrix(): 
        raise ValueError(f"Given matrix {matrix} is not square matrix")

    if is_fractioning or matrix.is_fractions:
        extended_matrix = Matrix(
            matrix=[
                  [Fraction(x) for x in row]  # convert row values to Fraction
                + [Fraction(1) if i == j else Fraction(0) for j in range(n)]  # append identity row
                  for i, row in enumerate(matrix)
            ]
        )
    else:
        extended_matrix = Matrix(
            matrix=[
                R + [1 if i == j else 0 for j in range(n)] 
                for i, R in enumerate(matrix)
            ]
        )

    for i in range(n):
        pivot = extended_matrix[i, i]

        if pivot == 0:
            for j in range(i+1, n):
                if extended_matrix[j, i] != 0:
                    extended_matrix.swap_rows(i, j)
                    break
            else:
                raise ValueError(f"Matrix is not invertible \n{matrix}")

            pivot = extended_matrix[i, i]

        factor = 1/pivot
        extended_matrix.multiply_row(i, factor)

        for j in range(n):
            if j != i:
                factor = -extended_matrix[j, i]
                extended_matrix.add_rows(j, i, factor)

    for i in range(n-1, -1, -1):
        for j in range(i-1, -1, -1):
            factor = -extended_matrix[j, i]
            extended_matrix.add_rows(j, i, factor)

    return Matrix(
        matrix=[row[n:] for row in extended_matrix]
    )

def parse_instructions(file_dir: str):
    """
    Executes given file as a python instuction set. 
    """

    file_dir = os.path.abspath(os.path.expanduser(file_dir))

    global_instructions = {
        'Matrix': Matrix,
        'inverse': inverse,
        'has_same_dimensions': has_same_dimensions,
        'det': det,
        'show': print,
        'print': print,
    }

    with open(file_dir) as f:
        code = f.read()

    print(f"\nCalculating file: {file_dir}\n")
    print("################################")
    print(code)
    print("################################")
    exec(code, global_instructions)
    print("Calculation finished")

def create_instruction_and_execute():
    tmp_file = os.path.join(os.path.curdir, 'tmp_instruction.txt')
    
    editor = os.environ.get('EDITOR', 'vim')

    with open(tmp_file, 'w') as f:
        f.write("# Write your instructions here\n")

    try:
        subprocess.run([editor, tmp_file], check=True)
        parse_instructions(tmp_file)

    except FileNotFoundError:
        print(f"Error: The editor '{editor}' was not found.")

    except subprocess.CalledProcessError:
        print(f"Error: The editor '{editor}' failed to open.")
        
    finally:
        os.remove(tmp_file)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        instruction = sys.argv[1]
        parse_instructions(instruction)
    elif len(sys.argv) == 1:
        # Open a text editor in tmp location and write instruction set
        create_instruction_and_execute()
    else:
        print("Incorrect arguments provided!")