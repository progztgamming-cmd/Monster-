from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests
import threading

API_URL = "http://127.0.0.1:8000/api/v1/execute" # سيتم تغييره لاحقاً لرابط Replit

class MonsterApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.title_label = Label(text="Monster AI Agent", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.title_label)
        
        self.input_box = TextInput(hint_text="Enter your command here...", multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.input_box)
        
        self.execute_btn = Button(text="Execute Task", size_hint=(1, 0.2))
        self.execute_btn.bind(on_press=self.send_command)
        self.layout.add_widget(self.execute_btn)
        
        self.output_label = TextInput(readonly=True, text="Ready.", size_hint=(1, 0.5))
        self.layout.add_widget(self.output_label)
        
        return self.layout

    def send_command(self, instance):
        command = self.input_box.text
        if not command:
            self.output_label.text = "Please enter a command."
            return
            
        self.output_label.text = "Processing..."
        self.execute_btn.disabled = True
        
        # تشغيل الطلب في خلفية لتجنب تجميد الواجهة
        threading.Thread(target=self._make_api_call, args=(command,)).start()

    def _make_api_call(self, command):
        try:
            response = requests.post(API_URL, json={"command": command})
            if response.status_code == 200:
                data = response.json()
                self.output_label.text = f"Status: {data.get('status')}\nCode Generated:\n{data.get('code')}"
            else:
                self.output_label.text = f"Error: HTTP {response.status_code}"
        except Exception as e:
            self.output_label.text = f"Connection Error: {str(e)}"
        finally:
            self.execute_btn.disabled = False

if __name__ == '__main__':
    MonsterApp().run()
  
