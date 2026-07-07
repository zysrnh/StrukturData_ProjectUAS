import difflib

# ============================================================
# MODUL 3: ALGORITMA FUZZY SEARCH (Levenshtein Distance)
# Digunakan untuk koreksi typo dan saran kata yang mirip
# ============================================================


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def get_fuzzy_suggestions(word, candidates, max_suggestions=5):
    if len(word) <= 2:
        max_distance = 1
    elif len(word) <= 4:
        max_distance = 2
    elif len(word) <= 7:
        max_distance = 2
    else:
        max_distance = 3

    matches = []
    for candidate in candidates:
        if abs(len(candidate) - len(word)) > max_distance:
            continue
        dist = levenshtein_distance(word, candidate)
        if dist <= max_distance and dist > 0:
            prefix_bonus = 0
            if len(word) >= 2 and len(candidate) >= 2:
                if word[:2] == candidate[:2]:
                    prefix_bonus = -0.5
            matches.append((candidate, dist + prefix_bonus))

    matches.sort(key=lambda item: (item[1], item[0]))
    if matches:
        return [(w, int(d)) for w, d in matches[:max_suggestions]]

    close_matches = difflib.get_close_matches(
        word, list(candidates), n=max_suggestions, cutoff=0.45)
    fallback = [(c, levenshtein_distance(word, c)) for c in close_matches]
    fallback.sort(key=lambda item: (item[1], item[0]))
    return fallback[:max_suggestions]
