"""Game solving algorithms for Sum10 puzzle."""

from typing import List, Tuple, Dict, Set
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

# Type aliases for better readability
Matrix = List[List[int]]
Coordinate = Tuple[int, int, int, int]  # x1, y1, x2, y2
Operation = List[Coordinate]


class BaseSolver(ABC):
    """Base class for Sum10 solvers."""
    
    def __init__(self, matrix: Matrix):
        self.matrix = [row[:] for row in matrix]  # Deep copy
        self.num_rows = len(matrix)
        self.num_cols = len(matrix[0]) if matrix else 0
        self.target_sum = 10
    
    @abstractmethod
    def solve(self) -> Tuple[int, Operation]:
        """Solve the puzzle and return max points and operations."""
        pass
    
    def _calculate_range_sum(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate sum of matrix elements in specified range."""
        total = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                total += self.matrix[i][j]
        return total
    
    def _calculate_points(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate points (non-zero cells) in specified range."""
        points = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                if self.matrix[i][j] != 0:
                    points += 1
        return points
    
    def _is_valid_range(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """Check if the range coordinates are valid."""
        return (0 <= x1 <= x2 < self.num_rows and 
                0 <= y1 <= y2 < self.num_cols)


class OptimalSolver(BaseSolver):
    """Optimal solver using dynamic programming with memoization."""
    
    def __init__(self, matrix: Matrix):
        super().__init__(matrix)
        self.memo: Dict[str, Tuple[int, Operation]] = {}
        self.seen: Set[str] = set()
    
    def _serialize_matrix(self) -> str:
        """Serialize matrix to string for memoization."""
        return ','.join(','.join(map(str, row)) for row in self.matrix)
    
    def _mark_removed_numbers(self, x1: int, y1: int, x2: int, y2: int) -> List[int]:
        """Mark numbers as removed and return original values."""
        original_values = []
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                original_values.append(self.matrix[i][j])
                self.matrix[i][j] = 0
        return original_values
    
    def _restore_numbers(self, x1: int, y1: int, x2: int, y2: int, values: List[int]) -> None:
        """Restore original values to the matrix."""
        idx = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.matrix[i][j] = values[idx]
                idx += 1
    
    def _find_best_move_from_position(self, start_x: int, start_y: int) -> Tuple[int, Operation]:
        """Find the best move starting from given position."""
        max_points = 0
        best_operation = []
        
        for end_x in range(start_x, self.num_rows):
            for end_y in range(start_y, self.num_cols):
                current_sum = self._calculate_range_sum(start_x, start_y, end_x, end_y)
                
                if current_sum > self.target_sum:
                    break  # No point checking larger rectangles in this row
                
                if current_sum == self.target_sum:
                    current_points = self._calculate_points(start_x, start_y, end_x, end_y)
                    
                    # Try this move and solve recursively
                    original_values = self._mark_removed_numbers(start_x, start_y, end_x, end_y)
                    sub_points, sub_operations = self.solve()
                    self._restore_numbers(start_x, start_y, end_x, end_y, original_values)
                    
                    total_points = current_points + sub_points
                    if total_points > max_points:
                        max_points = total_points
                        best_operation = [(start_x, start_y, end_x, end_y)] + sub_operations
        
        return max_points, best_operation
    
    def solve(self) -> Tuple[int, Operation]:
        """Solve using optimal algorithm with memoization."""
        matrix_key = self._serialize_matrix()
        
        if matrix_key in self.seen:
            return self.memo.get(matrix_key, (0, []))
        
        self.seen.add(matrix_key)
        
        max_points = 0
        best_operation = []
        
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.matrix[i][j] == 0:
                    continue
                
                points, operations = self._find_best_move_from_position(i, j)
                if points > max_points:
                    max_points = points
                    best_operation = operations
        
        self.memo[matrix_key] = (max_points, best_operation)
        
        if max_points >= 120:
            logger.info(f"High score achieved: {max_points} points")
        
        return max_points, best_operation


class GreedySolver(BaseSolver):
    """Greedy solver that finds valid combinations without backtracking."""
    
    def __init__(self, matrix: Matrix):
        super().__init__(matrix)
        self.operations: Operation = []
        self.prefix_sum = self._calculate_prefix_sum()
    
    def _calculate_prefix_sum(self) -> List[List[int]]:
        """Calculate prefix sum matrix for efficient range sum queries."""
        prefix_sum = [[0] * (self.num_cols + 1) for _ in range(self.num_rows + 1)]
        
        for i in range(1, self.num_rows + 1):
            for j in range(1, self.num_cols + 1):
                prefix_sum[i][j] = (prefix_sum[i-1][j] + prefix_sum[i][j-1] - 
                                  prefix_sum[i-1][j-1] + self.matrix[i-1][j-1])
        
        return prefix_sum
    
    def _get_range_sum_fast(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Get range sum using prefix sum array."""
        return (self.prefix_sum[x2+1][y2+1] + self.prefix_sum[x1][y1] - 
                self.prefix_sum[x1][y2+1] - self.prefix_sum[x2+1][y1])
    
    def _mark_cells_removed(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Mark cells as removed (set to 0)."""
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.matrix[i][j] = 0
    
    def _search_from_position(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Recursively search for valid combinations from given position."""
        if not self._is_valid_range(x1, y1, x2, y2):
            return
        
        current_sum = self._get_range_sum_fast(x1, y1, x2, y2)
        
        if current_sum > self.target_sum:
            return
        
        if current_sum == self.target_sum:
            coordinate = (x1, y1, x2, y2)
            if coordinate not in self.operations:
                self._mark_cells_removed(x1, y1, x2, y2)
                self.operations.append(coordinate)
            return
        
        # Try expanding the rectangle
        self._search_from_position(x1, y1, x2 + 1, y2)
        self._search_from_position(x1, y1, x2, y2 + 1)
        self._search_from_position(x1, y1, x2 + 1, y2 + 1)
    
    def solve(self) -> Tuple[int, Operation]:
        """Solve using greedy approach."""
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.matrix[i][j] == 0:
                    continue
                self._search_from_position(i, j, i, j)
        
        total_points = sum(self._calculate_points(*coord) for coord in self.operations)
        return total_points, self.operations


def solve_board_by_chunks(matrix: Matrix, chunk_size: int) -> Operation:
    """
    Solve board by dividing it into chunks.
    
    Args:
        matrix: Game board matrix
        chunk_size: Number of chunks to divide the board into
        
    Returns:
        List of operations to perform
    """
    num_rows = len(matrix)
    chunk_height = num_rows // chunk_size
    all_operations = []
    total_points = 0
    
    for i in range(0, num_rows, chunk_height):
        end_row = min(i + chunk_height, num_rows)
        matrix_chunk = matrix[i:end_row]
        
        solver = OptimalSolver(matrix_chunk)
        max_points, operations = solver.solve()
        total_points += max_points
        
        # Adjust coordinates for the full matrix
        adjusted_operations = []
        for x1, y1, x2, y2 in operations:
            adjusted_operations.append((x1 + i, y1, x2 + i, y2))
        
        all_operations.extend(adjusted_operations)
    
    logger.info(f"Total points from chunked solving: {total_points}")
    return all_operations
