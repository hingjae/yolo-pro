from xml.dom import minidom
import os # 현재 위치를 찾기위해

current_path = os.path.abspath(os.curdir)
print("Current path is {}".format(current_path))
YOLO_FORMAT_PATH = current_path + '/apple-data/train/images' # 이미지 파일 저장소
XML_FORMAT_PATH = current_path + '/apple-data/train/annotations' # xml 파일 저장소
file_count = 0
classes={} #클래스는 사과, 다친사과 두개 딕셔너리를 만들어줌
classes["apple"] = 0
classes["damaged_apple"] = 1

def getYoloCordinates(size, box):
    width_ratio = 1.0/size[0]
    height_ratio = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x * width_ratio
    w = w * width_ratio
    y = y * height_ratio
    h = h * height_ratio
    return (x,y,w,h)

os.chdir(XML_FORMAT_PATH) # anotation폴더로 이동

with open(YOLO_FORMAT_PATH + '/' + 'classes.txt', 'w') as txt: #classes.txt를 만들어줄 예정 클래스는 두개
    for item in classes:
        txt.write(item + '\n')
        print ("[%s] is added in classes.txt" % item)
    
for current_dir, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.xml'): #xml파일일 경우 파싱
            xmldoc = minidom.parse(file)
            yolo_format = (YOLO_FORMAT_PATH+'/'+file[:-4]+'.txt') #apple이름을 뺀

            with open(yolo_format, "w") as f:
    
                objects = xmldoc.getElementsByTagName('object')
                size = xmldoc.getElementsByTagName('size')[0]
                width = int((size.getElementsByTagName('width')[0]).firstChild.data)
                height = int((size.getElementsByTagName('height')[0]).firstChild.data)
    
                for item in objects:
                    name =  (item.getElementsByTagName('name')[0]).firstChild.data
                    if name in classes:
                        class_name = str(classes[name])
                    else: # 클래스 파일에 class_name이 없다면
                        class_name = "-1"
                        print ("[Warning]Class name ['%s'] is not in classes" % name)
    
                    # get bbox coordinates
                    xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                    ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                    xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                    ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                    xml_cordinates = (float(xmin), float(xmax), float(ymin), float(ymax))
                    yolo_cordinates = getYoloCordinates((width,height), xml_cordinates)
    
                    f.write(class_name + " " + " ".join([("%.6f" % a) for a in yolo_cordinates]) + '\n')
                    file_count += 1
    
            print ("{}. [{}] is created".format(file_count, yolo_format))
