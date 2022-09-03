import os

current_path = os.path.abspath(os.curdir)
COLAB_DARKNET_ESCAPE_PATH = '/content/gdrive/My\ Drive/darknet' #코랩에서 쓸 경로
COLAB_DARKNET_PATH = '/content/gdrive/My Drive/darknet'

YOLO_IMAGE_PATH = current_path + '/custom' #현재 경로 + /custom
YOLO_FORMAT_PATH = current_path + '/custom'

class_count = 0
test_percentage = 0.2
paths = []

with open(YOLO_FORMAT_PATH + '/' + 'classes.names', 'w') as names, \
     open(YOLO_FORMAT_PATH + '/' + 'classes.txt', 'r') as txt: #파일을 열고 alias설정 => names로 txt로
    for line in txt:
        names.write(line)  
        class_count += 1
    print ("[classes.names] is created")

with open(YOLO_FORMAT_PATH + '/' + 'custom_data.data', 'w') as data:
    data.write('classes = ' + str(class_count) + '\n')
    data.write('train = ' + COLAB_DARKNET_ESCAPE_PATH + '/custom/' + 'train.txt' + '\n')
    data.write('valid = ' + COLAB_DARKNET_ESCAPE_PATH + '/custom/' + 'test.txt' + '\n')
    data.write('names = ' + COLAB_DARKNET_ESCAPE_PATH + '/custom/' + 'classes.names' + '\n')
    data.write('backup = backup')
    print ("[custom_data.data] is created")

os.chdir(YOLO_IMAGE_PATH)
for current_dir, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.jpg'):
            image_path = COLAB_DARKNET_PATH + '/custom/' + f
            paths.append(image_path + '\n')


paths_test = paths[:int(len(paths) * test_percentage)]

paths = paths[int(len(paths) * test_percentage):]


with open(YOLO_FORMAT_PATH + '/' + 'train.txt', 'w') as train_txt:
    for path in paths:
        train_txt.write(path)
    print ("[train.txt] is created")

with open(YOLO_FORMAT_PATH + '/' + 'test.txt', 'w') as test_txt:
    for path in paths_test:
        test_txt.write(path)
    print ("[test.txt] is created")

