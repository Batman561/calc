import os

import math


RESET = "\033[0m"
BOLD = "\033[1m"
GRAY = "\033[38;5;245m"
PINK = "\033[38;5;205m"
GREEN = "\033[38;5;84m"
RED = "\033[38;5;203m"
YELLOW = "\033[38;5;221m"
CYAN = "\033[38;5;87m"

BUTTON_STYLE = "\033[48;5;99m\033[38;5;231m\033[1m"
ERROR_STYLE = "\033[48;5;203m\033[38;5;231m\033[1m"

LOGO = [
    " ██████╗ █████╗ ██╗      ██████╗",
    "██╔════╝██╔══██╗██║     ██╔════╝",
    "██║     ███████║██║     ██║     ",
    "██║     ██╔══██║██║     ██║     ",
    "╚██████╗██║  ██║███████╗╚██████╗",
    " ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝",
]

LOGO_COLORS = [
    "\033[38;5;48m",
    "\033[38;5;49m",
    "\033[38;5;50m",
    "\033[38;5;51m",
    "\033[38;5;45m",
    "\033[38;5;39m",
]

BOX_WIDTH = 72

OPERATOR_GROUPS = [
    ("Basic", [
        ("+", "add", "2 + 3"),
        ("-", "subtract", "10 - 4"),
        ("*", "multiply", "6 * 7"),
        ("/", "divide", "10 / 4"),
    ]),
    ("Advanced", [
        ("^", "power", "2 ^ 10"),
        ("%", "percent", "200 * 15%"),
        ("mod", "remainder", "17 mod 5"),
        ("!", "factorial", "5!"),
    ]),
    ("Trigonometry", [
        ("sin", "sine", "sin(30)"),
        ("asin", "arc sine", "asin(0.5)"),
        ("cos", "cosine", "cos(60)"),
        ("acos", "arc cosine", "acos(0.5)"),
        ("tan", "tangent", "tan(45)"),
        ("atan", "arc tangent", "atan(1)"),
    ]),
    ("Functions", [
        ("sqrt", "square root", "sqrt(16)"),
        ("cbrt", "cube root", "cbrt(27)"),
        ("log", "log base 10", "log(1000)"),
        ("ln", "natural log", "ln(e)"),
        ("exp", "e to the x", "exp(1)"),
        ("abs", "absolute", "abs(-7)"),
    ]),
    ("Constants", [
        ("pi", "3.14159...", "2pi"),
        ("e", "2.71828...", "e ^ 2"),
        ("ans", "last answer", "ans * 2"),
    ]),
    ("Grouping", [
        ("( )", "parentheses", "(2 + 3) * 4"),
    ]),
]


FUNCTION_NAMES = [
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sqrt", "cbrt", "log", "ln", "exp", "abs",
]

CONSTANTS = {
    "pi": math.pi,
    "π": math.pi,
    "e": math.e,
}

KNOWN_WORDS = FUNCTION_NAMES + list(CONSTANTS) + ["mod", "ans"]

angle_mode = "DEG"

last_answer = 0.0


def toggle_angle_mode():
    global angle_mode
    if angle_mode == "DEG":
        angle_mode = "RAD"
    else:
        angle_mode = "DEG"
    print(f"    {GRAY}╰─{RESET} {GREEN}Angle mode: {angle_mode}{RESET}")
    print()


def to_radians(angle):
    if angle_mode == "DEG":
        return math.radians(angle)
    return angle


def from_radians(angle):
    if angle_mode == "DEG":
        return math.degrees(angle)
    return angle


def factorial(number):
    if not number.is_integer() or number < 0:
        raise ValueError("Factorial needs a whole number >= 0")
    if number > 170:
        raise OverflowError
    return float(math.factorial(int(number)))


