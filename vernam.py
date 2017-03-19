# Tomás Abril
# --Criptografia Vernam / one time pad--

import sys
import getopt

import unidecode
import Crypto.Random

# --- alfapeto padrão
# 63 caracteres
# 0 à 62
# ---
# Letras, numeros ou simbolos podem ser inseridos ou retirados do alfabeto abaixo.
# apenas caracteres que pertencem a lista abaixo passarao pelo algoritmo.
# seria interessante adicionar por exemplo '\n', '.', ',', '-', etc
#
alfabeto = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U',
            'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# a única restrição é que é preciso descriptografar a mensagem com o mesmo alfabeto em que ela foi criptografada

def criptografa(des, keyfile, in_name, out_name):
    f_in = open(in_name, 'r', encoding='utf8')
    texto_com_acento = f_in.read()
    frase_mod = ""
    keys = []

    # pra tirar os acentos
    texto_original = unidecode.unidecode(texto_com_acento)
    print("texto de entrada")
    print(texto_com_acento)
    print("texto convertido para ASCII")
    print(texto_original)

    if des:
        f_key = open(keyfile, 'r', encoding='utf8')
        keys = f_key.readlines()  # cria uma lista com cada linha do arquivo
        keys = [i.strip() for i in keys]  # tira " " e '\n'
        keys = [int(i) for i in keys]  # transforma em int
    else:
        for i in range(len(texto_original)):
            randombytes = Crypto.Random.get_random_bytes(sys.getsizeof(1))  # bytes randomicos no tamanho de um int
            randomint = int.from_bytes(randombytes, byteorder='big')  # transforma os bytes em int
            keys.append(randomint)

    for i in range(len(texto_original)):
        # ---
        # if texto_original[i].isalpha() or texto_original[i].isdigit() or texto_original[i] == ' ':
        if texto_original[i] in alfabeto:
            posicao = alfabeto.index(texto_original[i])
            posicao = posicao - keys[i] if des else posicao + keys[i]
            posicao = posicao % len(alfabeto)
            frase_mod += alfabeto[posicao]
        # outros caracteres permanecem
        else:
            frase_mod += texto_original[i]
    # salvando no arquivo de saida
    f_out = open(out_name, 'w')
    f_out.write(frase_mod)
    f_in.close()
    f_out.close()
    print("resultado")
    print(frase_mod)
    # saving keys quando necessario
    if not des:
        f_key = open("keys_" + out_name, 'w')
        f_key.write('\n'.join([str(i) for i in keys]))
    f_key.close()


def main(argv):
    desc = False
    keyfile_name = ""
    try:
        opts, args = getopt.getopt(argv, "hcdk:i:o:")
    except getopt.GetoptError:
        print('erro ao interpretar comando\nmodo de uso:\nvernam.py -c -i input.txt -o output.txt')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("modo de uso:\n"
                  + "vernam.py -c -i texto.txt -o saida.txt\n"
                  + "vernam.py -d -k key.txt -i texto.txt -o saida.txt\n"
                  + "opcoes:\n"
                  + " -i :arquivo de entrada\n"
                  + " -o :arquivo de saida\n"
                  + " -c :criptografa\n"
                  + " -d :descriptografa\n"
                  + " -k key.txt :chave (apenas para descriptografar)")
            sys.exit()
        elif opt in ("-i"):
            inputfile_name = arg
        elif opt in ("-o"):
            outputfile_name = arg
        elif opt in ("-c"):
            desc = False
        elif opt in ("-d"):
            desc = True
        elif opt in ("-k"):
            keyfile_name = arg

    criptografa(desc, keyfile_name, inputfile_name, outputfile_name)


if __name__ == "__main__":
    main(sys.argv[1:])
