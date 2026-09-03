# Probability Week 4: Common Distributions

Week 4 is about recognizing probability patterns. A distribution is a complete description of how probability is assigned to the possible values of a random variable.

The goal is not to memorize names in isolation. The goal is to learn the story each distribution tells.

## 1. What A Distribution Does

A probability distribution tells you:

- What values a random variable can take.
- How likely each value or range of values is.
- What the center and spread look like.

For discrete variables, the distribution gives probabilities for exact values.

```text
P(X = x)
```

For continuous variables, exact values usually have probability 0, so the distribution gives probabilities over intervals.

```text
P(a <= X <= b)
```

## 2. Bernoulli Distribution

The Bernoulli distribution models one trial with two possible outcomes.

Usually:

```text
1 = success
0 = failure
```

If the probability of success is `p`, then:

```text
P(X = 1) = p
P(X = 0) = 1 - p
```

Notation:

```text
X ~ Bernoulli(p)
```

Mean and variance:

```text
E[X] = p
Var(X) = p(1 - p)
```

Examples:

- A user clicks an ad or does not.
- A customer churns or does not.
- A coin lands heads or tails.
- A machine part passes inspection or fails.

## 3. Binomial Distribution

The binomial distribution models the number of successes in a fixed number of independent Bernoulli trials.

Use it when:

- There are `n` trials.
- Each trial has success or failure.
- The probability of success is the same each time.
- Trials are independent.
- You count the number of successes.

Notation:

```text
X ~ Binomial(n, p)
```

Formula:

```text
P(X = k) = C(n, k) p^k (1 - p)^(n-k)
```

Mean and variance:

```text
E[X] = np
Var(X) = np(1 - p)
```

Example: toss a fair coin 10 times. What is the probability of exactly 6 heads?

```text
n = 10
p = 1/2
k = 6

P(X = 6) = C(10, 6)(1/2)^6(1/2)^4
P(X = 6) = C(10, 6)(1/2)^10
P(X = 6) = 210 / 1024
```

## 4. Geometric Distribution

The geometric distribution models the number of trials until the first success.

Use it when:

- Each trial has success or failure.
- Trials are independent.
- Success probability is always `p`.
- You wait until the first success.

One common version counts the trial number of the first success.

Notation:

```text
X ~ Geometric(p)
```

Formula:

```text
P(X = k) = (1 - p)^(k-1)p
```

This means:

```text
first k-1 trials fail, then trial k succeeds
```

Mean and variance:

```text
E[X] = 1 / p
Var(X) = (1 - p) / p^2
```

Example: a salesperson closes a deal with probability `0.2` on each call. What is the probability the first success happens on the 4th call?

```text
P(X = 4) = (0.8)^3(0.2) = 0.1024
```

## 5. Poisson Distribution

The Poisson distribution models counts of events in a fixed interval.

Use it when:

- You count events.
- Events occur independently.
- Events happen at an average rate.
- Two events are unlikely to happen at exactly the same instant.

Notation:

```text
X ~ Poisson(lambda)
```

Here `lambda` is the average number of events in the interval.

Formula:

```text
P(X = k) = e^(-lambda) lambda^k / k!
```

Mean and variance:

```text
E[X] = lambda
Var(X) = lambda
```

Examples:

- Number of calls arriving per minute.
- Number of defects per meter of fabric.
- Number of support tickets per hour.
- Number of rare events in a fixed period.

Example: a website gets an average of 3 signups per hour. Assuming a Poisson model, what is the probability of exactly 5 signups in one hour?

```text
lambda = 3
k = 5

P(X = 5) = e^(-3) 3^5 / 5!
```

## 6. Uniform Distribution

A uniform distribution gives equal probability to all outcomes in a range.

Discrete example: fair die.

```text
P(X = x) = 1/6
```

for:

```text
x in {1, 2, 3, 4, 5, 6}
```

Continuous example: choose a random number between 0 and 1.

```text
X ~ Uniform(0, 1)
```

For a continuous uniform distribution from `a` to `b`:

```text
E[X] = (a + b) / 2
Var(X) = (b - a)^2 / 12
```

## 7. Normal Distribution

The normal distribution is the familiar bell-shaped distribution.

Notation:

```text
X ~ Normal(mu, sigma^2)
```

Where:

- `mu` is the mean.
- `sigma^2` is the variance.
- `sigma` is the standard deviation.

The standard normal distribution has:

```text
mu = 0
sigma = 1
```

Normal distributions are useful for:

- Measurement error.
- Natural variation.
- Averages of many small independent effects.
- Approximate behavior from the central limit theorem.

## 8. Standardization And Z-Scores

A z-score tells you how many standard deviations a value is from the mean.

```text
Z = (X - mu) / sigma
```

Example: exam scores are normally distributed with mean 70 and standard deviation 10. A student scores 85.

```text
Z = (85 - 70) / 10 = 1.5
```