def apply_function(name, x):
    try:
        if name == "sin":
            return round(math.sin(to_radians(x)), 12)
        if name == "cos":
            return round(math.cos(to_radians(x)), 12)
        if name == "tan":
            if round(math.cos(to_radians(x)), 12) == 0:
                raise ValueError
            return round(math.tan(to_radians(x)), 12)
        if name == "asin":
            return from_radians(math.asin(x))
        if name == "acos":
            return from_radians(math.acos(x))
        if name == "atan":
            return from_radians(math.atan(x))
        if name == "sqrt":
            return math.sqrt(x)
        if name == "cbrt":
            return math.copysign(abs(x) ** (1 / 3), x)
        if name == "log":
            return math.log10(x)
        if name == "ln":
            return math.log(x)
        if name == "exp":
            return math.exp(x)
        if name == "abs":
            return abs(x)
    except ValueError:
        raise ValueError(f"{name}() can't take {format_number(x)}")


def tokenize(text):
    text = text.lower()
    tokens = []
    i = 0

    while i < len(text):
        char = text[i]

        if char == " ":
            i += 1

        elif char.isdigit() or char == ".":
            number = ""
            while i < len(text) and (text[i].isdigit() or text[i] == "."):
                number += text[i]
                i += 1
            if number == "." or number.count(".") > 1:
                raise ValueError(f"'{number}' is not a valid number")
            tokens.append(number)

        elif char.isalpha():
            word = ""
            while i < len(text) and text[i].isalpha():
                word += text[i]
                i += 1
            if word not in KNOWN_WORDS:
                raise ValueError(f"Unknown name '{word}'")
            tokens.append(word)

        elif text[i:i + 2] == "**":
            tokens.append("^")
            i += 2

        elif char in "+-*/^%!()":
            tokens.append(char)
            i += 1

        else:
            raise ValueError(f"Unknown character '{char}'")

    return tokens


def peek(tokens):
    if len(tokens) > 0:
        return tokens[0]
    return None


def starts_a_value(token):
    return token == "(" or token in FUNCTION_NAMES or token in CONSTANTS or token == "ans"


def parse_expression(tokens):
    value = parse_term(tokens)
    while peek(tokens) in ("+", "-"):
        operator = tokens.pop(0)
        right = parse_term(tokens)
        if operator == "+":
            value = value + right
        else:
            value = value - right
    return value


def parse_term(tokens):
    value = parse_unary(tokens)
    while peek(tokens) in ("*", "/", "mod") or starts_a_value(peek(tokens)):
        if starts_a_value(peek(tokens)):
            operator = "*"
        else:
            operator = tokens.pop(0)
        right = parse_unary(tokens)
        if operator == "*":
            value = value * right
        elif operator == "/":
            value = value / right
        else:
            value = value % right
    return value


def parse_unary(tokens):
    if peek(tokens) == "-":
        tokens.pop(0)
        return -parse_unary(tokens)
    if peek(tokens) == "+":
        tokens.pop(0)
        return parse_unary(tokens)
    return parse_power(tokens)


def parse_power(tokens):
    base = parse_postfix(tokens)
    if peek(tokens) == "^":
        tokens.pop(0)
        exponent = parse_unary(tokens)
        result = base ** exponent
        if isinstance(result, complex):
            raise ValueError("This power has no real answer")
        return result
    return base


def parse_postfix(tokens):
    value = parse_primary(tokens)
    while peek(tokens) in ("%", "!"):
        operator = tokens.pop(0)
        if operator == "%":
            value = value / 100
        else:
            value = factorial(value)
    return value


def read_parentheses(tokens):
    value = parse_expression(tokens)
    if peek(tokens) != ")":
        raise ValueError("A ')' is missing")
    tokens.pop(0)
    return value


