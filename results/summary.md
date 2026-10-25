### Agents = 5, budget = 25% of demand, cost noise = ±40% (mean over seeds)

| Allocator | Mechanism | Strategy | Welfare / budget | Success | Jain | Wasted | Unspent | Transfers |
|---|---|---|---|---|---|---|---|---|
| split | proportional_fair | naive | 0.775 ± 0.440 | 14.3% | 0.981 | 65.5% | 0.0% | 0 |
| split | proportional_fair | mechanism_aware | 0.492 ± 0.436 | 9.8% | 0.539 | 0.9% | 74.7% | 0 |
| split | proportional_fair | mixed | 0.952 ± 0.462 | 16.0% | 0.244 | 48.9% | 3.1% | 0 |
| split | priority_auction | naive | 1.613 ± 0.434 | 21.5% | 0.315 | 20.8% | 0.0% | 5164 |
| split | priority_auction | mechanism_aware | 1.670 ± 0.504 | 20.2% | 0.552 | 2.4% | 20.9% | 1620 |
| split | priority_auction | mixed | 1.529 ± 0.564 | 20.8% | 0.258 | 10.4% | 10.3% | 3873 |
| split | vcg | naive | 1.613 ± 0.434 | 21.5% | 0.315 | 20.8% | 0.0% | 4868 |
| split | vcg | mechanism_aware | 1.670 ± 0.504 | 20.2% | 0.552 | 2.4% | 20.9% | 1081 |
| split | vcg | mixed | 1.529 ± 0.564 | 20.8% | 0.258 | 10.4% | 10.3% | 1497 |
| whole | proportional_fair | naive | 1.362 ± 0.366 | 18.2% | 0.200 | 8.5% | 22.6% | 0 |
| whole | proportional_fair | mechanism_aware | 1.814 ± 0.495 | 25.5% | 0.555 | 3.8% | 10.4% | 0 |
| whole | proportional_fair | mixed | 1.639 ± 0.410 | 26.2% | 0.379 | 4.4% | 10.3% | 0 |
| whole | priority_auction | naive | 1.362 ± 0.366 | 18.2% | 0.200 | 8.5% | 22.6% | 3979 |
| whole | priority_auction | mechanism_aware | 1.831 ± 0.468 | 25.3% | 0.567 | 3.8% | 9.5% | 1791 |
| whole | priority_auction | mixed | 1.613 ± 0.437 | 24.8% | 0.325 | 5.1% | 9.8% | 3454 |
| whole | vcg | naive | 1.362 ± 0.366 | 18.2% | 0.200 | 8.5% | 22.6% | 3931 |
| whole | vcg | mechanism_aware | 1.831 ± 0.468 | 25.3% | 0.567 | 3.8% | 9.5% | 1179 |
| whole | vcg | mixed | 1.613 ± 0.437 | 24.8% | 0.325 | 5.1% | 9.8% | 1278 |

### Agents = 5, budget = 50% of demand, cost noise = ±40% (mean over seeds)

