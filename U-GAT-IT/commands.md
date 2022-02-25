## Train
- gender:
    > `python main --datasets [path_to]/gender`
- glasses:
    > `python main --datasets [path_to]/glasses`

The trained model will be saved to `[path_to]/[dataset]/model`

## Test
- gender:
    > `python main --datasets [path_to]/gender --phase test`
- glasses:
    > `python main --datasets [path_to]/glasses --phase test`

The test output will be saved to `[path_to]/[dataset]/test`.
I modified the code a little bit so that
A to B translation result (fake B images) will be saved to `[path_to]/[dataset]/test/A2B`, and
the B to A, `[path_to]/[dataset]/test/B2A`.
