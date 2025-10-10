from ..dashutils import get_span
from ..dashutils import get_span_column_count
from ..dashutils import get_longest_line_length

def get_output_column_widths(table, spans):
    """
    Gets the widths of the columns of the output table

    Parameters
    ----------
    table : list of lists of str
        The table of rows of text
    spans : list of lists of int
        The [row, column] pairs of combined cells

    Returns
    -------
    widths : list of int
        The widths of each column in the output table
    """
    # PERFORMANCE: Build lookup cache for get_span() to avoid O(n) lookups
    span_cache = {}
    for span in spans:
        for cell in span:
            span_cache[(cell[0], cell[1])] = span
    
    widths = []
    for column in table[0]:
        widths.append(3)

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = span_cache.get((row, column))
            column_count = get_span_column_count(span)

            if column_count == 1:
                text_row = span[0][0]
                text_column = span[0][1]

                text = table[text_row][text_column]

                length = get_longest_line_length(text)
                if length > widths[column]:
                    widths[column] = length

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = span_cache.get((row, column))
            column_count = get_span_column_count(span)

            if column_count > 1:
                text_row = span[0][0]
                text_column = span[0][1]

                text = table[text_row][text_column]

                end_column = text_column + column_count

                available_space = sum(
                    widths[text_column:end_column])
                available_space += column_count - 1

                length = get_longest_line_length(text)

                # PERFORMANCE: Calculate shortage once instead of incrementing by 1
                if length > available_space:
                    shortage = length - available_space
                    # Distribute shortage evenly across columns
                    per_column = shortage // column_count
                    remainder = shortage % column_count
                    
                    for i in range(text_column, end_column):
                        widths[i] += per_column
                        # Add 1 more to first 'remainder' columns
                        if i - text_column < remainder:
                            widths[i] += 1
    return widths
