# Probability Week 1: Foundations

Week 1 is about learning the language of probability. Before formulas become useful, you need to know what the possible outcomes are, what event you care about, and whether the outcomes are equally likely.

## 1. What Probability Means

Probability is a number that measures uncertainty.

```text
0 <= P(A) <= 1
```

If `P(A) = 0`, event `A` is impossible.

If `P(A) = 1`, event `A` is certain.

If `P(A) = 0.5`, event `A` has a 50% chance under the assumptions of the problem.

Probability is not a guarantee about one single attempt. It is a model of uncertainty. If a fair coin has probability `1/2` of heads, that does not mean every two tosses must contain exactly one head. It means that over many tosses, the long-run fraction of heads should be close to `1/2`.

## 2. Experiments, Outcomes, and Sample Spaces

A probability experiment is any process with uncertain results.

Examples:

- Tossing a coin.
- Rolling a die.
- Drawing a card.
- Checking whether a customer clicks a link.
- Measuring tomorrow's rainfall.

An outcome is one possible result of the experiment.

The sample space is the set of all possible outcomes. It is usually written as `S`.

Example: toss one coin.

```text
S = {H, T}
```

Example: roll one fair die.

```text
S = {1, 2, 3, 4, 5, 6}
```

Example: toss two coins.

```text
S = {HH, HT, TH, TT}
```

The sample space matters because probability is always measured relative to the possible outcomes you have defined.

## 3. Events

An event is a set of outcomes inside the sample space.

Example: roll one die.

```text
S = {1, 2, 3, 4, 5, 6}
```

Let `A` be the event "roll an even number".

```text
A = {2, 4, 6}
```

Let `B` be the event "roll a number greater than 4".

```text
B = {5, 6}
```

Events can contain one outcome, many outcomes, or no outcomes.

The event that cannot happen is the empty event:

```text
empty event = {}
```

The event that always happens is the whole sample space:

```text
S
```

## 4. Probability With Equally Likely Outcomes

When all outcomes are equally likely:

```text
P(A) = number of outcomes in A / number of outcomes in S
```

Example: roll a fair die. What is the probability of rolling an even number?

```text
S = {1, 2, 3, 4, 5, 6}
A = {2, 4, 6}

P(A) = 3 / 6 = 1 / 2
```

This formula is simple, but it depends on a big assumption: all outcomes must be equally likely.

For a loaded die, this method may fail because each face may not have probability `1/6`.

## 5. Complement Rule

The complement of event `A` is the event that `A` does not happen.

It is often written as `A^c` or `not A`.

```text
P(A^c) = 1 - P(A)
```

Example: roll one die. What is the probability of not rolling a 6?

```text
P(6) = 1 / 6
P(not 6) = 1 - 1/6 = 5/6
```

The complement rule is especially useful for "at least one" problems.

Example: toss a fair coin 3 times. What is the probability of getting at least one head?

Directly listing all outcomes with at least one head works, but the complement is faster.

```text
P(at least one head) = 1 - P(no heads)
P(no heads) = P(TTT) = 1/8
P(at least one head) = 1 - 1/8 = 7/8
```

Whenever you see "at least one", ask whether "none" is easier to calculate.

## 6. Union, Intersection, and Difference

The union of two events means either event happens.

```text
A union B = A or B
```

The intersection of two events means both events happen.

```text
A intersection B = A and B
```

Example: roll one die.

```text
A = even = {2, 4, 6}
B = greater than 4 = {5, 6}
```

Then:

```text
A or B = {2, 4, 5, 6}
A and B = {6}
```

The difference `A but not B` means outcomes in `A` that are not in `B`.

```text
A but not B = {2, 4}
```

## 7. Addition Rule

For any two events:

```text
P(A or B) = P(A) + P(B) - P(A and B)
```

Why subtract `P(A and B)`?

When you add `P(A)` and `P(B)`, the overlap gets counted twice. Subtracting it once fixes the double-counting.

Example: roll one die.

```text
A = even = {2, 4, 6}
B = greater than 4 = {5, 6}

P(A) = 3/6
P(B) = 2/6
P(A and B) = 1/6

P(A or B) = 3/6 + 2/6 - 1/6 = 4/6 = 2/3
```

Check against the event directly:

```text
A or B = {2, 4, 5, 6}
P(A or B) = 4/6 = 2/3
```

## 8. Mutually Exclusive Events

Two events are mutually exclusive if they cannot both happen.

```text
P(A and B) = 0
```

Example: one coin toss.

```text
A = heads
B = tails
```

The coin cannot be both heads and tails on the same toss, so the events are mutually exclusive.

