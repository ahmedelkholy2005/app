from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform
import requests


class WebViewApp(App):
    def build(self):
        # واجهة المستخدم الرئيسية
        self.layout = BoxLayout(orientation='vertical')

        # التحقق من النظام الأساسي
        if platform == 'android':
            from jnius import autoclass, cast
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            Context = autoclass('android.content.Context')

            # إنشاء WebView
            self.webview = WebView(activity)
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.setWebViewClient(WebViewClient())

            # إضافة WebView إلى الواجهة
            self.layout.add_widget(self.webview)

            # تحميل موقع الويب
            self.webview.loadUrl('https://www.eva-store.store')
        else:
            # إذا لم يكن النظام Android، عرض رسالة
            self.layout.add_widget(Label(text='WebView is only supported on Android', font_size=20))

        # بدء التحقق الدوري من الاتصال بالإنترنت
        Clock.schedule_interval(self.check_internet, 10)  # التحقق كل 10 ثوانٍ

        return self.layout

    def check_internet(self, *args):
        try:
            # التحقق من الاتصال بالإنترنت
            response = requests.get('https://www.eva-store.store', timeout=5)
            if response.status_code == 200:
                self.connected()
            else:
                self.not_connected()
        except:
            self.not_connected()

    def connected(self, *args):
        # إذا كان الاتصال متاحًا، افتح موقع الويب
        if platform == 'android' and hasattr(self, 'webview'):
            self.webview.loadUrl('https://www.eva-store.store')

    def not_connected(self, *args):
        # إذا لم يكن الاتصال متاحًا، أغلق موقع الويب
        if platform == 'android' and hasattr(self, 'webview'):
            self.webview.loadUrl('about:blank')  # إفراغ WebView

        # عرض رسالة الخطأ
        if not hasattr(self, 'popup') or not self.popup:
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            content.add_widget(Label(text='No internet connection', font_size=20))
            retry_button = Button(text='Retry', size_hint=(1, 0.2))
            retry_button.bind(on_press=self.retry_connection)

            self.popup = Popup(title='Connection Error', content=content, size_hint=(0.8, 0.4))
            self.popup.open()

    def retry_connection(self, *args):
        # إغلاق النافذة المنبثقة وإعادة التحقق من الاتصال
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
            self.popup = None
        self.check_internet()


if __name__ == '__main__':
    WebViewApp().run()
