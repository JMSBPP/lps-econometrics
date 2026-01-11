
Pg 14 --> Behavioral Encapsulation
You follow fucntional programmisn principles appliaed to python on ecnometrics analys


Focus on readbaility in the sense of abstracting from the user "how" data is constructed, but rather

Here is some data  of some category. The code MUST read as what do I need to do with that


# Behavioral Encapsulation (via Closures)
design closures ("operations with data attached") instead of classes ("data with operations")



# Control Structure

## Recursion

1. "hidden iteration"
--> use loops if risk of stack to deep or permformance issues
- if not stack too deep, but complex algrithmereads more intuitivily with recursion use it (a.k.a problem is (can be modelled) naturally a tree)

2. "divide and conquer"

Given a set $A$ where we need to do transformations or state transitions.

If we can partition $A$ optimally and disjointly
$$
A = \bigcup_i A_i \;\implies\; f(A) = \bigcup_i f(A_i)
$$

For this apprach apply recursion

```
def f(A):
    A1, A2 = partition(A)
    assert A1 ∪ A2 == A

    return f(A1) ⊕ f(A2)
```

## Generators and Comprehension 
If dataNeeded is stream-like
```
rawData = [1,2,3,4,5]
generateDataNeeded = (
    value
    for value in rawData
    if condition(value)
)
data = dataStructure(generateDataNeeded)
```

If Data is a value
```
data = dataStructure(
    [value for value in rawData if condition(value) > 2]
)
```

# Composition Algebra

## Parallel (map)

Let \( A \) be a state (or collection of states), and let 
\( \{ f_i \}_{i=1}^n \) be a family of actions.
Where is f is some action toe be done on A result of a parallel set of actions 

We define a parallel action operator as:

$$
f(A) = \bigotimes_{i=1}^{n} f_i(A)
$$
where:

- \( A \) is the input state
- each \( f_i : A \rightarrow B_i \) is an independent action
- \( \otimes \) denotes parallel (pointwise) application
- the result is a structured collection of outputs, not a new state

Then, prioritze this aproach:

```
doCompositeAction = lambda fs, *args: [
    list(map(f, *args)) for f in fs
]
```


This corresponds to:


\{ f_i \}_{i=1}^{n} \times A
\;\longmapsto\;
\left( f_1(A), f_2(A), \dots, f_n(A) \right)

If what intended is compositer stae transitions that acieve a final one use:

```
from functools import reduce

doSequentialAction = lambda fs, x: reduce(
    lambda acc, f: f(acc),
    fs,
    x
)
```

## Sequential (fold)

If the intention is to model state evolution, then actions must be applied sequentially via function composition.

f(A)=(fn​∘fn−1​∘⋯∘f1​)(A)

For this apporach use:

```
from functools import reduce

doSequentialAction = lambda fs, x: reduce(
    lambda acc, f: f(acc),
    fs,
    x
)
```

This maps to 

A0​=A,Ak+1​=fk+1​(Ak​),An​=f(A)



