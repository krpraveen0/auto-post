# Probability Mastery Notes

These notes are designed to support a first serious pass through probability, starting with an intuition-first course such as Coursera's "An Intuitive Introduction to Probability" and then deepening into more mathematical practice.

## Study Goal

Master probability well enough to:

- Reason clearly about uncertainty.
- Solve conditional probability and random variable problems.
- Understand common distributions and when to use them.
- Prepare for statistics, machine learning, finance, algorithms, or exams.

## Learning Path

1. Build intuition with examples and visual thinking.
2. Practice counting, conditioning, and Bayes' rule until they feel natural.
3. Learn random variables, expectation, variance, and distributions.
4. Connect probability to statistics, inference, and real-world uncertainty.
5. Solve many problems, because probability is learned by doing.

## Complete 5-Week Notes

Visual HTML version:

- [Probability Visual Notes](probability-visual-notes.html)

Use these files in order:

1. [Week 1: Foundations](probability-week-01-foundations.md)
2. [Week 2: Conditional Probability](probability-week-02-conditional-probability.md)
3. [Week 3: Random Variables](probability-week-03-random-variables.md)
4. [Week 4: Common Distributions](probability-week-04-distributions.md)
5. [Week 5: Applications](probability-week-05-applications.md)

Each week includes explanations, formulas, worked examples, common mistakes, practice questions, and answer keys.

## Core Ideas

### 1. Probability

Probability measures how likely an event is.

An event has probability between 0 and 1:

- `0` means impossible.
- `1` means certain.
- Values between 0 and 1 describe uncertainty.

Basic rule:

```text
P(event) = favorable outcomes / total outcomes
```

This simple formula works best when all outcomes are equally likely.

Example:

```text
P(rolling a 4 on a fair die) = 1 / 6
```

### 2. Sample Space

The sample space is the set of all possible outcomes.

Example: tossing one coin.

```text
Sample space = {Heads, Tails}
```

Example: rolling one die.

```text
Sample space = {1, 2, 3, 4, 5, 6}
```

Good probability work starts by defining the sample space clearly.

### 3. Events

An event is a subset of the sample space.

Example: rolling an even number.

```text
Event = {2, 4, 6}
P(even) = 3 / 6 = 1 / 2
```

### 4. Complement Rule

The complement of an event means the event does not happen.

```text
P(not A) = 1 - P(A)
```

This is useful when calculating the direct probability is hard.

Example:

```text
P(at least one success) = 1 - P(no successes)
```

### 5. Addition Rule

For two events:

```text
P(A or B) = P(A) + P(B) - P(A and B)
```

The subtraction prevents double-counting the overlap.

If two events cannot happen together, they are mutually exclusive:

```text
P(A or B) = P(A) + P(B)
```

### 6. Conditional Probability

Conditional probability means the probability of one event given that another event has happened.

```text
P(A | B) = P(A and B) / P(B)
```

Read this as:

```text
Probability of A given B
```

Key idea: once B is known, the world has changed. The sample space shrinks to cases where B is true.

### 7. Independence

Two events are independent if knowing one happened does not change the probability of the other.

```text
P(A | B) = P(A)
```

Equivalent form:

```text
P(A and B) = P(A)P(B)
```

Important warning: independent does not mean mutually exclusive. In fact, mutually exclusive events are usually dependent, because if one happens the other cannot.

### 8. Bayes' Rule

Bayes' rule updates belief after new evidence.

```text
P(A | B) = P(B | A)P(A) / P(B)
```

Interpretation:

- `P(A)` is the prior belief.
- `P(B | A)` is how likely the evidence is if A is true.
- `P(A | B)` is the updated belief after seeing B.

Bayes' rule is central in statistics, machine learning, medical testing, spam detection, and decision-making under uncertainty.

### 9. Random Variables

A random variable assigns a number to each outcome.

Example: toss two coins and count heads.

```text
HH -> 2
HT -> 1
TH -> 1
TT -> 0
```

