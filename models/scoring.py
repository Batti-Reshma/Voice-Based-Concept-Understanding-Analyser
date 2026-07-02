def understanding_level(score):
    """
    Returns the understanding level based on
    the semantic similarity score.
    """

    if score >= 0.85:
        return "🟢 Strong Understanding"

    elif score >= 0.65:
        return "🟡 Moderate Understanding"

    else:
        return "🔴 Poor Understanding"