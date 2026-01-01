from rich.markdown import Markdown
from rich.console import Console
from rich.style import Style

from pathlib import Path

import time
import json
import sys

import _types


console = Console()

ERROR_STYLE = Style(
    color="bright_red",
)

TO_BUY_GADGETS = 7
TO_BUY_1_GEAR = 8
TO_BUY_STARPOWER = 9
TO_BUY_2_GEAR = 10
TO_BUY_HYPERCHARGE = 11


def _load_resources() -> _types.LevelUpResources:
    resources_file: Path = Path(__file__).parent / "upgrade-resources.json"

    try:
        resources = json.loads(
            resources_file.read_text(
                encoding="utf-8",
            ),
        )
    except (json.JSONDecodeError, FileNotFoundError):
        console.print(
            "Cannot calculate level up resources: upgrade resources missing.",
            style=ERROR_STYLE,
        )
        sys.exit(1)

    resources = _types.LevelUpResources(**resources)
    return resources


def _check_int(value: str) -> int | str:
    try:
        return int(value)
    except Exception:
        console.print("\nValor inválido.")
        console.rule(style=ERROR_STYLE)
        return value


def _get_initial_level() -> int:
    initial_level = console.input("Qual o nível inicial do brawler? (1-11) ").strip()

    int_check = _check_int(initial_level)
    if not isinstance(int_check, int):
        return _get_initial_level()

    return int_check


def _get_target_level(initial_level: int) -> int:
    if initial_level == 11:
        return 11

    target_level = console.input(
        f"Qual o nível alvo do brawler? ({initial_level}-11) "
    ).strip()

    int_check = _check_int(target_level)
    if not isinstance(int_check, int):
        return _get_target_level(initial_level)

    return int_check


def _get_gadget_amount() -> int:
    gadget_amount = console.input(
        "Quantos [bright_green]acessórios[/bright_green]? (0-2) "
    ).strip()

    int_check = _check_int(gadget_amount)
    if not isinstance(int_check, int):
        return _get_gadget_amount()

    if 0 < int_check > 2:
        console.print("Escolha entre 0 e 2.")
        console.rule(style=ERROR_STYLE)
        return _get_gadget_amount()

    return int_check


def _get_normal_gear_amount() -> int:
    normal_gear_amount = console.input(
        "Quantas [gray]engrenagens[/gray]? (0-6) "
    ).strip()

    int_check = _check_int(normal_gear_amount)
    if not isinstance(int_check, int):
        return _get_normal_gear_amount()

    if 0 < int_check > 6:
        console.print("Escolha entre 0 e 6.")
        console.rule(style=ERROR_STYLE)
        return _get_normal_gear_amount()

    return int_check


def _get_epic_gear_amount() -> int:
    epic_gear_amount = console.input(
        "Quantas [gray]engrenagens[/gray] [purple]épicas[/purple]? (0-1) "
    ).strip()

    int_check = _check_int(epic_gear_amount)
    if not isinstance(int_check, int):
        return _get_epic_gear_amount()

    if 0 < int_check > 1:
        console.print("Escolha entre 0 e 1.")
        console.rule(style=ERROR_STYLE)
        return _get_epic_gear_amount()

    return int_check


def _get_mythic_gear_amount() -> int:
    mythic_gear_amount = console.input(
        "Quantas [gray]engrenagens[/gray] [red]míticas[/red]? (0-1) "
    ).strip()

    int_check = _check_int(mythic_gear_amount)
    if not isinstance(int_check, int):
        return _get_mythic_gear_amount()

    if 0 < int_check > 1:
        console.print("Escolha entre 0 e 2.")
        console.rule(style=ERROR_STYLE)
        return _get_mythic_gear_amount()

    return int_check


def _get_starpower_amount() -> int:
    starpower_amount = console.input(
        "Quantos [bright_yellow]poderes de estrela[/bright_yellow]? (0-2) "
    ).strip()

    int_check = _check_int(starpower_amount)
    if not isinstance(int_check, int):
        return _get_starpower_amount()

    if 0 < int_check > 2:
        console.print("Escolha entre 0 e 2.")
        console.rule(style=ERROR_STYLE)
        return _get_starpower_amount()

    return int_check


