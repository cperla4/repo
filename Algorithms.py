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
