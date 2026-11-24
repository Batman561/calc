# ════════════════════════════════════════════════════════════
#   ماشین حساب مهندسی با پایتون (نسخه‌ی دوم)
#   همان ماشین حسابِ ساده، به‌علاوه‌ی توابع و ثابت‌های مهندسی
#   برای اجرا، در ترمینال این دستور را بزنید:
#       python scientific_calculator.py
# ════════════════════════════════════════════════════════════

# ماژول os را می‌آوریم تا صفحه‌ی ترمینال را پاک کنیم و با فایل‌ها کار کنیم
import os

# ماژول math جعبه‌ابزارِ ریاضیِ پایتون است: سینوس، لگاریتم، جذر، عدد پی و...
import math


# ════════════════════════════════════════════════════════════
#   بخش ۱: رنگ‌ها و ظاهر برنامه
# ════════════════════════════════════════════════════════════

# این رشته‌های عجیب «کد رنگ» هستند. ترمینال آن‌ها را چاپ نمی‌کند؛
# بلکه با دیدنشان، رنگ یا حالتِ متنِ بعدی را عوض می‌کند.
RESET = "\033[0m"
BOLD = "\033[1m"
GRAY = "\033[38;5;245m"
PINK = "\033[38;5;205m"
GREEN = "\033[38;5;84m"
RED = "\033[38;5;203m"
YELLOW = "\033[38;5;221m"
CYAN = "\033[38;5;87m"

# کدهای پس‌زمینه (رنگِ زیرِ متن) برای ساختن دکمه‌ها و برچسب خطا
BUTTON_STYLE = "\033[48;5;99m\033[38;5;231m\033[1m"
ERROR_STYLE = "\033[48;5;203m\033[38;5;231m\033[1m"

# لوگوی بزرگ برنامه که با کاراکترهای مخصوص کشیده شده است
LOGO = [
    " ██████╗ █████╗ ██╗      ██████╗",
    "██╔════╝██╔══██╗██║     ██╔════╝",
    "██║     ███████║██║     ██║     ",
    "██║     ██╔══██║██║     ██║     ",
    "╚██████╗██║  ██║███████╗╚██████╗",
    " ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝",
]

# برای هر خطِ لوگو یک رنگ: از سبز تا آبی (حالت گرادیان)
LOGO_COLORS = [
    "\033[38;5;48m",
    "\033[38;5;49m",
    "\033[38;5;50m",
    "\033[38;5;51m",
    "\033[38;5;45m",
    "\033[38;5;39m",
]

# پهنای داخلِ کادرها (کادرِ لوگو، کادرِ راهنما و کادرِ منو)
BOX_WIDTH = 72

# منوی کامل، دسته‌بندی‌شده.
# هر دسته یک اسم دارد و چند ردیف. هر ردیف هم سه چیز دارد:
# علامت یا اسمِ تابع، معنی‌اش، و یک مثال
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


# ════════════════════════════════════════════════════════════
#   بخش ۲: توابع و ثابت‌های مهندسی
# ════════════════════════════════════════════════════════════

# اسمِ همه‌ی توابعی که ماشین حساب می‌شناسد
FUNCTION_NAMES = [
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sqrt", "cbrt", "log", "ln", "exp", "abs",
]

# ثابت‌ها در یک «دیکشنری» هستند: هر اسم به یک عدد وصل شده است
CONSTANTS = {
    "pi": math.pi,
    "π": math.pi,
    "e": math.e,
}

# همه‌ی کلمه‌هایی که کاربر اجازه دارد تایپ کند
KNOWN_WORDS = FUNCTION_NAMES + list(CONSTANTS) + ["mod", "ans"]

# حالتِ زاویه برای توابعِ مثلثاتی: درجه یا رادیان
#   "DEG" = degree      "RAD" = radian
angle_mode = "DEG"

# آخرین جوابِ درست، تا بشود با کلمه‌ی ans از آن استفاده کرد
last_answer = 0.0


def toggle_angle_mode():
    # چون می‌خواهیم متغیرِ بیرونیِ angle_mode را عوض کنیم، کلمه‌ی global لازم است
    global angle_mode
    if angle_mode == "DEG":
        angle_mode = "RAD"
    else:
        angle_mode = "DEG"
    print(f"    {GRAY}╰─{RESET} {GREEN}Angle mode: {angle_mode}{RESET}")
    print()


