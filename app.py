import os
import random
import base64
from datetime import datetime

from flask import Flask, request, json, session, make_response

from com.yuanhang.model import Message, find_user_by_name, add_user, find_user, User, save_photo, find_photos_by_uid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatAreYouDoing907-()297'

#  定义文件上传路径
basedir = os.path.abspath(os.path.dirname(__name__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'}


#  限制文件上传类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#  对上传的文件进行重命名操作,避免文件重名
def photo_rename():
    now_time = datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = random.randint(10, 99)
    return str(now_time) + str(random_num)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=['post', 'get'])
def register():
    uname = request.args.get('uname')
    password = request.args.get('password')
    message = Message()
    if find_user_by_name(uname) != 0:
        message.status = 0
        message.description = "用户名重复"
        #json.dumps默认只支持基本类型,自定义对象转json需要先转为字典后再操作
        return json.dumps(message.__dict__)
    # 用户名未重复,所以可以进行注册操作
    id = add_user(uname,password)
    user = {'id':id, 'uname':uname, 'password': password}
    session['user'] = user
    return json.dumps(message.__dict__)


@app.route('/login', methods=['post', 'get'])
def login():
    uname = request.args.get('uname')
    password = request.args.get('password')
    message = Message()
    user = find_user(uname, password)
    if user is None:
        message.status = 0
        message.description = "用户名和密码不匹配"
    else:
        session['user'] = {"id": user.id, "uname": uname, "password": password}
    return json.dumps(message.__dict__)


@app.route('/upload_photo', methods=['post'])
def upload_photo():
    img = request.files.get('photo')
    filename = photo_rename()
    message = Message()
    #  img.filename中为上传图片名称
    if not allowed_file(img.filename):
        message.status = 0
        message.description = "图片格式不支持,请重新上传"
        return json.dumps(message.__dict__)
    path = basedir + "/static/photo/"
    file_path = path + filename + '.' + img.filename.rsplit('.', 1)[1]
    # 上传成功后需要将用户id和图片
    if session['user'] is not None:
        save_photo(filename + '.' + img.filename.rsplit('.', 1)[1], session['user']['id'], datetime.today().isoformat())
        img.save(file_path)
    return json.dumps(message.__dict__)


#  根据session中的用户数据查询photo中的路径名称
@app.route('/download_photo', methods=['get','post'])
def download_photo():
    photoByDate = None
    if session['user'] is not None:
        id = session['user']['id']
        photoByDate = find_photos_by_uid(id)
        # 将图片转为Base64编码格式
    return json.dumps(photoByDate)




if __name__ == '__main__':
    app.run()
