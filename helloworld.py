def say_hello(i):
    return "hello world "+str(i)

test = [say_hello(i) for i in range(5)]
print test
