#######################
# Script by Forestcat #
#######################

"""
This Script checks if a String is palindrome and returns True or False.
At the Bottom you have an example of the Function
Have fun and enjoy!
"""



def is_palindrome(string):
    for pos,i in enumerate(reversed(string)):
        if pos == 0:
            reversed_string = i
        else:
            reversed_string = reversed_string + i

    if string == reversed_string:
        return True
    else:
        return False

print(is_palindrome("racecar"))
# print("racecar" == "racecar"[::-1]) # Faster and cleaner way ^^
