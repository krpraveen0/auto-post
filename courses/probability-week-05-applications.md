# Probability Week 5: Applications

Week 5 connects probability to real decision-making. The goal is to use probability as a thinking tool: estimate risk, compare choices, reason from evidence, and understand why uncertainty does not disappear just because a calculation looks precise.

## 1. Probability As A Decision Tool

Probability helps when outcomes are uncertain and choices have consequences.

Examples:

- Should a business launch a feature?
- Is a medical test result strong evidence?
- How much inventory should a store hold?
- How risky is an investment?
- How reliable is a machine learning model's prediction?

Probability does not remove uncertainty. It helps you reason honestly under uncertainty.

## 2. Expected Value In Decisions

Expected value is useful when comparing repeated or average outcomes.

```text
E[X] = sum of outcome * probability
```

Example: a game costs `$10` to play.

You have:

```text
10% chance to win $100
90% chance to win $0
```

Expected winnings:

```text
0.10($100) + 0.90($0) = $10
```

After the `$10` cost:

```text
Expected profit = $10 - $10 = $0
```

This is a fair game by expected value.

But fair by expected value does not mean risk-free. Most individual plays lose `$10`.

## 3. Expected Value vs Utility

Expected money is not always the same as expected usefulness.

Example:

```text
Option A: guaranteed $1,000
Option B: 50% chance of $2,200 and 50% chance of $0
```

Expected value of B:

```text
0.5($2,200) + 0.5($0) = $1,100
```

Option B has higher expected money, but many people prefer A because certainty matters. Utility captures the personal or practical value of an outcome, not just its dollar amount.

This matters in finance, insurance, product decisions, and risk management.

## 4. Risk And Variance

Two choices can have the same expected value but different risk.

Example:

```text
Option A: receive $50 for sure.
Option B: 50% chance of $100, 50% chance of $0.
```

Both have expected value:

```text
$50
```

But Option B has more variance.

Variance matters when downside outcomes are painful. A startup, investor, or engineer designing a reliability system often cares about worst-case and tail outcomes, not only averages.

## 5. Base Rates

A base rate is the prior probability of something before specific evidence.

Ignoring base rates is one of the most common reasoning errors.

Example:

```text
Only 1 out of 1,000 people has a rare condition.
A test is positive.
```

Even if the test is good, the condition may still be unlikely after a positive result if false positives are common relative to the rare base rate.

Always ask:

```text
How common was this before the new evidence?
```

## 6. Bayesian Thinking

Bayesian thinking means updating beliefs when new evidence arrives.

The pattern:

```text
prior belief + evidence = updated belief
```

Bayes' rule:

```text
P(H | E) = P(E | H)P(H) / P(E)
```

Where:

- `H` is a hypothesis.
- `E` is evidence.
- `P(H)` is the prior.
- `P(E | H)` is the likelihood.
- `P(H | E)` is the posterior.

Example: spam detection.

```text
H = email is spam
E = email contains a suspicious phrase
```

The system asks:

```text
How common is spam?
How often do spam emails contain this phrase?
How often do normal emails contain this phrase?
```

The answer is an updated probability that the email is spam.

## 7. Simulation

Simulation uses repeated random experiments to approximate probabilities.

This is useful when exact formulas are hard.

Basic simulation pattern:

1. Model one random trial.
2. Repeat it many times.
3. Count how often the event happens.
4. Estimate probability as frequency.

Example: estimate probability of at least one 6 in two dice rolls.

```text
repeat many times:
  roll die 1
  roll die 2
  check whether either die is 6

estimated probability = successes / repetitions
```

The exact answer is:

```text
1 - (5/6)^2 = 11/36
```

The simulation should get close when repetitions are large.

## 8. Law Of Large Numbers

The law of large numbers says that as the number of independent trials grows, the sample average tends to get closer to the expected value.

Example: fair coin.

For a small number of tosses, the fraction of heads can vary a lot.

For a large number of tosses, the fraction of heads tends to move closer to:

```text
0.5
```

Important: the law of large numbers does not say short-term results must balance out immediately. If you get several heads in a row, tails are not "due". Each fair coin toss still has probability `1/2` of heads and `1/2` of tails.

## 9. Central Limit Theorem

The central limit theorem says that averages or sums of many independent random variables often become approximately normal, even when the original variables are not normal.

This is why the normal distribution appears so often in statistics.

The idea:

```text
Many small independent sources of randomness combine into a bell-shaped pattern.
```

Applications:

- Polling.
- A/B testing.
- Measurement error.
- Confidence intervals.
- Quality control.

The central limit theorem is a bridge from probability to statistics.

## 10. Probability In Statistics

Statistics often asks the reverse of probability.

Probability:

```text
Given the model, what data might happen?
```

Statistics:

```text
Given the data, what model or explanation is plausible?
```

Example:

Probability question:

```text
If a coin is fair, what is the probability of 8 or more heads in 10 tosses?
```

Statistics question:

```text
If we observed 8 heads in 10 tosses, is the coin likely to be unfair?
```

Probability gives the mathematical foundation for inference.

## 11. Probability In Machine Learning

Machine learning often uses probability to represent uncertainty.

Examples:

