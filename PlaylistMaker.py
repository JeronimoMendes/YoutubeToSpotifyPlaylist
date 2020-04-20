import json
import webbrowser
import bs4
import requests

user_id = input("ID Spotify: ")
print("Uma pagina web vai abrir. Carrega em (GET TOKEN) e checka a primeira caixa da lista, depois copia o "
      "codigo e insere-o aqui. Carrega OK para abrir a pagina.")
r = input("")
webbrowser.open("https://developer.spotify.com/console/post-playlists/?user_id=&body=%7B%22name%22%3A%22New"
                "%20Playlist%22%2C%22description%22%3A%22New%20playlist%20description%22%2C%22public%22%3Afalse%7D")
spotify_token = input("Usa o website para obteres o token de acesso e insere-o aqui: ")
url_playlist = "https://www.youtube.com/playlist?list=PL1hQ6_WNAUuJaRlUIEtp3CS_UjlNw6Xnu"
nome_playlist = input("Nome da playlist: ")
descr = input("Descricao da playlist: ")

musicas = []

palavras_proibidas = ["OFFICIAL", "VIDEO", "ALBUM", "VERSION", "AUDIO", "(", ")",
                      "MUSIC VIDEO", "LYRICS", "[", "]", "MUSIC", "HD"]

print("A procurar as musicas...")


# ------------------------------------------Parte do youtube--------------------------------------------------------
# Funcao que retira o titulo do video youtube
def titulo_yt(url_playlist):
    html_link = requests.get(url_playlist)
    result = {}
    pagina = html_link.content
    title = bs4.BeautifulSoup(pagina, "html.parser")

    try:
        result['title'] = title.find("span", attrs={"class": "watch-title"}).text.strip()
        titulo = (str(result["title"])).upper()

        for palavra in palavras_proibidas:
            titulo = titulo.replace(palavra, "")

        return titulo
    except:
        print("Nao encontrado o titulo.")


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

print()


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

if len(lista_final) > 99:
    lista1 = []
    lista2 = []
    for uri in lista_final:
        if list.index(uri) > 90:
            lista2.append(uri)
        else:
            lista1.append(uri)
    adicionar_musicas(id_playlist, lista1)
    adicionar_musicas(id_playlist, lista2)
    print("Feito")
else:
    adicionar_musicas(id_playlist, lista_final)
    print("Feito")
