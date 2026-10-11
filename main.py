# Исследовательская работа по дисциплине "Алгоритмы и структуры данных"
# Тема: Числовые алгоритмы. Алгоритм Евклида. Алгоритмы факторизации и поиска
# простых. Псевдослучайные числа. Методы перемешивания.
# Выполнил: Осокин А.В., гр. 1214
#
# Программа делает 4 эксперимента:
#   1 - алгоритм Евклида (вычитание и остаток)
#   2 - простые числа и разложение на множители
#   3 - псевдослучайные числа (свой генератор и random)
#   4 - перемешивание массива (Фишер-Йетс и неправильный способ)
# Графики сохраняются в папку "графики" рядом с программой.

import math
import os
import random
import time

import matplotlib
matplotlib.use("Agg")  # чтобы графики сохранялись в файл, а не открывались окном
import matplotlib.pyplot as plt

# папка для графиков
PAPKA = "графики"
if not os.path.exists(PAPKA):
    os.mkdir(PAPKA)


# ============================================================
#  ЭКСПЕРИМЕНТ 1. АЛГОРИТМ ЕВКЛИДА
# ============================================================

def nod_vychitanie(a, b):
    # НОД через вычитание: из большего числа вычитаем меньшее
    shagi = 0
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
        shagi = shagi + 1
    return a, shagi


def nod_ostatok(a, b):
    # НОД через остаток от деления (обычный алгоритм Евклида)
    shagi = 0
    while b != 0:
        a, b = b, a % b
        shagi = shagi + 1
    return a, shagi


def fibonachchi(n):
    # n-е число Фибоначчи: F(1) = 1, F(2) = 1, F(3) = 2 ...
    a = 1
    b = 1
    for i in range(n - 2):
        a, b = b, a + b
    if n <= 2:
        return 1
    return b


