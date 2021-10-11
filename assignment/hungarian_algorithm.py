from typing import List, Tuple
from copy import deepcopy

class Hungarian():
    """
    Class implementing the Hungarian algorithm. Inspired by the Python
    implementation Munkres.

    usage:
        Hungarian([[0, 1], [0, 2]]).assignments() # [(0, 1), (1, 0)]
        Hungarian([[0, 1], [0, 2]]).value()       # 3

        # use deepcopy to keep the original matrix
        matrix = [[0, 1, 2], [0, 2, 4], [0, 3, 6]]
        Hungarian(deepcopy(matrix)).assignments() # [(0, 2), (1, 1), (2, 0)]
        print(matrix) # [[0, 1, 2], [0, 2, 4], [0, 3, 6]]
    """

    def __init__(self, matrix):
        self.matrix = matrix
        self.__matrix = deepcopy(matrix)
        self.__assignments = None

    def assignments(self) -> List[Tuple[int, int]]:
        """
        Return the optimal assignments for the matrix.
        The matrix has to be rectangular or square.
        This function is destructive.
        """
        self.__extend_matrix()
        self.__create_mask()
        self.__create_covers()

        steps = {
            1: self.step_one,
            2: self.step_two,
            3: self.step_three,
            4: self.step_four,
            5: self.step_five,
            6: self.step_six,
        }

        step = 1

        while step in steps:
            step = steps[step]()

        ret = []
        for r in range(self.orig_rows):
            for c in range(self.orig_cols):
                if self.mask[r][c] == 1:
                    ret.append((r, c))

        self.__assignments = ret

        return ret

    def value(self) -> int:
        if self.__assignments is None:
            self.assignments()

        return sum(self.__matrix[r][c] for r, c in self.__assignments)

    def __extend_matrix(self) -> None:
        """ Extend a rectangular matrix to become square """

        self.orig_rows = len(self.matrix)
        self.orig_cols = len(self.matrix[0])

        self.n = max(self.orig_rows, self.orig_cols)

        for r, row in enumerate(self.matrix):
            row += [0] * (self.n - len(row))

        while len(self.matrix) < self.n:
            self.matrix.append([0] * self.n)


    def __create_mask(self) -> None:
        """
        Create a mask matrix to keep track of primed and starred zeroes
        0 -> not (primed or starred)
        1 -> starred
        2 -> primed
        """
        self.mask = []
        for i in range(self.n):
            self.mask.append([0] * self.n)

    def __create_covers(self) -> None:
        """ Create lists to keep track of the covered rows and columns """
        self.row_cover = [False] * self.n
        self.col_cover = [False] * self.n

    def __find_zero(self) -> Tuple[int, int]:
        """ Return the row and column of a noncovered zero """
        for r, row in enumerate(self.matrix):
            for c, value in enumerate(row):
                if value == 0 \
                   and not self.row_cover[r] \
                   and not self.col_cover[c]:
                    return (r, c)

        return (-1, -1)

    def __clear_covers(self) -> None:
        """ Remove all covers """
        for i in range(self.n):
            self.row_cover[i] = False
            self.col_cover[i] = False

    def __find_star_in_row(self, r) -> int:
        """ Return the index of a starred zero in row r """
        for c in range(self.n):
            if self.mask[r][c] == 1:
                return c

        return -1

    def __find_prime_in_row(self, r) -> int:
        """ Return the index of a starred zero in row r """
        for c in range(self.n):
            if self.mask[r][c] == 2:
                return c

        return -1

    def __find_star_in_col(self, c) -> int:
        """ Return the index of a starred zero in col c """
        for r in range(self.n):
            if self.mask[r][c] == 1:
                return r

        return -1

    def __augment_path(self) -> None:
        """ Unstar starred zeroes on the path and star primed zeroes on the path """
        for r, c in self.path:
            if self.mask[r][c] == 1:
                self.mask[r][c] = 0
            else: # == 2
                self.mask[r][c] = 1

    def __erase_primes(self) -> None:
        """ Remove all primed zeroes """
        for r in range(self.n):
            for c in range(self.n):
                if self.mask[r][c] == 2:
                    self.mask[r][c] = 0

    def __find_smallest(self) -> int:
        """ Find the smallest uncovered value """
        min_val = None
        for r in range(self.n):
            for c in range(self.n):
                if not self.row_cover[r] and not self.col_cover[c]:
                    if min_val is None:
                        min_val = self.matrix[r][c]
                    else:
                        min_val = min(self.matrix[r][c], min_val)

        return min_val

    def step_one(self) -> int:
        """
        Step 1
        Subtract the smallest value in each row from all values in each row.
        """
        for row in self.matrix:
            min_val = min(row)
            for i in range(self.n):
                row[i] -= min_val

        return 2

    def step_two(self) -> int:
        """
        Step 2
        Star one zero in each row and column in the matrix.
        """
        for r, row in enumerate(self.matrix):
            for c, value in enumerate(row):
                if value == 0 \
                   and not self.row_cover[r] \
                   and not self.col_cover[c]:
                    self.mask[r][c] = 1
                    self.row_cover[r] = True
                    self.col_cover[c] = True
                    break

        self.__clear_covers()

        return 3

    def step_three(self) -> int:
        """
        Step 3
        Cover colums with starred zeroes. If all are covered, we are done.
        """
        for r in range(self.n):
            for c in range(self.n):
                if self.mask[r][c] == 1:
                    self.col_cover[c] = True

        col_count = self.col_cover.count(True)
        if col_count >= self.n:
            return 7
        else:
            return 4

    def step_four(self) -> int:
        """
        Step 4
        Find noncovered zeroes and prime them? Not sure exactly.
        """
        while True:
            r, c = self.__find_zero()
            if r == -1:
                return 6

            self.mask[r][c] = 2
            c2 = self.__find_star_in_row(r)
            if c2 != -1:
                self.row_cover[r] = True
                self.col_cover[c2] = False
            else:
                self.path_row_0 = r
                self.path_col_0 = c
                return 5

    def step_five(self) -> int:
        """
        Step 5
        Construct a series of alternating primed and starred zeroes.
        """
        self.path = [(self.path_row_0, self.path_col_0)]
        done = False

        while not done:
            r = self.__find_star_in_col(self.path[-1][1])
            if r > -1:
                self.path.append((r, self.path[-1][1]))
            else:
                done = True

            if not done:
                c = self.__find_prime_in_row(self.path[-1][0])
                self.path.append((self.path[-1][0], c))

        self.__augment_path()
        self.__clear_covers()
        self.__erase_primes()

        return 3

    def step_six(self) -> int:
        """
        Step 6
        Remove the smallest noncovered value from noncovered columns and add
        it to covered rows.
        """
        min_val = self.__find_smallest()
        for r in range(self.n):
            for c in range(self.n):
                if self.row_cover[r]:
                    self.matrix[r][c] += min_val
                if not self.col_cover[c]:
                    self.matrix[r][c] -= min_val

        return 4


if __name__ == "__main__":

    # Test the implementation against the Munkres implementation

    from munkres import Munkres
    from random import randint
    from copy import deepcopy

    m = Munkres()

    def cost(matrix, assignments):
        return sum((matrix[r][c] for r, c in assignments))


    for i in range(5):
        matrix = [[randint(0, 255) for j in range(60)] for k in range(60)]
        h = Hungarian(deepcopy(matrix))
        h_assignments = h.assignments()

        m_assignments = m.compute(matrix)
        assert m_assignments == h_assignments or \
                cost(matrix, m_assignments) == h.value()

    rect_matrix = [[10.01, 10.02,  8.03, 11.04],
                   [9.05,   8.06,  1.07,  1.08],
                   [9.09,    7.1,  4.11, 10.12]]

    m_assignments = m.compute(rect_matrix)
    h = Hungarian(rect_matrix)
    assert m_assignments == h.assignments()
