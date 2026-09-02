# Probability Week 3: Random Variables

Week 3 moves from events to numerical outcomes. A random variable lets you turn uncertain outcomes into numbers, which means you can calculate averages, spread, and long-run behavior.

## 1. What A Random Variable Is

A random variable is a rule that assigns a number to each outcome of a random experiment.

Despite the name, a random variable is not random in the ordinary sense. The experiment is random. The random variable is the function that converts the outcome into a number.

Example: toss two coins and let `X` be the number of heads.

```text
Outcome   X
HH        2
HT        1
TH        1
TT        0
```

The sample space contains coin sequences. The random variable summarizes each sequence as a number.

## 2. Discrete And Continuous Random Variables

A discrete random variable has countable possible values.

Examples:

- Number of heads in 10 coin tosses.
- Number of emails received today.
- Number of failed login attempts.
- Result of rolling a die.

A continuous random variable can take values on an interval.

Examples:

- Height.
- Time until a server responds.
- Temperature.
- Distance.

This week focuses mostly on discrete random variables because they are easier to learn first.

## 3. Probability Mass Function

For a discrete random variable, the probability mass function, or PMF, gives the probability of each possible value.

It is written:

```text
P(X = x)
```

Example: fair die roll.

```text
x        1    2    3    4    5    6
P(X=x)  1/6  1/6  1/6  1/6  1/6  1/6
```

A valid PMF must satisfy two rules:

```text
0 <= P(X = x) <= 1
sum of all probabilities = 1
```

## 4. Cumulative Distribution Function

The cumulative distribution function, or CDF, gives the probability that a random variable is less than or equal to a value.

```text
F(x) = P(X <= x)
```

Example: fair die.

```text
F(1) = P(X <= 1) = 1/6
F(2) = P(X <= 2) = 2/6
F(3) = P(X <= 3) = 3/6
F(4) = P(X <= 4) = 4/6
F(5) = P(X <= 5) = 5/6
F(6) = P(X <= 6) = 1
```

The PMF answers exact-value questions. The CDF answers up-to-this-value questions.

## 5. Expected Value

Expected value is the long-run average value of a random variable.

For a discrete random variable:

```text
E[X] = sum over all x of x * P(X = x)
```

Example: fair die roll.

```text
E[X] = 1(1/6) + 2(1/6) + 3(1/6) + 4(1/6) + 5(1/6) + 6(1/6)
E[X] = 21/6 = 3.5
```

The expected value is `3.5`, even though no die face is `3.5`. Expected value is an average, not necessarily a possible outcome.

## 6. Expected Value As Balance Point

You can think of expected value as the balance point of a probability distribution.

If high values have more probability, the expected value moves upward. If low values have more probability, it moves downward.

Example:

```text
X        0     10
P(X=x)  0.9   0.1
```

Expected value:

```text
E[X] = 0(0.9) + 10(0.1) = 1
```

Most of the time `X` is 0, but the occasional 10 pulls the average to 1.

## 7. Linearity Of Expectation

Linearity of expectation says:

```text
E[X + Y] = E[X] + E[Y]
```

And:

```text
E[aX + b] = aE[X] + b
```

This works even when `X` and `Y` are not independent.

Example: roll two fair dice. Let `X` be the first die and `Y` be the second die.

```text
E[X] = 3.5
E[Y] = 3.5
E[X + Y] = 7
```

You do not need to list all 36 outcomes to find the expected sum.

## 8. Indicator Random Variables

An indicator random variable is `1` if an event happens and `0` otherwise.

```text
I_A = 1 if A happens
I_A = 0 if A does not happen
```

The expected value of an indicator is the probability of the event:

```text
E[I_A] = P(A)
```

This simple idea is extremely useful.

Example: toss 10 fair coins. What is the expected number of heads?

Let `I_i` be 1 if toss `i` is heads.

```text
X = I_1 + I_2 + ... + I_10
```

Each indicator has expected value:

```text
E[I_i] = 1/2
```

So:

```text
E[X] = 10 * (1/2) = 5
```

## 9. Variance

Expected value tells you the center. Variance tells you the spread.

Definition:

```text
Var(X) = E[(X - E[X])^2]
```

This means:

1. Find the distance from the mean.
2. Square the distance.
3. Average the squared distance.

The shortcut formula is:

```text
Var(X) = E[X^2] - (E[X])^2
```

Standard deviation is:

```text
SD(X) = sqrt(Var(X))
```

Standard deviation is easier to interpret because it is in the same units as `X`.

## 10. Worked Example: Variance Of A Fair Die

