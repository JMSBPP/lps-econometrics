
# Problem Stament
Given a risky underlying contract $X$

## Claims 
- LP's as market makers $\implies$ impermanent loss is not the appropriate metric for evaluating LP performance
$\implies$ Market makers should be benchmarked against a delta-neutral, short-variance reference strategy with the following risk profile:
(definitiion (needs reference))

| Risk  | Exposure |
| ----- | -------- |
| Delta | 0        |
| Gamma | −        |
| Vega  | −        |
| Theta | +        |
| Drift | 0        |

(Impermanent loss instead benchmarks LPs against HODL, which is a directional, volatility-exposed strategy that is long delta and long volatility). 

As a result, impermanent loss measures an opportunity cost relative to a strategy with a fundamentally different risk profile.
> definition (needs reference)

## Proposed Solution

Liquidity providers should be evaluated as sellers of variance, not as failed holders of the underlying.

If LPs are market makers $\implies $
- the benchmark must be:

    - Delta-neutral

    - Drift-neutral

    - Self-financing

    - Paid only for variance risk

The canonical benchmark is:

A short-variance, delta-neutral reference portfolio

not HODL, not cash, not forward

> Theorem (needs demonstration)

- If Theorem is true: Then:

    VAL-PnL measures LP performance relative to a delta-neutral short-variance benchmark, instead of HODL.
->    “Did the LP get paid fairly for the variance risk they sold?”

VAL-PnL=Theta
Fee Income​​−Gamma
Variance Cost​​−Design Flaw
Directional Leakage​​

## Solution Validation


1. Demonstrate theorem

> Assuming theorem is correct ...

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


impermanent loss is the difference between the delta of a gamma-neutral position and a short gamma position, parameterized by the convexity of the pricing function. If we were to use the initial inventory on a strip of short straddles over $[\psi_{\text{bid}}, \psi_{\text{ask}}]$—this strategy would strongly outperform the LP's strategy because the straddle is maximally gamma-exposed.


Impermanent loss is the difference between the value process of a delta-neutral, self-financing benchmark (e.g. strip of short straddles) and the value process of a short-gamma strategy induced by the CFMM.



- Find the theoretical variance and directional components of the impermanent loss.

$$

IL = \text{convexity term}~ \text{Variance term} + \text{drift sensitivity}~ \text{Directional term}
$$

The convexity is controlled by a parameter that manages the tradeoffs of short gamma exposure to arbitrageurs trading on mispricings.

IL is an intrinsic, non-zero cost for LPs. 
- it's taxonomy is to be pure path-dependant due to it's variance component
However the CLAMM desing flaw adds to it a directional component (path + terminal dependent)

However, one could argue that the directional term (Asymmetrically exposure to trends) is undesired and thus does not belong to the fair cost of IL. This implies that CLAMM fails to fully identify the profile of the LPs, and thus its design misprices its costs. In particular, it adds an undesired short delta component to the IL. In other words, market making is discouraged as the underlying contract price approaches $\psi_{\text{ask}}$. Thus, the LP's auto-rebalancing by the CLAMM is NOT delta neutral. 

- Delta neutrality holds only locally and instantaneously

- Over paths, LPs acquire systematic drift sensitivity

- This shows up as asymmetric exposure to trends



## Claims

- A classical CFMM implicitly forces LPs to sell both variance and direction, despite LPs intending to act as delta-neutral market makers.

- This induces an undesired directional component of impermanent loss, which is not intrinsic to market making and represents a design inefficiency.

# Problem Testing

If LPs are understood as market makers, what are the theoretical preferences and risk profiles of LPs?
- Expectation: They are supposed to unbiasedly (delta-neutral) make buy and sell orders within a price range. They must be neutral with respect to price direction. Thus, they are theoretically purely short variance.
- Null Hypothesis: They are short delta by CFMM design; thus, their market making worsens as the underlying contract appreciates.
    - Testable to-do:

        - Impermanent loss grows as price appreciates for a given range. (confirms impermanent loss has shot-delta componnent)
        - Build a trade efficiency metric; as price appreciates, it should decrease, explained by the impermanent loss.

- What are they naturally and unavoidably exposed to?

- What are they not supposed to be exposed to? What misconceptions or design flaws create these exposures?

What profile is the LP forced to take on in a CLAMM?

- What profile are they forced to take on in a CLAMM, what is the taxonomy of this profile, and in what cases is such a profile optimal?
Is it, or can it be, optimal for LPs?


# Solution Overview


We propose a CFMM whose trading function is derived from the payoff structure of a variance swap, such that:

LPs are pure sellers of realized variance

Delta exposure is structurally neutralized

Impermanent loss corresponds exactly to variance PnL

Fees compensate explicitly for variance risk

This reframes liquidity provision as intentional volatility selling, rather than accidental trend betting.

Move from “LPs sell convexity with accidental direction” to “LPs sell variance by design.”