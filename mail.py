import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

# تنظیم سایز پنجره
Window.size = (520, 750)

# =========================
# دیکشنری ترجمه‌ها
# =========================
TRANSLATIONS = {
    'fa': {
        'app_title': 'ماشین حساب حرفه‌ای',
        'ready': 'آماده',
        'error': 'خطا',
        'geometry': 'هندسه',
        'vectors': 'بردارها',
        'proportion': 'تناسب',
        'algebra': 'جبر',
        'statistics': 'آمار',
        'n_or_height': 'n یا ارتفاع:',
        'value': 'مقدار (ضلع/قاعده/شعاع):',
        'diagonals': 'قطرها',
        'angles': 'زاویه‌ها',
        'perimeter': 'محیط',
        'triangle_area': 'مساحت مثلث',
        'sphere_volume': 'حجم کره',
        'cylinder_lateral': 'مساحت جانبی استوانه',
        'circle_area': 'مساحت دایره',
        'circle_circumference': 'محیط دایره',
        'vector1': 'بردار ۱ (x y)',
        'vector2': 'بردار ۲ (x y)',
        'add_vectors': 'جمع بردارها',
        'distance': 'فاصله',
        'dot_product': 'ضرب داخلی',
        'vector_length': 'اندازه بردار',
        'proportion_input': 'a b c یا جزء کل',
        'table_proportion': 'تناسب جدولی',
        'percent_of_total': 'درصد از کل',
        'algebra_input': 'a b c را وارد کنید',
        'solve_linear': 'حل ax+b=c',
        'quadratic': 'معادله درجه ۲',
        'stats_input': 'اعداد یا خوب کل',
        'average': 'میانگین',
        'maximum': 'بیشینه',
        'minimum': 'کمینه',
        'probability': 'احتمال',
        'previous': '➡ قبلی',
        'next': 'بعدی ⬅',
        'formula': 'فرمول:',
        'result': 'نتیجه:',
        'enter_n': 'n را وارد کنید',
        'enter_n_side': 'n و ضلع را وارد کنید',
        'enter_base_height': 'قاعده و ارتفاع را وارد کنید',
        'enter_radius': 'شعاع را وارد کنید',
        'enter_radius_height': 'شعاع و ارتفاع را وارد کنید',
        'use_x_y': 'از فرمت x y استفاده کنید',
        'use_a_b_c': 'از فرمت a b c استفاده کنید',
        'enter_numbers': 'اعداد را وارد کنید',
        'use_good_total': 'از فرمت خوب کل استفاده کنید',
        'no_real_roots': 'ریشه حقیقی ندارد'
    },
    'en': {
        'app_title': 'Smart Calculator Pro',
        'ready': 'Ready',
        'error': 'Error',
        'geometry': 'Geometry',
        'vectors': 'Vectors',
        'proportion': 'Proportion',
        'algebra': 'Algebra',
        'statistics': 'Statistics',
        'n_or_height': 'n or height:',
        'value': 'value (side/base/radius):',
        'diagonals': 'Diagonals',
        'angles': 'Angles',
        'perimeter': 'Perimeter',
        'triangle_area': 'Triangle Area',
        'sphere_volume': 'Sphere Volume',
        'cylinder_lateral': 'Cylinder Lateral',
        'circle_area': 'Circle Area',
        'circle_circumference': 'Circle Circumference',
        'vector1': 'Vector 1 (x y)',
        'vector2': 'Vector 2 (x y)',
        'add_vectors': 'Add Vectors',
        'distance': 'Distance',
        'dot_product': 'Dot Product',
        'vector_length': 'Vector Length',
        'proportion_input': 'Enter a b c or part total',
        'table_proportion': 'Table Proportion',
        'percent_of_total': 'Percent Of Total',
        'algebra_input': 'Enter a b c',
        'solve_linear': 'Solve ax+b=c',
        'quadratic': 'Quadratic Equation',
        'stats_input': 'Enter numbers or good total',
        'average': 'Average',
        'maximum': 'Maximum',
        'minimum': 'Minimum',
        'probability': 'Probability',
        'previous': '⬅ Previous',
        'next': 'Next ➡',
        'formula': 'Formula:',
        'result': 'Result:',
        'enter_n': 'Enter n',
        'enter_n_side': 'Enter n and side',
        'enter_base_height': 'Enter base and height',
        'enter_radius': 'Enter radius',
        'enter_radius_height': 'Enter radius and height',
        'use_x_y': 'Use: x y',
        'use_a_b_c': 'Use: a b c',
        'enter_numbers': 'Enter numbers',
        'use_good_total': 'Use: good total',
        'no_real_roots': 'No Real Roots'
    }
}

