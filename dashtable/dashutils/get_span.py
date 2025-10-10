def get_span(spans, row, column):
    """
    Gets the span containing the [row, column] pair

    Parameters
    ----------
    spans : list of lists of lists
        A list containing spans, which are lists of [row, column] pairs
        that define where a span is inside a table.

    Returns
    -------
    span : list of lists
        A span containing the [row, column] pair
    """
    # PERFORMANCE: Direct comparison instead of creating list and using 'in' operator
    for span in spans:
        for cell in span:
            if cell[0] == row and cell[1] == column:
                return span
    
    return None


