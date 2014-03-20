from flask import Flask, redirect, url_for, session, render_template, g, request, flash, jsonify
from flask_oauth import OAuth

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import json
import os

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console

# add the celery tasks as an import
import sys
sys.path.append('../../tasks')
from tasks import *


import os
if os.path.exists('/vagrant'):
    DATABASE_URI = 'sqlite:////vagrant/server/apps/annotator/annotator.sqlite'
    GOOGLE_CLIENT_ID = '688423433398-cb5t4hcsjc5pse5h0j33a058h26plg1r.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'oPYtDHYdQ5H5YIomDkb7jm3m'
    REDIRECT_URI = '/oauth/'  # one of the Redirect URIs from Google APIs console



elif os.path.exists('/Users'):

    DATABASE_URI = 'sqlite:///annotator.sqlite'
    GOOGLE_CLIENT_ID = '688423433398-cb5t4hcsjc5pse5h0j33a058h26plg1r.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'oPYtDHYdQ5H5YIomDkb7jm3m'
    REDIRECT_URI = '/oauth/'  # one of the Redirect URIs from Google APIs console


else:

    DATABASE_URI = 'sqlite:////home/flaskuser/annotationstation/app/annotator.sqlite'
    GOOGLE_CLIENT_ID = '688423433398-q7n4s4445ukdng5qsg8s70b494sgtnsf.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'grKyji51A0hX_WfRQOD2Kfsd'
    REDIRECT_URI = '/oauth/'  # one of the Redirect URIs from Google APIs console


SECRET_KEY = 'development key'
DEBUG = True

# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY



oauth = OAuth()

# setup sqlalchemy
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


# define a standard user model
class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)

    # considering add google ID and bIsEmailVerified here
    user_email = Column('user_email', String(60))
    user_oauth_token = Column('user_oauth_token', String(200))
    user_role = Column('user_role', String(200))
    user_oauth_secret = Column('user_oauth_secret', String(200))

    def __init__(self, email):
        self.user_email = email


# define the Image model
class Image(Base):
    __tablename__ = 'images'
    id = Column('id', Integer, primary_key=True)

    mskcc_key = Column('mskcc_key', String())
    mskcc_details = Column('mskcc_details', String())


# define the annotation model
class Annotation(Base):
    __tablename__ = 'annotations'
    id = Column('id', Integer, primary_key=True)
    image_id = Column('image_id', Integer)
    user_id = Column('user_id', Integer)
    details = Column('details', String())


class TaskList(Base):
    __tablename__ = 'tasklist'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    image_list = Column('image_list', String())



def init_db():
    Base.metadata.create_all(bind=engine)