- Classification models output class probabilities.
- Language models predict probability distributions over next tokens.
- Bayesian models update beliefs from data.
- Loss functions often come from probability models.
- Evaluation uses uncertainty, confidence intervals, and sampling variation.

Important idea: a model score is not automatically a calibrated probability. If a model says `0.9`, that should mean events like that happen about 90% of the time across similar cases. Many models need calibration before their scores can be interpreted that way.

## 12. Probability In Finance

Finance uses probability because future returns are uncertain.

Common concepts:

- Expected return.
- Variance and volatility.
- Correlation.
- Tail risk.
- Diversification.
- Risk of ruin.

Example: investment A and investment B may each be risky alone, but if they do not move together perfectly, combining them can reduce overall portfolio variance.

This is why independence and correlation matter.

## 13. Probability In Engineering Reliability

Reliability questions are probability questions.

Examples:

- What is the probability a server fails this month?
- What is the probability at least one backup succeeds?
- What is the probability a request times out?
- How much redundancy is enough?

Example: suppose one independent backup succeeds with probability `0.95`. You have two independent backups. What is the probability at least one succeeds?

Use the complement:

```text
P(at least one succeeds) = 1 - P(both fail)
P(both fail) = (0.05)(0.05) = 0.0025
P(at least one succeeds) = 0.9975
```

So reliability is `99.75%` under the independence assumption.

The assumption is the fragile part. If both backups fail for the same reason, independence is false.

## 14. Correlation And Dependence

Two variables are associated if knowing something about one tells you something about the other.

Correlation measures linear association.

Positive correlation:

```text
When X tends to be high, Y tends to be high.
```

Negative correlation:

```text
When X tends to be high, Y tends to be low.
```

Zero correlation does not always mean independence. Variables can have nonlinear dependence even when linear correlation is zero.

Independence is stronger:

```text
Knowing X tells you nothing about Y.
```

## 15. Decision Trees

A decision tree breaks a probability problem into stages.

Example: product experiment.

```text
Launch feature:
  60% chance adoption is high -> +$100,000
  40% chance adoption is low -> -$20,000
```

Expected value:

```text
0.60($100,000) + 0.40(-$20,000)
= $60,000 - $8,000
= $52,000
```

But before deciding, ask:

- Can the downside be absorbed?
- Are the probabilities credible?
- What assumptions drive the estimate?
- Is there an option to run a smaller experiment first?

## 16. Communicating Probability

Good probability communication includes:

- The probability estimate.
- The assumptions behind it.
- The relevant base rate.
- The downside risk.
- A plain-English interpretation.

Weak version:

```text
This has a 90% chance of success.
```

Better version:

```text
Under the current assumptions, about 9 out of 10 similar launches would be expected to succeed. The main risk is that our adoption estimate comes from a small sample.
```

Probability is more useful when paired with uncertainty about the estimate itself.

## 17. Final Review: How To Approach Any Probability Problem

Use this process:

1. Define the random experiment.
2. Identify the sample space.
3. Define the event or random variable.
4. Ask whether outcomes are equally likely.
5. Look for conditioning.
6. Check independence assumptions.
7. Choose a distribution if the pattern matches.
8. Calculate carefully.
9. Sanity-check the answer.
10. Explain the result in words.

## 18. Common Mistakes

- Optimizing only for expected value when downside risk matters.
- Ignoring base rates.
- Treating model confidence as calibrated probability.
- Assuming independence because it makes the math easier.
- Forgetting that short-term randomness can look patterned.
- Over-interpreting small samples.
- Confusing correlation with causation.

## 19. What To Memorize This Week

```text
Expected value for decisions:
E[X] = sum outcome * probability

Bayesian update:
posterior is proportional to likelihood * prior

Law of large numbers:
sample averages approach expected values over many independent trials

Central limit theorem:
sums or averages of many independent variables are often approximately normal

At least one:
P(at least one) = 1 - P(none)
```

## 20. Practice Questions

1. A game gives a 20% chance to win `$50` and an 80% chance to win `$0`. It costs `$8` to play. What is the expected profit?
2. A system has three independent components, each with a 90% chance of working. What is the probability all three work?
3. Using question 2, what is the probability at least one component fails?
4. A model labels a transaction as fraud with score `0.95`. Why might this not mean there is a true 95% chance of fraud?
5. An investment has a higher expected return but much higher variance than another investment. Why might someone reject it?
6. In a population, a rare event has base rate 0.1%. A test has false positives. Why does the base rate matter?

## 21. Practice Answers

1. Expected winnings are `0.20($50) + 0.80($0) = $10`. Expected profit is `$10 - $8 = $2`.
2. `(0.9)^3 = 0.729`.
3. `1 - 0.729 = 0.271`.
4. Model scores may be uncalibrated. A score of `0.95` only means 95% probability if similar scored cases are actually fraud about 95% of the time.
5. Because downside risk, cash needs, risk tolerance, or survival constraints may matter more than average return.
6. If the event is very rare, false positives can outnumber true positives even when the test seems accurate.

## 22. Week 5 Summary

Probability is not just a school topic. It is a disciplined way to think when outcomes are uncertain. The strongest probability thinkers are careful with assumptions, base rates, dependence, variance, and plain-English interpretation.
