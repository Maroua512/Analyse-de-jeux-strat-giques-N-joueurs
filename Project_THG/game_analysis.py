from typing import Dict, List, Sequence, Set, Tuple


Profile = Tuple[int, ...]
Payoff = Tuple[float, ...]
Payoffs = Dict[Profile, Payoff]


# Calcule les stratégies strictement dominantes et l'équilibre correspondant.
def calculate_dominant_strategies(num_players: int, strategies_per_player: Sequence[int], profiles: Sequence[Profile], payoffs: Payoffs) -> str:
    dominant_strategies: Dict[int, Set[int]] = {player: set() for player in range(num_players)}
    for player in range(num_players):
        for first_strategy in range(strategies_per_player[player]):
            strictly_dominates = True
            for second_strategy in range(strategies_per_player[player]):
                if first_strategy == second_strategy:
                    continue
                for profile in profiles:
                    if profile[player] != second_strategy:
                        continue
                    alternative = list(profile)
                    alternative[player] = first_strategy
                    if payoffs[tuple(alternative)][player] <= payoffs[profile][player]:
                        strictly_dominates = False
                        break
                if not strictly_dominates:
                    break
            if strictly_dominates:
                dominant_strategies[player].add(first_strategy)

    result = "\n".join(
        f"Joueur {player + 1} : stratégies strictement dominantes : {sorted(strategies) if strategies else 'Aucune'}"
        for player, strategies in dominant_strategies.items()
    )
    if all(len(strategies) == 1 for strategies in dominant_strategies.values()):
        equilibrium = tuple(next(iter(strategies)) for strategies in dominant_strategies.values())
        result += f"\n\n Équilibre en stratégies dominantes trouvé : {equilibrium}"
    else:
        result += "\n\n Aucun équilibre en stratégies dominantes (ou plusieurs dominantes par joueur)."
    return result


# Calcule les stratégies faiblement dominantes et l'équilibre correspondant.
def calculate_weakly_dominant_strategies(num_players: int, strategies_per_player: Sequence[int], profiles: Sequence[Profile], payoffs: Payoffs) -> str:
    dominant_strategies: Dict[int, Set[int]] = {player: set() for player in range(num_players)}
    for player in range(num_players):
        for first_strategy in range(strategies_per_player[player]):
            weakly_dominates = True
            strictly_better_once = False
            for second_strategy in range(strategies_per_player[player]):
                if first_strategy == second_strategy:
                    continue
                for profile in profiles:
                    if profile[player] != second_strategy:
                        continue
                    alternative = list(profile)
                    alternative[player] = first_strategy
                    if payoffs[tuple(alternative)][player] < payoffs[profile][player]:
                        weakly_dominates = False
                        break
                    if payoffs[tuple(alternative)][player] > payoffs[profile][player]:
                        strictly_better_once = True
                if not weakly_dominates:
                    break
            if weakly_dominates and strictly_better_once:
                dominant_strategies[player].add(first_strategy)

    result = "\n" + "\n".join(
        f"Joueur {player + 1} : stratégies faiblement dominantes : {sorted(strategies) if strategies else 'Aucune'}"
        for player, strategies in dominant_strategies.items()
    )
    if all(len(strategies) == 1 for strategies in dominant_strategies.values()):
        equilibrium = tuple(next(iter(strategies)) for strategies in dominant_strategies.values())
        result += f"\n\n Équilibre en stratégies faiblement dominantes trouvé : {equilibrium}"
    else:
        result += "\n\n Aucun équilibre en stratégies faiblement dominantes (ou plusieurs dominantes par joueur)."
    return result


# Recherche les profils dans lesquels aucun joueur ne peut améliorer son gain seul.
def calculate_nash_equilibria(num_players: int, strategies_per_player: Sequence[int], profiles: Sequence[Profile], payoffs: Payoffs) -> str:
    equilibria: List[Profile] = []
    for profile in profiles:
        is_nash = True
        for player in range(num_players):
            for alternative_strategy in range(strategies_per_player[player]):
                if alternative_strategy == profile[player]:
                    continue
                alternative = list(profile)
                alternative[player] = alternative_strategy
                if payoffs[tuple(alternative)][player] > payoffs[profile][player]:
                    is_nash = False
                    break
            if not is_nash:
                break
        if is_nash:
            equilibria.append(profile)
    return "\n" + "\n".join(
        [f"Équilibre de Nash : {profile}" for profile in equilibria]
        or ["Aucun équilibre de Nash trouvé"]
    )