def parse_primary(tokens):
    if len(tokens) == 0:
        raise ValueError("The expression is incomplete")

    token = tokens.pop(0)

    if token == "(":
        return read_parentheses(tokens)

    if token in FUNCTION_NAMES:
        if peek(tokens) != "(":
            raise ValueError(f"Use parentheses, like {token}(...)")
        tokens.pop(0)
        return apply_function(token, read_parentheses(tokens))

    if token in CONSTANTS:
        return CONSTANTS[token]

    if token == "ans":
        return last_answer

    if token[0].isdigit() or token[0] == ".":
        return float(token)

    raise ValueError(f"Unexpected '{token}'")


def calculate(text):
    tokens = tokenize(text)
    result = parse_expression(tokens)
    if len(tokens) > 0:
        raise ValueError(f"Unexpected '{tokens[0]}'")
    if not math.isfinite(result):
        raise OverflowError
    return result


def format_number(number):
    if number.is_integer() and abs(number) < 1e15:
        return f"{int(number):,}"
    return f"{number:,.10g}"


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def box_line(text, color):
    middle = text.center(BOX_WIDTH)
    print(f"  {GRAY}│{RESET}{color}{middle}{RESET}{GRAY}│{RESET}")


def button(key, label):
    return f"{BUTTON_STYLE} {key} {RESET} {GRAY}{label}{RESET}"


def box_divider(left, title, right):
    label = f" {title} "
    line = "─" * (BOX_WIDTH - 1 - len(label))
    print(f"  {GRAY}{left}─{RESET}{YELLOW}{BOLD}{label}{RESET}{GRAY}{line}{right}{RESET}")


def operator_row(symbol, meaning, example):
    answer = "= " + format_number(calculate(example))
    symbol_part = f"{CYAN}{BOLD}{symbol.ljust(8)}{RESET}"
    meaning_part = f"{GRAY}{meaning.ljust(16)}{RESET}"
    example_part = example.ljust(16)
    answer_part = f"{GREEN}{answer.ljust(BOX_WIDTH - 43)}{RESET}"
    print(f"  {GRAY}│{RESET}   {symbol_part}{meaning_part}{example_part}{answer_part}{GRAY}│{RESET}")


def print_operators():
    left, right = "╭", "╮"
    for title, operators in OPERATOR_GROUPS:
        if title == "Trigonometry":
            title = f"{title} ({angle_mode})"
        box_divider(left, title, right)
        left, right = "├", "┤"
        for symbol, meaning, example in operators:
            operator_row(symbol, meaning, example)
    border = "─" * BOX_WIDTH
    print(f"  {GRAY}╰{border}╯{RESET}")


def guide_cell(symbol, example):
    answer = "= " + format_number(calculate(example))
    symbol_part = f"{CYAN}{BOLD}{symbol.ljust(6)}{RESET}"
    example_part = example.ljust(13)
    answer_part = f"{GREEN}{answer.ljust(BOX_WIDTH // 2 - 21)}{RESET}"
    return "  " + symbol_part + example_part + answer_part