# =========================
# کلاس ورودی سفارشی
# =========================
class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 14
        self.size_hint_y = None
        self.height = 40
        self.padding = [10, 10]
        self.multiline = False
        self.background_color = (0.2, 0.23, 0.29, 1)
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = (1, 1, 0, 1)

# =========================
# کلاس صفحه پایه با پشتیبانی از زبان و تم
# =========================
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang = 'fa'  # پیش‌فرض فارسی
        self.theme = 'dark'  # پیش‌فرض تیره
    
    def update_language(self, lang):
        self.lang = lang
        self.update_texts()
    
    def update_theme(self, theme):
        self.theme = theme
        self.apply_theme()
    
    def update_texts(self):
        pass  # در کلاس‌های فرزند override می‌شود
    
    def apply_theme(self):
        bg_color = (0.12, 0.16, 0.23, 1) if self.theme == 'dark' else (0.95, 0.95, 0.95, 1)
        text_color = (1, 1, 1, 1) if self.theme == 'dark' else (0, 0, 0, 1)
        self.background_color = bg_color
        self.background_color = bg_color
    
    def show_error(self, msg_key):
        app = App.get_running_app()
        msg = app.translate(msg_key)
        popup = Popup(
            title=app.translate('error'),
            content=Label(text=msg),
            size_hint=(0.8, 0.4)
        )
        popup.open()

# =========================
# صفحه هندسه
# =========================
class GeometryScreen(BaseScreen):
    def update_texts(self):
        t = TRANSLATIONS[self.lang]
        self.ids.title.text = t['geometry']
        self.ids.label_n.text = t['n_or_height']
        self.ids.label_val.text = t['value']
        self.ids.btn_diagonals.text = t['diagonals']
        self.ids.btn_angles.text = t['angles']
        self.ids.btn_perimeter.text = t['perimeter']
        self.ids.btn_area.text = t['triangle_area']
        self.ids.btn_volume.text = t['sphere_volume']
        self.ids.btn_lateral.text = t['cylinder_lateral']
        self.ids.btn_circle_area.text = t['circle_area']
        self.ids.btn_circumference.text = t['circle_circumference']
    
    def diagonals(self):
        try:
            n = int(self.ids.n_entry.text)
            result = n * (n - 3) // 2
            formula = f"d = n(n-3)/2 = {n}({n-3})/2 = {result}"
            App.get_running_app().set_result(f"{self.translate('diagonals')}: {result}", formula)
        except:
            self.show_error('enter_n')
    
    def angles(self):
        try:
            n = int(self.ids.n_entry.text)
            total = (n - 2) * 180
            each = total / n
            formula = f"Sum = (n-2)×180 = ({n}-2)×180 = {total} | Each = {total}/{n} = {each}"
            App.get_running_app().set_result(f"Sum = {total} | Each = {each}", formula)
        except:
            self.show_error('enter_n')
    
    def perimeter(self):
        try:
            n = int(self.ids.n_entry.text)
            a = float(self.ids.val_entry.text)
            result = n * a
            formula = f"P = n×a = {n}×{a} = {result}"
            App.get_running_app().set_result(f"{self.translate('perimeter')} = {result}", formula)
        except:
            self.show_error('enter_n_side')
    
    def area(self):
        try:
            b = float(self.ids.val_entry.text)
            h = float(self.ids.n_entry.text)
            result = 0.5 * b * h
            formula = f"A = ½×b×h = ½×{b}×{h} = {result}"
            App.get_running_app().set_result(f"{self.translate('triangle_area')} = {result}", formula)
        except:
            self.show_error('enter_base_height')
    
    def volume(self):
        try:
            r = float(self.ids.val_entry.text)
            result = (4/3) * math.pi * r**3
            formula = f"V = 4/3×π×r³ = 4/3×π×{r}³ = {result}"
            App.get_running_app().set_result(f"{self.translate('sphere_volume')} = {result}", formula)
        except:
            self.show_error('enter_radius')
    
    def lateral(self):
        try:
            r = float(self.ids.val_entry.text)
            h = float(self.ids.n_entry.text)
            result = 2 * math.pi * r * h
            formula = f"LA = 2×π×r×h = 2×π×{r}×{h} = {result}"
            App.get_running_app().set_result(f"{self.translate('cylinder_lateral')} = {result}", formula)
        except:
            self.show_error('enter_radius_height')
    
    def circle_area(self):
        try:
            r = float(self.ids.val_entry.text)
            result = math.pi * r**2
            formula = f"A = π×r² = π×{r}² = {result}"
            App.get_running_app().set_result(f"{self.translate('circle_area')} = {result}", formula)
        except:
            self.show_error('enter_radius')
    
    def circle_perimeter(self):
        try:
            r = float(self.ids.val_entry.text)
            result = 2 * math.pi * r
            formula = f"C = 2×π×r = 2×π×{r} = {result}"
            App.get_running_app().set_result(f"{self.translate('circle_circumference')} = {result}", formula)
        except:
            self.show_error('enter_radius')
    
    def translate(self, key):
        return TRANSLATIONS[self.lang][key]

