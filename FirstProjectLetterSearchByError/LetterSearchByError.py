import numpy as np
from PIL import Image #библиотека "Pillow", чтобы получить доступ к конкретному пикселю 

CREATEBASE="off" #чтобы записать буквы с картинки в *txt, напишите "on" (создать базу) по оси x,y
BASE="base500" #наименование папки базы (500-кол-во циклов в нейронке)
ENTER=[[],[]]
                           


                                ##ФУНКЦИИ:

                        ##ПОЛУЧАЕМ МАТРИЦУ ИЗ КАРТИНКИ №1
def imageToMatrix(img,width,height,pix):
    matrix=[]
    for x in range(width):
        array=[]
        for y in range(height):        
            a = pix[x, y][0]
            b = pix[x, y][1]
            c = pix[x, y][2]
            S = a + b + c
            if (S > 255):
                array.append(0)
            else:
                array.append(1)
        matrix.append(array)
    matrix=np.array(matrix).T #получим матрицу от 0 до 1 из рисунка
                                                                                 
    #заполнит матрицу нулями по гориз. и по верт., чтобы алгоритм смог начать с отсеивания нулей.  
    matrix=np.column_stack((np.linspace(0,0,len(matrix[0])), matrix.T, np.linspace(0,0,len(matrix[0]))))
    matrix=np.column_stack((np.linspace(0,0,len(matrix[0])), matrix.T, np.linspace(0,0,len(matrix[0]))))
    return(matrix);

                     ##РАЗБИЕНИЕ МАТРИЦЫ НА ОТДЕЛЬНЫЕ ЧАСТИ №2

def createSpace(x):
    section=[]
    i=-1    
    for y in x:
        if sum(y)==0:
            i+=1
            m=[]      
            section.append(m)       
        section[i].insert(0,y)
    return(section)

def createSplit(x,y):
    for i in createSpace(x):
        letter=[]
        if np.sum(i)>0:
            z=0
            for n in createSpace(np.array(i).T):
                
                if np.sum(n)>0:
                    let=[]
                    for j in np.array(n).T:
                        let.insert(0,j)
                    let1=[]
                    for j in np.array(let).T:
                        let1.insert(0,j)         
                    letter.append(np.array(let1).T )
                    z=0
                if np.sum(n)==0:
                    z+=1
                if z>10:
                    z=0
                    letter.append([])
            #удаление лишних нулей
            for i in letter:
                arraystart=[]
                for j in i:
                    if sum(j)>0:
                        arraystart.insert(0,j)
                arraystart=np.array(arraystart)
                arrayend=[]
                for t in arraystart.T:
                    if sum(t)>0:
                        arrayend.insert(0,t)
                if i==[]:
                    arrayend.append([])
                arrayend=np.array(arrayend).T
                y.append(arrayend)
            y.append(ENTER)
 

                        ##ПОДСЧЕТ СРЕД. ШИР. И ДЛИНЫ БУКВ №3

            
def averageSizes(x):
    wi=0
    he=0
    g=0
    maxsizes=0
    for i in x:
        if np.sum(i)!=0:
            if len(i)<100 and len(i.T)<100:
                g+=1
                wi+=len(i)
                he+=len(i.T)
                if maxsizes<len(i):
                    maxsizes=len(i)
                if maxsizes<len(i.T):
                    maxsizes=len(i)
    i=int((wi/g+he/g)/2)
    if i<50:
        if maxsizes<50:
            maxsizes=20 #20 на 20 меняю вручную, временно
        else:
            maxsizes=100
    else:
        maxsizes=100  
    return(maxsizes)

                    ##ЗАПОЛНЕНИЕ МАТРИЦЫ НУЛЯМИ ДО НУЖНЫХ РАЗМЕРОВ #4.1

def addZeros(x):
    if len(x) % 2!=0:
        x=np.column_stack((np.linspace(0,0,len(x[0])), x.T))
        x=x.T
    if len(x.T) % 2!=0:
        x=np.column_stack((np.linspace(0,0,len(x)), x))
    diffheight=int(((maxsizes-len(x))/2))
    diffwidth=int(((maxsizes-len(x.T))/2))
    for i in range(diffheight):
        x=np.column_stack((np.linspace(0,0,len(x[0])), x.T, np.linspace(0,0,len(x[0]))))
        x=x.T
    for i in range(diffwidth):
        x=np.column_stack((np.linspace(0,0,len(x)), x, np.linspace(0,0,len(x))))
    return(x)
                    ##ПРОВЕРКА СООТВЕТСТВИЙ МАТРИЦ №4

