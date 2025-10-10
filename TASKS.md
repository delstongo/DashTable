# TASKS - SPATIAL INDEX OPTIMIZATION

## 🔥 MISSION: PROCESS MILLIONS OF SEC FILING TABLES 🔥

**Current Status**: Optimized from 1000s → 6.25s (160x faster)  
**Remaining Bottleneck**: merge_all_cells O(n²) = 5.2s  
**Target**: < 1 second total for MONSTER tables  
**Final Goal**: 500-1000x faster than original, production-ready for MILLIONS of tables

---

## Phase 1: Establish Baseline & Testing Infrastructure ✅

### 1.1 Run Existing Tests
- [ ] Run `tests/runner.py` or discover test command
- [ ] Verify ALL existing tests pass with current optimizations
- [ ] Document any failures and investigate
- [ ] Ensure test infrastructure is working

### 1.2 Analyze Existing Test Coverage
- [ ] Review all files in `tests/static/` 
- [ ] Document what edge cases are already covered
- [ ] Identify gaps in test coverage
- [ ] List complex scenarios NOT currently tested

### 1.3 Create Comprehensive Test Suite for Merge Algorithm
Create `tests/test_merge_all_cells.py` with:

- [ ] **Test: Simple 2x2 grid** - baseline sanity check
- [ ] **Test: Complex nested colspans/rowspans** - from `colspanANDrowspan2.html`
- [ ] **Test: Irregular grid patterns** - cells of varying sizes
- [ ] **Test: Empty cells scattered** - from `empty_cells.html` and `empty2.html`
- [ ] **Test: Maximum complexity** - MONSTER-level table (800+ cells)
- [ ] **Test: Border compatibility edge cases** - varying section counts
- [ ] **Test: Single row table** - boundary condition
- [ ] **Test: Single column table** - boundary condition  
- [ ] **Test: 100+ cell tables** - performance validation
- [ ] **Test: All static files** - convert each .html and validate against .rst
- [ ] **Test: Multiline content** - from `multiple_newlines.html`
- [ ] **Test: Hard test case** - from `hard_test.html`

### 1.4 Create Performance Benchmark Suite
- [ ] Add timing decorators to measure merge_all_cells specifically
- [ ] Create benchmark script that profiles JUST merge operation
- [ ] Establish baseline numbers for comparison
- [ ] Document current performance metrics

---

## Phase 2: Design Spatial Index Architecture 📐

### 2.1 Design Core Data Structure
- [ ] **Define `SpatialIndex` class specification**
  - Grid structure: `Dict[(row, col), Cell]` or better?
  - Cell tracking: Which cells still need processing?
  - Boundary tracking: Min/max row/col for validation
  
- [ ] **Design neighbor lookup API**
  ```python
  def get_neighbor(cell, direction: str) -> Optional[Cell]
  # direction in ['RIGHT', 'LEFT', 'TOP', 'BOTTOM']
  ```

- [ ] **Design incremental update strategy**
  - When cells merge, what grid entries change?
  - How to efficiently remove old cell from grid?
  - How to add merged cell to grid?
  - Track changed cells for re-evaluation

### 2.2 Design Merge Queue Algorithm
- [ ] **Define processing order**
  - Sort by (row, column)? 
  - Left→right, top→bottom?
  - Or different order for optimal merging?
  
- [ ] **Define re-check strategy**
  - After merging A+B, which neighbors need rechecking?
  - Only immediate neighbors? Or wider range?
  - How to avoid infinite loops?
  
- [ ] **Define termination conditions**
  - When are we done? (no more mergeable neighbors)
  - How to detect we're stuck? (safety check)
  - Maximum iteration limit?

- [ ] **Calculate expected complexity**
  - Current: O(n²) = n×n comparisons
  - Target: O(n×k) where k = avg neighbors (~4)
  - For 861 cells: 740,000 → 3,444 ops (215x reduction)

### 2.3 Document Edge Cases & Error Handling
- [ ] What if grid has gaps (missing cells)?
- [ ] What if cells overlap (malformed input)?
- [ ] What if cell has no neighbors (isolated)?
- [ ] What if borders incompatible (different section counts)?
- [ ] What if input is empty list?
- [ ] What if single cell (trivial case)?

### 2.4 Create Design Document
- [ ] Write detailed algorithm pseudocode
- [ ] Draw diagrams of grid structure
- [ ] Document example merge sequence step-by-step
- [ ] Get mental model crystal clear before coding

---

## Phase 3: Implement Spatial Index (INCREMENTAL & CAREFUL) 🛠️

### 3.1 Create New Module Structure
- [ ] Create `dashtable/data2rst/spatial_merge.py`
- [ ] Add module docstring explaining purpose
- [ ] Import necessary dependencies (Cell, merge_cells, get_merge_direction)
- [ ] Set up for easy testing