@app.before_request
def before_request():
    g.user = None
    if 'id' in session:
        g.user = User.query.get(session['id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response




@app.route('/')
def index():

    result = add.delay(4, 4)

    if g.user is not None:
        print g.user
    return render_template('index-revise.html')


@app.route('/admin')
def admin():
    if g.user is not None:
        print g.user.user_role
    return render_template('admin.html')

@app.route('/review/<image_id>')
def simpleImageView(image_id):

    # we actually don't use the image_id in flask, but angular will

    if g.user is not None:
        print g.user.user_role
    return render_template('simpleimageview.html')



@app.route('/test')
def apiTest():
    if g.user is not None:
        print g.user.user_role
    return render_template('apitest.html')




def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d


# def createFormRQ(input_data):

#     input_file = '/vagrant/docx_templates/' + input_data['form']['file']
#     output_file = '/vagrant/python_app/app/static/gen/' + input_data['form']['file']

#     print 'input: %s' % input_file
#     print 'temporary: %s ' % output_file

#     info_to_return = {}
#     info_to_return['local_path'] = static_file_path
#     info_to_return['remote_path'] = '/static/gen/%s' % output_file.split('/')[-1].split('.')[0] + '.pdf'

#     return info_to_return


@app.route('/point', methods=['GET', 'POST'])
def addPoint():

    import json



    msg = {}
    msg['status'] = 'start'

    if request.method == 'GET':
        print 'get test'

    elif request.method == 'POST':
        # import pprint

        opdata = json.loads(request.data)

        msg['point'] = opdata

    # print msg
    return json.dumps(msg)



@app.route('/segment', methods=['GET', 'POST'])
def segment():

    import json

    msg = {}
    msg['status'] = 'start'    

    if request.method == 'GET':
        print 'get test'

    elif request.method == 'POST':
        # import pprint
        # pprint.pprint(json.loads(request.data))

        opdata = json.loads(request.data)

        import cv2
        import numpy as np
        import Image
        import cStringIO
        import re


        imgstr = re.search(r'base64,(.*)', opdata['image']).group(1)
        tempimg = cStringIO.StringIO(imgstr.decode('base64'))
        tempimg.seek(0)
        cvimg = cv2.imdecode(np.asarray(bytearray(tempimg.read()), dtype=np.uint8), 1)
        imgray = cv2.cvtColor(cvimg,cv2.COLOR_BGR2GRAY)
        imgray = imgray*255

        cv2.imwrite('segment.jpg', imgray)

        # now have practical binary image

        contours = cv2.findContours(imgray,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # print imgray.shape

        extent = opdata['extent']
        tr = extent[0]
        bl = extent[1]

        # print extent
        # print len(contours)

        outer_contours = contours[0]

        # print outer_contours[0]

        # think -> each point is relative to the image dimension 0,0
        # we need to get this into native space

        # [[965.625, -90.9375], [-5.625, -629.0625]]

        # [tr, bl] 

        native_width = tr[0] - bl[0]
        native_height = -bl[1] + tr[1]

        # print imgray.shape
        # print native_width / native_height
        # print native_width, native_height
        # print imgray.shape[1] / float(imgray.shape[0])

        x_scale = native_width / imgray.shape[1]
        y_scale = native_height / imgray.shape[0]

        cnt_list = []

        for cnt in outer_contours:

            ca = np.array(cnt)[:,0,:]

            print 'start', ca.shape

            x_vals = np.round(ca[:,0] * x_scale) + bl[0]
            y_vals = -1*np.round(ca[:,1] * y_scale) + tr[1]

            new_cnt = np.column_stack((x_vals, y_vals))

            print 'new', new_cnt.shape

            cnt_list.append(new_cnt)


        class NumPyArangeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist() # or map(int, obj)
                return json.JSONEncoder.default(self, obj)
        print len(contours[0][0])

        contour_string = json.dumps(cnt_list, cls=NumPyArangeEncoder)

        print contour_string

        msg['contourstr'] = contour_string






    return json.dumps(msg)




@app.route('/fill', methods=['GET', 'POST'])
def fill():

    msg = {}
    msg['status'] = 'start'

    if request.method == 'GET':
        pass
    elif request.method == 'POST':

        # result = fillImage.delay(json.loads(request.data))

        result = fillImage(json.loads(request.data))

        msg['result'] = result

        # print result


    # msg['jobid'] = result.id

    return json.dumps(msg)





    #
    #
    #
    # elif request.method == 'POST':
    #     # import pprint
    #     # pprint.pprint(json.loads(request.data))
    #
    #     opdata = json.loads(request.data)
    #
    #     import cv2
    #     import urllib
    #     import numpy as np
    #
    #     print opdata
    #
    #     req = urllib.urlopen(opdata['image']['url'])
    #     arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    #     img = cv2.imdecode(arr,-1) # 'load it as it is'
    #     # imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #     h, w = img.shape[:2]
    #     mask = np.zeros((h+2, w+2), np.uint8)
    #
    #     lo = int(opdata['tolerance'])
    #     hi = int(opdata['tolerance'])
    #     connectivity = 4
    #     flags = connectivity
    #     flags |= cv2.FLOODFILL_FIXED_RANGE
    #
    #     seed_pt = (int(opdata['click']['relative'][0] * w), int(opdata['click']['relative'][1] * h))
    #
    #     print 'seed', seed_pt
    #     print 'seed value', img[seed_pt[1], seed_pt[0]]
    #
    #     cv2.floodFill(img, mask, seed_pt, (255,255,255), (lo,lo,lo), (hi,hi,hi), flags)
    #     cv2.circle(img, seed_pt, 2, (0, 0, 255), -1)
    #
    #     contours = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    #     # cv2.drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]) None
    #
    #     cv2.drawContours(img, contours[0], 0, (255,0,0), 1, 8)
    #     cv2.imwrite('output.jpg', img)
    #
    #     class NumPyArangeEncoder(json.JSONEncoder):
    #         def default(self, obj):
    #             if isinstance(obj, np.ndarray):
    #                 return obj.tolist() # or map(int, obj)
    #             return json.JSONEncoder.default(self, obj)
    #     print len(contours[0][0])
    #
    #     outer = json.dumps(contours[0][0], cls=NumPyArangeEncoder)
    #     # inner = json.dumps(contours[0][1], cls=NumPyArangeEncoder)
    #
    #     del img, mask
    #
    #
    #     msg['contour'] = {
    #         'outer' : outer
    #         # 'inner' : inner
    #     }
    #
    #
    #     # the points are now relative to the subimage we've obtained them from
    #     # so we need to scale it back up
    #
    #
    #     # divide subimage actual by what it is natively
    #     inverse_rel_width = w / float(opdata['image']['region']['size'][0])
    #     inverse_rel_height = h / float(opdata['image']['region']['size'][1])
    #
    #     # inverse_rel_height = 1
    #     # inverse_rel_width = 1
    #
    #     offset_x = opdata['image']['region']['origin'][0]
    #     offset_y = opdata['image']['region']['origin'][1]
    #
    #     xform = {
    #         'scale' : [inverse_rel_width, inverse_rel_height],
    #         'offset' : [offset_x, offset_y]
    #         }
    #
    #     print xform
    #     print w,h, opdata['image']['region']['size']
    #
    #     msg['xform'] = json.dumps(xform)
    #
    #
    #     # msg['job'] = job.id
    #     # msg['result'] = job.return_value
    #
    # return json.dumps(msg)



@app.route('/upload', methods=['POST'])
def uploadFile():

    return_arr = []

    print request.files

    for f in request.files:
        file = request.files[f]
        print file

        if 'docx' in file.filename:

            import os
            save_path = '/vagrant/docx_templates/%s' % file.filename

            file.save(save_path)
            return_arr.append(save_path)

    msg = {}
    msg['status'] = 'success'
    msg['result'] = return_arr

    print msg

    import json
    return json.dumps(msg)


##### Get all users
#
#	/users
#
#If normal user, returns the logged in user
#If admin, returns all users

@app.route('/users', methods=['GET'])
def userEndPoint():

    if g.user is not None:

        if g.user.user_role == 'admin':


            import json
            result = User.query.all()
            return_result = []

            for row in result:
                dict_row = row2dict(row)
                return_result.append(dict_row)
            return json.dumps(return_result)

        else:

            import json
            result = User.query.filter_by(id=g.user.id)
            return_result = []

            for row in result:
                dict_row = row2dict(row)

                dict_row['user_oauth_token'] = 'redacted'
                dict_row['user_oauth_secret'] = 'redacted'

                return_result.append(dict_row)

            return json.dumps(return_result)
            #return jsonify(return_result)


    else:

        return '{}'



##### Get a single user description
#
#	/user/{user_id}
#
#If normal, returns a description of the user if self
#If admin, returns a description of the user

@app.route('/user/<int:user_index>', methods=['GET'])
def getUser(user_index):

    # verify logged in
    if g.user is not None:
        if request.method == 'GET':

            # get this annotation if it exists, else return empty object
            result = User.query.filter_by(id=user_index)
            return_result = []

            for row in result:
                dict_row = row2dict(row)
                return_result.append(dict_row)

            return json.dumps(return_result)

    return '{}'


##### Get task list for a user
#
#	/user/{user_id}/tasks
#
#If normal, returns task list if user is self
#If admin, returns a task list for user

@app.route('/user/<int:user_index>/tasks', methods=['GET'])
def taskForUser(user_index):

    # verify logged in
    if g.user is not None:
        if request.method == 'GET':

            # get this annotation if it exists, else return empty object
            result = TaskList.query.filter_by(user_id=user_index)

            return_result = []
            #print result.length

            for row in result:
                dict_row = row2dict(row)
                return_result.append(dict_row)

            return json.dumps(return_result)

    return '{}'

##### Get annotation list for a user
#
#	/user/{user_id}/annotations
#
#If normal, returns annotation list if user is self
#If admin, returns an annotation list for user

@app.route('/user/<int:user_index>/annotations', methods=['GET'])
def annotationsForUser(user_index):

    # verify logged in
    if g.user is not None:
        if request.method == 'GET':


            # get this annotation if it exists, else return empty object
            result = Annotation.query.filter_by(user_id=user_index)

            return_result = []

            #print result.length

            for row in result:
                dict_row = row2dict(row)
                return_result.append(dict_row)

            return json.dumps(return_result)

    return '{}'




##### Get all images
#
#	/images
#
#Returns a list of all images

@app.route('/images', methods=['GET'])
def allImagesEndPoint():

    # verify logged in
    if g.user is not None:

        import json
        result = Image.query.order_by(Image.id)

        return_result = []
        for row in result:
            dict_row = row2dict(row)
            contents = json.loads(dict_row['mskcc_details'])

            # add some additional information to keep the db's in line
            contents['DA_id'] = dict_row['id']
            contents['DA_key'] = dict_row['mskcc_key']

            return_result.append(contents)
        return json.dumps(return_result)


    return '{}'






##### Get a subset of images
#
#	/images/{start}/{count}
#
#Returns a subset ({count}) of images, starting at {start}

@app.route('/images/<int:start_index>/<int:count>/', methods=['GET'])
def imageEndPoint(start_index, count):

    if g.user is not None:

        import json
        result = Image.query.order_by(Image.id).offset(start_index).limit(count)
        return_result = []
        for row in result:
            dict_row = row2dict(row)
            contents = json.loads(dict_row['mskcc_details'])

            # add some additional information to keep the db's in line
            contents['DA_id'] = dict_row['id']
            contents['DA_key'] = dict_row['mskcc_key']

            return_result.append(contents)
        return json.dumps(return_result)

    else:

        return '{}'




@app.route('/image/<int:image_index>', methods=['GET'])
def getSingleImage(image_index):

    if g.user is not None:

        import json
        result = Image.query.order_by(Image.id).filter_by(id=image_index)
        return_result = []
        for row in result:
            dict_row = row2dict(row)
            contents = json.loads(dict_row['mskcc_details'])

            # add some additional information to keep the db's in line
            contents['DA_id'] = dict_row['id']
            contents['DA_key'] = dict_row['mskcc_key']

            return_result.append(contents)
        return json.dumps(return_result)

    else:

        return '{}'


@app.route('/mskccimage/<key>', methods=['GET'])
def getSingleImageByMSKCC(key):

    if g.user is not None:

        import json
        result = Image.query.order_by(Image.id).filter_by(mskcc_key=key)
        return_result = []
        for row in result:
            dict_row = row2dict(row)
            contents = json.loads(dict_row['mskcc_details'])

            # add some additional information to keep the db's in line
            contents['DA_id'] = dict_row['id']
            contents['DA_key'] = dict_row['mskcc_key']

            return_result.append(contents)
        return json.dumps(return_result)

    else:

        return '{}'



##### Get all annotations for an image
#
#	/image/{image_id}/annotations
#
#If normal user, returns annotations created by the user
#If admin, returns all annotations for an image

@app.route('/image/<int:image_index>/annotation', methods=['GET'])
def annotationForImageEndPoint(image_index):

    # verify logged in
    if g.user is not None:
        if request.method == 'GET':

            print 'attempting to load annotation for image', image_index, g.user.id

            # get this annotation if it exists, else return empty object
            result = Annotation.query.filter_by(image_id=image_index).filter_by(user_id=g.user.id).first()

            if result:
                # should be a single row
                result_dict = row2dict(result)
                return json.dumps(result_dict)

            else:

                result_dict = {}
                result_dict['status'] = 'not found'
                return json.dumps(result_dict)


    return '{}'



#### Get all annotations
#
#	/annotations
#
#If normal user, returns annotations for all images created by user
#If admin, returns all annotations for all images

@app.route('/annotations', methods=['GET'])
def allAnnotations():

        # verify logged in
    if g.user is not None:

        import json
        result = Annotation.query.all()
        return_result = []
        for row in result:
            dict_row = row2dict(row)
            #contents = { int(dict_row['id']) : json .loads(dict_row['details']) }


            return_result.append(dict_row)
        return json.dumps(return_result)

    else:
        return '{}'


##### Get single annotation
#
#	/annotation/{annotation_id}
#
#If normal user, returns annotation if created by user
#If admin, returns annotation

@app.route('/annotation/<int:annotation_index>', methods=['GET', 'POST', 'DELETE'])
def annotationEndPoint(annotation_index):

    # verify logged in
    if g.user is not None:
        if request.method == 'GET':
            # get this annotation if it exists, else return empty object
            result = Annotation.query.filter_by(id=annotation_index).first()

            if result:
                # should be a single row
                result_dict = row2dict(result)
                return json.dumps(result_dict)



    return '{}'


##### Create a new annotation
#
#	/annotation
#
#Method: POST
#Contents:
#
#	{
#		image_id: the image id in the database
#		user_id: the user id in the database
#		details: {
#			normal: an array of annotations
#			lesion: an array of annotations
#			patterns: an array of annotations
#			details: an array of annotations
#		}
#	}
#
#Returns a json response. If successfully added to db, returns {status:'success'} and the annotation's id in the db.

@app.route('/annotation/', methods=['POST'])
def annotationCreateEndPoint():

    # verify logged in
    if g.user is not None:

        if request.method == 'POST':

            print request.data

            json_data = json.loads(request.data)

            # annotation = Annotation()

            # # annotation.user_id = json_data['user_id']
            # annotation.image_id = json_data['image_id']
            # annotation.details = json.dumps(json_data['details'])

            # db_session.add(annotation)
            # db_session.commit()

            response_dict = {}
            response_dict['status'] = 'success'
            # response_dict['new_id'] = annotation.id

            return json.dumps(response_dict)

    else:
        return '{}'













@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/guest')
def loginAsGuest():
    # g.user = None
    # g.user = User.query.get(session['id'])
    #
    session['id'] = 3
    return redirect(request.referrer or url_for('index'))

    # callback=url_for('authorized', _external=True)
    # return google.authorize(callback=callback)


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('access_token', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@google.tokengetter
def get_access_token():
    """This is used by the API to look for the auth token and secret
    it should use for API calls.  During the authorization handshake
    a temporary set of token and secret is used, but afterwards this
    function has to return the token and secret.  If you don't want
    to store this in the database, consider putting it into the
    session instead.
    """

    #user = g.user
    #if user is None:
    #    print 'We don\'t have a current user in the session...'
    #    return
        #return user.oauth_token, user.oauth_secret
    return session.get('access_token')


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):

    # get the next url to go to if login is a success (either passed via query string, or default to index)
    next_url = request.args.get('next') or url_for('index')

    if resp is None:
        print 'denied request'
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    access_token = resp['access_token']

    if access_token is None:
        print 'access token missing'
        flash(u'Access token is missing.')
        return redirect(next_url)

    # we have an access token, set it for the session
    session['access_token'] = access_token, ''

    # values in the google oauth response
    # 1) id_token
    # 2) access_token

    # need to resolve the rest of the google account info and update user in database

    real_access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('index'))

    # returns a json response with
    # 1) verified_email (boolean)
    # 2) id
    # 3) email
    import json
    user_data = json.loads(res.read())
    print user_data

    user = User.query.filter_by(user_email=user_data['email']).first()

    # if it's their first time, add them to the database
    if user is None:
        user = User(user_data['email'])
        db_session.add(user)

    # now set their most recent auth values
    user.oauth_token = resp['access_token']
    user.oauth_secret = resp['id_token']
    db_session.commit()

    # finally set, their user id as a session variable (this is the primary key in the users DB)
    # it is used to resolve the user prior to each request (wow this app is DB read heavy)
    session['id'] = user.id

    flash('You were signed in')

    return redirect(next_url)





def main():

    init_db()

    app.debug = True

    app.run()


if __name__ == '__main__':
    main()