def to_radians(angle):
    # توابعِ ماژولِ math زاویه را به رادیان می‌خواهند؛
    # پس اگر در حالتِ درجه هستیم، اول تبدیلش کن
    if angle_mode == "DEG":
        return math.radians(angle)
    return angle


def from_radians(angle):
    # جوابِ توابعِ معکوس (مثل asin) به رادیان است؛
    # در حالتِ درجه، آن را به درجه برگردان
    if angle_mode == "DEG":
        return math.degrees(angle)
    return angle


def factorial(number):
    # فاکتوریل فقط برای اعدادِ صحیحِ صفر و مثبت تعریف شده است
    if not number.is_integer() or number < 0:
        raise ValueError("Factorial needs a whole number >= 0")
    # فاکتوریلِ بیشتر از ۱۷۰ از بزرگ‌ترین عددی که کامپیوتر نگه می‌دارد بزرگ‌تر است
    if number > 170:
        raise OverflowError
    return float(math.factorial(int(number)))


def apply_function(name, x):
    # تابعی را که اسمش داده شده، روی عددِ x اجرا کن و جواب را برگردان
    try:
        if name == "sin":
            # کمی گرد می‌کنیم تا جوابِ چیزی مثلِ این، دقیقاً صفر شود:
            #   sin(180)
            return round(math.sin(to_radians(x)), 12)
        if name == "cos":
            return round(math.cos(to_radians(x)), 12)
        if name == "tan":
            # تانژانت جایی که کسینوس صفر است (مثلاً ۹۰ درجه) تعریف نشده
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
            # ریشه‌ی سومِ قدرِ مطلق را بگیر، بعد علامتِ x را رویش بگذار
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
        # مثلاً جذرِ عددِ منفی، لگاریتمِ صفر، یا تانژانتِ ۹۰ درجه
        raise ValueError(f"{name}() can't take {format_number(x)}")


# ════════════════════════════════════════════════════════════
#   بخش ۳: تکه‌تکه کردن عبارت (Tokenize)
#   "2sin(30)+pi"  -->  ["2", "sin", "(", "30", ")", "+", "pi"]
# ════════════════════════════════════════════════════════════

def tokenize(text):
    # همه‌ی حروف را کوچک می‌کنیم تا SIN و sin یکی حساب شوند
    text = text.lower()
    # یک لیست خالی برای نگه‌داشتنِ تکه‌ها (توکن‌ها)
    tokens = []
    # متغیر i شماره‌ی کاراکتری است که الان داریم نگاهش می‌کنیم
    i = 0

    # تا وقتی به آخرِ متن نرسیده‌ایم، ادامه بده
    while i < len(text):
        char = text[i]

        # فاصله مهم نیست؛ از رویش رد شو
        if char == " ":
            i += 1

        # اگر رقم یا نقطه بود، کلِ عدد را با هم بخوان (مثل 3.14)
        elif char.isdigit() or char == ".":
            number = ""
            while i < len(text) and (text[i].isdigit() or text[i] == "."):
                number += text[i]
                i += 1
            # یک نقطه‌ی تنها یا عددی با دو نقطه، عددِ درستی نیست
            if number == "." or number.count(".") > 1:
                raise ValueError(f"'{number}' is not a valid number")
            tokens.append(number)

        # اگر حرف بود، کلِ کلمه را با هم بخوان (مثل sin یا pi یا mod)
        elif char.isalpha():
            word = ""
            while i < len(text) and text[i].isalpha():
                word += text[i]
                i += 1
            # فقط کلمه‌هایی را قبول کن که می‌شناسیم
            if word not in KNOWN_WORDS:
                raise ValueError(f"Unknown name '{word}'")
            tokens.append(word)

        # اگر دو ستاره پشت‌سرهم آمد، آن هم مثل ^ یعنی توان
        elif text[i:i + 2] == "**":
            tokens.append("^")
            i += 2

        # علامت‌های تک‌حرفی
        elif char in "+-*/^%!()":
            tokens.append(char)
            i += 1

        # هر چیز دیگری را نمی‌شناسیم
        else:
            raise ValueError(f"Unknown character '{char}'")

    return tokens


# ════════════════════════════════════════════════════════════
#   بخش ۴: فهمیدن و حساب کردنِ عبارت (Parse)
#   هر تابع یک «طبقه» از اولویتِ عملگرهاست:
#       parse_expression  ->  +  -
#       parse_term        ->  *  /  mod   (and 2pi)
#       parse_unary       ->  -5
#       parse_power       ->  ^
#       parse_postfix     ->  %  !
#       parse_primary     ->  numbers, ( ), functions, constants, ans
# ════════════════════════════════════════════════════════════