def eksperiment_1():
    print()
    print("=" * 60)
    print("ЭКСПЕРИМЕНТ 1. Алгоритм Евклида: вычитание и остаток")
    print("=" * 60)

    # --- Часть А: маленький пример, чтобы было видно шаги ---
    print()
    print("Пример: НОД(1071, 462)")
    a = 1071
    b = 462
    while b != 0:
        print(f"  {a} = {b} * {a // b} + {a % b}")
        a, b = b, a % b
    print(f"  Ответ: НОД = {a}")

    # --- Часть Б: случайные пары чисел разного размера ---
    print()
    print("Случайные пары чисел (по 1000 пар каждого размера):")
    print(f"{'Числа до':>10} | {'Шагов (вычит.)':>15} | {'Шагов (остат.)':>15} | "
          f"{'Время вычит., мс':>17} | {'Время остат., мс':>17}")
    random.seed(2026)
    razmery = [10**2, 10**3, 10**4, 10**5, 10**6]
    vremya_minus = []
    vremya_ost = []
    for N in razmery:
        pary = []
        for i in range(1000):
            pary.append((random.randint(1, N), random.randint(1, N)))

        # проверяем, что оба способа дают правильный ответ
        for (x, y) in pary:
            if nod_vychitanie(x, y)[0] != math.gcd(x, y) or nod_ostatok(x, y)[0] != math.gcd(x, y):
                print("ОШИБКА в вычислении НОД!", x, y)

        # считаем шаги
        sum_minus = 0
        sum_ost = 0
        for (x, y) in pary:
            sum_minus = sum_minus + nod_vychitanie(x, y)[1]
            sum_ost = sum_ost + nod_ostatok(x, y)[1]

        # замеряем время на все 1000 пар
        start = time.perf_counter()
        for (x, y) in pary:
            nod_vychitanie(x, y)
        t1 = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        for (x, y) in pary:
            nod_ostatok(x, y)
        t2 = (time.perf_counter() - start) * 1000

        vremya_minus.append(t1)
        vremya_ost.append(t2)
        print(f"{N:>10} | {sum_minus / 1000:>15.1f} | {sum_ost / 1000:>15.1f} | "
              f"{t1:>17.3f} | {t2:>17.3f}")

    # --- Часть В: плохой случай для вычитания: пара (N, 1) ---
    print()
    print("Плохой случай для вычитания: НОД(N, 1)")
    print(f"{'N':>10} | {'Шагов (вычит.)':>15} | {'Шагов (остат.)':>15}")
    for N in [10**3, 10**4, 10**5, 10**6]:
        print(f"{N:>10} | {nod_vychitanie(N, 1)[1]:>15} | {nod_ostatok(N, 1)[1]:>15}")

    # --- Часть Г: соседние числа Фибоначчи (теорема Ламе) ---
    print()
    print("Соседние числа Фибоначчи F(n+1), F(n) - худший случай для остатка")
    print(f"{'n':>4} | {'F(n+1)':>12} | {'F(n)':>10} | {'Шагов (остат.)':>15} | "
          f"{'Шагов (вычит.)':>15} | {'Граница Ламе':>13}")
    spisok_n = []
    spisok_shagi = []
    spisok_lame = []
    for n in range(5, 41, 5):
        x = fibonachchi(n + 1)
        y = fibonachchi(n)
        shagi_ost = nod_ostatok(x, y)[1]
        shagi_minus = nod_vychitanie(x, y)[1]
        # граница Ламе: шагов не больше, чем 5 * (кол-во цифр меньшего числа)
        lame = 5 * len(str(y))
        spisok_n.append(n)
        spisok_shagi.append(shagi_ost)
        spisok_lame.append(lame)
        print(f"{n:>4} | {x:>12} | {y:>10} | {shagi_ost:>15} | {shagi_minus:>15} | {lame:>13}")

    # для сравнения: случайные числа такого же размера, как F(40)
    random.seed(1)
    y = fibonachchi(40)
    sredn = 0
    for i in range(1000):
        sredn = sredn + nod_ostatok(random.randint(1, y), random.randint(1, y))[1]
    print(f"Для сравнения: у случайных пар чисел до {y} в среднем {sredn / 1000:.1f} шагов")

    # --- графики ---
    plt.figure(figsize=(7, 4.5))
    plt.plot(razmery, vremya_minus, "o-", label="вычитание")
    plt.plot(razmery, vremya_ost, "s-", label="остаток от деления")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("размер чисел N")
    plt.ylabel("время на 1000 пар, мс")
    plt.title("Алгоритм Евклида: время работы")
    plt.legend()
    plt.grid(True)
    plt.savefig(PAPKA + "/1_evklid_vremya.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.plot(spisok_n, spisok_shagi, "o-", label="шагов на парах Фибоначчи")
    plt.plot(spisok_n, spisok_lame, "--", label="граница Ламе (5 x кол-во цифр)")
    plt.xlabel("n (номер числа Фибоначчи)")
    plt.ylabel("число шагов")
    plt.title("Худший случай алгоритма Евклида")
    plt.legend()
    plt.grid(True)
    plt.savefig(PAPKA + "/1_evklid_fibonachchi.png", dpi=150)
    plt.close()
    print("Графики сохранены в папку", PAPKA)


# ============================================================
#  ЭКСПЕРИМЕНТ 2. ПРОСТЫЕ ЧИСЛА И РАЗЛОЖЕНИЕ НА МНОЖИТЕЛИ
# ============================================================

def prostoe_perebor(n):
    # проверка на простоту перебором делителей до корня из n
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 2
    return True


def vse_prostye_perebor(N):
    # все простые до N, каждое число проверяем перебором
    otvet = []
    for i in range(2, N + 1):
        if prostoe_perebor(i):
            otvet.append(i)
    return otvet


def resheto(N):
    # решето Эратосфена
    prostoe = [True] * (N + 1)
    prostoe[0] = False
    prostoe[1] = False
    i = 2
    while i * i <= N:
        if prostoe[i]:
            # вычеркиваем кратные i, начиная с i*i
            for j in range(i * i, N + 1, i):
                prostoe[j] = False
        i = i + 1
    otvet = []
    for i in range(N + 1):
        if prostoe[i]:
            otvet.append(i)
    return otvet


def miller_rabin(n, k=20):
    # вероятностный тест Миллера - Рабина, k - сколько раз проверяем
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    # представляем n - 1 = 2^s * d, где d нечетное
    d = n - 1
    s = 0
    while d % 2 == 0:
        d = d // 2
        s = s + 1
    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d mod n
        if x == 1 or x == n - 1:
            continue
        sostavnoe = True
        for j in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                sostavnoe = False
                break
        if sostavnoe:
            return False  # точно составное
    return True  # вероятно простое


def razlozhit_perebor(n):
    # разложение на множители перебором делителей
    mnozhiteli = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            mnozhiteli.append(d)
            n = n // d
        d = d + 1
    if n > 1:
        mnozhiteli.append(n)
    return mnozhiteli


def pollard_ro(n):
    # ро-метод Полларда: ищет ОДИН делитель числа n
    if n % 2 == 0:
        return 2
    while True:
        x = random.randint(2, n - 1)
        y = x
        c = random.randint(1, n - 1)
        d = 1
        while d == 1:
            x = (x * x + c) % n          # "черепаха" - один шаг
            y = (y * y + c) % n          # "заяц" - два шага
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:  # если d == n, то не повезло, пробуем другое c
            return d


def razlozhit_pollard(n):
    # полное разложение: делим число на части, пока все не станут простыми
    if n == 1:
        return []
    if miller_rabin(n):
        return [n]
    d = pollard_ro(n)
    return razlozhit_pollard(d) + razlozhit_pollard(n // d)


def eksperiment_2():
    print()
    print("=" * 60)
    print("ЭКСПЕРИМЕНТ 2. Простые числа и разложение на множители")
    print("=" * 60)

    # --- Часть А: все простые до N ---
    print()
    print("Поиск всех простых чисел до N:")
    print(f"{'N':>9} | {'Найдено простых':>15} | {'Перебор, мс':>12} | {'Решето, мс':>11} | {'Во сколько раз':>14}")
    spisok_N = [10**3, 10**4, 10**5, 10**6]
    vremya_perebor = []
    vremya_resheto = []
    for N in spisok_N:
        start = time.perf_counter()
        p1 = vse_prostye_perebor(N)
        t1 = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        p2 = resheto(N)
        t2 = (time.perf_counter() - start) * 1000

        if p1 != p2:
            print("ОШИБКА: списки простых не совпали!")
        vremya_perebor.append(t1)
        vremya_resheto.append(t2)
        print(f"{N:>9} | {len(p2):>15} | {t1:>12.2f} | {t2:>11.2f} | {t1 / t2:>14.1f}")

    # --- Часть Б: проверка больших чисел на простоту ---
    print()
    print("Проверка больших чисел: перебор делителей и Миллер-Рабин (k = 20)")
    print(f"{'Число':>22} | {'Перебор':>10} | {'Время, мс':>10} | {'Миллер-Рабин':>13} | {'Время, мс':>10}")
    random.seed(2026)
    chisla = [561, 1000003, 10**9 + 7, 10**12 + 39, 2**61 - 1]
    for n in chisla:
        if n < 10**13:
            start = time.perf_counter()
            r1 = prostoe_perebor(n)
            t1 = (time.perf_counter() - start) * 1000
            r1_text = "простое" if r1 else "составное"
            t1_text = f"{t1:.3f}"
        else:
            # для 2^61 - 1 перебор займет слишком много времени
            r1_text = "-"
            t1_text = "долго"
        start = time.perf_counter()
        r2 = miller_rabin(n)
        t2 = (time.perf_counter() - start) * 1000
        r2_text = "простое" if r2 else "составное"
        print(f"{n:>22} | {r1_text:>10} | {t1_text:>10} | {r2_text:>13} | {t2:>10.3f}")

    # оценим, сколько бы шел перебор для 2^61 - 1
    # берем скорость перебора на числе 10^12 + 39
    n_test = 10**12 + 39
    start = time.perf_counter()
    prostoe_perebor(n_test)
    t_test = time.perf_counter() - start
    delitelei_test = math.isqrt(n_test) / 2
    delitelei_big = math.isqrt(2**61 - 1) / 2
    ocenka = t_test * delitelei_big / delitelei_test
    print(f"Оценка (не замер!): перебор для 2^61 - 1 занял бы примерно {ocenka:.0f} секунд")

    # --- Часть В: разложение на множители ---
    print()
    print("Разложение на множители: перебор и ро-метод Полларда")
    print(f"{'Число':>22} | {'Множители':>28} | {'Перебор, мс':>12} | {'Поллард, мс':>12}")
    random.seed(2026)
    chisla = [8051, 10403, 1000003 * 1000033, 10000019 * 10000079, (10**9 + 7) * (10**9 + 9)]
    spisok_razmer = []
    vremya_razl_perebor = []
    vremya_razl_pollard = []
    for n in chisla:
        start = time.perf_counter()
        m2 = sorted(razlozhit_pollard(n))
        t2 = (time.perf_counter() - start) * 1000

        if n < 10**15:
            start = time.perf_counter()
            m1 = razlozhit_perebor(n)
            t1 = (time.perf_counter() - start) * 1000
            if m1 != m2:
                print("ОШИБКА: разложения не совпали!")
            t1_text = f"{t1:.2f}"
            spisok_razmer.append(n)
            vremya_razl_perebor.append(t1)
            vremya_razl_pollard.append(t2)
        else:
            t1_text = "долго"

        proizvedenie = 1
        for m in m2:
            proizvedenie = proizvedenie * m
        if proizvedenie != n:
            print("ОШИБКА: произведение множителей не равно числу!")
        mn_text = " x ".join(str(m) for m in m2)
        print(f"{n:>22} | {mn_text:>28} | {t1_text:>12} | {t2:>12.3f}")

    # --- графики ---
    plt.figure(figsize=(7, 4.5))
    plt.plot(spisok_N, vremya_perebor, "o-", label="перебор делителей")
    plt.plot(spisok_N, vremya_resheto, "s-", label="решето Эратосфена")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("N (ищем все простые до N)")
    plt.ylabel("время, мс")
    plt.title("Поиск простых чисел")
    plt.legend()
    plt.grid(True)
    plt.savefig(PAPKA + "/2_prostye_vremya.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.plot(spisok_razmer, vremya_razl_perebor, "o-", label="перебор делителей")
    plt.plot(spisok_razmer, vremya_razl_pollard, "s-", label="ро-метод Полларда")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("раскладываемое число")
    plt.ylabel("время, мс")
    plt.title("Разложение на множители")
    plt.legend()
    plt.grid(True)
    plt.savefig(PAPKA + "/2_razlozhenie_vremya.png", dpi=150)
    plt.close()
    print("Графики сохранены в папку", PAPKA)


# ============================================================
#  ЭКСПЕРИМЕНТ 3. ПСЕВДОСЛУЧАЙНЫЕ ЧИСЛА
# ============================================================

def lkg(x, a, c, m):
    # линейный конгруэнтный генератор: следующее число
    return (a * x + c) % m


def najti_period(x0, a, c, m):
    # считаем, через сколько шагов генератор вернется в уже бывшее число
    bylo = {}
    x = x0
    shag = 0
    while x not in bylo:
        bylo[x] = shag
        x = lkg(x, a, c, m)
        shag = shag + 1
    return shag - bylo[x]


def hi_kvadrat(chisla, korziny):
    # критерий хи-квадрат: насколько равномерно числа (от 0 до 1) попали в корзины
    schet = [0] * korziny
    for v in chisla:
        nomer = int(v * korziny)
        if nomer == korziny:
            nomer = korziny - 1
        schet[nomer] = schet[nomer] + 1
    ozhid = len(chisla) / korziny
    hi = 0
    for s in schet:
        hi = hi + (s - ozhid) ** 2 / ozhid
    return hi, schet


def eksperiment_3():
    print()
    print("=" * 60)
    print("ЭКСПЕРИМЕНТ 3. Псевдослучайные числа")
    print("=" * 60)

    # параметры из книги Numerical Recipes
    A = 1664525
    C = 1013904223
    M = 2**32

    # --- Часть А: первые числа ---
    print()
    print("Первые 5 чисел моего генератора (зерно 2026):")
    x = 2026
    for i in range(5):
        x = lkg(x, A, C, M)
        print("  ", x)

    # --- Часть Б: период ---
    print()
    print("Период генератора при разных параметрах (m = 2^16 = 65536):")
    print(f"{'a':>6} | {'c':>6} | {'Период':>7} | Условия Халла-Добелла")
    varianty = [(25173, 13849, "выполнены"),
                (25173, 13850, "c четное - не выполнены"),
                (25175, 13849, "a-1 не делится на 4 - не выполнены")]
    for (a, c, usl) in varianty:
        p = najti_period(1, a, c, 2**16)
        print(f"{a:>6} | {c:>6} | {p:>7} | {usl}")
    print("Для параметров Numerical Recipes (m = 2^32) условия выполнены,")
    print("значит по теореме период = 2^32 =", 2**32, "(сами не проверяем - слишком долго)")
    print("У random (вихрь Мерсенна) период 2^19937 - 1 (из документации Python)")

    # --- Часть В: младший бит у ЛКГ ---
    print()
    print("Последний бит (четность) первых 20 чисел моего генератора:")
    x = 2026
    bity = ""
    for i in range(20):
        x = lkg(x, A, C, M)
        bity = bity + str(x % 2) + " "
    print("  ", bity)
    print("   (видно, что биты просто чередуются - это слабое место ЛКГ)")

    # --- Часть Г: равномерность ---
    print()
    print("Проверка равномерности (100000 чисел, 10 корзин, хи-квадрат)")
    print("Критическое значение для 9 степеней свободы и уровня 0.05: 16.92")
    kolvo = 100000
    x = 2026
    moi = []
    for i in range(kolvo):
        x = lkg(x, A, C, M)
        moi.append(x / M)
    random.seed(2026)
    ih = []
    for i in range(kolvo):
        ih.append(random.random())
    hi1, schet1 = hi_kvadrat(moi, 10)
    hi2, schet2 = hi_kvadrat(ih, 10)
    print(f"  Мой ЛКГ:  хи-квадрат = {hi1:.2f}, корзины: {schet1}")
    print(f"  random:   хи-квадрат = {hi2:.2f}, корзины: {schet2}")

    # --- Часть Д: скорость ---
    print()
    print("Скорость: генерируем 1 000 000 чисел")
    start = time.perf_counter()
    x = 2026
    for i in range(1000000):
        x = lkg(x, A, C, M)
    t1 = (time.perf_counter() - start) * 1000
    start = time.perf_counter()
    for i in range(1000000):
        random.random()
    t2 = (time.perf_counter() - start) * 1000
    print(f"  Мой ЛКГ: {t1:.1f} мс,  random: {t2:.1f} мс")

    # --- график ---
    nomera = list(range(1, 11))
    plt.figure(figsize=(8, 4.5))
    shirina = 0.4
    plt.bar([n - shirina / 2 for n in nomera], schet1, width=shirina, label="мой ЛКГ")
    plt.bar([n + shirina / 2 for n in nomera], schet2, width=shirina, label="random (вихрь Мерсенна)")
    plt.axhline(kolvo / 10, color="black", linestyle="--", label="ожидаемое (10000)")
    plt.ylim(9000, 10800)
    plt.xticks(nomera)
    plt.xlabel("номер корзины")
    plt.ylabel("сколько чисел попало")
    plt.title("Равномерность генераторов (100000 чисел)")
    plt.legend()
    plt.grid(True, axis="y")
    plt.savefig(PAPKA + "/3_ravnomernost.png", dpi=150)
    plt.close()
    print("График сохранен в папку", PAPKA)


# ============================================================
#  ЭКСПЕРИМЕНТ 4. ПЕРЕМЕШИВАНИЕ
# ============================================================

def fisher_yates(massiv):
    # правильное перемешивание: идем с конца, меняем с элементом от 0 до i
    for i in range(len(massiv) - 1, 0, -1):
        j = random.randint(0, i)
        massiv[i], massiv[j] = massiv[j], massiv[i]


def ploho_peremeshat(massiv):
    # НЕПРАВИЛЬНОЕ перемешивание: меняем с любым элементом от 0 до n-1
    n = len(massiv)
    for i in range(n):
        j = random.randint(0, n - 1)
        massiv[i], massiv[j] = massiv[j], massiv[i]


def eksperiment_4():
    print()
    print("=" * 60)
    print("ЭКСПЕРИМЕНТ 4. Перемешивание массива")
    print("=" * 60)

    # --- Часть А: частоты перестановок для [A, B, C] ---
    raz = 600000
    print()
    print(f"Перемешиваем массив [A, B, C] {raz} раз и считаем перестановки")
    random.seed(2026)
    schet_fy = {}
    schet_plo = {}
    for i in range(raz):
        m = ["A", "B", "C"]
        fisher_yates(m)
        kluch = "".join(m)
        schet_fy[kluch] = schet_fy.get(kluch, 0) + 1

        m = ["A", "B", "C"]
        ploho_peremeshat(m)
        kluch = "".join(m)
        schet_plo[kluch] = schet_plo.get(kluch, 0) + 1

    # теория для плохого способа: 27 исходов, а перестановок 6
    teoria_plo = {"ABC": 4, "ACB": 5, "BAC": 5, "BCA": 5, "CAB": 4, "CBA": 4}
    perestanovki = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    print(f"{'Перест.':>8} | {'Фишер-Йетс':>11} | {'доля':>7} | {'теория':>7} | "
          f"{'Неправильный':>13} | {'доля':>7} | {'теория':>7}")
    hi_fy = 0
    hi_plo = 0
    for p in perestanovki:
        d1 = schet_fy.get(p, 0) / raz
        d2 = schet_plo.get(p, 0) / raz
        t2 = teoria_plo[p] / 27
        print(f"{p:>8} | {schet_fy.get(p, 0):>11} | {d1:>7.4f} | {1/6:>7.4f} | "
              f"{schet_plo.get(p, 0):>13} | {d2:>7.4f} | {t2:>7.4f}")
        ozhid = raz / 6
        hi_fy = hi_fy + (schet_fy.get(p, 0) - ozhid) ** 2 / ozhid
        hi_plo = hi_plo + (schet_plo.get(p, 0) - ozhid) ** 2 / ozhid
    print(f"Хи-квадрат (проверка на равновероятность, крит. значение 11.07 для 5 ст. св.):")
    print(f"  Фишер-Йетс: {hi_fy:.2f}    Неправильный: {hi_plo:.2f}")

    # --- Часть Б: время Фишера-Йетса на больших массивах ---
    print()
    print("Время перемешивания больших массивов")
    print(f"{'n':>9} | {'Фишер-Йетс, мс':>15} | {'random.shuffle, мс':>19}")
    spisok_n = [10**3, 10**4, 10**5, 10**6]
    vremya_fy = []
    vremya_sh = []
    for n in spisok_n:
        m = list(range(n))
        start = time.perf_counter()
        fisher_yates(m)
        t1 = (time.perf_counter() - start) * 1000
        if sorted(m) != list(range(n)):
            print("ОШИБКА: после перемешивания потерялись элементы!")
        m = list(range(n))
        start = time.perf_counter()
        random.shuffle(m)
        t2 = (time.perf_counter() - start) * 1000
        vremya_fy.append(t1)
        vremya_sh.append(t2)
        print(f"{n:>9} | {t1:>15.2f} | {t2:>19.2f}")

    # --- графики ---
    x = list(range(6))
    plt.figure(figsize=(8, 4.5))
    shirina = 0.4
    plt.bar([i - shirina / 2 for i in x], [schet_fy.get(p, 0) / raz for p in perestanovki],
            width=shirina, label="Фишер-Йетс")
    plt.bar([i + shirina / 2 for i in x], [schet_plo.get(p, 0) / raz for p in perestanovki],
            width=shirina, label="неправильный способ")
    plt.axhline(1 / 6, color="black", linestyle="--", label="1/6 (равновероятно)")
    plt.xticks(x, perestanovki)
    plt.ylim(0.12, 0.2)
    plt.xlabel("перестановка")
    plt.ylabel("доля")
    plt.title(f"Частоты перестановок массива [A, B, C] ({raz} раз)")
    plt.legend()
    plt.grid(True, axis="y")
    plt.savefig(PAPKA + "/4_peremeshivanie_chastoty.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.plot(spisok_n, vremya_fy, "o-", label="мой Фишер-Йетс")
    plt.plot(spisok_n, vremya_sh, "s-", label="random.shuffle")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("размер массива n")
    plt.ylabel("время, мс")
    plt.title("Время перемешивания")
    plt.legend()
    plt.grid(True)
    plt.savefig(PAPKA + "/4_peremeshivanie_vremya.png", dpi=150)
    plt.close()
    print("Графики сохранены в папку", PAPKA)


# ============================================================
#  МЕНЮ
# ============================================================

def main():
    while True:
        print()
        print("Выберите эксперимент:")
        print("  1 - алгоритм Евклида")
        print("  2 - простые числа и разложение на множители")
        print("  3 - псевдослучайные числа")
        print("  4 - перемешивание")
        print("  5 - все эксперименты подряд")
        print("  0 - выход")
        vybor = input("Ваш выбор: ")
        if vybor == "1":
            eksperiment_1()
        elif vybor == "2":
            eksperiment_2()
        elif vybor == "3":
            eksperiment_3()
        elif vybor == "4":
            eksperiment_4()
        elif vybor == "5":
            start = time.perf_counter()
            eksperiment_1()
            eksperiment_2()
            eksperiment_3()
            eksperiment_4()
            print()
            print(f"Все эксперименты заняли {time.perf_counter() - start:.1f} с")
        elif vybor == "0":
            break
        else:
            print("Нет такого пункта, попробуйте еще раз")


main()
