from typing import List

import inquirer

from cli.classifiers_handler import handle_classifier_result
from cli.cli_constants import MenuOptions
from cli.data_generation_handler import handle_data_generation
from cli.database_preview_handlers import handle_database_preview
from cli.graphics_handler import handle_graphics


def get_menu_options() -> List[str]:
    return [
        MenuOptions.DATA_GENERATION,
        MenuOptions.GRAPHICS,
        MenuOptions.DATABASE_PREVIEW,
        MenuOptions.CLASSIFIERS,
        MenuOptions.EXIT
    ]


def handle_option(option: str) -> None:
    match option:
        case MenuOptions.DATA_GENERATION:
            handle_data_generation()
        case MenuOptions.GRAPHICS:
            handle_graphics()
        case MenuOptions.DATABASE_PREVIEW:
            handle_database_preview()
        case MenuOptions.CLASSIFIERS:
            handle_classifier_result()
        case _:
            pass


def main():
    while True:
        option = inquirer.list_input("Option", choices=get_menu_options())
        handle_option(option)
        if option == MenuOptions.EXIT:
            break
    print("Ending program")


if __name__ == "__main__":
    main()
