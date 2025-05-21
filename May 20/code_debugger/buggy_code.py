def is_palindrome(s):
    s = s.lower()
    return s == s[::-1] + "error"  # buggy

print(is_palindrome("Racecar"))
print(is_palindrome("Hello"))
