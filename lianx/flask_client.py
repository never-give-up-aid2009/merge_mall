"""
    xxxx
"""

from flask import Flask, send_file
import sys


app = Flask(__name__)

@app.route('/index/')
def index():
    #首页
    return send_file('templates/index.html')

@app.route('/register/')
def register():
    #注册
    return send_file('templates/register.html')

@app.route('/login/')
def login():
    #登录
    return send_file('templates/login.html')

@app.route('/info')
def info():
    #用户中心
    return send_file('templates/info.html')

@app.route('/place_order/<int:id>')
def order_dem(id):
    #订单支付
    return send_file('templates/place_order.html')

@app.route('/site')
def site_dem():
    #收货地址
    return send_file('templates/site.html')



@app.route('/release')
def blog_release():
    #发表分享内容
    return send_file('templates/release.html')
##################################################################
@app.route('/listall')
def blog_listall():
    #发表分享内容
    return send_file('templates/listall.html')

@app.route('/listuser')
def blog_listuser():
    #发表分享内容
    return send_file('templates/listuser.html')

@app.route('/delete/<b_id>')
def blog_delete(b_id):
    #删除内容
    return send_file('templates/delete.html')

@app.route('/comment/<username>/<b_id>')
def blog_comment(username,b_id):
    #评论
    return send_file('templates/comment.html')

@app.route('/collection/<username>/<b_id>')
def blog_collection(username,b_id):
    #点赞
    return send_file('templates/collection.html')

@app.route('/<username>/upload')
def product_upload(username):
    #商品上传===============================================
    return send_file('templates/upload.html')

@app.route('/<username>/list')
def product_list(username):
    #商品列表===============================================
    return send_file('templates/product_list.html')

@app.route('/<username>/search')
def search_product(username):
    #商品搜索===============================================
    return send_file('templates/search_product.html')
@app.route('/<id>/detail')
def product_detail(id):
    #商品详情===============================================
    return send_file('templates/product_detail.html')

@app.route('/pet_closet_add')
def pet_closet_add():
    #增加衣服===============================================
    return send_file('templates/pet_closet_add.html')

@app.route('/pet_closet_list')
def pet_closet_list():
    #衣服列表===============================================
    return send_file('templates/pet_closet_list.html')

if __name__ == '__main__':
    app.run(debug=True)