def print_quick_guide():
    left, right = "╭", "╮"
    for title, operators in OPERATOR_GROUPS:
        if title == "Trigonometry":
            title = f"{title} ({angle_mode})"
        box_divider(left, title, right)
        left, right = "├", "┤"
        for i in range(0, len(operators), 2):
            pair = operators[i:i + 2]
            row = ""
            for symbol, meaning, example in pair:
                row += guide_cell(symbol, example)
            empty = " " * (BOX_WIDTH - BOX_WIDTH // 2 * len(pair))
            print(f"  {GRAY}│{RESET}{row}{empty}{GRAY}│{RESET}")
    border = "─" * BOX_WIDTH
    print(f"  {GRAY}╰{border}╯{RESET}")


def print_banner():
    border = "─" * BOX_WIDTH

    print()
    print(f"  {GRAY}╭{border}╮{RESET}")
    box_line("", RESET)
    for line, color in zip(LOGO, LOGO_COLORS):
        box_line(line, BOLD + color)
    box_line("", RESET)
    box_line("~ scientific python calculator ~", GRAY)
    print(f"  {GRAY}╰{border}╯{RESET}")
    print()

    print_quick_guide()
    print()

    buttons = [
        button("H", "History"),
        button("D", "Delete history"),
        button("M", "Menu"),
        button("A", "Angle"),
        button("C", "Clear"),
        button("Q", "Quit"),
    ]
    print("   " + "  ".join(buttons))
    print()


def show_result(answer):
    print(f"    {GRAY}╰─{RESET} {GREEN}{BOLD}= {answer}{RESET}")
    print()


def show_error(message):
    print(f"    {GRAY}╰─{RESET} {ERROR_STYLE} ERROR {RESET} {RED}{message}{RESET}")
    print()


def show_history(history):
    print()
    print(f"   {PINK}╭─ {BOLD}History{RESET}")

    if len(history) == 0:
        print(f"   {PINK}│{RESET}  {GRAY}Nothing yet. Try typing sin(30){RESET}")

    longest = 0
    for expression, answer in history:
        if len(expression) > longest:
            longest = len(expression)

    number = 1
    for expression, answer in history:
        print(f"   {PINK}│{RESET}  {GRAY}{number:>2}.{RESET}  {expression.ljust(longest)}   {GREEN}= {answer}{RESET}")
        number += 1

    print(f"   {PINK}╰─{RESET} {GRAY}{len(history)} calculation(s) · saved in {HISTORY_FILE_NAME}{RESET}")
    print()


HISTORY_FILE_NAME = "scientific_history.txt"
FOLDER = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(FOLDER, HISTORY_FILE_NAME)


def load_history():
    history = []
    if not os.path.exists(HISTORY_FILE):
        return history
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(" = ")
            if len(parts) == 2:
                history.append((parts[0], parts[1]))
    return history


def save_to_history_file(expression, answer):
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(f"{expression} = {answer}\n")
    except OSError:
        show_error(f"Could not save to {HISTORY_FILE_NAME}")


def delete_history(history):
    if len(history) == 0:
        print(f"    {GRAY}╰─ History is already empty{RESET}")
        print()
        return

    try:
        reply = input(f"    {YELLOW}?{RESET} Delete all {len(history)} calculation(s)? {GRAY}(y/n){RESET} ")
    except (KeyboardInterrupt, EOFError):
        reply = "n"
    if reply.strip().lower() not in ("y", "yes"):
        print(f"    {GRAY}╰─ Cancelled, nothing was deleted{RESET}")
        print()
        return

    history.clear()
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            pass
    except OSError:
        show_error(f"Could not clear {HISTORY_FILE_NAME}")
        return
    print(f"    {GRAY}╰─{RESET} {GREEN}History deleted{RESET}")
    print()


def main():
    global last_answer

    history = load_history()

    clear_screen()
    print_banner()

    while True:
        try:
            text = input(f"  {GRAY}{angle_mode}{RESET} {PINK}{BOLD}»{RESET} ")
        except (KeyboardInterrupt, EOFError):
            break

        command = text.strip().lower()

        if command == "":
            continue
        elif command in ("q", "quit", "exit"):
            break
        elif command in ("h", "history"):
            show_history(history)
        elif command in ("d", "delete"):
            delete_history(history)
        elif command in ("m", "menu"):
            print()
            print_operators()
            print()
        elif command in ("a", "angle"):
            toggle_angle_mode()
        elif command in ("c", "clear"):
            clear_screen()
            print_banner()
        else:
            try:
                result = calculate(command)
                answer = format_number(result)
                last_answer = result
                history.append((command, answer))
                show_result(answer)
                save_to_history_file(command, answer)
            except ZeroDivisionError:
                show_error("You can't divide by zero")
            except OverflowError:
                show_error("The number is too big")
            except ValueError as error:
                show_error(str(error))

    print(f"\n  {PINK}Goodbye!{RESET}\n")


if __name__ == "__main__":
    main()
