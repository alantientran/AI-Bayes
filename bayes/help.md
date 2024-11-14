## Generalized Rules for Joining Factors in Bayesian Networks

### 1. Identify Shared Variables
   When joining two or more factors, identify any variables they share, either as conditioned (given) variables or variables in their distributions.

### 2. Multiply the Probabilities
   For two factors \( P(A | B) \) and \( P(B) \), the joint probability \( P(A, B) \) can be formed by multiplying these factors:
   \[
   P(A | B) \times P(B) = P(A, B)
   \]
   In general, multiplying factors \( P(X | Y, Z) \) and \( P(Y | Z) \) results in a new joint factor \( P(X, Y | Z) \) when they share the same conditioned variable \( Z \).

### 3. Conditioned Variables Stay in the Denominator
   When you multiply factors with shared conditioned variables (variables following a “|” symbol), those conditioned variables stay in the denominator. So, for \( P(X | Y, Z) \times P(Y | Z) \), you keep the condition \( Z \) in the final factor:
   \[
   P(X | Y, Z) \times P(Y | Z) = P(X, Y | Z)
   \]

### 4. Ensure Consistent Conditioning Across Factors
   When combining factors with independent variables, you can directly multiply them without needing to add extra conditions. For example, if \( Z \) is independent of \( W \) and \( Y \), the factors \( P(Z) \), \( P(V | W) \), and \( P(X | Y) \) can be multiplied without changing their conditions:
   \[
   P(V | W) \times P(X | Y) \times P(Z) = P(V, X, Z | W, Y)
   \]

### 5. General Formula for Joining Factors
   If you have factors \( P(X_1 | Y_1) \), \( P(X_2 | Y_2) \), ..., \( P(X_n | Y_n) \) and want to join them into a single joint factor, multiply all factors that share any conditional dependencies:
   \[
   \text{joinFactors}(P(X_1 | Y_1), P(X_2 | Y_2), \dots, P(X_n | Y_n)) = P(X_1, X_2, \dots, X_n | Y_1 \cup Y_2 \cup \dots \cup Y_n)
   \]
   where \( Y_1 \cup Y_2 \cup \dots \cup Y_n \) is the union of all conditioned variables across factors.

### Summary of Steps

1. **Multiply** all factors that contain overlapping variables (either in their distributions or conditions).
2. **Keep all conditional dependencies consistent** in the final joined factor, preserving shared conditions.
3. **Avoid redundant conditions** by assuming independence where appropriate.

These steps should allow you to join factors in a systematic way across a variety of cases in Bayesian networks.
