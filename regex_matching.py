"""
Regular Expression Matching - LeetCode Problem 10

Problem Statement:
Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
- '.' Matches any single character
- '*' Matches zero or more of the preceding element
- The matching should cover the entire input string (not partial)

This is a classic dynamic programming problem that can be solved in multiple ways.
"""

def isMatch_recursive(s, p):
    """
    Recursive solution - easier to understand but less efficient
    
    Time Complexity: O(2^(m+n)) in worst case
    Space Complexity: O(m+n) for recursion stack
    """
    def match(s_index, p_index):
        # Base case: if pattern is exhausted
        if p_index == len(p):
            return s_index == len(s)
        
        # Check if current characters match (including '.' for any character)
        first_match = (s_index < len(s) and 
                      (p[p_index] == s[s_index] or p[p_index] == '.'))
        
        # If next character is '*', we have two choices:
        if p_index + 1 < len(p) and p[p_index + 1] == '*':
            # Choice 1: Use '*' to match zero characters (skip current pattern)
            # Choice 2: Use '*' to match one or more characters (if first_match)
            return (match(s_index, p_index + 2) or  # Skip the '*' pattern
                    (first_match and match(s_index + 1, p_index)))  # Use '*' to match
        else:
            # No '*', just match current character and move both pointers
            return first_match and match(s_index + 1, p_index + 1)
    
    return match(0, 0)


def isMatch_dp(s, p):
    """
    Dynamic Programming solution - more efficient
    
    Time Complexity: O(m * n) where m = len(s), n = len(p)
    Space Complexity: O(m * n)
    """
    m, n = len(s), len(p)
    
    # dp[i][j] represents whether s[0:i] matches p[0:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    # Base case: empty string matches empty pattern
    dp[0][0] = True
    
    # Handle patterns like "a*", "a*b*", "a*b*c*" that can match empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Case 1: '*' matches zero characters (skip the pattern before '*')
                dp[i][j] = dp[i][j - 2]
                
                # Case 2: '*' matches one or more characters
                if s[i - 1] == p[j - 2] or p[j - 2] == '.':
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            else:
                # No '*', just check if current characters match
                if s[i - 1] == p[j - 1] or p[j - 1] == '.':
                    dp[i][j] = dp[i - 1][j - 1]
    
    return dp[m][n]


def isMatch_dp_optimized(s, p):
    """
    Space-optimized DP solution using only two rows
    
    Time Complexity: O(m * n)
    Space Complexity: O(n)
    """
    m, n = len(s), len(p)
    
    # Use only two rows: previous and current
    prev = [False] * (n + 1)
    curr = [False] * (n + 1)
    
    # Base case
    prev[0] = True
    
    # Handle patterns that can match empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            prev[j] = prev[j - 2]
    
    for i in range(1, m + 1):
        curr[0] = False  # Empty pattern can't match non-empty string
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                curr[j] = curr[j - 2]  # Match zero characters
                if s[i - 1] == p[j - 2] or p[j - 2] == '.':
                    curr[j] = curr[j] or prev[j]  # Match one or more
            else:
                if s[i - 1] == p[j - 1] or p[j - 1] == '.':
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = False
        
        # Swap rows for next iteration
        prev, curr = curr, prev
    
    return prev[n]


def test_solutions():
    """Test all solutions with various test cases"""
    test_cases = [
        # (string, pattern, expected_result, description)
        ("aa", "a", False, "Pattern 'a' doesn't match 'aa'"),
        ("aa", "a*", True, "Pattern 'a*' matches 'aa' (a repeated twice)"),
        ("ab", ".*", True, "Pattern '.*' matches 'ab' (any char repeated)"),
        ("aab", "c*a*b", True, "Pattern 'c*a*b' matches 'aab' (c* matches 0, a* matches 2)"),
        ("mississippi", "mis*is*p*.", False, "Complex pattern that doesn't match"),
        ("", "a*", True, "Empty string matches 'a*' (zero occurrences)"),
        ("", ".*", True, "Empty string matches '.*' (zero occurrences)"),
        ("a", "ab*", True, "Pattern 'ab*' matches 'a' (b* matches zero)"),
        ("ab", ".*c", False, "Pattern '.*c' doesn't match 'ab'"),
        ("aaa", "a*a", True, "Pattern 'a*a' matches 'aaa'"),
    ]
    
    solutions = [
        ("Recursive", isMatch_recursive),
        ("DP", isMatch_dp),
        ("DP Optimized", isMatch_dp_optimized)
    ]
    
    print("Testing Regular Expression Matching Solutions")
    print("=" * 50)
    
    for i, (s, p, expected, description) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {description}")
        print(f"String: '{s}', Pattern: '{p}', Expected: {expected}")
        
        for name, func in solutions:
            try:
                result = func(s, p)
                status = "✓ PASS" if result == expected else "✗ FAIL"
                print(f"  {name:12}: {result:5} {status}")
            except Exception as e:
                print(f"  {name:12}: ERROR - {e}")


def explain_step_by_step(s, p):
    """
    Explain the matching process step by step for educational purposes
    """
    print(f"\nStep-by-Step Explanation for: s='{s}', p='{p}'")
    print("=" * 50)
    
    def match_with_explanation(s_index, p_index, depth=0):
        indent = "  " * depth
        print(f"{indent}Checking: s[{s_index}:]='{s[s_index:]}', p[{p_index}:]='{p[p_index:]}'")
        
        if p_index == len(p):
            result = s_index == len(s)
            print(f"{indent}→ Pattern exhausted. String also exhausted? {result}")
            return result
        
        first_match = (s_index < len(s) and 
                      (p[p_index] == s[s_index] or p[p_index] == '.'))
        print(f"{indent}→ First character match? {first_match}")
        
        if p_index + 1 < len(p) and p[p_index + 1] == '*':
            print(f"{indent}→ Found '*', trying two options:")
            
            # Option 1: Skip the '*' pattern
            print(f"{indent}  Option 1: Skip '*' (match zero characters)")
            result1 = match_with_explanation(s_index, p_index + 2, depth + 1)
            
            # Option 2: Use '*' to match
            if first_match:
                print(f"{indent}  Option 2: Use '*' (match one character, keep pattern)")
                result2 = match_with_explanation(s_index + 1, p_index, depth + 1)
                result = result1 or result2
            else:
                print(f"{indent}  Option 2: Skip (first_match=False)")
                result = result1
        else:
            print(f"{indent}→ No '*', simple character match")
            result = first_match and match_with_explanation(s_index + 1, p_index + 1, depth + 1)
        
        print(f"{indent}→ Result: {result}")
        return result
    
    return match_with_explanation(0, 0)


if __name__ == "__main__":
    # Run tests
    test_solutions()
    
    # Show step-by-step explanation for a simple case
    print("\n" + "="*60)
    explain_step_by_step("aa", "a*")
    
    print("\n" + "="*60)
    explain_step_by_step("ab", ".*")