For mutually exclusive events, the addition rule becomes:

```text
P(A or B) = P(A) + P(B)
```

Important mistake to avoid: mutually exclusive is not the same as independent. If two non-impossible events are mutually exclusive, knowing one happened tells you the other did not happen.

## 9. Counting Basics

Counting matters because probability often means:

```text
favorable cases / total cases
```

### Multiplication Rule For Counting

If one choice has `m` options and another independent choice has `n` options, then the pair has:

```text
m * n
```

possible outcomes.

Example: a shirt has 3 color choices and pants have 2 color choices.

```text
Total outfits = 3 * 2 = 6
```

For multiple stages, multiply all choices.

Example: a password has 2 letters followed by 2 digits. Letters can repeat and digits can repeat.

```text
26 * 26 * 10 * 10 = 67,600
```

### Permutations

Permutations count arrangements where order matters.

The number of ways to arrange `n` distinct objects is:

```text
n!
```

Example: arrange 4 books.

```text
4! = 4 * 3 * 2 * 1 = 24
```

The number of ways to choose and arrange `r` objects from `n` distinct objects is:

```text
nPr = n! / (n - r)!
```

Example: choose 3 winners from 10 people for first, second, and third place.

```text
10P3 = 10! / 7! = 10 * 9 * 8 = 720
```

Order matters because first-second-third is different from third-second-first.

### Combinations

Combinations count selections where order does not matter.

The number of ways to choose `r` objects from `n` distinct objects is:

```text
nCr = n! / (r!(n - r)!)
```

Example: choose 3 people from 10 for a committee.

```text
10C3 = 10! / (3!7!) = 120
```

Order does not matter because the same 3 people form the same committee.

## 10. Worked Example: Cards

Question: A standard deck has 52 cards. What is the probability of drawing either a heart or a king?

Let:

```text
A = heart
B = king
```

There are 13 hearts and 4 kings. The king of hearts belongs to both groups.

```text
P(A) = 13/52
P(B) = 4/52
P(A and B) = 1/52
```

Use the addition rule:

```text
P(A or B) = 13/52 + 4/52 - 1/52
P(A or B) = 16/52 = 4/13
```

Plain-English answer: the chance of drawing a heart or a king is `4/13`.

## 11. Worked Example: At Least One

Question: If you roll two fair dice, what is the probability of getting at least one 6?

Use the complement.

```text
P(at least one 6) = 1 - P(no 6s)
```

For one die:

```text
P(not 6) = 5/6
```

For two independent dice:

```text
P(no 6s) = (5/6)(5/6) = 25/36
```

So:

```text
P(at least one 6) = 1 - 25/36 = 11/36
```

## 12. What To Memorize This Week

```text
P(A) = favorable outcomes / total outcomes
P(A^c) = 1 - P(A)
P(A or B) = P(A) + P(B) - P(A and B)
n! = n * (n - 1) * ... * 2 * 1
nPr = n! / (n - r)!
nCr = n! / (r!(n - r)!)
```

## 13. Practice Questions

1. Roll one fair die. What is the probability of rolling a number less than 5?
2. Roll one fair die. What is the probability of rolling an odd number or a number greater than 4?
3. Toss 4 fair coins. What is the probability of getting at least one head?
4. A bag contains 5 red balls, 3 blue balls, and 2 green balls. What is the probability of drawing a red or green ball?
5. How many ways can 5 books be arranged on a shelf?
6. How many ways can you choose 2 students from a group of 8?
7. From a standard deck, what is the probability of drawing a queen or a spade?

## 14. Practice Answers

1. `{1, 2, 3, 4}` gives `4/6 = 2/3`.
2. Odd is `{1, 3, 5}` and greater than 4 is `{5, 6}`. Union is `{1, 3, 5, 6}`, so probability is `4/6 = 2/3`.
3. `1 - P(no heads) = 1 - (1/2)^4 = 15/16`.
4. Red or green gives `5 + 2 = 7` favorable balls out of `10`, so probability is `7/10`.
5. `5! = 120`.
6. `8C2 = 8! / (2!6!) = 28`.
7. Queens: `4`. Spades: `13`. Queen of spades overlap: `1`. Probability is `(4 + 13 - 1) / 52 = 16/52 = 4/13`.

## 15. Week 1 Summary

Probability problems become easier when you slow down and name the structure:

- What is the experiment?
- What is the sample space?
- What event are you measuring?
- Are outcomes equally likely?
- Are you dealing with "or", "and", "not", or "at least one"?

Most early mistakes happen before calculation. The setup is the real work.
