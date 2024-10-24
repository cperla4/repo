#Diagnol Difference
def diagonalDifference(arr):
    r = 0
    lf = 0
    n = len(arr)
    for i in range(0, n):
        r += arr[i][i]
        lf += arr[i][n - i - 1]
    return abs(r - lf)

#Matching First and Last in array
def first_last6(nums):
    return (nums[0] == 6 or nums[len(nums)-1] == 6)

#Comparing 3 conditions through 2 arrays
def compareTriplets(a, b):    
    i = 0
    alice_points = 0
    bob_points = 0
    while i < len(a):
        if a[i] > b[i]:
            alice_points += 1
        elif a[i] < b[i]:
            bob_points += 1
        i += 1
    return f'{alice_points}{bob_points}'

#Grabbing Count of element within a string
def count_example(str):
    return str.count('example')

#Same example of the one above without the [count] function
def count_example_alt(str):
    sum = 0
    ## Loop to length-1 and access index i and i+1
    ## in the loop.
    for i in range(len(str)-1):
        if str[i:i+2] == 'example':
            sum = sum + 1
    return sum

#Find max and print max only in the array
def arr(nums):
    find_max = max(nums)
    return [find_max for _ in nums]
