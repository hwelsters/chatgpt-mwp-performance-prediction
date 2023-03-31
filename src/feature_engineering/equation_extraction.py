import nltk
import re

class EquationExtraction:
    @staticmethod
    def extract_equations(text : str):
        text = text.replace('  ', '\n')
        text = re.sub(r'\([a-zA-Z][a-zA-Z]', '\n', text)

        split_text = text.split('\n')

        equations = []
        for t in split_text:
            temp = re.sub('\+|\-|\/|\*|[0-9]|\s|=|\(|\)|\÷', ' ', t)
            
            failed = False

            token = nltk.word_tokenize(temp)
            pos_tagged = nltk.pos_tag(token)

            for tag in pos_tagged:
                if tag[1][0:2] == 'VB': failed = True

            if t.count('=') + t.count('>') + t.count('<') + t.count('≤') + t.count('≥') == 0: failed = True
            
            if not failed: equations.append(t.strip())
            
        return equations