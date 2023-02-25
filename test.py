from random import randrange

if __name__ == '__main__':
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(l)
    new_l = [l.pop(randrange(len(l))) for _ in range(3)]

    print(l)
    print(new_l)
