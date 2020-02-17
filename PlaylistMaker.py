from pprint import pprint
import bs4
import requests
import json

spotify_token = "BQBAtxNrhuw-3ZthKLP3i6fXYelsYi_W1atCpWp84evEgtjpLyU4huJrkoj" \
                "HqmRN4A33sja8mGsAZAef2IrIU2ua8awDYQmoVmCI2CQ3c225UAVIqiaQdk" \
                "LDNUagFRTrWMDyNF3iwhvNDQJNyRANaKmEqA_s8ZGelCKN21JIm18UYpuxH" \
                "_ZahKdou-e2eKFnH8xDjE_NV9V4MvZJ5VGp24SFrWfHeoH7CSlPnNWKsyxR" \
                "g1YIRZ-atub5poaiLLwamb46jZn5"

musicas = []
url_playlist = "https://www.youtube.com/playlist?list=PL1hQ6_WNAUuIurc2oKsk5VU1jFE55cfmR"
user_id = input("Qual o teu ID Spotify? ")
nome_playlist = input("Qual o nome da playlist? ")
descr = input("Descricao da playlist: ")

palavras_proibidas = ["OFFICIAL", "VIDEO", "ALBUM", "VERSION", "AUDIO", "(", ")", "MUSIC VIDEO", "LYRICS", "[", "]"]


# ------------------------------------------Parte do youtube--------------------------------------------------------
# Funcao que retira o titulo do video youtube
def titulo_yt(url_playlist):
    html_link = requests.get(url_playlist)
    result = {}
    pagina = html_link.content
    title = bs4.BeautifulSoup(pagina, "html.parser")

    result['title'] = title.find("span", attrs={"class": "watch-title"}).text.strip()

    titulo = (str(result["title"])).upper()

    for palavra in palavras_proibidas:
        titulo = titulo.replace(palavra, "")

    return titulo


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
nr = 0  #

# Corre as duas funcoes, acabando com um lista com os nomes das musicas da playlist
for i in playlist_links(url_playlist):
    nr += 1
    titulo = titulo_yt(i)

    musicas.append(titulo)
    print("Música ", nr, " recolhida! : ", titulo)


# ----------------------------------------------Parte do Spotify------------------------------------------------------

# Funcao que cria a playlist:
def criar_playlist():
    request_body = json.dumps({
        "name": "{}".format(nome_playlist),
        "description": "{}".format(descr),
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()

    # id da playlist
    return response_json["id"]


def pesquisa_musica(m):
    query = "https://api.spotify.com/v1/search?q={}&type=track&limit=3".format(m)

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()
    # pprint(response_json)
    try:
        musica_spotify = response_json["tracks"]["items"][0]["uri"]
        return musica_spotify
    except:
        print("Musica nao foi encontrada no Spotify: {}".format(m))


# Funcao que adiciona as musicas a playlist:
def adicionar_musicas(id_playlist, musicas_playlist):
    request_data = json.dumps(musicas_playlist)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(id_playlist)

    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()
    return response_json


id_playlist = criar_playlist()
uri_musicas = []

for musica in musicas:
    uri_musicas.append(pesquisa_musica(musica))

a = ""
lista_final = list(filter(None, uri_musicas))

adicionar_musicas(id_playlist, lista_final)
print("Feito")
