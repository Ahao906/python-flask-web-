from flask import Flask, render_template, request, jsonify

#创建服务器
app  =Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/a/<id>')
def a(id):
    return id

@app.route('/index')
def index():
    return render_template('index.html',name='zhangsan',password='lisi',age='18',position='manater')

@app.route('/b',methods=['POST'])
def b():
    username=request.form.get('username')
    password=request.form.get('password')
    return username+ password

@app.route('/query')
def arg_query():
    username=request.args.get('username')
    password =request.args.get('password')
    return 'arg_query' + username + password

@app.route('/json')
def re_json():
    json ={'name':'zhangsan','age':'18'}
    return jsonify(json)# 把字典数据转换为json字符串

@app.route('/divide/<int:a>/<int:b>')
def re_error(a,b):
    try:
        result=a/b
        return str(result)
    except Exception as e:
        return str(e),200

@app.errorhandler(404)
def do_error(error):
    return 'Page Not found',404

@app.route('/base')
def rend_base():
    return render_template('base.html')

@app.route('/child')
def rend_child():
    return render_template('child.html')
# @app.before_request
# def  before(response):
#     print('error')
#     return response
@app.route('/uploadhtml')
def rend_upload():
    return render_template('upload.html')


@app.route('/upload',methods=['POST'])
def upload():
    #接收文件 并且保存到磁盘本地
    f=request.files.get('xxx')
    if f:
        f.save('./static/upload/'+f.filename)
        return 'upload success'
    return  'upload error'


if __name__ == '__main__':
    app.run()