# =========================
# صفحه بردارها
# =========================
class VectorsScreen(BaseScreen):
    def update_texts(self):
        t = TRANSLATIONS[self.lang]
        self.ids.title.text = t['vectors']
        self.ids.label_v1.text = t['vector1']
        self.ids.label_v2.text = t['vector2']
        self.ids.btn_add.text = t['add_vectors']
        self.ids.btn_distance.text = t['distance']
        self.ids.btn_dot.text = t['dot_product']
        self.ids.btn_length.text = t['vector_length']
    
    def add_vectors(self):
        try:
            x1, y1 = map(float, self.ids.v1.text.split())
            x2, y2 = map(float, self.ids.v2.text.split())
            result = (x1+x2, y1+y2)
            formula = f"V1+V2 = ({x1},{y1})+({x2},{y2}) = ({result[0]},{result[1]})"
            App.get_running_app().set_result(f"Sum = ({result[0]}, {result[1]})", formula)
        except:
            self.show_error('use_x_y')
    
    def distance_vectors(self):
        try:
            x1, y1 = map(float, self.ids.v1.text.split())
            x2, y2 = map(float, self.ids.v2.text.split())
            d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            formula = f"d = √(({x2}-{x1})²+({y2}-{y1})²) = {d}"
            App.get_running_app().set_result(f"Distance = {d}", formula)
        except:
            self.show_error('use_x_y')
    
    def dot_product(self):
        try:
            x1, y1 = map(float, self.ids.v1.text.split())
            x2, y2 = map(float, self.ids.v2.text.split())
            result = x1*x2 + y1*y2
            formula = f"V1·V2 = {x1}×{x2}+{y1}×{y2} = {result}"
            App.get_running_app().set_result(f"Dot Product = {result}", formula)
        except:
            self.show_error('use_x_y')
    
    def vector_length(self):
        try:
            x, y = map(float, self.ids.v1.text.split())
            result = math.sqrt(x*x + y*y)
            formula = f"|V| = √({x}²+{y}²) = {result}"
            App.get_running_app().set_result(f"Length = {result}", formula)
        except:
            self.show_error('use_x_y')
    
    def translate(self, key):
        return TRANSLATIONS[self.lang][key]

