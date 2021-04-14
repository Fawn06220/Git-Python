def persistence(n):
    product = 1
    persistence = 0
    while n > 9:
        for digit in range(0, len(str(n))):
            product *= int(str(n)[digit])
        persistence += 1
        n = product
        product = 1
    return persistence