def _get_hypercharge() -> bool:
    hypercharge = console.input("[purple]Hipercarga[/purple]? (s/N) ").strip().lower()

    if not hypercharge:
        hypercharge = "n"
    if hypercharge not in ("s", "n"):
        console.print("Escolha entre 's' e 'n'.")
        console.rule(style=ERROR_STYLE)
        return _get_hypercharge()

    bool_opt = {"s": True, "n": False}

    return bool_opt[hypercharge]


def start_flow(new_brawler: _types.BrawlerLevelUp) -> _types.BrawlerLevelUp:
    """
    Asks the user how much they want their brawler upgraded.
    """
    console.rule("Nível do Brawler")

    new_brawler.initial_level = _get_initial_level()
    new_brawler.target_level = _get_target_level(new_brawler.initial_level)

    if new_brawler.target_level < 7:
        return new_brawler

    console.rule("Acessórios")

    new_brawler.gadget_amount = _get_gadget_amount()

    if new_brawler.target_level >= 8:
        new_brawler.normal_gear_amount = _get_normal_gear_amount()
        new_brawler.epic_gear_amount = _get_epic_gear_amount()
        new_brawler.mythic_gear_amount = _get_mythic_gear_amount()

    if new_brawler.target_level >= 9:
        new_brawler.starpower_amount = _get_starpower_amount()

    if new_brawler.target_level == 11:
        new_brawler.hypercharge = _get_hypercharge()

    return new_brawler


def main():
    resources = _load_resources()

    new_brawler = _types.BrawlerLevelUp(resources=resources)
    new_brawler = start_flow(new_brawler)

    console.print()
    with console.status("Calculando Recursos para Subir de Nível..."):
        time.sleep(2)

    console.print(Markdown("# Recursos para Subir de Nível"))
    console.print(
        Markdown(
            f"\nNível **{new_brawler.initial_level}** ao **{new_brawler.target_level}**:\n"
        )
    )

    level_resources = new_brawler.level_resources

    console.print()
    console.print(f"[bright_yellow]Ouro[/bright_yellow]: {level_resources.gold}")
    console.print(f"[purple]Pontos de Poder[/purple]: {level_resources.power_points}")

    gear_resources = new_brawler.gear_resources

    if gear_resources == 0:
        sys.exit(0)

    console.print()
    with console.status("Calculando Recursos para Acessórios..."):
        time.sleep(2)

    console.print(Markdown("# Recursos para Acessórios"))

    console.print(
        f"Quantidade de [bright_green]Acessórios[/bright_green]: {new_brawler.gadget_amount}"
    )
    console.print(
        f"Quantidade de [gray]Engrenagens Normais[/gray]: {new_brawler.normal_gear_amount}"
    )
    console.print(
        f"Quantidade de [gray]Engrenagens[/gray] [purple]Épicas[/purple]: {new_brawler.epic_gear_amount}"
    )
    console.print(
        f"Quantidade de [gray]Engrenagens[/gray] [red]Míticas[/red]: {new_brawler.mythic_gear_amount}"
    )
    console.print(
        f"Quantidade de [bright_yellow]Poderes de Estrela[/bright_yellow]: {new_brawler.starpower_amount}"
    )

    bool_opt = {
        "True": "Sim",
        "False": "Não",
    }

    console.print(
        f"[purple]Hipercarga[/purple]: {bool_opt[str(new_brawler.hypercharge)]}"
    )

    console.print(f"\n[bright_yellow]Ouro[/bright_yellow]: {gear_resources}\n")

    console.print(Markdown("# Total"))

    console.print(
        f"\n[bright_yellow]Ouro[/bright_yellow]: {level_resources.gold + gear_resources}"
    )
    console.print(f"[purple]Pontos de Poder[/purple]: {level_resources.power_points}\n")


if __name__ == "__main__":
    main()