def checkMatrix(x):
    checkarray=[]
    for i in x:
        if i!=ENTER:
            if len(i)<100 and len(i.T)<100:
                if i!=[]:
                    checkarray.append(addZeros(i))
                else:
                    checkarray.append([])
        else:
            checkarray.append(ENTER)
    return(checkarray)


                            ##НЕЙРОНКА №5


              
def NeuralNetwork(x,y):
    np.random.seed(1) #чтоб рандома не было
    weight0 = 2*np.random.random((maxsizes,10)) - 1 #веса которые будем обновлять
    weight1 = 2*np.random.random((10,maxsizes)) - 1 
    for i in range(500):
        out0 = 1/(1+np.exp(-(np.dot(y,weight0)))) 
        out1 = 1/(1+np.exp(-(np.dot(out0,weight1)))) #создает сигмойду + веса добавляем
        error1 = x - out1
        predictions1 = error1*(out1*(1-out1)) #наши предсказания (делаем производные)
        error0 = predictions1.dot(weight1.T)
        predictions0 = error0 * (out0*(1-out0))
        weight1 += out0.T.dot(predictions1) #обновляем веса
        weight0 += y.T.dot(predictions0)
    error1=np.mean(np.abs(error1)) #узнаем насколько мы ошиблись в среднем
    return error1


                            #ЗАПУСК! RUN! в 5 этапов

 
transcript=[["А"],["а"],["Б"],["б"],["В"],["в"],["Г"],["г"],["G"],["g"],["Д"],["д"],["Д"],["ь"],["д"],["ь"],["Е"],["е"],["Ё"],["ё"],["Ж"],["ж"],["З"],["з"],["И"],["и"],["Й"],["й"],["К"],["к"],["Л"],["л"],["М"],["м"],["Н"],["н"],["НГ"],["нг"],["Н"],["ь"],["н"],["ь"],["О"],["о"],["82"],["8"],["П"],["п"],["Р"],["р"],["С"],["с"],["h2"],["h"],["T"],["т"],["У"],["у"],["Y"],["y"],["Ф"],
             ["ф"],["X"],["x"],["Ц"],["ц"],["Ч"],["ч"],["Ш"],["ш"],["Щ"],["щ"],["Ъ"],["ъ"],["Ь"],["I"],["ь"],["i"],["Ь"],["ь"],["Э"],["э"],["Ю"],["ю"],["Я"],["я"]]
lettersmatrix=[]
out=[" "]
#1 
img = Image.open("kartinka1.jpg")
width = img.size[0] 
height = img.size[1] 
pix = img.load()
matrix=imageToMatrix(img,width,height,pix)

#2
createSplit(matrix, lettersmatrix)
#print(lettersmatrix)
#3
maxsizes = averageSizes(lettersmatrix)
#4
lettersmatrix=checkMatrix(lettersmatrix) 

                        #5 поиск букв с помощью нейронки
    
if CREATEBASE!="on":
    for letter in lettersmatrix:
        if letter!=[]:
            if letter==ENTER:
                out.append("enter")
            else:
                number=0
                for i in range(86):
                    baseletters=np.loadtxt(BASE+"/"+str(number)+".txt")
                    basemeanerror=np.loadtxt(BASE+"/"+"errors.txt")
                    meanerror=NeuralNetwork(baseletters,letter)
                    percent=int(meanerror*100/basemeanerror[number])  #сравниваем ошибку с базой
                    if percent<100:
                        if percent>99.9:
                            out.append(str(transcript[number])+",")
                            break
                    else:
                        if 200-percent>99.9:
                            out.append(str(transcript[number])+",")
                            break
                    number+=1
        else:
            if out[-1]!=" ":
                out.append(" ")
    correctionout=''
    for i in out:
        if i!="enter":    
            correctionout=correctionout+i
        else:
            correctionout=correctionout+"\n"
    print(correctionout)



                            #Создать БАЗУ

if CREATEBASE=="on":
    cleanmatrix=[]
    for letter in lettersmatrix:
        if letter!=[] and letter!=[[],[]]:
            cleanmatrix.append(letter)
    lettersmatrix=[]
    number=0
    for text in cleanmatrix:
        np.savetxt(str(number)+".txt", addZeros(cleanmatrix[number]), fmt="%d")
        number+=1
        lettersmatrix.append(NeuralNetwork(text,text))
    np.savetxt("errors.txt", lettersmatrix)    




    
