import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class NetSecApp(App):

  def build(self):
    self.title = 'NetSec Tool'
    root = BoxLayout(orientation='vertical', padding=15, spacing=10)

    title_label = Label(
        text='🛡️ NetSec Intelligence',
        size_hint_y=None,
        height=40,
        font_size=18,
        bold=True,
        color=(0, 0.8, 1, 1),
    )
    root.add_widget(title_label)

    self.input_field = TextInput(
        hint_text='أدخل الهدف هنا (موقع أو IP)...',
        size_hint_y=None,
        height=50,
        multiline=False,
        font_size=16,
    )
    root.add_widget(self.input_field)

    btn_layout = BoxLayout(
        orientation='vertical', spacing=8, size_hint_y=None, height=160
    )

    btn_port = Button(
        text='🔌 فحص المنافذ (Port Scan)',
        background_color=(0.8, 0.2, 0.2, 1),
        font_size=15,
    )
    btn_port.bind(on_press=self.on_scan_ports)
    btn_layout.add_widget(btn_port)

    btn_dns = Button(
        text='🔍 استعلام DNS',
        background_color=(0.5, 0.2, 0.8, 1),
        font_size=15,
    )
    btn_dns.bind(on_press=self.on_dns_lookup)
    btn_layout.add_widget(btn_dns)

    root.add_widget(btn_layout)

    self.output_label = Label(
        text='جاهز للفحص...',
        size_hint_y=None,
        height=200,
        halign='right',
        valign='top',
        font_size=15,
    )
    self.output_label.bind(
        size=lambda s, w: setattr(s, 'text_size', (w - 20, None))
    )

    scroll = ScrollView(size_hint=(1, 1))
    scroll.add_widget(self.output_label)
    root.add_widget(scroll)

    return root

  def on_scan_ports(self, instance):
    target = self.input_field.text.strip()
    if not target:
      self.output_label.text = '⚠️ يرجى إدخال الهدف أولاً.'
      return
    self.output_label.text = f'⏳ جاري الفحص لـ {target}...'
    try:
      ip = socket.gethostbyname(target)
      self.output_label.text = f'🔓 تم إيجاد العنوان IP:\n{ip}'
    except Exception as e:
      self.output_label.text = f'❌ خطأ: {e}'

  def on_dns_lookup(self, instance):
    target = self.input_field.text.strip()
    if not target:
      self.output_label.text = '⚠️ يرجى إدخال النطاق أولاً.'
      return
    try:
      hostname, aliases, ips = socket.gethostbyname_ex(target)
      self.output_label.text = f"🌐 نتائج DNS:\n- IPs: {', '.join(ips)}"
    except Exception as e:
      self.output_label.text = f'❌ خطأ: {e}'


if __name__ == '__main__':
  NetSecApp().run()
    