The random variable is not the random process itself. It is a numerical summary of the outcome.

### 10. Expected Value

Expected value is the long-run average value of a random variable.

For a discrete random variable:

```text
E[X] = sum of x * P(X = x)
```

Example: fair die roll.

```text
E[X] = 1*(1/6) + 2*(1/6) + 3*(1/6) + 4*(1/6) + 5*(1/6) + 6*(1/6)
E[X] = 3.5
```

The expected value does not have to be a possible outcome.

### 11. Variance

Variance measures spread around the expected value.

```text
Var(X) = E[(X - E[X])^2]
```

Useful equivalent form:

```text
Var(X) = E[X^2] - (E[X])^2
```

Standard deviation is the square root of variance.

### 12. Common Distributions

#### Bernoulli Distribution

Models one trial with two outcomes: success or failure.

```text
X = 1 with probability p
X = 0 with probability 1 - p
```

Example: whether one email is spam.

#### Binomial Distribution

Models the number of successes in `n` independent Bernoulli trials.

```text
X ~ Binomial(n, p)
```

Example: number of heads in 10 coin tosses.

#### Geometric Distribution

Models how many trials are needed until the first success.

Example: number of coin tosses until the first heads.

#### Poisson Distribution

Models counts of events in a fixed interval when events happen at an average rate.

Example: number of website visits per minute.

#### Normal Distribution

A bell-shaped continuous distribution used to model many natural and measurement-based quantities.

Example: measurement errors, heights, test scores, and many averages.

## Problem-Solving Checklist

When solving probability problems:

1. Define the sample space.
2. Identify the event of interest.
3. Check whether outcomes are equally likely.
4. Look for conditioning: has new information changed the sample space?
5. Check whether events are independent or dependent.
6. Use complements for "at least one" problems.
7. Choose the right distribution if the problem has a known pattern.
8. Write the formula before calculating.
9. Sanity-check whether the answer is between 0 and 1.
10. Interpret the result in plain English.

## Practice Plan

### Week 1: Foundations

- Probability basics
- Sample spaces
- Events
- Complements
- Addition rule

Practice goal: solve simple counting and event probability problems.

### Week 2: Conditional Probability

- Conditional probability
- Independence
- Multiplication rule
- Bayes' rule

Practice goal: solve medical test, card, dice, and diagnostic reasoning problems.

### Week 3: Random Variables

- Discrete random variables
- Probability mass functions
- Expected value
- Variance

Practice goal: compute expectation and variance from tables and word problems.

### Week 4: Distributions

- Bernoulli
- Binomial
- Geometric
- Poisson
- Normal distribution

Practice goal: identify the right distribution from the story of the problem.

### Week 5: Applications

- Risk
- Decision-making
- Simulation
- Statistics bridge
- Machine learning bridge

Practice goal: explain uncertainty and expected outcomes in real scenarios.

## Key Mistakes To Avoid

- Treating dependent events as independent.
- Forgetting to subtract overlap in `P(A or B)`.
- Confusing `P(A | B)` with `P(B | A)`.
- Using Bayes' rule without calculating the total probability of the evidence.
- Assuming expected value must be a possible result.
- Memorizing distributions without learning the story each distribution represents.

## Quick Reference

```text
Complement:
P(not A) = 1 - P(A)

Addition:
P(A or B) = P(A) + P(B) - P(A and B)

Conditional:
P(A | B) = P(A and B) / P(B)

Independent events:
P(A and B) = P(A)P(B)

Bayes:
P(A | B) = P(B | A)P(A) / P(B)

Expected value:
E[X] = sum of x * P(X = x)

Variance:
Var(X) = E[X^2] - (E[X])^2
```

## Next Notes To Add

- Counting rules: permutations and combinations
- Law of total probability
- Joint, marginal, and conditional distributions
- Continuous random variables
- Cumulative distribution functions
- Central limit theorem
- Simulation examples in Python