# =========================
# صفحه تناسب
# =========================
class ProportionScreen(BaseScreen):
    def update_texts(self):
        t = TRANSLATIONS[self.lang]
        self.ids.title.text = t['proportion']
        self.ids.label_input.text = t['proportion_input']
        self.ids.btn_table.text = t['table_proportion']
        self.ids.btn_percent.text = t['percent_of_total']
    
    def table(self):
        try:
            a, b, c = map(float, self.ids.prop_entry.text.split())
            result = (b*c)/a
            formula = f"x = (b×c)/a = ({b}×{c})/{a} = {result}"
            App.get_running_app().set_result(f"x = {result}", formula)
        except:
            self.show_error('use_a_b_c')
    
    def percent_p(self):
        try:
            p, t = map(float, self.ids.prop_entry.text.split())
            result = (p/t)*100
            formula = f"% = (p/t)×100 = ({p}/{t})×100 = {result}%"
            App.get_running_app().set_result(f"Percent = {result}%", formula)
        except:
            self.show_error('use_good_total')
    
    def translate(self, key):
        return TRANSLATIONS[self.lang][key]

# =========================
# صفحه جبر
# =========================
class AlgebraScreen(BaseScreen):
    def update_texts(self):
        t = TRANSLATIONS[self.lang]
        self.ids.title.text = t['algebra']
        self.ids.label_input.text = t['algebra_input']
        self.ids.btn_linear.text = t['solve_linear']
        self.ids.btn_quadratic.text = t['quadratic']
    
    def solve_linear(self):
        try:
            a, b, c = map(float, self.ids.algebra_entry.text.split())
            x = (c-b)/a
            formula = f"x = (c-b)/a = ({c}-{b})/{a} = {x}"
            App.get_running_app().set_result(f"x = {x}", formula)
        except:
            self.show_error('use_a_b_c')
    
    def quadratic(self):
        try:
            a, b, c = map(float, self.ids.algebra_entry.text.split())
            delta = b**2 - 4*a*c
            if delta < 0:
                App.get_running_app().set_result(self.translate('no_real_roots'), "")
                return
            x1 = (-b + math.sqrt(delta))/(2*a)
            x2 = (-b - math.sqrt(delta))/(2*a)
            formula = f"Δ = b²-4ac = {b}²-4×{a}×{c} = {delta}\nx1 = (-b+√Δ)/2a = {x1}\nx2 = (-b-√Δ)/2a = {x2}"
            App.get_running_app().set_result(f"x1 = {x1} | x2 = {x2}", formula)
        except:
            self.show_error('use_a_b_c')
    
    def translate(self, key):
        return TRANSLATIONS[self.lang][key]

# =========================
# صفحه آمار
# =========================
class StatisticsScreen(BaseScreen):
    def update_texts(self):
        t = TRANSLATIONS[self.lang]
        self.ids.title.text = t['statistics']
        self.ids.label_input.text = t['stats_input']
        self.ids.btn_avg.text = t['average']
        self.ids.btn_max.text = t['maximum']
        self.ids.btn_min.text = t['minimum']
        self.ids.btn_prob.text = t['probability']
    
    def average(self):
        try:
            nums = list(map(float, self.ids.stats_entry.text.split()))
            result = sum(nums)/len(nums)
            formula = f"Avg = ({'+'.join(map(str,nums))})/{len(nums)} = {result}"
            App.get_running_app().set_result(f"Average = {result}", formula)
        except:
            self.show_error('enter_numbers')
    
    def maximum(self):
        try:
            nums = list(map(float, self.ids.stats_entry.text.split()))
            result = max(nums)
            formula = f"Max = max({', '.join(map(str,nums))}) = {result}"
            App.get_running_app().set_result(f"Max = {result}", formula)
        except:
            self.show_error('enter_numbers')
    
    def minimum(self):
        try:
            nums = list(map(float, self.ids.stats_entry.text.split()))
            result = min(nums)
            formula = f"Min = min({', '.join(map(str,nums))}) = {result}"
            App.get_running_app().set_result(f"Min = {result}", formula)
        except:
            self.show_error('enter_numbers')
    
    def probability(self):
        try:
            g, t = map(float, self.ids.stats_entry.text.split())
            result = g/t
            formula = f"P = good/total = {g}/{t} = {result}"
            App.get_running_app().set_result(f"Probability = {result}", formula)
        except:
            self.show_error('use_good_total')
    
    def translate(self, key):
        return TRANSLATIONS[self.lang][key]

