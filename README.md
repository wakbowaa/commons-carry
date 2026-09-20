# Commons Carry

## The rule of the shared channel

Finished work earns its full mark. Missing work earns none. Partial work keeps its honest credit—and only the unfinished balance travels forward.

That is the entire social promise behind Commons Carry. A convener writes a round of member-specific commons pledges and points. A separate keeper later anchors two independent work logs. GenLayer consensus assigns each pledge to `completed`, `partial`, or `missing` and reports earned points. The contract enforces the arithmetic and derives carry points itself.

### Example tally

```text
upper field   10 promised / 10 earned / 0 carried
lower field    8 promised /  3 earned / 5 carried
```

No pledge can disappear from the tally. Completed marks require full points; missing marks require zero; partial marks must sit strictly between. The source bytes and their SHA-256 digests remain in the round record.

### Seasonal rhythm

`CONVENED` → `BALANCED` → `SETTLED`

`CONVENED` → `CARRY_OPEN` → fresh audit or `CARRIED`

Closures are permissionless after the review deadline. A cure uses a changed pair of log origins, avoiding a cosmetic replay of the same evidence.

### Try the tally

Run the GenVM linter and `pytest`. The direct tests check full settlement, partial-credit arithmetic, keeper authority, independent witnesses, and validator resistance to inflated credit. Live transaction arguments are staged in `evidence/`.
