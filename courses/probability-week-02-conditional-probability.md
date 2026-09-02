# Probability Week 2: Conditional Probability

Week 2 is about learning how information changes probability. Conditional probability is the heart of probability theory because real life rarely asks, "What is the chance before we know anything?" More often, it asks, "What is the chance now that we know this?"

## 1. The Main Idea

Conditional probability means the probability of event `A` given that event `B` has happened.

It is written:

```text
P(A | B)
```

Read it as:

```text
Probability of A given B
```

The formula is:

```text
P(A | B) = P(A and B) / P(B)
```

This only makes sense when:

```text
P(B) > 0
```

because you cannot condition on an impossible event.

## 2. Conditional Probability Changes The Sample Space

The cleanest intuition:

```text
Once B is known, only outcomes inside B are still possible.
```

So `P(A | B)` asks:

```text
Among the B outcomes, how many also satisfy A?
```

Example: roll one fair die.

Let:

```text
A = roll an even number = {2, 4, 6}
B = roll a number greater than 3 = {4, 5, 6}
```

Now calculate `P(A | B)`.

Since `B` happened, the possible outcomes are only:

```text
{4, 5, 6}
```

Inside that smaller world, the even outcomes are:

```text
{4, 6}
```

So:

```text
P(A | B) = 2 / 3
```

Using the formula:

```text
P(A and B) = P({4, 6}) = 2/6
P(B) = 3/6

P(A | B) = (2/6) / (3/6) = 2/3
```

Both methods agree.

## 3. `P(A | B)` Is Not Usually The Same As `P(B | A)`

This is one of the most important warnings in probability.

Example:

```text
A = person is a professional basketball player
B = person is tall
```

`P(tall | professional basketball player)` is high.

`P(professional basketball player | tall)` is low.

The condition changes the reference group. In the first case, you are only looking at professional basketball players. In the second case, you are only looking at tall people.

## 4. Multiplication Rule

Start with the conditional probability formula:

```text
P(A | B) = P(A and B) / P(B)
```

Rearrange it:

```text
P(A and B) = P(A | B)P(B)
```

You can also write:

```text
P(A and B) = P(B | A)P(A)
```

This is called the multiplication rule.

Example: a bag has 5 red balls and 3 blue balls. You draw 2 balls without replacement. What is the probability both are red?

First draw:

```text
P(first red) = 5/8
```

After drawing one red, there are 4 red balls left out of 7 total balls.

```text
P(second red | first red) = 4/7
```

So:

```text
P(both red) = (5/8)(4/7) = 20/56 = 5/14
```

The phrase "without replacement" usually means the probabilities change after each draw.

## 5. Independence

Events `A` and `B` are independent if knowing one happened does not change the probability of the other.

```text
P(A | B) = P(A)
```

Equivalent test:

```text
P(A and B) = P(A)P(B)
```

Example: toss a fair coin and roll a fair die.

Let:

```text
A = coin is heads
B = die is 6
```

Knowing the coin is heads does not change the die result.

```text
P(A and B) = P(A)P(B) = (1/2)(1/6) = 1/12
```

## 6. Independent vs Mutually Exclusive

Mutually exclusive means two events cannot both happen.

Independent means knowing one happened does not change the probability of the other.

These are very different.

Example: roll one die.

```text
A = roll a 1
B = roll a 2
```

These are mutually exclusive:

```text
P(A and B) = 0
```

But they are not independent:

```text
P(A) = 1/6
P(A | B) = 0
```

Knowing `B` happened makes `A` impossible.

## 7. Law Of Total Probability

Sometimes an event can happen through several cases.

If `B1, B2, ..., Bn` split the sample space into non-overlapping cases, then:

```text
P(A) = P(A | B1)P(B1) + P(A | B2)P(B2) + ... + P(A | Bn)P(Bn)
```

The idea is simple:

```text
overall probability = weighted average across cases
```

Example: a factory has two machines.

```text
Machine 1 makes 60% of items and has a 2% defect rate.
Machine 2 makes 40% of items and has a 5% defect rate.
```

What is the probability a random item is defective?

```text
P(defective) = P(defective | M1)P(M1) + P(defective | M2)P(M2)
P(defective) = (0.02)(0.60) + (0.05)(0.40)
P(defective) = 0.012 + 0.020
P(defective) = 0.032
```

So the defect probability is `3.2%`.

## 8. Bayes' Rule

Bayes' rule reverses conditional probability.

```text
P(A | B) = P(B | A)P(A) / P(B)
```

It answers:

```text
After seeing evidence B, how likely is cause A?
```

Bayes' rule combines:

- Prior belief: `P(A)`
- Evidence likelihood: `P(B | A)`
- Total evidence probability: `P(B)`
- Updated belief: `P(A | B)`

