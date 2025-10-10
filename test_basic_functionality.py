"""
Basic functionality tests to ensure optimizations don't break core features.
Run this after making changes to verify everything still works.
"""
import dashtable


def test_simple_table():
    """Test basic 2x2 table"""
    html = '<table><tr><td>A</td><td>B</td></tr><tr><td>C</td><td>D</td></tr></table>'
    expected = """+---+---+
| A | B |
+---+---+
| C | D |
+---+---+"""
    
    result = dashtable.html2rst(html)
    assert result == expected, f"Simple table failed!\nExpected:\n{expected}\nGot:\n{result}"
    print("✓ Simple table test PASSED")


def test_colspan():
    """Test table with colspan"""
    html = '<table><tr><td colspan="2">Header</td></tr><tr><td>A</td><td>B</td></tr></table>'
    expected = """+--------+
| Header |
+----+---+
| A  | B |
+----+---+"""
    
    result = dashtable.html2rst(html)
    assert result == expected, f"Colspan table failed!\nExpected:\n{expected}\nGot:\n{result}"
    print("✓ Colspan test PASSED")


def test_rowspan():
    """Test table with rowspan"""
    html = '<table><tr><td rowspan="2">Left</td><td>Top</td></tr><tr><td>Bottom</td></tr></table>'
    expected = """+------+--------+
| Left | Top    |
|      +--------+
|      | Bottom |
+------+--------+"""
    
    result = dashtable.html2rst(html)
    assert result == expected, f"Rowspan table failed!\nExpected:\n{expected}\nGot:\n{result}"
    print("✓ Rowspan test PASSED")


def test_colspan_and_rowspan():
    """Test table with both colspan and rowspan"""
    html = '''<table>
        <tr><td colspan="2" rowspan="2">Big</td><td>R1C3</td></tr>
        <tr><td>R2C3</td></tr>
        <tr><td>R3C1</td><td>R3C2</td><td>R3C3</td></tr>
    </table>'''
    
    result = dashtable.html2rst(html)
    # Just verify it doesn't crash and produces some output
    assert len(result) > 0, "Combined colspan/rowspan failed to produce output"
    assert '+' in result and '|' in result, "Combined colspan/rowspan didn't produce table structure"
    print("✓ Combined colspan/rowspan test PASSED")


def test_empty_cells():
    """Test table with empty cells"""
    html = '<table><tr><td></td><td>B</td></tr><tr><td>C</td><td></td></tr></table>'
    
    result = dashtable.html2rst(html)
    assert len(result) > 0, "Empty cells table failed"
    assert '+' in result and '|' in result, "Empty cells didn't produce table structure"
    print("✓ Empty cells test PASSED")


def test_multiline_content():
    """Test table with multi-line content"""
    html = '<table><tr><td>Line1<br/>Line2</td><td>Single</td></tr></table>'
    
    result = dashtable.html2rst(html)
    assert 'Line1' in result and 'Line2' in result, "Multi-line content not preserved"
    print("✓ Multi-line content test PASSED")


if __name__ == "__main__":
    print("Running basic functionality tests...")
    print("=" * 60)
    
    try:
        test_simple_table()
        test_colspan()
        test_rowspan()
        test_colspan_and_rowspan()
        test_empty_cells()
        test_multiline_content()
        
        print("=" * 60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("=" * 60)
    except AssertionError as e:
        print("=" * 60)
        print(f"✗✗✗ TEST FAILED ✗✗✗")
        print("=" * 60)
        print(str(e))
        exit(1)
    except Exception as e:
        print("=" * 60)
        print(f"✗✗✗ UNEXPECTED ERROR ✗✗✗")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
