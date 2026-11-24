<div align="center">

# 🧮 ماشین‌حساب ترمینالی با پایتون

**دو ماشین‌حساب خوش‌ظاهر برای ترمینال، همراه با آموزش خط به خط کد به زبان فارسی**

<br>

![Python](https://img.shields.io/static/v1?label=Python&message=3.8%2B&color=3776AB&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/static/v1?label=Dependencies&message=None&color=2ea44f)
![Docs](https://img.shields.io/static/v1?label=Docs&message=Persian&color=8957e5)

</div>

<br>

ترمینال لازم نیست خشک و بی‌روح باشد. این پروژه یک ماشین‌حساب ساده و یک ماشین‌حساب مهندسی است که در ترمینال اجرا می‌شوند، با لوگوی رنگی، کادرهای مرتب، دکمه‌های میان‌بُر، تاریخچه‌ای که با بستن برنامه پاک نمی‌شود، و پیام‌های خطایی که واقعاً می‌گویند مشکل کجاست.

نکته‌ی اصلی اما چیز دیگری است: کنار کد، صفحه‌های آموزشی هست که **تک‌تک خط‌ها** را به زبان ساده توضیح می‌دهند. یعنی هم یک ابزار کاربردی دارید و هم یک کلاس کوچک پایتون. ✨

<br>

## 👀 نگاهی به برنامه

```text
  ╭────────────────────────────────────────────────────────────────────────╮
  │                                                                        │
  │                     ██████╗ █████╗ ██╗      ██████╗                    │
  │                    ██╔════╝██╔══██╗██║     ██╔════╝                    │
  │                    ██║     ███████║██║     ██║                         │
  │                    ██║     ██╔══██║██║     ██║                         │
  │                    ╚██████╗██║  ██║███████╗╚██████╗                    │
  │                     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝                    │
  │                                                                        │
  │                    ~ scientific python calculator ~                    │
  ╰────────────────────────────────────────────────────────────────────────╯

  DEG » sin(30) + 2pi
    ╰─ = 6.783185307

  DEG » sqrt(16) * 5!
    ╰─ = 480

  DEG » log(1000) ^ 2
    ╰─ = 9
```

<br>

## 🚀 شروع سریع

فقط کافی است **پایتون ۳.۸ یا جدیدتر** روی سیستم‌تان نصب باشد. هیچ کتابخانه‌ی اضافه‌ای لازم نیست. اگر پایتون ندارید، از [python.org](https://www.python.org/downloads/) دانلودش کنید.

```bash
git clone https://github.com/Batman561/calc.git
cd calc
python scientific_calculator.py
```

برای نسخه‌ی ساده هم بنویسید `python calculator.py`. در مک و لینوکس اگر `python` کار نکرد، `python3` را امتحان کنید.

<br>

## 🧭 دو نسخه، یک ایده

<table dir="rtl">
  <tr><th></th><th>🧮 ساده</th><th>🔬 مهندسی</th></tr>
  <tr><td>فایل</td><td><code>calculator.py</code></td><td><code>scientific_calculator.py</code></td></tr>
  <tr><td>چهار عمل اصلی، توان، درصد، باقی‌مانده و پرانتز</td><td>✅</td><td>✅</td></tr>
  <tr><td>سینوس، کسینوس، تانژانت و معکوس‌هایشان</td><td></td><td>✅</td></tr>
  <tr><td>جذر، ریشه‌ی سوم، لگاریتم، توان e و قدرمطلق</td><td></td><td>✅</td></tr>
  <tr><td>فاکتوریل، عدد پی، عدد e و جواب قبلی</td><td></td><td>✅</td></tr>
  <tr><td>حالت درجه و رادیان</td><td></td><td>✅</td></tr>
  <tr><td>ضرب بدون علامت، مثل <code>2pi</code></td><td></td><td>✅</td></tr>
  <tr><td>تاریخچه‌ی ماندگار در فایل</td><td>✅</td><td>✅</td></tr>
  <tr><td>آموزش خط به خط</td><td>✅</td><td>✅</td></tr>
</table>

<br>

## ⌨️ چه چیزهایی می‌شود نوشت؟

<table dir="rtl">
  <tr><th>عملیات</th><th>مثال</th><th>جواب</th></tr>
  <tr><td>چهار عمل اصلی</td><td><code>2 + 3 * 4</code></td><td><code>14</code></td></tr>
  <tr><td>پرانتز</td><td><code>(2 + 3) * 4</code></td><td><code>20</code></td></tr>
  <tr><td>توان</td><td><code>2 ^ 10</code></td><td><code>1,024</code></td></tr>
  <tr><td>درصد</td><td><code>200 * 15%</code></td><td><code>30</code></td></tr>
  <tr><td>باقی‌مانده‌ی تقسیم</td><td><code>17 mod 5</code></td><td><code>2</code></td></tr>
  <tr><td>🔬 مثلثات</td><td><code>sin(30)</code></td><td><code>0.5</code></td></tr>
  <tr><td>🔬 معکوس مثلثاتی</td><td><code>asin(0.5)</code></td><td><code>30</code></td></tr>
  <tr><td>🔬 جذر و ریشه‌ی سوم</td><td><code>sqrt(16) + cbrt(27)</code></td><td><code>7</code></td></tr>
  <tr><td>🔬 لگاریتم</td><td><code>log(1000)</code></td><td><code>3</code></td></tr>
  <tr><td>🔬 فاکتوریل</td><td><code>5!</code></td><td><code>120</code></td></tr>
  <tr><td>🔬 عدد پی</td><td><code>2pi</code></td><td><code>6.283185307</code></td></tr>
  <tr><td>🔬 جواب قبلی</td><td><code>ans * 2</code></td><td>دو برابرِ جواب قبلی</td></tr>
</table>

ردیف‌هایی که 🔬 دارند فقط در نسخه‌ی مهندسی هستند. زاویه‌ها به‌طور پیش‌فرض درجه‌اند.

<br>

## 🎛️ دکمه‌ها

حرف را تایپ کنید و Enter بزنید:

<table dir="rtl">
  <tr><td><kbd>H</kbd></td><td>نمایش تاریخچه</td></tr>
  <tr><td><kbd>D</kbd></td><td>پاک کردن تاریخچه (اول تأیید می‌گیرد)</td></tr>
  <tr><td><kbd>M</kbd></td><td>منوی کامل علامت‌ها با مثال</td></tr>
  <tr><td><kbd>A</kbd></td><td>🔬 جابه‌جایی بین درجه و رادیان</td></tr>
  <tr><td><kbd>C</kbd></td><td>پاک کردن صفحه</td></tr>
  <tr><td><kbd>Q</kbd></td><td>خروج</td></tr>
</table>

<br>

## 📖 آموزش خط به خط

هر صفحه کل کد را خط به خط نشان می‌دهد و زیر هر خط، به زبان ساده توضیح می‌دهد که آن خط چه کار می‌کند و چرا آن‌جاست. روی شماره‌ی هر خط هم که بزنید، لینک مستقیم همان خط را دارید.

<table dir="rtl">
  <tr><td>🧮</td><td><a href="https://batman561.github.io/calc/calculator_explained.html"><b>آموزش نسخه‌ی ساده</b></a></td><td>همراه با الفبای پایتون و یک جعبه‌ی «خودتان امتحان کنید»</td></tr>
  <tr><td>🔬</td><td><a href="https://batman561.github.io/calc/scientific_calculator_explained.html"><b>آموزش نسخه‌ی مهندسی</b></a></td><td>مینیمال، با حالت روشن و تیره</td></tr>
  <tr><td>✂️</td><td><a href="https://batman561.github.io/calc/scientific_calculator_no_comments_explained.html"><b>نسخه‌ی مهندسی بدون کامنت</b></a></td><td>همان کد، تمیز و بدون کامنت، با همه‌ی توضیح‌ها</td></tr>
</table>

<br>

## 🗂️ ساختار پروژه

```text
calc
├── calculator.py                                     ماشین‌حساب ساده
├── calculator_explained.html                         آموزش نسخه‌ی ساده
├── scientific_calculator.py                          ماشین‌حساب مهندسی
├── scientific_calculator_explained.html              آموزش نسخه‌ی مهندسی
├── scientific_calculator_no_comments.py              نسخه‌ی مهندسی بدون کامنت
└── scientific_calculator_no_comments_explained.html  آموزش نسخه‌ی بدون کامنت
```

<br>

## 💡 چند نکته

* بهترین ظاهر را در **Windows Terminal** (ترمینال پیش‌فرض ویندوز ۱۱) یا هر ترمینال مدرن دیگری می‌بینید.
* نوشته‌های داخل برنامه انگلیسی‌اند، چون ترمینال‌ها هنوز متن فارسی را درست نشان نمی‌دهند. در عوض همه‌ی کامنت‌های کد فارسی‌اند.
* اعداد فارسی هم کار می‌کنند؛ مثلاً `۲ + ۳`.
* تاریخچه در فایل‌های `history.txt` و `scientific_history.txt` کنار خود برنامه ذخیره می‌شود.

<br>

<div align="center">

ساخته‌شده با ❤️ و پایتون

اگر این پروژه به کارتان آمد، با یک ⭐ خوشحالمان کنید

</div>
