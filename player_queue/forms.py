from django import forms
from .models import url
import yt_dlp, traceback

class url_form(forms.ModelForm):
    class Meta:
        model = url
        fields = '__all__'
        widgets = {
            'yt_url' : forms.TextInput(attrs={'class' : 'url_input'}),
        }
        labels = {
            'yt_url': '',
        }
    
    def clean_yt_url(self):
        yt_url = self.cleaned_data.get('yt_url')
        yt_correct_urls = ('https://www.youtube.com/', 'https://m.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')
        if any(yt_url.startswith(url) for url in yt_correct_urls):
            self.check_url(yt_url)
        else:
            self.add_error('yt_url', 'To nie jest link YouTube.')
            
            
        return yt_url


    def get_info(self, url):
        ytdlp_opts = {
            'extract_flat': True
        }
        with yt_dlp.YoutubeDL(ytdlp_opts) as ytdlp:
            info = ytdlp.extract_info(url, download=False)
            
        return info


    def get_durations(self, info):
        if "entries" in info:
            video_durations = list(map(lambda entry: entry['duration'],info['entries']))
            self.get_urls(info)
        elif "duration" in info:
            video_durations = [info['duration']]
            self.get_urls(info)
        else:
            info = self.get_info(url=info['url'])
            video_durations = self.get_durations(info)
            
        return video_durations
    
    
    def get_urls(self, info):
        if "entries" in info:
            video_urls = list(map(lambda entry: entry['url'],info['entries']))
            self.save_urls(video_urls)
        elif "duration" in info:
            video_urls = [info['original_url']]
            self.save_urls(video_urls)
        else:
            info = self.get_info(url=info['url'])
            video_urls = self.get_urls(info)
        
        return video_urls


    def check_url(self, url):
        url = str(url)
        try:
            info = self.get_info(url)
            # all_good jest prawdą kiedy wszystkie filmy z playlisty mają długość mniejszą niż godzina
            all_good = all(map(lambda duration: duration < 3600, self.get_durations(info)))
            if not all_good:
                self.add_error('yt_url', 'Film musi być krótszy niż godzina.')
            return True
        except Exception:
            self.add_error('yt_url', 'Wystąpił nieznany błąd.')
            traceback.print_exc()
            return False
        
    
    def save_urls(self, urls):
        for url in urls:
            url_model = self.Meta.model(yt_url=url)
            url_model.save()