# Identifie les profils de Pareto qui ne sont dominés par aucun autre profil.
def calculate_pareto_optima(num_players: int, profiles: Sequence[Profile], payoffs: Payoffs) -> str:
    pareto_optima: List[Profile] = []
    for profile in profiles:
        is_dominated = False
        for other in profiles:
            if profile == other:
                continue
            better_or_equal = all(payoffs[other][player] >= payoffs[profile][player] for player in range(num_players))
            strictly_better = any(payoffs[other][player] > payoffs[profile][player] for player in range(num_players))
            if better_or_equal and strictly_better:
                is_dominated = True
                break
        if not is_dominated:
            pareto_optima.append(profile)
    return "\n" + "\n".join(
        [f"Profil optimal de Pareto : {profile}" for profile in pareto_optima]
        or ["Aucun optimum de Pareto trouvé"]
    )


# Calcule le niveau de sécurité garanti par chaque joueur avec sa meilleure stratégie prudente.
def calculate_security_levels(num_players: int, strategies_per_player: Sequence[int], profiles: Sequence[Profile], payoffs: Payoffs) -> str:
    result = ""
    for player in range(num_players):
        minimum_payoffs = []
        for strategy in range(strategies_per_player[player]):
            outcomes = [payoffs[profile][player] for profile in profiles if profile[player] == strategy]
            if outcomes:
                minimum_payoffs.append(min(outcomes))
        level = max(minimum_payoffs) if minimum_payoffs else "Inconnu"
        result += f"Niveau de sécurité du joueur {player + 1} : {level}\n"
    return result


# Élimine successivement les stratégies dominées et décrit la matrice restante.
def calculate_iterated_elimination(num_players: int, strategies_per_player: Sequence[int], profiles: Sequence[Profile], payoffs: Payoffs) -> str:
    remaining_strategies = {player: set(range(strategies_per_player[player])) for player in range(num_players)}
    remaining_profiles = set(profiles)
    elimination_steps = []

    # Vérifie si une stratégie est strictement ou faiblement dominée par une autre.
    def dominance_type(player: int, strategy: int, alternative_strategy: int) -> str | None:
        comparisons = []
        for profile in remaining_profiles:
            if profile[player] != strategy:
                continue
            alternative = list(profile)
            alternative[player] = alternative_strategy
            alternative_profile = tuple(alternative)
            if alternative_profile in payoffs:
                comparisons.append((payoffs[alternative_profile][player], payoffs[profile][player]))

        if not comparisons:
            return None
        if all(alternative > current for alternative, current in comparisons):
            return "strictement"
        if all(alternative >= current for alternative, current in comparisons) and any(
            alternative > current for alternative, current in comparisons
        ):
            return "faiblement"
        return None

    changed = True
    while changed:
        changed = False
        for player in range(num_players):
            for strategy in list(remaining_strategies[player]):
                for alternative_strategy in list(remaining_strategies[player]):
                    if strategy == alternative_strategy:
                        continue
                    domination = dominance_type(player, strategy, alternative_strategy)
                    if domination is not None:
                        remaining_strategies[player].discard(strategy)
                        elimination_steps.append(
                            f"Joueur {player + 1} : stratégie {strategy} éliminée "
                            f"({domination} dominée par {alternative_strategy})"
                        )
                        changed = True
                        break
                if changed:
                    break
            if changed:
                remaining_profiles = {
                    profile for profile in remaining_profiles
                    if all(profile[p] in remaining_strategies[p] for p in range(num_players))
                }
                break

    result = "\nÉlimination itérative des stratégies strictement et faiblement dominées :\n"
    result += "\n".join(elimination_steps) if elimination_steps else "Aucune stratégie strictement ou faiblement dominée détectée."
    result += "\n\nMatrice réduite après élimination :\n"
    result += "".join(f"{profile} : {payoffs[profile]}\n" for profile in sorted(remaining_profiles))
    if len(remaining_profiles) == 1:
        result += f"\n Équilibre trouvé par élimination successive : {next(iter(remaining_profiles))}"
    else:
        result += f"\n Aucun équilibre unique trouvé par élimination successive (profils restants : {len(remaining_profiles)})"
    return result