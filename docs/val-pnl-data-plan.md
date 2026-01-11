2. For a set of pools do the right smapling and everyhing and get   

VAL-PnL = Theta
Fee Income − Gamma
Variance Cost − Design Flaw
Directional Leakage

For all these pools, then:

- Find the Directional Leakage component of the Val-PNL and demonstrate its
    - existence — show that it is not artificial, is time-invariant, and possesses the relevant econometric properties for this error term
    - consistency among all pools
    - worsening in certain pools
    - validate that the identified error term coincides with the theoretical definition of directional leakage



 Premliminary work

 Let's simplify the work. What is the simplest CFMM where we can do the analysis, and its simplicity does not affect the results?

 Claim: Uniswap V2
-  Hypothesis 
    - If the directional leakage problem exists in v2, it is fundamental — not an artifact of concentration or LP strategy.


# Cross-Sectional

0. Let's fix a time: $t_0$ (good time to analyse)
--> time were the number of LP'S was the highest over a specifed time interval
AND the liqudiity was high too

1. Define the LP-Value

$$
\Pi^{\text{\texttt{LP}}} \big (P \big) = 2L\sqrt{P}
$$

The lp-payoff is then


$$
\begin{align*}

\Pi_{i}^{\text{\texttt{LP}}} \big (P \big) = 2Lw_i\sqrt{P}

\end{align*}
$$

where $\sum_{i=1}^{\# \text{lp's}} w_i = 1$

In uniswap V2, LP-tokens are fungible were totalSupply represents the total liquidity and each lp balance of the token represents and the LP's account balance of this token is it's liquidity contributiuon to the pool. Thus $w_i = \frac{s_i}{S}$ under the invariant $\sum_{i=1}^{\# \text{lp's}} s_i = S$, Then each lp's position value can be written m,opre explicityly as

$$
\begin{align*}

\Pi_{i}^{\text{\texttt{LP}}} \big (P \big) = 2L\big ( \frac{s_i}{S}\big)\sqrt{P}

\end{align*}
$$

## LP's position Cross-Sectional Greeks

The inmediate lp-position delta is:

$$
\begin{cases}
\Delta_i &= \partial_{P} \Pi_i^{\text{\texttt{LP}}} 
         &= L\cdot \big (\frac{s_i}{S\cdot\sqrt{P}}\big) \\
        \\
\Gamma_i &= \partial^2_{P} \Pi_i^{\text{\texttt{LP}}}
         &= \frac{-L}{2}\cdot \big( \frac{s_i}{S\cdot\sqrt{P^3}}\big)
\end{cases}
$$


> Long theta is not incorporated becuase this is cross-sectional and we are not analysing time here.
Vega does not apply to V2 because all LP's are have same exposure to volatility as they can not concentrate liquidity


We expect LP's to be gamma-neutral $\Delta_i = 0$. However we might see that LP's indeed have have 
- assymetric directional exposure, more specifically they are slightly short delta

The approach is to define the directional leakage $\delta (\Delta)$ as the component of delta that is not explained by gamma.
Formally we define:

$$
\Delta_i​=\beta_0+\beta_1\Gamma_i + \varepsilon_i​ \\
\\
\implies \delta_i(\Delta) = \varepsilon_i
$$

Where $\mathbb{E} \big [\delta_i(\Delta) \big | \Gamma_i \big] = 0$

What tests do I need here ? ...

[TEST PASSES] -->

$$
\Pi_{i}^{\text{\texttt{LP}}} = \overline{\beta_0} + \beta_{\text{\texttt{var}}}\Gamma_i + \beta_{\text{\texttt{leak}}}\delta_i(\Delta_i) + u_i
$$

Under:

$$
H_0: \beta_{\text{\texttt{leak}}} = 0 \\
H_1: \beta_{\text{\texttt{leak}}} < 0
$$


What test passes here ?

This proofs empirically LP'S are NOT delta neutral. And the negative sign shows they are short delta. 

# Time-Series
# Panel-Data