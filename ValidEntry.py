from Modulos import *
from Relatorio import *
from Funcao_BD import *

class Validadores:      #validador de caracteres
    def validate_entry2(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100    #100 é referente a 2 digitos 