import pymysql
from flask import Flask, render_template, request, jsonify
#引入蓝图模块
from book.book_blueprint import book_blueprint
app =Flask('__name__')

app.register_blueprint(book_blueprint,url_prefix='/book')


def get_db_connection():
    connection = pymysql.connect(
        host='localhost', #localhost
        user='root',
        password='zfh20040906',
        database='test',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
def execute_sql_result(sql,*args):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql,args)
        result = cursor.fetchall()
        # 关闭游标
        cursor.close()
        # 关闭连接
        connection.close()
        return result
def execute_sql_no_result(sql,*args):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql,args)
        # 提交事务
        connection.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        connection.close()
@app.route('/')
def  hello_world():
    return render_template('book_index.html')

@app.route('/login')
def  login_page():
    return render_template('login.html')

#登录数据处理方法
@app.route('/dologin',methods=['GET','POST'])
def doLogin():
    #从表单中接收数据
    username = request.form.get('username')
    password = request.form.get('password')
    #连接数据库
    connection = get_db_connection()
    #获取游标
    with connection.cursor() as cursor:
        #编写sql语句
        sql = 'select * from users where username=%s and password=%s'
        #执行sql语句
        cursor.execute(sql,(username,password))
        #获取结果
        result = cursor.fetchone()
        #关闭游标
        cursor.close()
        #关闭连接
        connection.close()
        #判断结果
        if result:
            return  render_template('index.html')
        else:
            return render_template('login.html',error='用户名密码错误')

@app.route('/users')
def users_page():
    #连接数据库
    # 连接数据库
    connection = get_db_connection()
    # 获取游标
    with connection.cursor() as cursor:
        # 编写sql语句
        sql = ' select * from users '
        # 执行sql语句
        cursor.execute(sql)
        # 获取结果
        result = cursor.fetchall()
        # 关闭游标
        cursor.close()
        # 关闭连接
        connection.close()
        # 判断结果
    return render_template('users.html',users=result)


@app.route('/deleteuser/<int:user_id>')
def delete_user(user_id):
    connection = get_db_connection()
    # 获取游标
    with connection.cursor() as cursor:
        # 编写sql语句
        sql = ' delete from users where user_id=%s '
        # 执行sql语句
        cursor.execute(sql,(user_id))

        sql2=' select *  from users'

        cursor.execute(sql2)
        # 获取结果
        result = cursor.fetchall()
        # 关闭游标
        connection.commit()
        cursor.close()
        # 关闭连接
        connection.close()
    return render_template('users.html',users=result)

@app.route('/adduser',methods=['POST'])
def ajax_add():
    json =request.get_json()
    username = json['username']
    password = json['password']
    sql =' insert into users(username,password) values(%s,%s) '
    execute_sql_no_result(sql,username,password)
    return jsonify({'status':'ok'})


@app.route('/edituser',methods=['POST'])
def ajax_edit():
    json =request.get_json()
    username = json['username']
    password = json['password']
    user_id = json['user_id']
    sql =' update users set username=%s,password=%s where user_id=%s '
    execute_sql_no_result(sql,username,password,user_id)
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    app.run(debug=True)