from collections import Counter

def berechne_punkte(wuerfel: list[int]) -> dict:
    return {
        "Einsen": berechne_augen(wuerfel, 1),
        "Zweien": berechne_augen(wuerfel, 2),
        "Dreien": berechne_augen(wuerfel, 3),
        "Vieren": berechne_augen(wuerfel, 4),
        "Fünfen": berechne_augen(wuerfel, 5),
        "Sechsen": berechne_augen(wuerfel, 6),
        "Dreierpasch": berechne_dreierpasch(wuerfel),
        "Viererpasch": berechne_viererpasch(wuerfel),
        "Full House": berechne_full_house(wuerfel),
        "Kleine Straße": berechne_kleine_strasse(wuerfel),
        "Große Straße": berechne_grosse_strasse(wuerfel),
        "Kniffel": berechne_kniffel(wuerfel),
        "Chance": berechne_chance(wuerfel)
    }

def berechne_augen(wuerfel, zahl):
    return wuerfel.count(zahl) * zahl

def berechne_dreierpasch(wuerfel):
    counts = Counter(wuerfel)
    if any(count >= 3 for count in counts.values()):
        return sum(wuerfel)
    return 0

def berechne_viererpasch(wuerfel):
    counts = Counter(wuerfel)
    if any(count >= 4 for count in counts.values()):
        return sum(wuerfel)
    return 0

def berechne_full_house(wuerfel):
    counts = sorted(Counter(wuerfel).values())
    if counts == [2, 3]:
        return 25
    return 0

def berechne_kleine_strasse(wuerfel):
    sets = [set([1, 2, 3, 4]),
            set([2, 3, 4, 5]),
            set([3, 4, 5, 6])]
    w_set = set(wuerfel)
    for s in sets:
        if s.issubset(w_set):
            return 30
    return 0

def berechne_grosse_strasse(wuerfel):
    if set([1, 2, 3, 4, 5]).issubset(wuerfel) or set([2, 3, 4, 5, 6]).issubset(wuerfel):
        return 40
    return 0

def berechne_kniffel(wuerfel):
    if len(set(wuerfel)) == 1:
        return 50
    return 0

def berechne_chance(wuerfel):
    return sum(wuerfel)