### 3.2 Implement SpatialIndex Class
- [ ] **`__init__(self, cells: List[Cell])`**
  ```python
  # Build grid mapping (row, col) -> Cell
  # Track all cells that need processing
  # Calculate grid boundaries
  ```
  
- [ ] **`get_neighbor(self, cell: Cell, direction: str) -> Optional[Cell]`**
  ```python
  # Calculate neighbor position based on direction
  # Return cell at that position (or None)
  # Handle edge cases (out of bounds, no cell there)
  ```
  
- [ ] **`update_after_merge(self, merged_cell: Cell, removed_cell: Cell)`**
  ```python
  # Remove removed_cell from all grid positions it occupied
  # Add merged_cell to all grid positions it now occupies
  # Update tracking of cells needing processing
  ```
  
- [ ] **`get_remaining_cells(self) -> List[Cell]`**
  ```python
  # Return unique list of cells still in grid
  ```
  
- [ ] **`is_valid_merge(self, cell1: Cell, cell2: Cell, direction: str) -> bool`**
  ```python
  # Check if cells are actually neighbors in that direction
  # Verify borders are compatible (delegate to get_merge_direction)
  ```

### 3.3 Implement New Merge Algorithm
- [ ] **`merge_all_cells_spatial(cells: List[Cell]) -> str`**
  ```python
  # 1. Build spatial index
  # 2. Create merge queue (sorted by position)
  # 3. While queue not empty:
  #      - Pop cell from queue
  #      - For each direction (RIGHT, BOTTOM, LEFT, TOP):
  #          - Get neighbor
  #          - Check if can merge
  #          - If yes: merge, update index, add affected cells back to queue
  # 4. Return final cell.text
  ```

### 3.4 Preserve Legacy Algorithm
- [ ] Rename current `merge_all_cells` to `merge_all_cells_legacy`
- [ ] Keep it unchanged for comparison
- [ ] Add docstring marking it as legacy/reference implementation
- [ ] Ensure it's still callable for A/B testing

### 3.5 Add Extensive Comments & Logging
- [ ] Comment each major section of algorithm
- [ ] Add debug logging (optional, disabled by default)
- [ ] Document WHY design choices were made
- [ ] Add examples in comments showing grid state

---

## Phase 4: Testing & Validation 🧪

### 4.1 Unit Tests for Spatial Index Components
Create `tests/test_spatial_index.py`:

- [ ] **Test: SpatialIndex initialization** - grid built correctly
- [ ] **Test: get_neighbor RIGHT** - correct cell returned
- [ ] **Test: get_neighbor LEFT** - correct cell returned  
- [ ] **Test: get_neighbor TOP** - correct cell returned
- [ ] **Test: get_neighbor BOTTOM** - correct cell returned
- [ ] **Test: get_neighbor at edge** - returns None appropriately
- [ ] **Test: update_after_merge** - grid state correct after merge
- [ ] **Test: get_remaining_cells** - correct unique list
- [ ] **Test: Empty grid** - handles gracefully
- [ ] **Test: Single cell grid** - trivial case works

### 4.2 Integration Tests - Algorithm Comparison
Create `tests/test_algorithm_comparison.py`:

- [ ] **Test: Run both algorithms on simple table** - outputs match
- [ ] **Test: Run both algorithms on MONSTER table** - outputs match
- [ ] **Test: Run both on ALL static test files** - all outputs match
- [ ] **Test: Character-by-character comparison** - no differences
- [ ] **Test: Edge cases** - both handle same way

### 4.3 Run Comprehensive Test Suite
- [ ] Run all tests from Phase 1.3 with NEW algorithm
- [ ] Ensure 100% pass rate
- [ ] Debug any failures immediately
- [ ] Don't proceed until ALL tests pass

### 4.4 Performance Benchmarking
- [ ] Profile new algorithm with cProfile on MONSTER table
- [ ] Compare timing: old merge vs new merge
- [ ] Target: merge_all_cells < 0.5 seconds (from 5.2s)
- [ ] Document actual speedup achieved
- [ ] Verify O(n) or O(n log n) behavior, NOT O(n²)

### 4.5 Memory Profiling
- [ ] Use memory_profiler to check memory usage
- [ ] Ensure spatial index doesn't leak memory
- [ ] Test on 100 tables in sequence - memory should be stable
- [ ] Document peak memory usage

---

## Phase 5: Integration & Switchover 🔄

### 5.1 Feature Flag Implementation
- [ ] Add `use_spatial_merge=True` parameter to `data2rst()`
- [ ] Wire parameter through to merge function selection
- [ ] Default to `False` initially (legacy algorithm)
- [ ] Add parameter to `html2rst()` as well

### 5.2 Modify merge_all_cells Dispatcher
```python
def merge_all_cells(cells, use_spatial=False):
    if use_spatial:
        return merge_all_cells_spatial(cells)
    else:
        return merge_all_cells_legacy(cells)
```
- [ ] Implement dispatcher function
- [ ] Test both code paths work
- [ ] Verify flag propagates correctly