Let `X` be the result of one fair die roll.

We already know:

```text
E[X] = 3.5
```

Now calculate `E[X^2]`.

```text
E[X^2] = 1^2(1/6) + 2^2(1/6) + 3^2(1/6) + 4^2(1/6) + 5^2(1/6) + 6^2(1/6)
E[X^2] = (1 + 4 + 9 + 16 + 25 + 36) / 6
E[X^2] = 91 / 6
```

Then:

```text
Var(X) = E[X^2] - (E[X])^2
Var(X) = 91/6 - 3.5^2
Var(X) = 91/6 - 12.25
Var(X) = 35/12
```

So:

```text
SD(X) = sqrt(35/12)
```

## 11. Transforming Random Variables

If you transform a random variable, its expected value changes predictably for linear transformations.

If:

```text
Y = aX + b
```

then:

```text
E[Y] = aE[X] + b
Var(Y) = a^2 Var(X)
```

Notice that adding `b` shifts the random variable but does not change the spread. Multiplying by `a` scales the spread, and variance uses `a^2`.

Example: convert Celsius to Fahrenheit.

```text
F = (9/5)C + 32
```

Then:

```text
E[F] = (9/5)E[C] + 32
Var(F) = (9/5)^2 Var(C)
```

## 12. Joint Distributions

A joint distribution describes two or more random variables together.

For discrete variables:

```text
P(X = x, Y = y)
```

Example: roll two dice.

```text
X = first die
Y = second die
```

For fair dice:

```text
P(X = x, Y = y) = 1/36
```

for every pair `(x, y)` where each value is from 1 to 6.

## 13. Marginal Distributions

A marginal distribution is what you get when you focus on one variable and sum out the others.

```text
P(X = x) = sum over y of P(X = x, Y = y)
```

Example: if you know the joint distribution of first die and second die, the marginal distribution of the first die is still:

```text
P(X = x) = 1/6
```

## 14. Conditional Distributions

A conditional distribution describes one random variable after another is known.

```text
P(X = x | Y = y)
```

Example: roll two dice. Let:

```text
S = X + Y
```

If you know `S = 3`, the possible ordered outcomes are:

```text
(1, 2), (2, 1)
```

So:

```text
P(X = 1 | S = 3) = 1/2
P(X = 2 | S = 3) = 1/2
```

The condition changes the possible outcomes.

## 15. Common Mistakes

- Thinking the expected value must be a possible outcome.
- Forgetting that probabilities in a PMF must sum to 1.
- Confusing PMF with CDF.
- Treating variance as average distance instead of average squared distance.
- Forgetting to square the scaling factor in `Var(aX + b)`.
- Assuming linearity of expectation requires independence. It does not.

## 16. What To Memorize This Week

```text
PMF:
P(X = x)

CDF:
F(x) = P(X <= x)

Expected value:
E[X] = sum xP(X = x)

Linearity:
E[X + Y] = E[X] + E[Y]
E[aX + b] = aE[X] + b

Variance:
Var(X) = E[(X - E[X])^2]
Var(X) = E[X^2] - (E[X])^2

Standard deviation:
SD(X) = sqrt(Var(X))

Indicator:
E[I_A] = P(A)
```

## 17. Practice Questions

1. Let `X` be the result of rolling one fair die. What is `P(X <= 4)`?
2. A random variable has `P(X=0)=0.2`, `P(X=1)=0.5`, and `P(X=2)=0.3`. Find `E[X]`.
3. For the random variable in question 2, find `E[X^2]` and `Var(X)`.
4. Toss 20 fair coins. What is the expected number of heads?
5. If `E[X] = 10` and `Var(X) = 4`, find `E[3X + 2]` and `Var(3X + 2)`.
6. Roll two fair dice. What is the expected sum?

## 18. Practice Answers

1. `P(X <= 4) = 4/6 = 2/3`.
2. `E[X] = 0(0.2) + 1(0.5) + 2(0.3) = 1.1`.
3. `E[X^2] = 0^2(0.2) + 1^2(0.5) + 2^2(0.3) = 1.7`. `Var(X) = 1.7 - 1.1^2 = 0.49`.
4. Use indicators: `20 * 1/2 = 10`.
5. `E[3X + 2] = 3(10) + 2 = 32`. `Var(3X + 2) = 3^2 * 4 = 36`.
6. `3.5 + 3.5 = 7`.

## 19. Week 3 Summary

Random variables are the bridge from uncertain events to numerical analysis. Once outcomes become numbers, you can describe their center with expected value, their spread with variance, and their relationships with joint and conditional distributions.
