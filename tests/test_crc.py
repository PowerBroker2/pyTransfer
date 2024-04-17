import pytest

from pySerialTransfer.CRC import CRC
from io import StringIO
import sys


def test_crc_init():
    """Test the initialization of the CRC class."""
    crc = CRC()
    assert crc.poly == 0x9B
    assert crc.crc_len == 8
    assert crc.table_len == 256
    assert len(crc.cs_table) == 256


def test_crc_poly():
    """Test the initialization of the CRC class with a custom polynomial."""
    polynomial = 0x8C
    crc = CRC(polynomial)
    assert crc.poly == polynomial & 0xFF
    assert crc.crc_len == 8
    assert crc.table_len == 256
    assert len(crc.cs_table) == 256


#  Note: The CRC class has no upper limit on the crc_len parameter, but attempting to use a value greater than 32 hangs
#  the test. The CRC class should be updated to handle this case.
@pytest.mark.parametrize('crc_len', [4, 8, 16])    
def test_custom_positive_crc_len(crc_len):
    """Test the initialization of the CRC class with a custom crc length."""
    expected_table_len = pow(2, crc_len)
    crc = CRC(crc_len=crc_len)
    assert crc.table_len == expected_table_len
    assert len(crc.cs_table) == expected_table_len


def test_crc_calculate():
    """Test the calculate method of the CRC class returns an integer."""
    crc = CRC()
    result = crc.calculate([0x31])
    assert isinstance(result, int)


def test_calculate_with_int_list_no_dist():
    crc_instance = CRC()
    arr = [0x31, 0x32, 0x33, 0x34, 0x35]
    expected_output = 218
    result = crc_instance.calculate(arr)
    assert result == expected_output


def test_calculate_with_int_list_with_dist():
    crc_instance = CRC()
    arr = [0x31, 0x32, 0x33, 0x34, 0x35]
    dist = 3
    expected_output = 209
    result = crc_instance.calculate(arr, dist)
    assert result == expected_output


def test_calculate_with_char_list_no_dist():
    crc_instance = CRC()
    arr = ["1", "2", "3", "4", "5"]
    expected_output = 128
    result = crc_instance.calculate(arr)
    assert result == expected_output


def test_calculate_with_char_list_with_dist():
    crc_instance = CRC()
    arr = ["1", "2", "3", "4", "5"]
    dist = 3
    expected_output = 68
    result = crc_instance.calculate(arr, dist)
    assert result == expected_output


def test_calculate_with_int_no_dist():
    crc_instance = CRC()
    arr = 0x31
    expected_output = 205
    result = crc_instance.calculate(arr)
    assert result == expected_output


def test_calculate_with_non_int_no_dist():
    crc_instance = CRC()
    arr = ["a", "b", "c", "d", "e"]
    expected_output = 52
    result = crc_instance.calculate(arr)
    assert result == expected_output
    

def test_calculate_with_non_int_with_dist():
    crc_instance = CRC()
    arr = ["a", "b", "c", "d", "e"]
    dist = 3
    expected_output = 245
    result = crc_instance.calculate(arr, dist)
    assert result == expected_output


# TODO: Handle this case in the calculate method   
@pytest.mark.xfail(reason="not currently handled in the calculate method")   
def test_calculate_with_dist_greater_than_list_length():
    crc_instance = CRC()
    arr = [0x31, 0x32, 0x33, 0x34, 0x35]
    dist = 10
    expected_output = 218
    result = crc_instance.calculate(arr, dist)
    assert result == expected_output


