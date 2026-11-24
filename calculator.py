# ════════════════════════════════════════════════════════════
#   ماشین حساب ترمینالی ساده با پایتون
#   برای اجرا، در ترمینال این دستور را بزنید:
#       python calculator.py
# ════════════════════════════════════════════════════════════

# ماژول os را می‌آوریم تا صفحه‌ی ترمینال را پاک کنیم و با فایل‌ها کار کنیم
import os

# ماژول math را می‌آوریم تا بفهمیم یک عدد بی‌نهایت شده یا نه
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

# برای هر خطِ لوگو یک رنگ: از فیروزه‌ای تا صورتی (حالت گرادیان)
LOGO_COLORS = [
    "\033[38;5;51m",
    "\033[38;5;81m",
    "\033[38;5;111m",
    "\033[38;5;141m",
    "\033[38;5;171m",
    "\033[38;5;201m",
]

# پهنای داخلِ کادرها (کادرِ لوگو و کادرِ راهنما)
BOX_WIDTH = 46

# راهنمای علامت‌ها، دسته‌بندی‌شده.
# هر دسته یک اسم دارد و چند علامت. هر علامت هم سه چیز دارد:
# خودِ علامت، معنی‌اش، و یک مثال
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
    ]),
    ("Grouping", [
        ("( )", "parentheses", "(2 + 3) * 4"),
    ]),
]


# ════════════════════════════════════════════════════════════
#   بخش ۲: تکه‌تکه کردن عبارت (Tokenize)
#   "(2+3)*4"  -->  ["(", "2", "+", "3", ")", "*", "4"]
# ════════════════════════════════════════════════════════════

def tokenize(text):
    # همه‌ی حروف را کوچک می‌کنیم تا MOD و mod یکی حساب شوند
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

        # اگر دو ستاره پشت‌سرهم آمد، آن هم مثل ^ یعنی توان
        elif text[i:i + 2] == "**":
            tokens.append("^")
            i += 2

        # کلمه‌ی mod یعنی باقی‌مانده‌ی تقسیم
        elif text[i:i + 3] == "mod":
            tokens.append("mod")
            i += 3

        # علامت‌های تک‌حرفی
        elif char in "+-*/^%()":
            tokens.append(char)
            i += 1

        # هر چیز دیگری را نمی‌شناسیم
        else:
            raise ValueError(f"Unknown character '{char}'")

    return tokens


# ════════════════════════════════════════════════════════════
#   بخش ۳: فهمیدن و حساب کردنِ عبارت (Parse)
#   هر تابع یک «طبقه» از اولویتِ عملگرهاست:
#       parse_expression  ->  +  -
#       parse_term        ->  *  /  mod
#       parse_unary       ->  -5
#       parse_power       ->  ^
#       parse_percent     ->  %
#       parse_primary     ->  numbers and ( )
# ════════════════════════════════════════════════════════════

def peek(tokens):
    # اولین توکن را «نگاه» می‌کند، بدون اینکه از لیست برش دارد
    if len(tokens) > 0:
        return tokens[0]
    return None


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
    # تا وقتی بعدش * یا / یا mod می‌آید، ادامه بده
    while peek(tokens) in ("*", "/", "mod"):
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
    base = parse_percent(tokens)
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


def parse_percent(tokens):
    value = parse_primary(tokens)
    # علامتِ % بعد از عدد یعنی «تقسیم بر صد»:
    #   50%  =  0.5
    while peek(tokens) == "%":
        tokens.pop(0)
        value = value / 100
    return value


def parse_primary(tokens):
    # اگر توکنی نمانده، عبارت ناقص است؛ مثلاً بعد از علامتِ + چیزی نیامده
    if len(tokens) == 0:
        raise ValueError("The expression is incomplete")

    token = tokens.pop(0)

    # پرانتز: داخلش را مثل یک عبارتِ کامل، از اول حساب کن
    if token == "(":
        value = parse_expression(tokens)
        if peek(tokens) != ")":
            raise ValueError("A ')' is missing")
        tokens.pop(0)
        return value

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
#   بخش ۴: نمایشِ زیبا در ترمینال
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
    symbol_part = f"{CYAN}{BOLD}{symbol.ljust(6)}{RESET}"
    meaning_part = f"{GRAY}{meaning.ljust(13)}{RESET}"
    example_part = example.ljust(13)
    # ستونِ آخر، باقی‌مانده‌ی پهنای کادر را پر می‌کند
    # 35 = 3 + 6 + 13 + 13
    answer_part = f"{GREEN}{answer.ljust(BOX_WIDTH - 35)}{RESET}"
    print(f"  {GRAY}│{RESET}   {symbol_part}{meaning_part}{example_part}{answer_part}{GRAY}│{RESET}")


def print_operators():
    # خطِ اول گوشه‌های گرد دارد؛ خط‌های بعدی به دیواره‌های کادر وصل می‌شوند
    left, right = "╭", "╮"
    for title, operators in OPERATOR_GROUPS:
        box_divider(left, title, right)
        left, right = "├", "┤"
        # هر علامتِ این دسته را در یک ردیف چاپ کن
        for symbol, meaning, example in operators:
            operator_row(symbol, meaning, example)
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
    box_line("~ simple python calculator ~", GRAY)
    # کفِ کادر
    print(f"  {GRAY}╰{border}╯{RESET}")
    print()

    # کادرِ راهنمای علامت‌ها، دسته‌بندی‌شده و با مثال
    print_operators()
    print()

    # دکمه‌ها
    buttons = [
        button("H", "History"),
        button("D", "Delete history"),
        button("M", "Menu"),
        button("C", "Clear"),
        button("Q", "Quit"),
    ]
    print("   " + "   ".join(buttons))
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
        print(f"   {PINK}│{RESET}  {GRAY}Nothing yet. Try typing 2 + 2{RESET}")

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

    print(f"   {PINK}╰─{RESET} {GRAY}{len(history)} calculation(s) · saved in history.txt{RESET}")
    print()


# ════════════════════════════════════════════════════════════
#   بخش ۵: ذخیره‌ی تاریخچه در فایل
#   هر خطِ فایل یک حساب است؛ مثل این:
#       2 + 3 = 5
# ════════════════════════════════════════════════════════════

# پوشه‌ای که همین فایلِ پایتون داخلش قرار دارد
FOLDER = os.path.dirname(os.path.abspath(__file__))
# آدرسِ کاملِ فایلِ تاریخچه: داخلِ همان پوشه، با اسمِ history.txt
HISTORY_FILE = os.path.join(FOLDER, "history.txt")


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
        show_error("Could not save to history.txt")


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
        show_error("Could not clear history.txt")
        return
    print(f"    {GRAY}╰─{RESET} {GREEN}History deleted{RESET}")
    print()


# ════════════════════════════════════════════════════════════
#   بخش ۶: برنامه‌ی اصلی
# ════════════════════════════════════════════════════════════

def main():
    # تاریخچه‌ی دفعه‌های قبل را از فایل بخوان تا از دست نرود
    history = load_history()

    clear_screen()
    print_banner()

    # حلقه‌ی بی‌پایان: هر دور، یک ورودی از کاربر می‌گیریم
    while True:
        try:
            text = input(f"  {PINK}{BOLD}»{RESET} ")
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
            # کادرِ راهنمای علامت‌ها را دوباره نشان بده
            print()
            print_operators()
            print()
        elif command in ("c", "clear"):
            clear_screen()
            print_banner()
        else:
            # سعی کن حساب کنی؛ اگر خطایی پیش آمد، پیامِ مناسبش را نشان بده
            try:
                result = calculate(command)
                answer = format_number(result)
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
