from pygame import Rect
class Ret:
    def __init__(self):
        self.id = ''
        self.x = 0
        self.y = 0
        self.height = 0
        self.width = 0
def str2ret(string_vetor: str) -> list:
    ret = Ret()
    for str in string_vetor:
        str_part = str.split('=')
        str_part_init = str_part[0]
        if str_part_init == 'id':
            ret.id = str_part[1].split('"')[1]
        if str_part_init == 'width':
            ret.width = float(str_part[1].split('"')[1])
        if str_part_init == 'height':
            ret.height = float(str_part[1].split('"')[1])
        if str_part_init == 'x':
            ret.x = float(str_part[1].split('"')[1])
        if str_part_init == 'y':
            ret.y = float(str_part[1].split('"')[1])
    return Rect(ret.x, ret.y, ret.width, ret.height)
def svg2retv(path_svg: str):
    ret_vector = []
    img = open(path_svg)
    dados = img.read()
    for i in range(0, len(dados)): 
        if dados[i] == '<':
            tag = ''
            while dados[i] != '>':
                i += 1
                if dados[i] != '\n':
                    tag += dados[i]
            tags = tag.split(' ')
            date = []
            for ch in tags:
                if ch != '':
                    date.append(ch)
            if date[0] == 'rect':
                ret_vector.append(str2ret(date))
    return ret_vector