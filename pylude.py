# basic
Identity = lambda x: x;
Flip = lambda f: lambda x: lambda y: f (y) (x);
Compose = lambda f: lambda g: lambda x: f (g (x))

# booleans
true = lambda x: lambda _: x;
false = lambda _: lambda y: y;
FromPythonBool = lambda b: true if b else false;

# if
If = lambda c: lambda x: lambda y: c (x) (y);

# logical operators
Not = lambda x: Flip (x);
And = lambda x: lambda y: x (y) (false);
Or = lambda x: lambda y: x (true) (y);

# constants
Empty = lambda: ();
Zero = lambda: 0;
One = lambda: 1;

# comparisions
Eq = lambda x: lambda y: FromPythonBool (x == y);
Gt = lambda x: lambda y: FromPythonBool (x > y);
Lt = lambda x: lambda y: FromPythonBool (x < y);

# arithmetic
Add = lambda x: lambda y: x + y;
Subtract = lambda x: lambda y: x - y;
Multiply = lambda x: lambda y: x * y;
Divide = lambda x: lambda y: x / y;
FloorDivide = lambda x: lambda y: x // y;
Modulo = lambda x: lambda y: x % y;

# atom / singleton
Atom = Singleton = lambda x: (x,);

# join
Join = lambda x: lambda y: x + y;

# step
Step = lambda x: Join (x) (One ());

# head, tail
Head = lambda xs: xs[0];
Tail = lambda xs: xs[1:];

# last, init
Last = lambda xs: xs[-1]
Init = lambda xs: xs[:-1]

# left fold
Foldl = lambda f: lambda acc: lambda xs: If (Eq (xs) (Empty ())) (lambda: acc) (lambda: Foldl (f) (f (acc) (Head (xs))) (Tail (xs))) ();
assert Foldl (Divide) (1) ((10,5,2)) == 0.01;

# right fold
Foldr = lambda f: lambda acc: lambda xs: If (Eq (xs) (Empty ())) (lambda: acc) (lambda: Foldr (f) (f (Last (xs)) (acc)) (Init (xs))) ();
assert Foldr (Divide) (1) ((10,5,2)) == 4.0;

# reduce
Reduce = lambda f: lambda x: Foldl (f) (Head (x)) (Tail (x));
assert Reduce (Add) ((1,2,3)) == 6

# filter
FilterRecursion = lambda f: lambda xs: If (Eq (xs) (Empty ())) (Empty) (lambda: Join (If (f (Head (xs))) (lambda: Atom (Head (xs))) (Empty) ()) (FilterRecursion (f) (Tail (xs)))) ();
FilterFoldl = lambda f: lambda xs: Foldl (lambda acc: lambda x: If (f (x)) (Join (acc) (Atom (x))) (acc)) (Empty ()) (xs);
Filter = FilterRecursion
assert FilterRecursion (lambda x: Eq (Modulo (x) (2)) (Zero ())) ((1,2,3,4)) == FilterFoldl (lambda x: Eq (Modulo (x) (2)) (Zero ())) ((1,2,3,4)) == (2,4);

# map
MapRecursion = lambda f: lambda xs: If (Eq (xs) (Empty ())) (Empty) (lambda: Join (Atom((f (Head (xs))))) (MapRecursion (f) (Tail (xs)))) ();
MapFoldl = lambda f: lambda xs: Foldl (lambda acc: lambda x: Join (acc) (Atom (f (x)))) (Empty ()) (xs);
Map = MapRecursion;
assert MapRecursion (lambda x: Multiply (x) (2)) ((1,2,3,4)) == MapFoldl (lambda x: Multiply (x) (2)) ((1,2,3,4)) == (2,4,6,8);

# length
Length = lambda xs: Foldl (lambda acc: lambda _: Step (acc)) (Zero ()) (xs);
assert Length ((1,2,3,4,"foo")) == 5;

# zipwith
ZipWith = lambda f: lambda xs: lambda ys: If (Or (Eq (xs) (Empty ())) (Eq (ys) (Empty ()))) (Empty) (lambda: Join (Atom (f (Head (xs)) (Head (ys)))) (ZipWith (f) (Tail (xs)) (Tail (ys)))) ();

# zip
Zip = lambda xs: lambda ys: ZipWith (lambda x: lambda y: Join (Atom (x)) (Atom (y))) (xs) (ys);
assert Zip ((1,2,3)) ((4,5,6)) == ((1,4),(2,5),(3,6));
assert Zip ((1,2,3)) ((4,5)) == ((1,4),(2,5));

# range
Range = lambda x: lambda y: If (Lt (x) (y)) (lambda: Join (Atom (x)) (Range (Step (x)) (y))) (Empty) ();
assert Range (1) (10) == (1,2,3,4,5,6,7,8,9);

# take
TakeRecursion = lambda x: lambda xs: If (Or (Lt (x) (1)) (Eq (xs) (Empty ()))) (Empty) (lambda: Join (Atom (Head (xs))) (TakeRecursion (Subtract (x) (One ())) (Tail (xs)))) ();
TakeZip = lambda x: lambda xs: Map (lambda x: Head(Tail(x))) (Zip (Range (0) (x)) (xs));
Take = TakeRecursion;
assert TakeRecursion (3) ((1,2,3,4,5)) == (1,2,3) == TakeZip (3) ((1,2,3,4,5));
assert TakeRecursion (100) ((1,2,3,4,5)) == (1,2,3,4,5) == TakeZip (100) ((1,2,3,4,5));

# reverse
Reverse = lambda xs: Foldl (lambda acc: lambda x: Join (Atom (x)) (acc)) (Empty ()) (xs)

# count
Count = lambda x: lambda xs: Foldl (lambda acc: lambda y: Add (acc) (If (Eq (x) (y)) (One) (Zero) ())) (Zero ()) (xs)
assert Count (3) ((1,2,3,3,3,4,5,3)) == 4

# any, all
Any = lambda xs: If (Eq (xs) (Empty ())) (lambda: false) (lambda: If (Head (xs)) (lambda: true) (lambda: Any (Tail (xs))) ()) ()
All = lambda xs: If (Eq (xs) (Empty ())) (lambda: true) (lambda: If (Head (xs)) (lambda: All (Tail (xs))) (lambda: false) ()) ()
assert Any ((false,false,false)) == false
assert Any ((false,false,true)) == true
assert All ((true,true,true)) == true
assert All ((true,true,false)) == false

# max, min
Max = lambda xs: Reduce (lambda x: lambda y: (If (Gt (x) (y)) (x) (y))) (xs)
Min = lambda xs: Reduce (lambda x: lambda y: (If (Lt (x) (y)) (x) (y))) (xs)
assert Max ((1,2,3,4,5,4,3,2,1,6,3,2,1)) == 6
assert Min ((4,5,4,4,2,3,4,5,1,0,2,3,1,2,-5)) == -5

# locate
LocateN = lambda x: lambda n: lambda xs: If (Eq (xs) (Empty ())) (lambda: Subtract (Zero ()) (One ())) (lambda: If (Eq (Head (xs)) (x)) (lambda: n) (lambda: LocateN (x) (Step (n)) (Tail (xs))) ()) ()
Locate = lambda x: lambda xs: LocateN (x) (Zero ()) (xs)
assert Locate (3) ((1,2,3,4,5,6,7,3)) == 2

# take while
TakeWhile = lambda f: lambda xs: If (Eq (xs) (Empty ())) (Empty) (lambda: If (f (Head (xs))) (lambda: Join (Atom (Head (xs))) (TakeWhile (f) (Tail (xs)))) (Empty) ()) ();