def peek(tokens):
    # اولین توکن را «نگاه» می‌کند، بدون اینکه از لیست برش دارد
    if len(tokens) > 0:
        return tokens[0]
    return None


def starts_a_value(token):
    # آیا این توکن می‌تواند شروعِ یک مقدارِ تازه باشد؟
    # یعنی پرانتزِ باز، اسمِ یک تابع، اسمِ یک ثابت، یا ans
    return token == "(" or token in FUNCTION_NAMES or token in CONSTANTS or token == "ans"


def parse_expression(tokens):
    # اول یک تکه‌ی ضرب‌وتقسیمی را حساب کن
    value = parse_term(tokens)
    # تا وقتی بعدش + یا - می‌آید، تکه‌ی بعدی را هم حساب کن
    while peek(tokens) in ("+", "-"):
        operator = tokens.pop(0)
        right = parse_term(tokens)
        if operator == "+":
            value = value + right
        else:
            value = value - right
    return value


def parse_term(tokens):
    # اول یک عدد (شاید منفی) را حساب کن
    value = parse_unary(tokens)
    # تا وقتی بعدش * یا / یا mod می‌آید، یا مستقیم یک مقدارِ تازه شروع می‌شود، ادامه بده
    while peek(tokens) in ("*", "/", "mod") or starts_a_value(peek(tokens)):
        # ضربِ پنهان: وقتی بینِ دو مقدار علامتی نیست، یعنی ضرب؛ مثل این دو:
        #   2pi    2(3+4)
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
    # علامتِ منفی قبل از عدد؛ مثل این دو:
    #   -5    -(2+3)
    if peek(tokens) == "-":
        tokens.pop(0)
        return -parse_unary(tokens)
    # علامت مثبت قبل از عدد اثری ندارد
    if peek(tokens) == "+":
        tokens.pop(0)
        return parse_unary(tokens)
    return parse_power(tokens)


def parse_power(tokens):
    base = parse_postfix(tokens)
    if peek(tokens) == "^":
        tokens.pop(0)
        # توان از راست حساب می‌شود:
        #   2^3^2  =  2^(3^2)  =  2^9
        exponent = parse_unary(tokens)
        result = base ** exponent
        # مثلاً جذرِ عددِ منفی، جوابِ حقیقی ندارد
        if isinstance(result, complex):
            raise ValueError("This power has no real answer")
        return result
    return base


def parse_postfix(tokens):
    value = parse_primary(tokens)
    # علامت‌هایی که «بعد از» عدد می‌آیند:
    #   50%  =  0.5        5!  =  5*4*3*2*1  =  120
    while peek(tokens) in ("%", "!"):
        operator = tokens.pop(0)
        if operator == "%":
            value = value / 100
        else:
            value = factorial(value)
    return value


def read_parentheses(tokens):
    # پرانتزِ باز قبلاً برداشته شده؛ داخلش را حساب کن و پرانتزِ بسته را هم بردار
    value = parse_expression(tokens)
    if peek(tokens) != ")":
        raise ValueError("A ')' is missing")
    tokens.pop(0)
    return value


def parse_primary(tokens):
    # اگر توکنی نمانده، عبارت ناقص است؛ مثلاً بعد از علامتِ + چیزی نیامده
    if len(tokens) == 0:
        raise ValueError("The expression is incomplete")

    token = tokens.pop(0)

    # پرانتز: داخلش را مثل یک عبارتِ کامل، از اول حساب کن
    if token == "(":
        return read_parentheses(tokens)

    # اسمِ تابع: بعدش حتماً باید پرانتز بیاید، مثل sin(30)
    if token in FUNCTION_NAMES:
        if peek(tokens) != "(":
            raise ValueError(f"Use parentheses, like {token}(...)")
        tokens.pop(0)
        return apply_function(token, read_parentheses(tokens))

    # اسمِ ثابت: عددش را از دیکشنری بردار
    if token in CONSTANTS:
        return CONSTANTS[token]

    # کلمه‌ی ans یعنی آخرین جواب
    if token == "ans":
        return last_answer

    # اگر توکن با رقم یا نقطه شروع شده، یک عدد است
    if token[0].isdigit() or token[0] == ".":
        return float(token)

    # هر چیز دیگری اینجا بی‌جاست (مثلاً یک * در اولِ عبارت)
    raise ValueError(f"Unexpected '{token}'")


