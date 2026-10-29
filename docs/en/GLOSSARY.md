# Glossary

**English** · [Русский](../ru/GLOSSARY.md)

> Terms used in the code and the documentation, with short explanations and numbers. An entry is added in the same change that introduces the term.

The running example is five apartments, with the area in m² and the price in millions: 30 m² cost 6.5, 45 m² cost 8.5, 60 m² cost 12, 80 m² cost 15.5 and 100 m² cost 20.

## The task

- **Regression**: a task where the model predicts a number, not a class. The price of an apartment, the delivery time of an order, the latency of the next request. Quality is measured by how far the prediction is from the fact, for example "on average the model is off by 0.3 million".
- **Linear regression**: the simplest regression, a straight line through the points "area → price": `price = k × area + b`. "Linear" means the dependence is drawn as a straight line. With several features every feature gets its own coefficient: `price = k1 × area + k2 × floor + b`.
- **Feature**: what is known about an object and goes into the model. Area, floor, distance to the metro.
- **Target**: what the model predicts. The price of the apartment.
- **Coefficient (weight)**: the number a feature is multiplied by. In `price = k × area + b` the coefficient `k` is the slope: how much the price grows per extra m². The number `b` is the intercept: the price at zero area, the starting point of the line. For the five apartments the best line has `k ≈ 0.195` (about 195 thousand per m²) and `b ≈ 0.23`.
- **Training**: choosing the coefficients so that the line passes as close to all the points as possible. For the line above it is the choice of two numbers, `k` and `b`.
- **Prediction (inference)**: putting a new object into the trained formula. For 70 m²: `0.195 × 70 + 0.23 ≈ 13.9` million. The coefficients are fixed at this step, nothing is fitted again.

## Errors and metrics

- **Residual**: the fact minus the prediction for one object. For the five apartments the best line gives residuals +0.43, −0.49, +0.08, −0.31, +0.29: the first apartment is 0.43 more expensive than the line says, the second one 0.49 cheaper.
- **Least squares**: the way to choose the best line. Square every residual, add them up, and take the line with the smallest sum. For the best line the sum is about 0.617, for the line `k = 0.2, b = 0` it is 0.75, so the first line is better. Squares remove the signs, so pluses and minuses do not cancel each other, and they punish big misses harder.
- **MAE (mean absolute error)**: the average size of the residual without the sign, in the same units as the target. For the five apartments `(0.43 + 0.49 + 0.08 + 0.31 + 0.29) / 5 ≈ 0.32` million: "the prediction is off by 0.32 million on average".
- **RMSE (root mean squared error)**: the same question as MAE, but big misses count more. Square the residuals, take their average, then the square root: about 0.35 million for the five apartments. RMSE is never smaller than MAE, and the bigger the gap between them, the more big misses are among the errors.

## Optimization

- **Loss function**: a number that tells how bad the model is. For linear regression here it is the sum of squared residuals: the smaller, the better.
- **Gradient descent**: a way to find the coefficients step by step instead of by a formula. Picture a person in thick fog on a hillside who wants to get down: feel which way the ground tilts, take a step downhill, repeat. Here the "height" is the loss and the "place on the hill" is the pair `k`, `b`. The tilt at the current point is the gradient: it points where the loss grows fastest, so the step goes the opposite way. Neural networks are trained the same way, only with millions of coefficients.
- **Learning rate**: the size of one gradient descent step. Example for the five apartments with `b` fixed at 0.23: start at `k = 0.10`, the loss is 206.5, the gradient is −4345 (the minus sign means "increase k"). With a learning rate of 0.00002 the shift is `0.00002 × 4345 ≈ 0.087`, so `k` becomes 0.187 and the loss drops to 2.0. A rate that is too small makes the descent crawl, a rate that is too large jumps over the valley and the loss grows with every step.

## Data and evaluation

- **Train and test sets**: the data is split into two parts before training. The model fits the coefficients on the train part and is checked on the test part, which it has not seen. Example: 1000 sold apartments, 800 go to training and 200 are kept aside. The train error shows how well the model fits what it saw, the test error shows how it works on new data, and only the second one matters in real use.
- **Overfitting**: the model fits the training examples together with the random noise, as if it had memorized the answers without understanding the topic. The train error is small, the test error is much bigger. A model trained on five apartments can pass through all of them and still miss new apartments badly.
- **Baseline**: the simplest possible model, the reference point for every other model. For apartments it is "always answer the average price". For the five apartments the average is 12.5, and the baseline is off by 4.2 million on average (MAE), against 0.32 for the straight line. A model that does not beat the baseline is useless.
- **Synthetic data**: data generated by a rule chosen in advance, for example `price = 0.2 × area + 0.3` plus random noise. The right answer (`k = 0.2`, `b = 0.3`) is known beforehand, so it is possible to check whether the model found it.
- **Seed**: the number a random number generator starts from. The same seed gives the same "random" data on every run, so an experiment can be repeated exactly.