| Allocator | Mechanism | Strategy | Welfare / budget | Success | Jain | Wasted | Unspent | Transfers |
|---|---|---|---|---|---|---|---|---|
| split | proportional_fair | naive | 1.352 ± 0.343 | 39.7% | 0.981 | 27.9% | 0.0% | 0 |
| split | proportional_fair | mechanism_aware | 1.235 ± 0.343 | 35.8% | 0.815 | 2.5% | 34.1% | 0 |
| split | proportional_fair | mixed | 1.375 ± 0.337 | 38.5% | 0.554 | 12.5% | 14.8% | 0 |
| split | priority_auction | naive | 1.630 ± 0.369 | 42.0% | 0.539 | 17.6% | 0.0% | 10077 |
| split | priority_auction | mechanism_aware | 1.715 ± 0.371 | 44.3% | 0.814 | 4.6% | 10.0% | 3365 |
| split | priority_auction | mixed | 1.618 ± 0.442 | 44.0% | 0.625 | 8.9% | 7.4% | 5775 |
| split | vcg | naive | 1.630 ± 0.369 | 42.0% | 0.539 | 17.6% | 0.0% | 8933 |
| split | vcg | mechanism_aware | 1.715 ± 0.371 | 44.3% | 0.814 | 4.6% | 10.0% | 1023 |
| split | vcg | mixed | 1.618 ± 0.442 | 44.0% | 0.628 | 8.0% | 8.3% | 759 |
| whole | proportional_fair | naive | 1.463 ± 0.311 | 37.5% | 0.406 | 15.4% | 10.1% | 0 |
| whole | proportional_fair | mechanism_aware | 1.773 ± 0.386 | 49.8% | 0.843 | 5.0% | 5.5% | 0 |
| whole | proportional_fair | mixed | 1.655 ± 0.454 | 47.3% | 0.651 | 7.3% | 5.3% | 0 |
| whole | priority_auction | naive | 1.463 ± 0.311 | 37.5% | 0.406 | 15.4% | 10.1% | 9081 |
| whole | priority_auction | mechanism_aware | 1.765 ± 0.389 | 48.7% | 0.836 | 5.0% | 5.6% | 3456 |
| whole | priority_auction | mixed | 1.655 ± 0.454 | 47.3% | 0.651 | 7.3% | 5.3% | 5722 |
| whole | vcg | naive | 1.463 ± 0.311 | 37.5% | 0.406 | 15.4% | 10.1% | 7071 |
| whole | vcg | mechanism_aware | 1.765 ± 0.389 | 48.7% | 0.836 | 5.0% | 5.6% | 985 |
| whole | vcg | mixed | 1.655 ± 0.454 | 47.3% | 0.651 | 7.3% | 5.3% | 1009 |

### Agents = 5, budget = 75% of demand, cost noise = ±40% (mean over seeds)

| Allocator | Mechanism | Strategy | Welfare / budget | Success | Jain | Wasted | Unspent | Transfers |
|---|---|---|---|---|---|---|---|---|
| split | proportional_fair | naive | 1.495 ± 0.245 | 65.7% | 0.978 | 19.6% | 0.0% | 0 |
| split | proportional_fair | mechanism_aware | 1.411 ± 0.318 | 60.2% | 0.916 | 3.6% | 21.2% | 0 |
| split | proportional_fair | mixed | 1.453 ± 0.331 | 62.3% | 0.801 | 10.9% | 10.6% | 0 |
| split | priority_auction | naive | 1.626 ± 0.305 | 66.8% | 0.785 | 14.1% | 0.0% | 14519 |
| split | priority_auction | mechanism_aware | 1.654 ± 0.307 | 67.7% | 0.892 | 6.0% | 7.4% | 4980 |
| split | priority_auction | mixed | 1.567 ± 0.337 | 65.2% | 0.822 | 11.6% | 4.9% | 7480 |
| split | vcg | naive | 1.626 ± 0.305 | 66.8% | 0.785 | 14.1% | 0.0% | 11440 |
| split | vcg | mechanism_aware | 1.654 ± 0.307 | 67.7% | 0.892 | 6.0% | 7.4% | 851 |
| split | vcg | mixed | 1.572 ± 0.332 | 65.3% | 0.825 | 11.3% | 4.9% | 719 |
| whole | proportional_fair | naive | 1.459 ± 0.294 | 59.2% | 0.612 | 17.9% | 5.9% | 0 |
| whole | proportional_fair | mechanism_aware | 1.701 ± 0.298 | 72.0% | 0.895 | 6.5% | 3.9% | 0 |
| whole | proportional_fair | mixed | 1.591 ± 0.340 | 68.7% | 0.843 | 10.1% | 4.1% | 0 |
| whole | priority_auction | naive | 1.475 ± 0.299 | 60.3% | 0.627 | 16.7% | 6.0% | 13650 |
| whole | priority_auction | mechanism_aware | 1.695 ± 0.306 | 71.5% | 0.897 | 6.9% | 3.7% | 5122 |
| whole | priority_auction | mixed | 1.585 ± 0.340 | 67.8% | 0.837 | 10.8% | 4.0% | 7438 |
| whole | vcg | naive | 1.475 ± 0.299 | 60.3% | 0.627 | 16.7% | 6.0% | 9628 |
| whole | vcg | mechanism_aware | 1.695 ± 0.306 | 71.5% | 0.897 | 6.9% | 3.7% | 957 |
| whole | vcg | mixed | 1.588 ± 0.335 | 68.0% | 0.840 | 10.4% | 4.2% | 819 |

