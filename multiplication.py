def multiplication(num):
    return 0 if num < 10 else 1 + multiplication(eval("*".join(str(num))))
    
print(multiplication(999))