def calculate(text):
    # قدم اول: متن را تکه‌تکه کن
    tokens = tokenize(text)
    # قدم دوم: از پایین‌ترین طبقه شروع کن و جواب را حساب کن
    result = parse_expression(tokens)
    # اگر چیزی اضافه ماند (مثلاً دو عدد بدون علامت)، عبارت غلط است
    if len(tokens) > 0:
        raise ValueError(f"Unexpected '{tokens[0]}'")
    # اگر جواب بی‌نهایت شد، یعنی عدد بیش از حد بزرگ است
    if not math.isfinite(result):
        raise OverflowError
    return result


def format_number(number):
    # عددِ بدون اعشار (مثل 20.0) را تمیز و با جداکننده‌ی هزارگان نشان بده
    if number.is_integer() and abs(number) < 1e15:
        return f"{int(number):,}"
    # بقیه را با حداکثر ۱۰ رقمِ معنی‌دار نشان بده تا جوابِ این عبارت 0.3 دیده شود:
    #   0.1 + 0.2
    return f"{number:,.10g}"


# ════════════════════════════════════════════════════════════
#   بخش ۵: نمایشِ زیبا در ترمینال
# ════════════════════════════════════════════════════════════

def clear_screen():
    # ویندوز با دستور cls و لینوکس و مک با دستور clear صفحه را پاک می‌کنند
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def box_line(text, color):
    # متن را وسطِ خط می‌گذارد و دو طرفش دیواره‌ی کادر می‌کشد
    middle = text.center(BOX_WIDTH)
    print(f"  {GRAY}│{RESET}{color}{middle}{RESET}{GRAY}│{RESET}")


def button(key, label):
    # یک «دکمه» می‌سازد: حرفِ کلید روی پس‌زمینه‌ی رنگی، و اسمش کنارش
    return f"{BUTTON_STYLE} {key} {RESET} {GRAY}{label}{RESET}"


def box_divider(left, title, right):
    # یک خطِ افقیِ کادر که اسمِ یک دسته رویش نوشته شده
    label = f" {title} "
    line = "─" * (BOX_WIDTH - 1 - len(label))
    print(f"  {GRAY}{left}─{RESET}{YELLOW}{BOLD}{label}{RESET}{GRAY}{line}{right}{RESET}")


def operator_row(symbol, meaning, example):
    # جوابِ مثال را با خودِ ماشین حساب حساب می‌کنیم تا همیشه درست باشد
    answer = "= " + format_number(calculate(example))
    # هر ستون را با ljust به پهنای ثابتی می‌رسانیم تا ستون‌ها زیرِ هم بیفتند
    symbol_part = f"{CYAN}{BOLD}{symbol.ljust(8)}{RESET}"
    meaning_part = f"{GRAY}{meaning.ljust(16)}{RESET}"
    example_part = example.ljust(16)
    # ستونِ آخر، باقی‌مانده‌ی پهنای کادر را پر می‌کند
    # 43 = 3 + 8 + 16 + 16
    answer_part = f"{GREEN}{answer.ljust(BOX_WIDTH - 43)}{RESET}"
    print(f"  {GRAY}│{RESET}   {symbol_part}{meaning_part}{example_part}{answer_part}{GRAY}│{RESET}")


def print_operators():
    # خطِ اول گوشه‌های گرد دارد؛ خط‌های بعدی به دیواره‌های کادر وصل می‌شوند
    left, right = "╭", "╮"
    for title, operators in OPERATOR_GROUPS:
        # کنارِ اسمِ دسته‌ی مثلثات، حالتِ زاویه را هم بنویس؛ چون جواب‌هایش به آن بستگی دارد
        if title == "Trigonometry":
            title = f"{title} ({angle_mode})"
        box_divider(left, title, right)
        left, right = "├", "┤"
        # هر علامتِ این دسته را در یک ردیف چاپ کن
        for symbol, meaning, example in operators:
            operator_row(symbol, meaning, example)
    # کفِ کادر
    border = "─" * BOX_WIDTH
    print(f"  {GRAY}╰{border}╯{RESET}")


def guide_cell(symbol, example):
    # یک خانه از کادرِ راهنما: علامت، مثال، و جوابِ همان مثال
    answer = "= " + format_number(calculate(example))
    symbol_part = f"{CYAN}{BOLD}{symbol.ljust(6)}{RESET}"
    example_part = example.ljust(13)
    # هر خانه دقیقاً نصفِ پهنای کادر است؛ جواب، باقی‌مانده‌ی خانه را پر می‌کند
    # 21 = 2 + 6 + 13
    answer_part = f"{GREEN}{answer.ljust(BOX_WIDTH // 2 - 21)}{RESET}"
    return "  " + symbol_part + example_part + answer_part


