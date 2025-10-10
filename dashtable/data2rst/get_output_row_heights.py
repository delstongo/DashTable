from ..dashutils import get_span
from ..dashutils import get_span_row_count


def get_output_row_heights(table, spans):
    """
    Get the heights of the rows of the output table.

    Parameters
    ----------
    table : list of lists of str
    spans : list of lists of int

    Returns
    -------
    heights : list of int
        The heights of each row in the output table
    """
    # PERFORMANCE: Build lookup cache for get_span() to avoid O(n) lookups
    span_cache = {}
    for span in spans:
        for cell in span:
            span_cache[(cell[0], cell[1])] = span
    
    heights = []
    for row in table:
        heights.append(-1)

    for row in range(len(table)):
        for column in range(len(table[row])):
            text = table[row][column]
            span = span_cache.get((row, column))
            row_count = get_span_row_count(span)
            height = len(text.split('\n'))
            if row_count == 1 and height > heights[row]:
                heights[row] = height

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = span_cache.get((row, column))
            row_count = get_span_row_count(span)
            if row_count > 1:
                text_row = span[0][0]
                text_column = span[0][1]

                end_row = text_row + row_count

                text = table[text_row][text_column]

                height = len(text.split('\n')) - (row_count - 1)

                # PERFORMANCE: Calculate shortage once instead of incrementing by 1
                current_height = sum(heights[text_row:end_row])
                if height > current_height:
                    shortage = height - current_height
                    # Distribute shortage evenly across rows
                    per_row = shortage // row_count
                    remainder = shortage % row_count
                    
                    for i in range(text_row, end_row):
                        heights[i] += per_row
                        # Add 1 more to first 'remainder' rows
                        if i - text_row < remainder:
                            heights[i] += 1
    return heights
