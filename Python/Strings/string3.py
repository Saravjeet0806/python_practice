#strings are immutable

name = "Saravjeet"  

print(name.lower())
print(name.upper())

name = "Boy!!!!!!!!"
#to string ! we use rstrip // only for trailing
print(name.rstrip("!"))

name = "              Catasourous          "
print(name.strip())  #removes leading and trailing white spaces

print(name.replace("Catasourous", "Saravjeet"))

str1 = "hello everyone today is a beautiful day"
print(str1.split(" ")) #split according to whitespace 
print(str1.capitalize()) ##only first character to capital and others to lower

print(str1.count('a')) #return count
print(str1.count('hello'))

print(str1.find("hello")) #0 is the first index of the first occurrence
print(str1.title())  #each word capital of a string