# =========================
# کلاس اصلی اپلیکیشن
# =========================
class APZApp(App):
    result_text = StringProperty("آماده")
    formula_text = StringProperty("")
    current_screen = NumericProperty(0)
    active_entry = None
    current_lang = 'fa'
    current_theme = 'dark'
    
    def build(self):
        self.sm = ScreenManager()
        
        # اضافه کردن صفحات
        self.sm.add_widget(GeometryScreen(name='geometry'))
        self.sm.add_widget(VectorsScreen(name='vectors'))
        self.sm.add_widget(ProportionScreen(name='proportion'))
        self.sm.add_widget(AlgebraScreen(name='algebra'))
        self.sm.add_widget(StatisticsScreen(name='statistics'))
        
        # ساخت UI اصلی
        root = BoxLayout(orientation='vertical')
        
        # نوار ابزار بالا (زبان و تم)
        toolbar = BoxLayout(size_hint_y=None, height=50, spacing=5, padding=5)
        toolbar.background_color = (0.12, 0.16, 0.23, 1)
        
        # دکمه زبان
        self.lang_btn = Button(
            text='🇮🇷 فارسی',
            size_hint_x=None,
            width=100,
            background_color=(0.2, 0.23, 0.29, 1),
            color=(1, 1, 1, 1)
        )
        self.lang_btn.bind(on_press=self.toggle_language)
        toolbar.add_widget(self.lang_btn)
        
        # دکمه تم
        self.theme_btn = Button(
            text='🌙 تیره',
            size_hint_x=None,
            width=100,
            background_color=(0.2, 0.23, 0.29, 1),
            color=(1, 1, 1, 1)
        )
        self.theme_btn.bind(on_press=self.toggle_theme)
        toolbar.add_widget(self.theme_btn)
        
        # عنوان
        title_label = Label(
            text=TRANSLATIONS['fa']['app_title'],
            font_size=16,
            bold=True,
            color=(1, 1, 1, 1)
        )
        toolbar.add_widget(title_label)
        self.title_label = title_label
        
        root.add_widget(toolbar)
        
        # نوار نتیجه (نتیجه و فرمول)
        result_box = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=5)
        result_box.background_color = (0.08, 0.12, 0.18, 1)
        
        # نتیجه
        self.result_label = Label(
            text=self.result_text,
            font_size=16,
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=None,
            height=40,
            halign='center',
            valign='middle'
        )
        result_box.add_widget(self.result_label)
        
        # فرمول
        self.formula_label = Label(
            text=self.formula_text,
            font_size=12,
            color=(0.5, 0.8, 1, 1),
            size_hint_y=None,
            height=40,
            halign='center',
            valign='middle',
            text_size=(Window.width, 40)
        )
        result_box.add_widget(self.formula_label)
        
        root.add_widget(result_box)
        
        # ScreenManager
        root.add_widget(self.sm)
        
        # ناوبری
        nav = BoxLayout(size_hint_y=None, height=60, spacing=20, padding=10)
        
        prev_btn = Button(
            text=TRANSLATIONS['fa']['previous'],
            background_color=(0.49, 0.23, 0.93, 1),
            color=(1, 1, 1, 1)
        )
        prev_btn.bind(on_press=self.prev_screen)
        
        next_btn = Button(
            text=TRANSLATIONS['fa']['next'],
            background_color=(0.49, 0.23, 0.93, 1),
            color=(1, 1, 1, 1)
        )
        next_btn.bind(on_press=self.next_screen)
        
        nav.add_widget(prev_btn)
        nav.add_widget(next_btn)
        root.add_widget(nav)
        
        # کیبورد مجازی
        keypad = GridLayout(cols=4, spacing=2, size_hint_y=None, height=200, padding=5)
        
        buttons = [
            '7', '8', '9', '-',
            '4', '5', '6', '.',
            '1', '2', '3', ' ',
            '0'
        ]
        
        for btn_text in buttons:
            btn = Button(text=btn_text)
            btn.bind(on_press=lambda x, t=btn_text: self.insert_num(t))
            keypad.add_widget(btn)
        
        # دکمه‌های ویژه
        backspace_btn = Button(text='⌫', background_color=(0.86, 0.15, 0.15, 1), color=(1, 1, 1, 1))
        backspace_btn.bind(on_press=self.backspace)
        keypad.add_widget(backspace_btn)
        
        clear_btn = Button(text='C', background_color=(0.86, 0.15, 0.15, 1), color=(1, 1, 1, 1))
        clear_btn.bind(on_press=self.clear_entry)
        keypad.add_widget(clear_btn)
        
        root.add_widget(keypad)
        
        # تنظیم پیش‌فرض
        self.update_all_screens()
        
        return root
    
    def toggle_language(self, instance):
        if self.current_lang == 'fa':
            self.current_lang = 'en'
            self.lang_btn.text = '🇬🇧 English'
            self.title_label.text = TRANSLATIONS['en']['app_title']
        else:
            self.current_lang = 'fa'
            self.lang_btn.text = '🇮🇷 فارسی'
            self.title_label.text = TRANSLATIONS['fa']['app_title']
        
        self.update_all_screens()
        self.result_label.text = TRANSLATIONS[self.current_lang]['ready']
    
    def toggle_theme(self, instance):
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            self.theme_btn.text = '☀️ روشن'
            self.apply_theme_to_all('light')
        else:
            self.current_theme = 'dark'
            self.theme_btn.text = '🌙 تیره'
            self.apply_theme_to_all('dark')
    
    def apply_theme_to_all(self, theme):
        bg_color = (0.95, 0.95, 0.95, 1) if theme == 'light' else (0.12, 0.16, 0.23, 1)
        text_color = (0, 0, 0, 1) if theme == 'light' else (1, 1, 1, 1)
        
        # اعمال به همه صفحات
        for screen in self.sm.screens:
            screen.background_color = bg_color
            for child in screen.walk():
                if hasattr(child, 'background_color'):
                    if theme == 'light':
                        child.background_color = (0.9, 0.9, 0.9, 1)
                    else:
                        child.background_color = (0.2, 0.23, 0.29, 1)
                if hasattr(child, 'color'):
                    child.color = text_color
    
    def update_all_screens(self):
        for screen in self.sm.screens:
            if hasattr(screen, 'update_language'):
                screen.update_language(self.current_lang)
    
    def insert_num(self, num):
        if self.active_entry:
            self.active_entry.insert_text(num)
    
    def backspace(self, instance):
        if self.active_entry:
            text = self.active_entry.text
            if len(text) > 0:
                self.active_entry.text = text[:-1]
    
    def clear_entry(self, instance):
        if self.active_entry:
            self.active_entry.text = ''
    
    def set_active_entry(self, entry):
        self.active_entry = entry
    
    def set_result(self, result, formula=""):
        self.result_text = result
        self.formula_text = formula
        self.result_label.text = result
        self.formula_label.text = f"📐 {formula}" if formula else ""
    
    def show_error(self, msg_key):
        msg = TRANSLATIONS[self.current_lang].get(msg_key, msg_key)
        popup = Popup(
            title=TRANSLATIONS[self.current_lang]['error'],
            content=Label(text=msg),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def next_screen(self, instance):
        if self.current_screen < 4:
            self.current_screen += 1
            self.sm.current = self.sm.screen_names[self.current_screen]
    
    def prev_screen(self, instance):
        if self.current_screen > 0:
            self.current_screen -= 1
            self.sm.current = self.sm.screen_names[self.current_screen]
    
    def translate(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

# =========================
# اجرای برنامه
# =========================
if __name__ == '__main__':
    APZApp().run()