The score is 1.5 standard deviations above the mean.

Standardization lets you convert any normal distribution into the standard normal distribution.

## 9. Empirical Rule

For a normal distribution:

```text
About 68% of values are within 1 standard deviation of the mean.
About 95% of values are within 2 standard deviations.
About 99.7% of values are within 3 standard deviations.
```

Example: if heights are approximately normal with mean 170 cm and standard deviation 10 cm:

```text
About 68% are between 160 and 180 cm.
About 95% are between 150 and 190 cm.
About 99.7% are between 140 and 200 cm.
```

## 10. Exponential Distribution

The exponential distribution models waiting time until the next event in a Poisson process.

If events happen at rate `lambda`, then waiting time `T` can be modeled as:

```text
T ~ Exponential(lambda)
```

Mean and variance:

```text
E[T] = 1 / lambda
Var(T) = 1 / lambda^2
```

Examples:

- Time until the next customer arrives.
- Time until a machine fails.
- Time until the next support ticket arrives.

Connection:

```text
Poisson counts events in an interval.
Exponential measures waiting time between events.
```

## 11. Choosing The Right Distribution

Ask what the random variable represents.

If it is one yes/no event:

```text
Bernoulli
```

If it is number of successes in fixed independent trials:

```text
Binomial
```

If it is trials until first success:

```text
Geometric
```

If it is count of events in an interval:

```text
Poisson
```

If all values in a range are equally likely:

```text
Uniform
```

If it is bell-shaped natural variation or an average:

```text
Normal
```

If it is waiting time until next event:

```text
Exponential
```

## 12. Worked Example: Which Distribution?

Question: A website visitor has a 3% chance of signing up. You observe 100 independent visitors. What is the distribution of the number of signups?

This is:

- Fixed number of trials: 100 visitors.
- Success/failure per visitor.
- Same success probability: 0.03.
- Count number of successes.

So:

```text
X ~ Binomial(100, 0.03)
```

Expected signups:

```text
E[X] = np = 100 * 0.03 = 3
```

Variance:

```text
Var(X) = np(1 - p) = 100 * 0.03 * 0.97 = 2.91
```

## 13. Worked Example: Poisson

Question: A call center receives an average of 2 calls per minute. What is the probability of no calls in a minute?

Let:

```text
X ~ Poisson(2)
```

Use:

```text
P(X = k) = e^(-lambda) lambda^k / k!
```

For `k = 0`:

```text
P(X = 0) = e^(-2) 2^0 / 0!
P(X = 0) = e^(-2)
P(X = 0) is about 0.135
```

So there is about a `13.5%` chance of no calls in a minute.

## 14. Common Mistakes

- Using binomial when trials are not independent.
- Using geometric when the question asks for successes in a fixed number of trials.
- Forgetting that Poisson needs a rate for a specific interval.
- Mixing up Poisson counts and exponential waiting times.
- Treating continuous exact values as having positive probability.
- Using normal distribution for heavily skewed data without checking whether it makes sense.

## 15. What To Memorize This Week

```text
Bernoulli:
E[X] = p
Var(X) = p(1-p)

Binomial:
P(X = k) = C(n,k)p^k(1-p)^(n-k)
E[X] = np
Var(X) = np(1-p)

Geometric:
P(X = k) = (1-p)^(k-1)p
E[X] = 1/p

Poisson:
P(X = k) = e^(-lambda)lambda^k/k!
E[X] = lambda
Var(X) = lambda

Normal z-score:
Z = (X - mu) / sigma
```

## 16. Practice Questions

1. A coin has probability `0.6` of heads. Let `X = 1` if heads and `0` otherwise. What distribution is this?
2. A quiz has 20 multiple-choice questions. Each guess has probability `0.25` of being correct. What distribution models the number correct?
3. A basketball player makes a free throw with probability `0.8`. What is the probability their first make is on the 3rd attempt?
4. A server gets an average of 4 requests per second. What distribution models the number of requests in one second?
5. If `X ~ Binomial(50, 0.1)`, find `E[X]` and `Var(X)`.
6. If `X ~ Poisson(7)`, find `E[X]` and `Var(X)`.
7. A value is normally distributed with mean 100 and standard deviation 15. What is the z-score of 130?

## 17. Practice Answers

1. `Bernoulli(0.6)`.
2. `Binomial(20, 0.25)`.
3. `(0.2)^2(0.8) = 0.032`.
4. `Poisson(4)`.
5. `E[X] = 50(0.1) = 5`. `Var(X) = 50(0.1)(0.9) = 4.5`.
6. `E[X] = 7`. `Var(X) = 7`.
7. `Z = (130 - 100) / 15 = 2`.

## 18. Week 4 Summary

Distributions are reusable probability stories. Once you recognize the story, the formulas become much easier to remember. Always ask what is being counted or measured before choosing a distribution.
