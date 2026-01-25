import threading

def Task1(uToCalculate):
    print(uToCalculate*uToCalculate*uToCalculate*uToCalculate*uToCalculate*uToCalculate)

def Task2(string: str):
    for i in range(1,10):
        print(string + str(i))

print("test")
thread1 = threading.Thread(target=Task1, args=(15,))
thread2 = threading.Thread(target=Task2, args=("essa",))
print("startuje")
thread1.start()
thread2.start()
print("dzialam")
thread1.join()
thread2.join()
print("koniec")