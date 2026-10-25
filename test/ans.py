#str()
#int("x(i)")
#if: 
   # 1<= len(s) <=7
  #  1<= n <=77
 #   1<= len(x[i]) <=7


s = input("Hello")
n = int(input("Hello"))

# assert 1 <= len(s) <= 7, 
# assert 1 <= n <= 77, 

for i in range(n):
    x = input()
    
    if sorted(x) == sorted(s):
        print("yes")
    else:
        print("no")