### Agents = 5, budget = 25% of demand, cost noise = ±0% (mean over seeds)

| Allocator | Mechanism | Strategy | Welfare / budget | Success | Jain | Wasted | Unspent | Transfers |
|---|---|---|---|---|---|---|---|---|
| split | proportional_fair | naive | 0.677 ± 0.275 | 14.0% | 0.981 | 62.3% | 0.0% | 0 |
| split | proportional_fair | mechanism_aware | 1.412 ± 0.371 | 20.8% | 0.685 | 0.0% | 26.1% | 0 |
| split | proportional_fair | mixed | 1.150 ± 0.320 | 18.3% | 0.286 | 39.6% | 2.0% | 0 |
| split | priority_auction | naive | 1.666 ± 0.313 | 22.3% | 0.299 | 13.4% | 0.0% | 4985 |
| split | priority_auction | mechanism_aware | 1.765 ± 0.400 | 23.0% | 0.751 | 0.0% | 10.6% | 1225 |
| split | priority_auction | mixed | 1.697 ± 0.329 | 23.2% | 0.274 | 2.6% | 7.5% | 3677 |
| split | vcg | naive | 1.666 ± 0.313 | 22.3% | 0.299 | 13.4% | 0.0% | 4697 |
| split | vcg | mechanism_aware | 1.765 ± 0.400 | 23.0% | 0.751 | 0.0% | 10.6% | 272 |
| split | vcg | mixed | 1.697 ± 0.329 | 23.2% | 0.274 | 2.6% | 7.5% | 1041 |
| whole | proportional_fair | naive | 1.499 ± 0.362 | 20.0% | 0.200 | 0.0% | 22.4% | 0 |
| whole | proportional_fair | mechanism_aware | 1.850 ± 0.414 | 26.0% | 0.764 | 0.0% | 4.8% | 0 |
| whole | proportional_fair | mixed | 1.745 ± 0.329 | 28.2% | 0.416 | 0.0% | 6.0% | 0 |
| whole | priority_auction | naive | 1.499 ± 0.362 | 20.0% | 0.200 | 0.0% | 22.4% | 3896 |
| whole | priority_auction | mechanism_aware | 1.852 ± 0.430 | 25.5% | 0.760 | 0.0% | 4.7% | 1284 |
| whole | priority_auction | mixed | 1.750 ± 0.347 | 26.3% | 0.342 | 0.0% | 5.7% | 3297 |
| whole | vcg | naive | 1.499 ± 0.362 | 20.0% | 0.200 | 0.0% | 22.4% | 3931 |
| whole | vcg | mechanism_aware | 1.852 ± 0.430 | 25.5% | 0.760 | 0.0% | 4.7% | 492 |
| whole | vcg | mixed | 1.750 ± 0.347 | 26.3% | 0.342 | 0.0% | 5.7% | 1005 |

### Agents = 5, budget = 50% of demand, cost noise = ±0% (mean over seeds)

