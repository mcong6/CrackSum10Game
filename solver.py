class FindSum10:
    def __init__(self, matrix):
        self.matrix = matrix
        self.num_row = len(matrix)
        self.num_col = len(matrix[0])
        self.res = []
        self.memo = {}
        self.seen = set()

    def serialized(self):
        str_rows = []
        for i in range(self.num_row):
            str_arr = [str(x) for x in self.matrix[i]]
            str_rows.append(",".join(str_arr))
        return ",".join(str_rows)

    def mark_removed_numbers(self, x1, y1, x2, y2):
        temp = []
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                temp.append(self.matrix[i][j])
                self.matrix[i][j] = 0
        return temp

    def reverse_numbers(self, x1, y1, x2, y2, temp):
        k = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.matrix[i][j] = temp[k]
                k += 1

    def calc_range_sum(self, x1, y1, x2, y2):
        total = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                total += self.matrix[i][j]
        return total

    def calc_points(self, x1, y1, x2, y2):
        points = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                if self.matrix[i][j] != 0:
                    points += 1
        return points

    def helper(self, x, y):
        points = 0
        operation = []
        for i in range(x, self.num_row):
            for j in range(y, self.num_col):
                total = self.calc_range_sum(x, y, i, j)
                if total > 10:
                    break
                elif total == 10:
                    cur_points = self.calc_points(x, y, i, j)
                    temp = self.mark_removed_numbers(x, y, i, j)
                    sub_points_remove, sub_operation = self.start_solver()

                    self.reverse_numbers(x, y, i, j, temp)
                    if cur_points + sub_points_remove > points:
                        operation = [[x, y, i, j]] + sub_operation
                        points = cur_points + sub_points_remove
        return points, operation

    def start_solver(self):
        serialized_matrix = self.serialized()
        if serialized_matrix in self.seen:
            return self.memo[self.serialized()]
        self.seen.add(serialized_matrix)

        points = 0
        operation = []
        for i in range(self.num_row):
            for j in range(self.num_col):
                sub_points, sub_operation = self.helper(i, j)
                if sub_points > points:
                    points = sub_points
                    operation = sub_operation
        self.memo[self.serialized()] = [points, operation]
        if points >= 120:
            print(f"Points: {points}")
        return points, operation

    def run(self):
        max_points, operation = self.start_solver()
        print(f"Max points is {max_points}")
        print(f"Operations is {operation}")
        return max_points, operation


def solve_board_by_chunks(matrix, chunk_size):
    num_row = len(matrix)
    h = num_row // chunk_size
    all_operation = []
    total_points = 0
    for i in range(0, num_row, h):
        matrix_chunk = matrix[i:i + h]
        solver = FindSum10(matrix_chunk)
        max_points, operation = solver.run()
        total_points += max_points
        for each_operation in operation:
            each_operation[0] = each_operation[0] + i
            each_operation[2] = each_operation[2] + i
        all_operation += operation
    print(f"Max total points: {total_points}")
    return all_operation


class FindSum10Lazy:
    def __init__(self, matrix):
        self.matrix = matrix
        self.num_row = len(matrix)
        self.num_col = len(matrix[0])
        self.res = []
        self.prefix_sum = self.calc_prefix_sum()

    def mark_removed_numbers(self, x1, y1, x2, y2):
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.matrix[i][j] = 0

    def helper(self, x1, y1, x2, y2):
        if x1 < 0 or x1 >= self.num_row or y1 < 0 or y1 >= self.num_col or x2 >= self.num_row or x2 < 0 or y2 >= self.num_col or y2 < 0:
            return
        cur_sum = self.prefix_sum[x2 + 1][y2 + 1] + self.prefix_sum[x1][y1] - self.prefix_sum[x1][y2 + 1] - \
                  self.prefix_sum[x2 + 1][y1]
        if cur_sum > 10:
            return
        if cur_sum == 10:
            if [x1, y1, x2, y2] in self.res:
                return
            self.mark_removed_numbers(x1, y1, x2, y2)
            self.res.append([x1, y1, x2, y2])
            return
        self.helper(x1, y1, x2 + 1, y2)
        self.helper(x1, y1, x2, y2 + 1)
        self.helper(x1, y1, x2 + 1, y2 + 1)

    def start_solver(self):
        for i in range(self.num_row):
            for j in range(self.num_col):
                if self.matrix[i][j] == 0:
                    continue
                self.helper(i, j, i, j)

    def calc_prefix_sum(self):
        prefix_sum = [[0 for i in range(self.num_col + 1)] for i in range(self.num_row + 1)]
        for i in range(1, self.num_row + 1):
            for j in range(1, self.num_col + 1):
                prefix_sum[i][j] = prefix_sum[i - 1][j] + prefix_sum[i][j - 1] - prefix_sum[i - 1][j - 1] + \
                                   self.matrix[i - 1][j - 1]
        return prefix_sum