def test_print_table():
    """Test the print_table method of the CRC class."""
    # Create an instance of CRC
    crc_instance = CRC()

    # Redirect stdout to a buffer
    stdout = sys.stdout
    sys.stdout = StringIO()

    # Call the method
    crc_instance.print_table()

    # Get the output and restore stdout
    output = sys.stdout.getvalue()
    sys.stdout = stdout

    # Prepare the expected output for the default length of 8
    expected_output = """
0x0 0x9B 0xAD 0x36 0xC1 0x5A 0x6C 0xF7 0x19 0x82 0xB4 0x2F 0xD8 0x43 0x75 0xEE
0x32 0xA9 0x9F 0x4 0xF3 0x68 0x5E 0xC5 0x2B 0xB0 0x86 0x1D 0xEA 0x71 0x47 0xDC
0x64 0xFF 0xC9 0x52 0xA5 0x3E 0x8 0x93 0x7D 0xE6 0xD0 0x4B 0xBC 0x27 0x11 0x8A
0x56 0xCD 0xFB 0x60 0x97 0xC 0x3A 0xA1 0x4F 0xD4 0xE2 0x79 0x8E 0x15 0x23 0xB8
0xC8 0x53 0x65 0xFE 0x9 0x92 0xA4 0x3F 0xD1 0x4A 0x7C 0xE7 0x10 0x8B 0xBD 0x26
0xFA 0x61 0x57 0xCC 0x3B 0xA0 0x96 0xD 0xE3 0x78 0x4E 0xD5 0x22 0xB9 0x8F 0x14
0xAC 0x37 0x1 0x9A 0x6D 0xF6 0xC0 0x5B 0xB5 0x2E 0x18 0x83 0x74 0xEF 0xD9 0x42
0x9E 0x5 0x33 0xA8 0x5F 0xC4 0xF2 0x69 0x87 0x1C 0x2A 0xB1 0x46 0xDD 0xEB 0x70
0xB 0x90 0xA6 0x3D 0xCA 0x51 0x67 0xFC 0x12 0x89 0xBF 0x24 0xD3 0x48 0x7E 0xE5
0x39 0xA2 0x94 0xF 0xF8 0x63 0x55 0xCE 0x20 0xBB 0x8D 0x16 0xE1 0x7A 0x4C 0xD7
0x6F 0xF4 0xC2 0x59 0xAE 0x35 0x3 0x98 0x76 0xED 0xDB 0x40 0xB7 0x2C 0x1A 0x81
0x5D 0xC6 0xF0 0x6B 0x9C 0x7 0x31 0xAA 0x44 0xDF 0xE9 0x72 0x85 0x1E 0x28 0xB3
0xC3 0x58 0x6E 0xF5 0x2 0x99 0xAF 0x34 0xDA 0x41 0x77 0xEC 0x1B 0x80 0xB6 0x2D
0xF1 0x6A 0x5C 0xC7 0x30 0xAB 0x9D 0x6 0xE8 0x73 0x45 0xDE 0x29 0xB2 0x84 0x1F
0xA7 0x3C 0xA 0x91 0x66 0xFD 0xCB 0x50 0xBE 0x25 0x13 0x88 0x7F 0xE4 0xD2 0x49
0x95 0xE 0x38 0xA3 0x54 0xCF 0xF9 0x62 0x8C 0x17 0x21 0xBA 0x4D 0xD6 0xE0 0x7B
""".lstrip()

    # Assert that the output matches the expected output
    assert output == expected_output
    

def test_calculate_with_empty_list():
    """Test that the calculate method returns 0 when an empty list is passed."""
    crc_instance = CRC()
    arr = []
    result = crc_instance.calculate(arr)
    assert result == 0


# TODO: Handle this case in the calculate method   
@pytest.mark.xfail(reason="not currently handled in the calculate method") 
def test_calculate_with_negative_dist():
    """Test that the calculate method raises a ValueError when the dist parameter is negative."""
    crc_instance = CRC()
    arr = [0x31, 0x32, 0x33, 0x34, 0x35]
    dist = -1
    with pytest.raises(ValueError):
        crc_instance.calculate(arr, dist)

        
def test_calculate_with_string_input():
    """Test that the calculate method can handle a string input."""
    crc_instance = CRC()
    arr = "abc"
    result = crc_instance.calculate(arr)
    assert result == 245


def test_calculate_with_list_of_mixed_types():
    """Test that the calculate method can handle a list of mixed types."""
    crc_instance = CRC()
    arr = [0x31, "a", 0x33, "b", 0x35]
    result = crc_instance.calculate(arr)
    assert result == 254