| Allocator | Mechanism | Strategy | Welfare / budget | Success | Jain | Wasted | Unspent | Transfers |
|---|---|---|---|---|---|---|---|---|
| split | proportional_fair | naive | 1.338 ± 0.258 | 38.5% | 0.981 | 28.5% | 0.0% | 0 |
| split | proportional_fair | mechanism_aware | 1.611 ± 0.266 | 45.0% | 0.895 | 0.0% | 14.5% | 0 |
| split | proportional_fair | mixed | 1.525 ± 0.206 | 43.5% | 0.643 | 0.0% | 17.1% | 0 |
| split | priority_auction | naive | 1.817 ± 0.238 | 46.2% | 0.522 | 5.6% | 0.0% | 9685 |
| split | priority_auction | mechanism_aware | 1.810 ± 0.273 | 48.3% | 0.914 | 0.0% | 4.2% | 2514 |
| split | priority_auction | mixed | 1.787 ± 0.252 | 48.5% | 0.718 | 0.0% | 5.2% | 4988 |
| split | vcg | naive | 1.817 ± 0.238 | 46.2% | 0.522 | 5.6% | 0.0% | 8568 |
| split | vcg | mechanism_aware | 1.810 ± 0.273 | 48.3% | 0.914 | 0.0% | 4.2% | 345 |
| split | vcg | mixed | 1.787 ± 0.252 | 48.5% | 0.718 | 0.0% | 5.2% | 362 |
| whole | proportional_fair | naive | 1.632 ± 0.249 | 41.3% | 0.406 | 0.0% | 16.0% | 0 |
| whole | proportional_fair | mechanism_aware | 1.836 ± 0.274 | 50.2% | 0.913 | 0.0% | 2.6% | 0 |
| whole | proportional_fair | mixed | 1.817 ± 0.243 | 50.8% | 0.735 | 0.0% | 2.6% | 0 |
| whole | priority_auction | naive | 1.632 ± 0.249 | 41.3% | 0.406 | 0.0% | 16.0% | 8209 |
| whole | priority_auction | mechanism_aware | 1.837 ± 0.273 | 49.8% | 0.915 | 0.0% | 2.7% | 2553 |
| whole | priority_auction | mixed | 1.817 ± 0.243 | 50.8% | 0.735 | 0.0% | 2.6% | 5029 |
| whole | vcg | naive | 1.632 ± 0.249 | 41.3% | 0.406 | 0.0% | 16.0% | 6903 |
| whole | vcg | mechanism_aware | 1.837 ± 0.273 | 49.8% | 0.915 | 0.0% | 2.7% | 480 |
| whole | vcg | mixed | 1.817 ± 0.243 | 50.8% | 0.735 | 0.0% | 2.6% | 379 |

### Agents = 5, budget = 75% of demand, cost noise = ±0% (mean over seeds)

| Allocator | Mechanism | Strategy | Welfare / budget | Success | Jain | Wasted | Unspent | Transfers |
|---|---|---|---|---|---|---|---|---|
| split | proportional_fair | naive | 1.501 ± 0.221 | 65.2% | 0.981 | 17.0% | 0.0% | 0 |
| split | proportional_fair | mechanism_aware | 1.648 ± 0.209 | 70.7% | 0.945 | 0.0% | 8.3% | 0 |
| split | proportional_fair | mixed | 1.621 ± 0.234 | 69.5% | 0.899 | 0.0% | 10.3% | 0 |
| split | priority_auction | naive | 1.814 ± 0.202 | 72.3% | 0.760 | 3.2% | 0.0% | 13967 |
| split | priority_auction | mechanism_aware | 1.760 ± 0.218 | 73.7% | 0.937 | 0.0% | 2.7% | 3668 |
| split | priority_auction | mixed | 1.762 ± 0.182 | 73.8% | 0.912 | 0.0% | 3.2% | 6177 |
| split | vcg | naive | 1.814 ± 0.202 | 72.3% | 0.760 | 3.2% | 0.0% | 11019 |
| split | vcg | mechanism_aware | 1.760 ± 0.218 | 73.7% | 0.937 | 0.0% | 2.7% | 258 |
| split | vcg | mixed | 1.762 ± 0.182 | 73.8% | 0.912 | 0.0% | 3.2% | 322 |
| whole | proportional_fair | naive | 1.581 ± 0.170 | 62.7% | 0.607 | 0.0% | 16.3% | 0 |
| whole | proportional_fair | mechanism_aware | 1.779 ± 0.220 | 75.3% | 0.943 | 0.0% | 1.8% | 0 |
| whole | proportional_fair | mixed | 1.781 ± 0.186 | 76.2% | 0.913 | 0.0% | 1.6% | 0 |
| whole | priority_auction | naive | 1.591 ± 0.188 | 62.7% | 0.608 | 0.0% | 16.2% | 11939 |
| whole | priority_auction | mechanism_aware | 1.775 ± 0.223 | 75.0% | 0.938 | 0.0% | 1.9% | 3698 |
| whole | priority_auction | mixed | 1.783 ± 0.185 | 75.8% | 0.912 | 0.0% | 1.6% | 6223 |
| whole | vcg | naive | 1.591 ± 0.188 | 62.7% | 0.608 | 0.0% | 16.2% | 9230 |
| whole | vcg | mechanism_aware | 1.775 ± 0.223 | 75.0% | 0.938 | 0.0% | 1.9% | 443 |
| whole | vcg | mixed | 1.783 ± 0.185 | 75.8% | 0.912 | 0.0% | 1.6% | 426 |
