import requests

headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'
    }

data = {
    'form': 'login',
    'u_return': '/',
    'u_email': 'center@berbex.ru',
    'u_password': '45789rit',
    'u_remember': 'on'

}

def get_html(url):    
    with requests.Session() as s:
        resp = s.get(url, headers=headers)
        s.post(url=url, data=data, headers=headers)
        resp = s.get(url, headers=headers)
    with open('page.html', 'w') as file:
        file.write(resp.text)
    




get_html('http://www.estateline.ru/project/40458/')



# form: login
# u_return: /
# u_email: center@berbex.ru
# u_password: 45789rit
# u_remember: on