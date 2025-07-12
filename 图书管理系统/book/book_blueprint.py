import time

import pymysql
from flask import render_template, Blueprint, request, redirect

book_blueprint = Blueprint('book',__name__)

@book_blueprint.route('/addbook')#二级路径
def  add_book():
    return  render_template('add_book.html')

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',  # localhost
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

@book_blueprint.route('/savebook',methods=['POST'])#二级路径
def save_book():
    #从表单中取出文件列表
    files= request.files.getlist('files')
    print(len(files))
    urls =[]
    for file in files:
        if file:
            #保存文件
            #获取文件后缀名
            ext = file.filename.split('.')[-1]
            #系统时间毫秒做文件名
            fname = str(int(round(time.time()*1000)))+'.'+ext
            file.save('static/upload/'+fname)
            urls.append(fname)
    print(urls)
    book_name =request.form['book_name']
    author_name = request.form['author_name']
    publisher_name = request.form['publisher_name']
    price = request.form['price']
    page_number = request.form['page_number']
    isbn_number = request.form['isbn_number']
    publish_date = request.form['publish_date']
    uploader_name = request.form['uploader_name']
    sql=' insert into books(book_name,author_name,publisher_name,price,page_number,isbn_number,publish_date,img_url,img1_url,img2_url,img3_url,img4_url,uploader_name) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    execute_sql_no_result(sql,book_name,author_name,publisher_name,price,page_number,isbn_number,publish_date,urls[0],urls[1],urls[2],urls[3],urls[4],uploader_name)
    #查询所有数据
    sql = ' select * from books  where uploader_name=%s'
    result = execute_sql_result(sql,'zhangfenghao')
    #保存文件
    return  render_template('book_list.html',books=result)


@book_blueprint.route('/lists')#二级路径
def book_list():
    sql = ' select * from books  where uploader_name=%s'
    result = execute_sql_result(sql, 'zhangfenghao')
    return  render_template('book_list.html',books=result)


@book_blueprint.route('/delete/<int:book_id>')#二级路径
def book_delete(book_id):
    #删数据
    sql = ' delete from books where book_id=%s'
    execute_sql_no_result(sql,book_id)
    return  redirect('/book/lists')

@book_blueprint.route('/detail/<int:book_id>')#二级路径
def book_detail(book_id):
    sql = ' select * from books where book_id=%s'
    result = execute_sql_result(sql,book_id)
    return  render_template('book_detail.html',book=result[0])