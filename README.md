# bobaka

"bobaka" is my own programming language that was created as a mixture of Haskell and tradiotional imperative languages.

## Description

This project was done for the Compilers course on the Faculty of Computing, Belgrade. We were required to think of a unique grammar for our own language, as well as to write a compiler for it (to a language of choice). The compiler is written in Python, and "bobaka" compiles to Python for simplicity's sake. "bobaka" has support for:

- Arithmetic operations (addition, subtraction, multiplication, division)
- Logical operations (equality, greater, less etc.)
- Most common data types (integer, float, string, boolean)
- Conditionals
- Loops
- Functions
- Libraries
- Input/Output
- Reading from a file

The goal of the project was to be able to compile programs written in "bobaka". The compilation process creates an output Python file and the file can be run instantly, without any changes needed to the code (for the supported operations and syntax).

## Techniques used

- Breaking down the input string on tokens
- Construction of an abstract syntax tree
- Traversal of the abstrax syntax tree (manually implemented, no libraries used)

## Examples

There are 10 examples written in "bobaka" that you can use to see the input/output of the compiler and to get a feel for the structure of the language. The programs do the following:

1. Calculates ideal weight for a male or female person based on input height
2. Checks if sum of digits of an input number is greater than 10
3. Finds maximum out of 4 numbers
4. Calculates the mean for an arbitrary amount of numbers
5. Prints n random numbers from 1 to 100 where n is the input
6. Reads numbers from the input until a negative number comes up, then prints out all the numbers read that are squares
7. Reads a string and puts a '#' between every occurence of a digit followed by a letter, and a '\*' between every occurence of a letter followed by a digit, and outputs the modified string
8. For a given string, the program should produce an output in the following fashion:
   - Input: monkey
   - Output:  
        &nbsp;&nbsp;&nbsp;&nbsp;nk  
       &nbsp;&nbsp;onke  
      monkey  
9. For a given string and integer n, output the same string, but with all words with length greater than n transformed to uppercase.
10. Given a set of words and a file, output the number of occurences in the file for each word given in the set.

## Usage

The compiler can be used by running geterate_trees.py. As mentioned, there are already 10 example programs that can be compiled. In order to select another example for compiling, you should chagne the path variable in geterate_trees.py.