## 9. Bayes' Rule With Total Probability

Often `P(B)` is not directly given. You calculate it with the law of total probability.

For two cases, `A` and `not A`:

```text
P(B) = P(B | A)P(A) + P(B | A^c)P(A^c)
```

Then:

```text
P(A | B) = P(B | A)P(A) / [P(B | A)P(A) + P(B | A^c)P(A^c)]
```

## 10. Worked Example: Medical Test

Suppose:

```text
1% of people have a disease.
The test is positive for 99% of people with the disease.
The test is falsely positive for 5% of people without the disease.
```

Question: if a person tests positive, what is the probability they actually have the disease?

Let:

```text
D = has disease
T = tests positive
```

Given:

```text
P(D) = 0.01
P(D^c) = 0.99
P(T | D) = 0.99
P(T | D^c) = 0.05
```

Calculate total probability of a positive test:

```text
P(T) = P(T | D)P(D) + P(T | D^c)P(D^c)
P(T) = (0.99)(0.01) + (0.05)(0.99)
P(T) = 0.0099 + 0.0495
P(T) = 0.0594
```

Now use Bayes:

```text
P(D | T) = P(T | D)P(D) / P(T)
P(D | T) = 0.0099 / 0.0594
P(D | T) = 1/6
```

So the probability is about `16.7%`.

This surprises many people. The test is accurate, but the disease is rare, so false positives can be a large share of all positive results.

## 11. Natural Frequency Version

Bayes' rule often feels easier with counts.

Imagine 10,000 people.

```text
Have disease: 1% of 10,000 = 100
Do not have disease: 9,900
```

Positive tests:

```text
True positives: 99% of 100 = 99
False positives: 5% of 9,900 = 495
Total positives: 99 + 495 = 594
```

Among the 594 positive tests, only 99 actually have the disease.

```text
P(D | T) = 99 / 594 = 1/6
```

Natural frequencies are a powerful way to avoid Bayes mistakes.

## 12. Conditional Probability In Tables

Suppose a class has 100 students.

```text
                 Passed   Failed   Total
Studied             45        5      50
Did not study       20       30      50
Total               65       35     100
```

Question: What is `P(Passed | Studied)`?

Condition on studied. That row has 50 students.

```text
P(Passed | Studied) = 45 / 50 = 0.90
```

Question: What is `P(Studied | Passed)`?

Condition on passed. That column has 65 students.

```text
P(Studied | Passed) = 45 / 65
```

These are not the same because the denominator changed.

## 13. Common Mistakes

- Confusing `P(A | B)` with `P(B | A)`.
- Forgetting that the denominator is the condition.
- Treating "without replacement" as independent.
- Assuming high test accuracy means high probability after a positive test.
- Calling mutually exclusive events independent.
- Skipping the total probability of the evidence in Bayes' rule.

## 14. What To Memorize This Week

```text
Conditional probability:
P(A | B) = P(A and B) / P(B)

Multiplication rule:
P(A and B) = P(A | B)P(B)

Independence:
P(A | B) = P(A)
P(A and B) = P(A)P(B)

Law of total probability:
P(A) = sum over cases P(A | case)P(case)

Bayes' rule:
P(A | B) = P(B | A)P(A) / P(B)
```

## 15. Practice Questions

1. A card is drawn from a standard deck. Given that it is a heart, what is the probability it is a king?
2. A bag has 4 red and 6 blue balls. Two balls are drawn without replacement. What is the probability both are blue?
3. A fair die is rolled. Given that the result is even, what is the probability it is greater than 3?
4. A company has two suppliers. Supplier A provides 70% of parts with a 1% defect rate. Supplier B provides 30% with a 4% defect rate. What is the probability a random part is defective?
5. Using question 4, if a part is defective, what is the probability it came from Supplier B?

## 16. Practice Answers

1. There are 13 hearts and 1 king of hearts, so probability is `1/13`.
2. `(6/10)(5/9) = 30/90 = 1/3`.
3. Even outcomes are `{2, 4, 6}`. Greater than 3 inside that set is `{4, 6}`. Probability is `2/3`.
4. `(0.01)(0.70) + (0.04)(0.30) = 0.007 + 0.012 = 0.019`, or `1.9%`.
5. `P(B | defective) = P(defective | B)P(B) / P(defective) = (0.04)(0.30) / 0.019 = 0.012 / 0.019`, about `63.2%`.

## 17. Week 2 Summary

Conditional probability teaches you to ask: "What world am I in now?" Once a condition is known, the denominator changes. Bayes' rule then lets you reverse the direction of reasoning, moving from evidence back to the likely cause.
