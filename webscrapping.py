import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


def ws(tipos, npages: int):
    # Define las listas en las que se almacenara la información leida
    titulos = []
    href = []
    valoraciones = []
    duracion = []
    dificultad = []
    categorias = []
    ingredientes = []


    # Enlace comun de todas las recetas
    website = "http://www.quehayenlanevera.com/recetas-de-"

    for tipo in tipos:
        path = website + tipo + '/pag-'
        # Repetir para las primeras tres páginas de resultados
        for i in range(1, npages):
          # adiciona a la url el número de página
          url = path + str(i)
          page = urlopen(url)
          html = page.read().decode("utf-8")
          soup = BeautifulSoup(html, "html.parser")
          recetas = soup.find_all("div", class_="divRecetaListado")

          # Extrae de la pagina los elementos requeridos
          for r in recetas:
            # Titulo de la receta
            titulos.append(r.find("a").get("title"))
            # Enlace de la receta
            href.append(r.find("a").get("href"))
            # Valoración de la receta
            valoracion_text = r.find("span").get_text()
            valoracion = [int(s) for s in valoracion_text.split() if s.isdigit()][0]
            valoraciones.append(valoracion)
            # duracion y dificultad
            dur_dif = r.find(class_="descRecetaLista").find_all("strong")
            duracion.append(dur_dif[0].get_text())
            dificultad.append(dur_dif[1].get_text())
            strong = r.find(class_="descRecetaLista").find_all("strong")
            # Categoria
            categoria = r.find(class_="icoTag")
            if categoria != None:
              bloque_cat = categoria.next_element.next_element.next_element
              bloque_cat = bloque_cat.find_all("a")
              cat = [a.get_text() for a in bloque_cat]
              categorias.append(cat)
            else:
              categorias.append(list())
            # Ingredientes
            ingrediente = r.find(class_="icoIngr")
            if ingrediente != None:
              bloque_ing = ingrediente.next_element.next_element.next_element
              ing = bloque_ing.get_text()
              ingredientes.append(ing.split(", "))
            else:
              ingredientes.append(list())

    # Convierte los datos en un dataframe
    recetas = pd.DataFrame({
        "titulo": titulos,
        "href": href,
        "valoracion": valoraciones,
        "duracion": duracion,
        "dificultad": dificultad,
        "categorias": categorias,
        "ingredientes": ingredientes
    })

    return recetas
