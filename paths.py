from pathlib import Path

# Get the base path of the working directory
PATH = Path(__file__).parent
if not (PATH / "data/").resolve().exists():
    # The executable is running, not the source files.
    PATH = PATH.parent.parent

# Path to fonts
fonts_path = (PATH / "data/fonts").resolve()

# Path to the perfumes database
perfumes_path = (PATH / "data/filteredDatabase.csv").resolve()

# Path to question and answers pairs database
questionanswer_path = (PATH / "data/question_answer_pairs.csv").resolve()

# Path to olfactory families database
families_path = (PATH / "data/olfactory_families.csv").resolve()

# Path to ingredients database
ingredients_path = (PATH / "data/ingredients.csv").resolve()

# Path to logo
logo_path = (PATH / "data/Logo-PL-liggend.png").resolve()
