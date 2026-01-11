If LPs are understood as market makers, what are the theoretical preferences and risk profiles of LPs?

Answer:

If LPs are market makers, their ideal exposure is:
| Risk  | Exposure |
| ----- | -------- |
| Delta | 0        |
| Gamma | −        |
| Vega  | −        |
| Theta | +        |
| Drift | 0        |


- Expectation: They are supposed to unbiasedly (delta-neutral) make buy and sell orders within a price range. They must be neutral with respect to price direction. Thus, they are theoretically purely short variance.
- Null Hypothesis: They are short delta by CFMM design; thus, their market making worsens as the underlying contract appreciates.
    - Testable to-do:

        - Impermanent loss grows as price appreciates for a given range. (confirms impermanent loss has shot-delta componnent)
        - Build a trade efficiency metric; as price appreciates, it should decrease, explained by the impermanent loss.

- What are they naturally and unavoidably exposed to?

Answer:

- Short gamma / convexity

- Inventory risk at infinitesimal time scales

- Liquidity risk



- What are they not supposed to be exposed to? What misconceptions or design flaws create these exposures?

Avoidable:

Systematic drift exposure

Asymmetric upside loss

Trend-dependent capital erosion

Thus, directional exposure is not fundamental; it is design-induced.


What profile are they forced to take on in a CLAMM, what is the taxonomy of this profile, and in what cases is such a profile optimal?
Is it, or can it be, optimal for LPs?

A CLAMM forces LPs into:

Short gamma + short upside drift + long theta

More precisely:

Negative gamma

Delta that becomes increasingly negative as price rises

Asymmetric exposure near upper bounds

This is not a canonical market-making profile.
It is closer to:

A covered call writer with forced rebalancing

A barrier short straddle with skew

The problem is that That’s a speculative volatility strategy, not neutral market making.Such profile is optimal only when:

Price is mean-reverting

Volatility is high relative to drift

LPs have strong conviction about bounded upside