import re
from kivy._event import partial
from pytube import YouTube

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from kivy.core.window import Window

Window.size = (500, 600)


class MyApp(MDApp):
    def GetLinkInfo(self, event, layout):
        self.link = self.link_input.text

        self.checklink = re.match("^https://www.youtube.com/*", self.link)
        self.checklink_2 = re.match("^https://youtu.be/*", self.link)

        if self.checklink or self.checklink_2:
            self.error_label.text = ""
            self.error_label.pos_hint = {"center_x": 0.5, "center_y": 20}
            try:
                self.yt = YouTube(self.link)
                self.error_label.text = ""
                self.error_label.pos_hint = {"center_x": 0.5, "center_y": 20}
                print("Tittle :" + self.yt.title)
                self.title_Label.text = "Tittle: " + self.yt.title
                self.title_Label.pos_hint = {"center_x": 0.4, "center_y": 0.45}
                self.length_Label.pos_hint = {"center_x": 0.4, "center_y": 0.35}
                self.views_Label.pos_hint = {"center_x": 0.4, "center_y": 0.25}
                self.length_Label.text = "Length: " + str(self.yt.length)
                self.views_Label.text = "Views: " + str(self.yt.views)
                self.download_button.text = "Download"
                self.download_button.pos_hint = {"center_x": 0.4, "center_y": 0.15}
                self.video = self.yt.streams.filter(file_extension="mp4").order_by("resolution").desc()
                self.dropDown = DropDown()

                for vid in self.video:
                    bttn = Button(text=vid.resolution, size_hint=(None, None), height=30)
                    bttn.bind(on_release=lambda bttn: self.dropDown.select(bttn.text))

                    self.dropDown.add_widget(bttn)

                self.mainButton = Button(text="144p", size_hint=(None, None), pos=(350, 65), height=50)
                self.mainButton.bind(on_release=self.dropDown.open)

                self.dropDown.bind(on_select=lambda instance, x: setattr(self.mainButton, "text", x))
                layout.add_widget(self.mainButton)


            except:
                self.error_label.text = "Connection or Unknown Error"
                self.error_label.pos_hint = {"center_x": 0.5, "center_y": 0.45}

        else:
            self.error_label.text = "Error! Invalid Link"
            self.error_label.pos_hint = {"center_x": 0.5, "center_y": 0.45}

    def DownloadVideo(self, event, window):
        self.ys = self.yt.streams.filter(file_extension="mp4").filter(resolution=self.mainButton.text).first()

        self.ys.download("C:/Users/Windows/Videos")

        print("Download Completed")

    def build(self):
        layout = MDRelativeLayout(md_bg_color=[248 / 255, 200 / 248, 220 / 255])
        self.img = Image(source="youtube.png", size_hint=(0.3, 0.3),
                         pos_hint={"center_x": 0.5, "center_y": 0.9})
        self.youtube_link = Label(text="Please Enter YouTube Video Link to download",
                                  pos_hint={"center_x": 0.5, "center_y": 0.75}, size_hint=(1, 1),
                                  font_size=20, color=(1, 0, 0))
        self.link_input = TextInput(text="", pos_hint={"center_x": 0.5, "center_y": 0.65},
                                    size_hint=(1, None), height=48,
                                    font_size=29, foreground_color=(0.1, 0.1, 0.8))
        self.link_button = Button(text="Get Link", pos_hint={"center_x": 0.5, "center_y": 0.55},
                                  size_hint=(0.2, 0.1), font_size=24, font_name="Comic",
                                  background_color=(0, 1, 0))

        self.link_button.bind(on_press=partial(self.GetLinkInfo, layout))
        self.title_Label = Label(text="", pos_hint={"center_x": 0.5, "center_y": 20},
                                 size_hint=(1, 1), font_size=20)
        self.length_Label = Label(text="", pos_hint={"center_x": 0.5, "center_y": 20},
                                  size_hint=(1, 1), font_size=20)
        self.views_Label = Label(text="", pos_hint={"center_x": 0.5, "center_y": 20},
                                 size_hint=(1, 1), font_size=20)

        self.download_button = Button(pos_hint={"center_x": 0.5, "center_y": 20},
                                      size_hint=(0.3, 0.1), size=(75, 75), bold=True, font_size=24,
                                      font_name="Comic", background_color=(0, 1, 0))

        self.download_button.bind(on_press=partial(self.DownloadVideo, layout))

        self.error_label = Label(text="", pos_hint={"center_x": 0.5, "center_y": 20},
                                 size_hint=(1, 1), font_size=20, color=(1, 0, 0))
        layout.add_widget(self.img)
        layout.add_widget(self.youtube_link)
        layout.add_widget(self.link_input)
        layout.add_widget(self.link_button)
        layout.add_widget(self.title_Label)
        layout.add_widget(self.views_Label)
        layout.add_widget(self.length_Label)
        layout.add_widget(self.download_button)
        layout.add_widget(self.error_label)

        return layout


if __name__ == "__main__":
    MyApp().run()