def print_quick_guide():
    # همان داده‌های منو، این بار فشرده: در هر ردیف دو علامت کنارِ هم
    left, right = "╭", "╮"
    for title, operators in OPERATOR_GROUPS:
        if title == "Trigonometry":
            title = f"{title} ({angle_mode})"
        box_divider(left, title, right)
        left, right = "├", "┤"
        # علامت‌ها را دوتا‌دوتا بردار؛ شماره‌های 0 و 1، بعد 2 و 3، و...
        for i in range(0, len(operators), 2):
            pair = operators[i:i + 2]
            row = ""
            for symbol, meaning, example in pair:
                row += guide_cell(symbol, example)
            # اگر تعداد فرد بود، جای خالیِ خانه‌ی دوم را با فاصله پر کن
            empty = " " * (BOX_WIDTH - BOX_WIDTH // 2 * len(pair))
            print(f"  {GRAY}│{RESET}{row}{empty}{GRAY}│{RESET}")
    # کفِ کادر
    border = "─" * BOX_WIDTH
    print(f"  {GRAY}╰{border}╯{RESET}")


def print_banner():
    # یک خطِ افقی به اندازه‌ی پهنای کادر می‌سازیم
    border = "─" * BOX_WIDTH

    # سقفِ کادر
    print()
    print(f"  {GRAY}╭{border}╮{RESET}")
    box_line("", RESET)
    # هر خطِ لوگو را با رنگِ مخصوصِ خودش چاپ کن
    for line, color in zip(LOGO, LOGO_COLORS):
        box_line(line, BOLD + color)
    box_line("", RESET)
    box_line("~ scientific python calculator ~", GRAY)
    # کفِ کادر
    print(f"  {GRAY}╰{border}╯{RESET}")
    print()

    # کادرِ راهنمای فشرده: همه‌ی علامت‌ها و توابع، دسته‌بندی‌شده و با مثال
    print_quick_guide()
    print()

    # دکمه‌ها
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
    # جوابِ درست را سبز و پررنگ نشان بده
    print(f"    {GRAY}╰─{RESET} {GREEN}{BOLD}= {answer}{RESET}")
    print()


def show_error(message):
    # خطا را با یک برچسبِ قرمز نشان بده
    print(f"    {GRAY}╰─{RESET} {ERROR_STYLE} ERROR {RESET} {RED}{message}{RESET}")
    print()


def show_history(history):
    print()
    print(f"   {PINK}╭─ {BOLD}History{RESET}")

    # اگر لیست خالی است، یعنی هنوز هیچ حسابی انجام نشده
    if len(history) == 0:
        print(f"   {PINK}│{RESET}  {GRAY}Nothing yet. Try typing sin(30){RESET}")

    # طولانی‌ترین عبارت را پیدا کن تا علامت‌های = زیرِ هم بیفتند
    longest = 0
    for expression, answer in history:
        if len(expression) > longest:
            longest = len(expression)

    # هر حساب را با شماره‌اش چاپ کن
    number = 1
    for expression, answer in history:
        print(f"   {PINK}│{RESET}  {GRAY}{number:>2}.{RESET}  {expression.ljust(longest)}   {GREEN}= {answer}{RESET}")
        number += 1

    print(f"   {PINK}╰─{RESET} {GRAY}{len(history)} calculation(s) · saved in {HISTORY_FILE_NAME}{RESET}")
    print()


# ════════════════════════════════════════════════════════════
#   بخش ۶: ذخیره‌ی تاریخچه در فایل
#   هر خطِ فایل یک حساب است؛ مثل این:
#       sin(30) = 0.5
# ════════════════════════════════════════════════════════════

# اسمِ فایل؛ جدا از فایلِ نسخه‌ی ساده، تا تاریخچه‌ها قاطی نشوند
HISTORY_FILE_NAME = "scientific_history.txt"
# پوشه‌ای که همین فایلِ پایتون داخلش قرار دارد
FOLDER = os.path.dirname(os.path.abspath(__file__))
# آدرسِ کاملِ فایلِ تاریخچه: داخلِ همان پوشه
HISTORY_FILE = os.path.join(FOLDER, HISTORY_FILE_NAME)


def load_history():
    history = []
    # اگر فایل هنوز ساخته نشده (مثلاً بارِ اولِ اجرا)، تاریخچه خالی است
    if not os.path.exists(HISTORY_FILE):
        return history
    # فایل را برای خواندن باز کن و خط به خط بخوان
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        for line in file:
            # خط را از جای علامتِ مساوی به دو تکه تقسیم کن: عبارت و جواب
            parts = line.strip().split(" = ")
            # فقط خط‌های سالم را قبول کن (خط‌های خالی یا خراب را رد کن)
            if len(parts) == 2:
                history.append((parts[0], parts[1]))
    return history


def save_to_history_file(expression, answer):
    # فایل را در حالتِ «افزودن» باز کن تا حسابِ جدید به تهِ فایل اضافه شود؛
    # اگر فایل وجود نداشته باشد، خودش ساخته می‌شود
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(f"{expression} = {answer}\n")
    except OSError:
        # اگر نوشتن ممکن نبود (مثلاً پوشه قفل بود)، برنامه نباید بترکد
        show_error(f"Could not save to {HISTORY_FILE_NAME}")


def delete_history(history):
    # اگر چیزی برای پاک کردن نیست، همین را بگو و برگرد
    if len(history) == 0:
        print(f"    {GRAY}╰─ History is already empty{RESET}")
        print()
        return

    # پاک کردن برگشت ندارد؛ پس اول از کاربر مطمئن شو
    try:
        reply = input(f"    {YELLOW}?{RESET} Delete all {len(history)} calculation(s)? {GRAY}(y/n){RESET} ")
    except (KeyboardInterrupt, EOFError):
        reply = "n"
    if reply.strip().lower() not in ("y", "yes"):
        print(f"    {GRAY}╰─ Cancelled, nothing was deleted{RESET}")
        print()
        return

    # لیستِ داخلِ حافظه را خالی کن
    history.clear()
    # فایل را در حالتِ «نوشتن» باز کن و هیچ چیز ننویس؛ این‌طوری فایل خالی می‌شود
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            pass
    except OSError:
        show_error(f"Could not clear {HISTORY_FILE_NAME}")
        return
    print(f"    {GRAY}╰─{RESET} {GREEN}History deleted{RESET}")
    print()


# ════════════════════════════════════════════════════════════
#   بخش ۷: برنامه‌ی اصلی
# ════════════════════════════════════════════════════════════

def main():
    # این تابع مقدارِ last_answer را عوض می‌کند؛ پس می‌گوییم منظورمان همان متغیرِ بیرونی است
    global last_answer

    # تاریخچه‌ی دفعه‌های قبل را از فایل بخوان تا از دست نرود
    history = load_history()

    clear_screen()
    print_banner()

    # حلقه‌ی بی‌پایان: هر دور، یک ورودی از کاربر می‌گیریم
    while True:
        try:
            # حالتِ زاویه (DEG یا RAD) را کنارِ علامتِ ورودی نشان بده
            text = input(f"  {GRAY}{angle_mode}{RESET} {PINK}{BOLD}»{RESET} ")
        except (KeyboardInterrupt, EOFError):
            # اگر کاربر Ctrl+C زد، بدون پیامِ خطا بیرون برو
            break

        # فاصله‌های اول و آخر را حذف و حروف را کوچک کن
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
            # کادرِ منوی کامل را با مثال‌ها نشان بده
            print()
            print_operators()
            print()
        elif command in ("a", "angle"):
            toggle_angle_mode()
        elif command in ("c", "clear"):
            clear_screen()
            print_banner()
        else:
            # سعی کن حساب کنی؛ اگر خطایی پیش آمد، پیامِ مناسبش را نشان بده
            try:
                result = calculate(command)
                answer = format_number(result)
                # جوابِ دقیق را برای ans نگه دار
                last_answer = result
                history.append((command, answer))
                show_result(answer)
                # حساب را در فایل هم بنویس تا بعد از بستنِ برنامه هم بماند
                save_to_history_file(command, answer)
            except ZeroDivisionError:
                show_error("You can't divide by zero")
            except OverflowError:
                show_error("The number is too big")
            except ValueError as error:
                show_error(str(error))

    print(f"\n  {PINK}Goodbye!{RESET}\n")


# فقط وقتی این فایل مستقیماً اجرا شد (نه وقتی import شد)، برنامه را شروع کن
if __name__ == "__main__":
    main()
