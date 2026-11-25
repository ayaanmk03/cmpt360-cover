# cmpt360-cover
CMPT360 – Cover: Orange Trees, Cacti and Sprinklers

## Problem

Choose a subset of sprinklers that waters every orange tree while minimizing the
number of distinct cacti watered. A cactus covered by multiple sprinklers counts
once.

## Inputs

All positions lie on the same horizontal line.

| Array | Meaning |
| --- | --- |
| `O` | Positions of orange trees |
| `C` | Positions of cacti |
| `S` | Positions of sprinklers |
| `R` | Watering radii in the same order as `S` |

Sprinkler `i` waters every position from `S[i] - R[i]` to `S[i] + R[i]`,
including both endpoints.

## Example

```python
O = [2, 6, 11]
C = [4, 8, 14]
S = [3, 7, 12]
R = [2, 2, 1]
```

The watering intervals are `[1, 5]`, `[5, 9]`, and `[11, 13]`. Each orange
tree lies in exactly one interval, so all three sprinklers are required. The
selected sprinklers water the cacti at 4 and 8, giving an optimal count of 2.
