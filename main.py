import pandas as pd
import re
import json

df = pd.read_csv('assets/LFA_HS_G1.csv')
po = pd.read_csv('assets/palavras_ofensivas.txt')


class Comentario:
    def __init__(
            self, id_c, comentario, likes, dislikes, manchete, regiao, palavra_chave, eh_ofensivo, palavras_ofensivas, correspondencias
    ):
        self.correspondencias = correspondencias
        self.palavras_ofensivas = palavras_ofensivas
        self.eh_ofensivo = eh_ofensivo
        self.palavra_chave = palavra_chave
        self.regiao = regiao
        self.manchete = manchete
        self.dislikes = dislikes
        self.likes = likes
        self.comentario = comentario
        self.id_c = id_c


def regex_construtor(palavra):
    vogais = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    regex_string = ''

    for x in palavra:
        if x in vogais:
            regex_string += "[" + x + "0-9\\W]+[0-9\\W]*"
        else:
            regex_string += x
    return regex_string


if __name__ == '__main__':

    comentarios = []
    palavras_ofensivas = []
    regex_palavras_ofensivas = []

    for x in df.values:

        comentario_a = Comentario(x[0], x[1], x[2], x[3], x[4], x[5], x[6], '', [], [])
        comentarios.append(comentario_a)

    for x in po.values:

        regex_palavras_ofensivas.append({
            "palavra": x[0],
            "regex": regex_construtor(x[0])
        })

    # print(regex_palavras_ofensivas)

    for comentario in comentarios:

        for regex in regex_palavras_ofensivas:

            matches = re.finditer(regex["regex"], comentario.comentario, re.MULTILINE | re.IGNORECASE)

            for matchNum, match in enumerate(matches, start=1):

                if regex["palavra"] in comentario.palavras_ofensivas:

                    pass

                else:
                    comentario.palavras_ofensivas.append(regex["palavra"])

                # print(regex["regex"])
                # print(match)
                comentario.eh_ofensivo = True
                comentario.correspondencias.append("{match}".format(matchNum=matchNum,start=match.start(),end=match.end(),match=match.group()))

    for comentario in comentarios:

        if comentario.eh_ofensivo:

            print("Comentario: " + comentario.comentario)
            temp = "Palavras: "
            for x in comentario.palavras_ofensivas:
                temp += x + " "
            print(temp)
            temp2 = "Correspondencias: "
            for x in comentario.correspondencias:
                temp2 += x + " "
            print(temp2)

