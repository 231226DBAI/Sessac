class mathhead():


    def __init__(self):
        pass
    def factorial(self, n):
        # base case
        if n <= 0: # 1
            return 1
        return n*self.factorial(n-1) # 2

if __name__ == "__main__":
    mh = mathhead()
    for i in range(1, 6):
        print(mh.factorial(i))