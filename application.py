from flask import Flask, render_template, jsonify, request
import search, crawl, rank, like, bookmark, category
from login import naver, kakao, google
import category_data_scheduler, rank_init_scheduler
from flask_cors import CORS
import os
import boto3

application = Flask(__name__)

cors = CORS(application, resources={r"/*": {"origins": "*"}})

application.register_blueprint(search.bp) # 법안 조회 API
application.register_blueprint(crawl.bp) # 법안 상세페이지 크롤링 API
application.register_blueprint(rank.bp) # 순위
application.register_blueprint(like.bp) # 좋아요
application.register_blueprint(bookmark.bp) # 즐겨찾기
application.register_blueprint(category.bp) # 카테고리별 조회 API

application.register_blueprint(kakao.bp) # 카카오 로그인 API
application.register_blueprint(google.bp) # 구글 로그인 API
application.register_blueprint(naver.bp)

application.register_blueprint(category_data_scheduler.bp)

@application.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    application.debug = True
    application.run()

@application.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file']
    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
                      )
    s3.put_object(
        ACL="public-read",
        Bucket=os.environ["BUCKET_NAME"],
        Body=file,
        Key=file.filename,
        ContentType=file.content_type
    )
    return jsonify({'result': 'success'})