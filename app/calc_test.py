def calculate_average(total, count):
    """
    Calculates the average of a total sum over a given count.

    Args:
        total (int or float): The sum of all values.
        count (int or float): The number of values.

    Returns:
        float: The calculated average.

    Raises:
        TypeError: If total or count are not numbers.
        ValueError: If count is zero or negative, as an average requires a positive count.
    """
    if not isinstance(total, (int, float)):
        raise TypeError("Total must be a number.")
    if not isinstance(count, (int, float)):
        raise TypeError("Count must be a number.")

    if count <= 0:
        raise ValueError("Count must be a positive number to calculate an average.")
    
    return total / count

if __name__ == '__main__':
    import math

    print("Running tests for calculate_average...")

    # Test Case 1: Basic positive integers
    try:
        result = calculate_average(10, 2)
        assert result == 5.0, f"Test Case 1 Failed: Expected 5.0, Got {result}"
        print(f"Test Case 1 Passed: calculate_average(10, 2) = {result}")
    except Exception as e:
        print(f"Test Case 1 Failed with exception: {e}")

    # Test Case 2: Total is zero
    try:
        result = calculate_average(0, 5)
        assert result == 0.0, f"Test Case 2 Failed: Expected 0.0, Got {result}"
        print(f"Test Case 2 Passed: calculate_average(0, 5) = {result}")
    except Exception as e:
        print(f"Test Case 2 Failed with exception: {e}")

    # Test Case 3: Floating point numbers
    try:
        result = calculate_average(7.5, 2.5)
        assert result == 3.0, f"Test Case 3 Failed: Expected 3.0, Got {result}"
        print(f"Test Case 3 Passed: calculate_average(7.5, 2.5) = {result}")
    except Exception as e:
        print(f"Test Case 3 Failed with exception: {e}")

    # Test Case 4: Negative total
    try:
        result = calculate_average(-10, 2)
        assert result == -5.0, f"Test Case 4 Failed: Expected -5.0, Got {result}"
        print(f"Test Case 4 Passed: calculate_average(-10, 2) = {result}")
    except Exception as e:
        print(f"Test Case 4 Failed with exception: {e}")

    # Test Case 5: Edge case - count is 1
    try:
        result = calculate_average(100, 1)
        assert result == 100.0, f"Test Case 5 Failed: Expected 100.0, Got {result}"
        print(f"Test Case 5 Passed: calculate_average(100, 1) = {result}")
    except Exception as e:
        print(f"Test Case 5 Failed with exception: {e}")

    # Test Case 6: Aggressive test - count is 0 (should raise ValueError)
    try:
        calculate_average(10, 0)
        print("Test Case 6 Failed: Expected ValueError for count = 0, but no exception was raised.")
    except ValueError as e:
        assert "Count must be a positive number" in str(e), f"Test Case 6 Failed: Expected specific ValueError message, Got {e}"
        print(f"Test Case 6 Passed: Caught expected ValueError for count = 0: {e}")
    except Exception as e:
        print(f"Test Case 6 Failed: Caught unexpected exception for count = 0: {type(e).__name__}: {e}")

    # Test Case 7: Aggressive test - count is negative (should raise ValueError)
    try:
        calculate_average(10, -2)
        print("Test Case 7 Failed: Expected ValueError for negative count, but no exception was raised.")
    except ValueError as e:
        assert "Count must be a positive number" in str(e), f"Test Case 7 Failed: Expected specific ValueError message, Got {e}"
        print(f"Test Case 7 Passed: Caught expected ValueError for negative count: {e}")
    except Exception as e:
        print(f"Test Case 7 Failed: Caught unexpected exception for negative count: {type(e).__name__}: {e}")

    # Test Case 8: Aggressive test - total is not a number (should raise TypeError)
    try:
        calculate_average("abc", 5)
        print("Test Case 8 Failed: Expected TypeError for non-numeric total, but no exception was raised.")
    except TypeError as e:
        assert "Total must be a number" in str(e), f"Test Case 8 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 8 Passed: Caught expected TypeError for non-numeric total: {e}")
    except Exception as e:
        print(f"Test Case 8 Failed: Caught unexpected exception for non-numeric total: {type(e).__name__}: {e}")

    # Test Case 9: Aggressive test - count is not a number (should raise TypeError)
    try:
        calculate_average(10, "xyz")
        print("Test Case 9 Failed: Expected TypeError for non-numeric count, but no exception was raised.")
    except TypeError as e:
        assert "Count must be a number" in str(e), f"Test Case 9 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 9 Passed: Caught expected TypeError for non-numeric count: {e}")
    except Exception as e:
        print(f"Test Case 9 Failed: Caught unexpected exception for non-numeric count: {type(e).__name__}: {e}")

    # Test Case 10: Large numbers
    try:
        result = calculate_average(1_000_000, 100)
        assert result == 10000.0, f"Test Case 10 Failed: Expected 10000.0, Got {result}"
        print(f"Test Case 10 Passed: calculate_average(1_000_000, 100) = {result}")
    except Exception as e:
        print(f"Test Case 10 Failed with exception: {e}")

    # --- Additional Aggressive Test Cases (from original prompt) ---

    # Test Case 11: Negative float total, positive float count
    try:
        result = calculate_average(-7.5, 2.5)
        assert result == -3.0, f"Test Case 11 Failed: Expected -3.0, Got {result}"
        print(f"Test Case 11 Passed: calculate_average(-7.5, 2.5) = {result}")
    except Exception as e:
        print(f"Test Case 11 Failed with exception: {e}")

    # Test Case 12: Very small positive float count (close to zero, but valid)
    try:
        result = calculate_average(10, 0.000001)
        assert abs(result - 10_000_000.0) < 1e-9, f"Test Case 12 Failed: Expected 10_000_000.0, Got {result}"
        print(f"Test Case 12 Passed: calculate_average(10, 0.000001) = {result}")
    except Exception as e:
        print(f"Test Case 12 Failed with exception: {e}")

    # Test Case 13: Boolean total (False, which is 0 in numeric context)
    try:
        result = calculate_average(False, 5)
        assert result == 0.0, f"Test Case 13 Failed: Expected 0.0, Got {result}"
        print(f"Test Case 13 Passed: calculate_average(False, 5) = {result}")
    except Exception as e:
        print(f"Test Case 13 Failed with exception: {e}")

    # Test Case 14: Boolean total (True, which is 1 in numeric context)
    try:
        result = calculate_average(True, 1)
        assert result == 1.0, f"Test Case 14 Failed: Expected 1.0, Got {result}"
        print(f"Test Case 14 Passed: calculate_average(True, 1) = {result}")
    except Exception as e:
        print(f"Test Case 14 Failed with exception: {e}")

    # Test Case 15: Mixed types - int total, float count
    try:
        result = calculate_average(10, 2.5)
        assert result == 4.0, f"Test Case 15 Failed: Expected 4.0, Got {result}"
        print(f"Test Case 15 Passed: calculate_average(10, 2.5) = {result}")
    except Exception as e:
        print(f"Test Case 15 Failed with exception: {e}")

    # Test Case 16: Mixed types - float total, int count
    try:
        result = calculate_average(7.5, 3)
        assert result == 2.5, f"Test Case 16 Failed: Expected 2.5, Got {result}"
        print(f"Test Case 16 Passed: calculate_average(7.5, 3) = {result}")
    except Exception as e:
        print(f"Test Case 16 Failed with exception: {e}")

    # --- NEW AGGRESSIVE TEST CASES ---

    # Test Case 17: Aggressive test - total is None (should raise TypeError)
    try:
        calculate_average(None, 5)
        print("Test Case 17 Failed: Expected TypeError for None total, but no exception was raised.")
    except TypeError as e:
        assert "Total must be a number" in str(e), f"Test Case 17 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 17 Passed: Caught expected TypeError for None total: {e}")
    except Exception as e:
        print(f"Test Case 17 Failed: Caught unexpected exception for None total: {type(e).__name__}: {e}")

    # Test Case 18: Aggressive test - count is None (should raise TypeError)
    try:
        calculate_average(10, None)
        print("Test Case 18 Failed: Expected TypeError for None count, but no exception was raised.")
    except TypeError as e:
        assert "Count must be a number" in str(e), f"Test Case 18 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 18 Passed: Caught expected TypeError for None count: {e}")
    except Exception as e:
        print(f"Test Case 18 Failed: Caught unexpected exception for None count: {type(e).__name__}: {e}")

    # Test Case 19: Aggressive test - total is a complex number (should raise TypeError)
    try:
        calculate_average(3 + 4j, 5)
        print("Test Case 19 Failed: Expected TypeError for complex total, but no exception was raised.")
    except TypeError as e:
        assert "Total must be a number" in str(e), f"Test Case 19 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 19 Passed: Caught expected TypeError for complex total: {e}")
    except Exception as e:
        print(f"Test Case 19 Failed: Caught unexpected exception for complex total: {type(e).__name__}: {e}")

    # Test Case 20: Aggressive test - count is a complex number (should raise TypeError)
    try:
        calculate_average(10, 1 + 2j)
        print("Test Case 20 Failed: Expected TypeError for complex count, but no exception was raised.")
    except TypeError as e:
        assert "Count must be a number" in str(e), f"Test Case 20 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 20 Passed: Caught expected TypeError for complex count: {e}")
    except Exception as e:
        print(f"Test Case 20 Failed: Caught unexpected exception for complex count: {type(e).__name__}: {e}")

    # Test Case 21: Aggressive test - total is a list (should raise TypeError)
    try:
        calculate_average([1, 2, 3], 3)
        print("Test Case 21 Failed: Expected TypeError for list total, but no exception was raised.")
    except TypeError as e:
        assert "Total must be a number" in str(e), f"Test Case 21 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 21 Passed: Caught expected TypeError for list total: {e}")
    except Exception as e:
        print(f"Test Case 21 Failed: Caught unexpected exception for list total: {type(e).__name__}: {e}")

    # Test Case 22: Aggressive test - count is a tuple (should raise TypeError)
    try:
        calculate_average(10, (1, 2))
        print("Test Case 22 Failed: Expected TypeError for tuple count, but no exception was raised.")
    except TypeError as e:
        assert "Count must be a number" in str(e), f"Test Case 22 Failed: Expected specific TypeError message, Got {e}"
        print(f"Test Case 22 Passed: Caught expected TypeError for tuple count: {e}")
    except Exception as e:
        print(f"Test Case 22 Failed: Caught unexpected exception for tuple count: {type(e).__name__}: {e}")

    # Test Case 23: Resulting in a non-terminating decimal (check with epsilon)
    try:
        result = calculate_average(1, 3)
        expected = 1/3
        assert abs(result - expected) < 1e-9, f"Test Case 23 Failed: Expected {expected}, Got {result}"
        print(f"Test Case 23 Passed: calculate_average(1, 3) = {result}")
    except Exception as e:
        print(f"Test Case 23 Failed with exception: {e}")

    # Test Case 24: Very large total, very small count, resulting in a very large float
    # (Python handles this, but good to test the limits before inf)
    try:
        large_total = 1e300 # A very large float
        small_count = 1e-300 # A very small float
        result = calculate_average(large_total, small_count)
        expected = large_total / small_count # Should be 1e600, which is inf
        assert math.isinf(result), f"Test Case 24 Failed: Expected inf, Got {result}"
        print(f"Test Case 24 Passed: calculate_average({large_total}, {small_count}) = {result}")
    except Exception as e:
        print(f"Test Case 24 Failed with exception: {e}")

    # Test Case 25: Negative total, very small positive float count
    try:
        result = calculate_average(-10, 0.0000001)
        assert abs(result - -100_000_000.0) < 1e-9, f"Test Case 25 Failed: Expected -100_000_000.0, Got {result}"
        print(f"Test Case 25 Passed: calculate_average(-10, 0.0000001) = {result}")
    except Exception as e:
        print(f"Test Case 25 Failed with exception: {e}")

    print("\nAll tests completed.")