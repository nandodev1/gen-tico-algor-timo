def reafSVG():
    rects = open('tst.svg')
    valores = []
    for line in rects:
        l = line.split(' ')
        try:
            if l[-1].split('=')[0] == 'width':
                width = float(l[-1].split('=')[1].split('"')[1])
                valores.append(width)
            if l[-1].split('=')[0] == 'height':
                height =  float(l[-1].split('=')[1].split('"')[1])
                valores.append(height)
            if l[-1].split('=')[0] == 'x':
                x =  float(l[-1].split('=')[1].split('"')[1])
                valores.append(x)
            if l[-2].split('=')[0] == 'y':
                y =  float(l[-2].split('=')[1].split('"')[1])
                valores.append(y)
        except IndexError:
            pass
    return valores