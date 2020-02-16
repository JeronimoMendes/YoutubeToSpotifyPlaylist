import webbrowser
import bs4
import requests
import spotipy

musicas = []
url_playlist = input("Link da playlist: ")


# Parte do youtube
# Funcao que retira o titulo do video youtube
def titulo_yt(url_playlist):
    html_link = requests.get(url_playlist)
    result = {}
    pagina = html_link.content
    title = bs4.BeautifulSoup(pagina, "html.parser")
    titulo = title.find_all("style-scope ytd-video-primary-info-renderer")

    result['title'] = title.find("span", attrs={"class": "watch-title"}).text.strip()
    return result["title"]


# Funcao que retira os links de cada musica da playlist
def playlist_links(link_playlist):
    links = []
    r = requests.get(link_playlist)
    page = r.text
    soup = bs4.BeautifulSoup(page, 'html.parser')
    res = soup.find_all("a", {'class': 'pl-video-title-link'})
    for l in res:
        links.append(("http://www.youtube.com/" + l.get("href")))
    return links

# Serve para dar informação ao utilizador de quais a músicas retiradas do youtube
nr = 0 #

# Corre as duas funcoes, acabando com um lista com os nomes das musicas da playlist
for i in playlist_links(url_playlist):
    nr += 1
    titulo = titulo_yt((i))
    musicas.append(titulo)
    print("Música ", nr," : ", titulo, " recolhida!")

# Parte do Spotify

# Permite acessar a API


token = util.prompt_for_user_token("stilton19", scope='playlist-modify-private,playlist-modify-public',
                                   client_id='your-spotify-client-id', client_secret='your-spotify-client-secret',
                                   redirect_uri='your-app-redirect-url')
