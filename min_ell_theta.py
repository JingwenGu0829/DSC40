"""Threshold learning helpers for separating red and blue points."""


def learn_theta(data, colors):
    """
    Given that every blue point is <= every red point, return a separating theta.

    Runs in O(n) by scanning once for the maximum blue and minimum red.
    """
    max_blue = None
    min_red = None
    for x, c in zip(data, colors):
        if c == "blue":
            max_blue = x if max_blue is None else max(max_blue, x)
        else:
            min_red = x if min_red is None else min(min_red, x)

    if max_blue is None or min_red is None:
        raise ValueError("Both red and blue points are required.")

    return (max_blue + min_red) / 2.0


def compute_ell(data, colors, theta):
    """
    Compute loss L(theta) = (# red points <= theta) + (# blue points > theta).

    Runs in O(n).
    """
    loss = 0
    for x, c in zip(data, colors):
        if c == "red":
            if x <= theta:
                loss += 1
        else:
            if x > theta:
                loss += 1
    return float(loss)


def minimize_ell(data, colors):
    """
    Quadratic-time search for a theta minimizing L on unsorted data.

    Assumes the smallest point is blue. Checks each data value as a candidate.
    """
    if not data:
        return None

    best_theta = None
    best_loss = None
    for theta in data:
        loss = compute_ell(data, colors, theta)
        if best_loss is None or loss < best_loss:
            best_loss = loss
            best_theta = theta
    return float(best_theta)


def minimize_ell_sorted(data, colors):
    """
    Linear-time minimizer for sorted data.

    Maintains the invariant: after processing index a, blue_gt_theta equals
    the number of blue points greater than data[a].
    """
    n = len(data)
    if n == 0:
        return None

    total_blue = sum(1 for c in colors if c == "blue")
    blue_gt_theta = total_blue  # theta is initially left of data[0]
    red_le_theta = 0

    best_theta = data[0]
    best_loss = blue_gt_theta  # no reds counted yet

    for x, c in zip(data, colors):
        if c == "red":
            red_le_theta += 1
        else:
            blue_gt_theta -= 1

        current_loss = red_le_theta + blue_gt_theta
        if current_loss < best_loss:
            best_loss = current_loss
            best_theta = x

    return float(best_theta)


__all__ = [
    "learn_theta",
    "compute_ell",
    "minimize_ell",
    "minimize_ell_sorted",
]

