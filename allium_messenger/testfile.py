
print(__name__)

def do_thing1():
    print("thing1")
    pass

def do_thing2(x):
    print(f"thing2: x={x}")
    pass

if __name__ == '__main__':
    print("hello")
    do_thing2(3)
    do_thing1()
