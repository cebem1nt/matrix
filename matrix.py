from fractions import Fraction

class Matrix:
    """
    2D Matrix implementation. 
        - Takes rows only instead of default [[], [], []]
        - To access row & column use [i, j] instead of [i][j] 
    """

    def __init__(self, *rows: list[int | float]):
        self._matrix = list(rows)
        self.rows = len(self._matrix)

        if not self._matrix:
            self.columns = 0
        else:
            self.columns = len(self._matrix[0])
            if not all(len(row) == self.columns for row in self._matrix):
                raise ValueError("Invalid matrix dimensions")

    def __eq__(self, other):
        return self._matrix == other.matrix

    def __getitem__(self, index: int | tuple[int]):
        if isinstance(index, int):
            return self._matrix[index]

        elif isinstance(index, tuple) and len(index) == 2:
            i, j = index
            return self._matrix[i][j]

        else:
            raise IndexError("Invalid index")

    def __setitem__(self, index: int | tuple[int], value: int | float):
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
        
        return Matrix(*result_matrix)

    def __sub__(self, other):
        if not has_same_dimensions(self, other):
            raise AssertionError("Matrixes don't have same dimensions")

        result_matrix = []

        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(self[i, j] - other[i, j])
            result_matrix.append(row)
        
        return Matrix(*result_matrix)

    def __mul__(self, other):
        result_matrix = []

        if isinstance(other, (int, float)):
            for row in self:
                new_row = []
                for x in row:
                    new_row.append(x * other)
                result_matrix.append(new_row)
            return Matrix(*result_matrix)
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

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        string = "\n"
        for row in self:
            for item in row:
                string += str(item) + " "
            string += "\n"
        return string

    # Elementary operations:

    def swap_rows(self, R1: int, R2: int):
        """
        Swaps first row with second row
        """
        self[R1], self[R2] = self[R2], self[R1]

    def multiply_row(self, R: int, factor=1):
        self[R] = [x * factor for x in self[R]]

    def add_rows(self, R1: int, R2: int, factor=1):
        """
        Adds elements of R2 to R1 
        """
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

def has_same_dimensions(original: Matrix, other: Matrix) -> bool:
    return (original.columns == other.columns) and (original.rows == other.rows) 

def inverse_matrix(matrix: Matrix, is_fractioning=False) -> Matrix:
    """ 
    Implementation of matrix inversion using Gauss elimination
        - Returns new inversed matrix
        - Won't work with 0s on main diagonal
        - Optionally will return matrix with fractions
    """

    n = matrix.rows

    if is_fractioning:
        extended_matrix = Matrix(
            *[
                [Fraction(value) for value in R] + [Fraction(1.0) if i == j else Fraction(0.0) for j in range(n)] for i, R in enumerate(matrix)
            ]
        )
    else:
        extended_matrix = Matrix(
            *[R + [1.0 if i == j else 0.0 for j in range(n)] for i, R in enumerate(matrix)]
        )

    if not matrix.is_sqare_matrix(): 
        raise ValueError("Given matrix is not square matrix")

    for i in range(n):
        pivot = extended_matrix[i, i]

        if pivot == 0:
            for j in range(i+1, n):
                if extended_matrix[j, i] != 0:
                    extended_matrix.swap_rows(i, j)
                    break
            else:
                raise ValueError("Matrix is not invertible")

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
        *[row[n:] for row in extended_matrix ]
    )

if __name__ == "__main__":
    A = Matrix([1, 2, 3],
               [4, 5, 6])

    B = Matrix([1, 2, 3],
               [4, 5, 6])

    C = Matrix([0, -1, 1],
               [-1, 2, -1],
               [1, -1, 2])

    inversed = inverse_matrix(C)

    print(inversed)