### 5.3 Code Review Checkpoint ⚠️
- [ ] **Review ALL code changes** - line by line
- [ ] Check for potential bugs (off-by-one, None checks, etc.)
- [ ] Verify error handling (what if merge fails?)
- [ ] Check memory management (references cleaned up?)
- [ ] Look for edge cases not covered by tests
- [ ] Profile one more time

### 5.4 Gradual Rollout
- [ ] Test with spatial=True on 100 random tables
- [ ] Check for any failures or differences
- [ ] If clean: test on 1,000 tables
- [ ] If clean: test on 10,000 tables
- [ ] Monitor for errors, timeouts, or anomalies

### 5.5 Switch Default to Spatial Index
- [ ] Change default: `use_spatial_merge=True`
- [ ] Update all internal calls to use new default
- [ ] Keep legacy code available (but not default)
- [ ] Update documentation to reflect new default

---

## Phase 6: Million Table Validation 🚀

### 6.1 SEC Filing Sample Testing
- [ ] Download sample of 1,000 random SEC XBRL filings
- [ ] Extract all tables from each filing
- [ ] Run batch conversion script
- [ ] Log any failures, errors, or timeouts
- [ ] Analyze failure patterns if any

### 6.2 Stress Testing
- [ ] Process 10,000 tables continuously
- [ ] Monitor memory usage over time (check for leaks)
- [ ] Monitor CPU usage and timing distribution
- [ ] Verify no degradation over time
- [ ] Check for any crashes or hangs

### 6.3 Production Readiness Features
- [ ] Add progress logging for large tables (optional)
  ```python
  # "Merging 861 cells... 50% complete"
  ```
- [ ] Add timeout protection (fail gracefully if > 30s)
- [ ] Add memory limit checks (fail if > 1GB for single table?)
- [ ] Improve error messages for debugging
- [ ] Add retry logic for transient failures?

### 6.4 Long-Running Process Testing
- [ ] Create script that processes tables for 24 hours
- [ ] Monitor memory, CPU, errors continuously  
- [ ] Verify system remains stable
- [ ] Check logs for any warnings or issues
- [ ] Document production deployment recommendations

---

## Phase 7: Cleanup & Documentation 📚

### 7.1 Remove Legacy Code (After Proven Stable)
- [ ] Delete `merge_all_cells_legacy()` function
- [ ] Remove `use_spatial_merge` feature flag
- [ ] Rename `merge_all_cells_spatial` to `merge_all_cells`
- [ ] Clean up any old comments referencing O(n²)
- [ ] Remove performance warnings from code

### 7.2 Update Documentation
- [ ] **Update PERFORMANCE_IMPROVEMENTS.md**
  - Document spatial index algorithm in detail
  - Show before/after performance numbers
  - Explain the optimization strategy
  - Include complexity analysis

- [ ] **Update code docstrings**
  - Document SpatialIndex class thoroughly
  - Explain merge algorithm step by step
  - Add examples showing grid transformations
  
- [ ] **Update README.md**
  - Highlight "Production ready for millions of tables"
  - Show performance characteristics
  - Add benchmarks section
  - Maybe add a badge? 😎

### 7.3 Create Examples & Tutorials
- [ ] Add example showing performance improvement
- [ ] Create tutorial for processing large batches
- [ ] Document best practices for SEC filings
- [ ] Add troubleshooting guide

---

## 🎯 SUCCESS METRICS

### Performance Targets
- ✅ **Phase 1 Complete**: 1000s → 6.25s (160x faster)
- 🎯 **Phase 2-6 Target**: 6.25s → ~1.5s (4x faster, 667x total)
  - merge_all_cells: 5.2s → 0.5s (10x faster)
  - Total: ~1.5s for MONSTER table
- 🏆 **Final Goal**: Process 1 million tables without failure

### Quality Targets
- ✅ All existing tests pass
- ✅ New comprehensive test suite passes  
- ✅ 100% output match vs legacy algorithm
- ✅ No memory leaks over 10,000 tables
- ✅ No performance degradation over time

### Production Readiness
- ✅ Handles malformed input gracefully
- ✅ Timeout protection for pathological cases
- ✅ Clear error messages for debugging
- ✅ Proven stable over 24+ hour runs
- ✅ Documentation complete

---

## 📊 PROGRESS TRACKER

**Phase 1**: ⬜ Not Started  
**Phase 2**: ⬜ Not Started  
**Phase 3**: ⬜ Not Started  
**Phase 4**: ⬜ Not Started  
**Phase 5**: ⬜ Not Started  
**Phase 6**: ⬜ Not Started  
**Phase 7**: ⬜ Not Started  

---

## 🏆 MOTIVATION

**YOU ARE A CHAMPION!**  
**YOU GOT THIS!**  
**LET'S MAKE THIS LIBRARY PROCESS MILLIONS OF TABLES!**  

**THE ENTIRE SEC DATABASE AWAITS!** 🚀🔥💪
