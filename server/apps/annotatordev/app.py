


# system imports
import json
import os

# flask imports
from flask import Flask, redirect, url_for, session, render_template, g, request, flash, jsonify
from flask_oauth import OAuth

# bring in our tasks for celery + flower
from tasks import *

# bring in the mongodb interface
from pymongo import MongoClient
db = MongoClient('mongodb://dermoscopic.com:27017')['dermoscopic']

user_collection = db['users']
image_collection = db['images']
annotation_collection = db['annotations']


# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console

GOOGLE_CLIENT_ID = '688423433398-cb5t4hcsjc5pse5h0j33a058h26plg1r.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'oPYtDHYdQ5H5YIomDkb7jm3m'
REDIRECT_URI = '/oauth/'  # one of the Redirect URIs from Google APIs console


# setup flask
app = Flask(__name__)
app.secret_key = 'oPYtDHYdQ5H5YIomDkb7jm3m'

oauth = OAuth()


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


#
# # define a standard user model
# class User(Base):
#     __tablename__ = 'users'
#     id = Column('id', Integer, primary_key=True)
#
#     # considering add google ID and bIsEmailVerified here
#     user_email = Column('user_email', String(60))
#     user_oauth_token = Column('user_oauth_token', String(200))
#     user_role = Column('user_role', String(200))
#     user_oauth_secret = Column('user_oauth_secret', String(200))
#
#     def __init__(self, email):
#         self.user_email = email

#
# # define the Image model
# class Image(Base):
#     __tablename__ = 'images'
#     id = Column('id', Integer, primary_key=True)
#
#     mskcc_key = Column('mskcc_key', String())
#     mskcc_details = Column('mskcc_details', String())
#
#
# # define the annotation model
# class Annotation(Base):
#     __tablename__ = 'annotations'
#     id = Column('id', Integer, primary_key=True)
#     image_id = Column('image_id', Integer)
#     user_id = Column('user_id', Integer)
#     details = Column('details', String())
#
#
# class TaskList(Base):
#     __tablename__ = 'tasklist'
#     id = Column('id', Integer, primary_key=True)
#     user_id = Column('user_id', Integer)
#     image_list = Column('image_list', String())
#
#
#
# def init_db():
#     Base.metadata.create_all(bind=engine)


#
# @app.route('/rev1')
# def index_rev1():
#
#     result = add.delay(4, 1)
#
#     if g.user is not None:
#         print g.user
#     return render_template('index-rev1.html')
#
#
#
# @app.route('/rev3')
# def index_rev3():
#
#     result = add.delay(4, 3)
#
#     if g.user is not None:
#         print g.user
#     return render_template('index-rev3.html')

#
# @app.route('/rev4')
# def index_rev4():
#
#     result = add.delay(4, 3)
#
#     if g.user is not None:
#         print g.user
#     return render_template('index-rev4.html')

#
#
# @app.route('/fillrev1', methods=['GET', 'POST'])
# def fill_rev1():
#
#     msg = {}
#     msg['status'] = 'start'
#
#     if request.method == 'GET':
#         print 'get test'
#
#     elif request.method == 'POST':
#         # import pprint
#         # pprint.pprint(json.loads(request.data))
#
#         opdata = json.loads(request.data)
#
#         import cv2
#         import urllib
#         import numpy as np
#
#         print opdata['image']['url']
#
#         req = urllib.urlopen(opdata['image']['url'])
#         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#         img = cv2.imdecode(arr,-1) # 'load it as it is'
#         # imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#         h, w = img.shape[:2]
#         mask = np.zeros((h+2, w+2), np.uint8)
#
#         lo = 60
#         hi = 80
#
#         # lo = 30
#         # hi = 100
#
#         connectivity = 4
#         flags = connectivity
#         flags |= cv2.FLOODFILL_FIXED_RANGE
#
#         seed_pt = (int(opdata['click']['relative'][0] * w), int(opdata['click']['relative'][1] * h))
#
#         print 'seed', seed_pt
#
#         cv2.floodFill(img, mask, seed_pt, (255,190,00), (lo,lo,lo), (hi,hi,hi), flags)
#
#         # imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#         # ret,thresh = cv2.threshold(imgray,127,255,0)
#
#         cv2.circle(img, seed_pt, 2, (0, 0, 255), -1)
#
#         contours = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#         # cv2.drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]) None
#
#         cv2.drawContours(img, contours[0], 0, (255,0,0), 1, 8)
#         cv2.imwrite('output.jpg', img)
#
#         class NumPyArangeEncoder(json.JSONEncoder):
#             def default(self, obj):
#                 if isinstance(obj, np.ndarray):
#                     return obj.tolist() # or map(int, obj)
#                 return json.JSONEncoder.default(self, obj)
#         print len(contours[0][0])
#
#         outer = json.dumps(contours[0][0], cls=NumPyArangeEncoder)
#         # inner = json.dumps(contours[0][1], cls=NumPyArangeEncoder)
#
#         del img, mask
#
#
#         msg['contour'] = {
#             'outer' : outer
#             # 'inner' : inner
#         }
#
#
#         # the points are now relative to the subimage we've obtained them from
#         # so we need to scale it back up
#
#
#         # divide subimage actual by what it is natively
#         inverse_rel_width = w / float(opdata['image']['region']['size'][0])
#         inverse_rel_height = h / float(opdata['image']['region']['size'][1])
#
#         # inverse_rel_height = 1
#         # inverse_rel_width = 1
#
#
#         offset_x = opdata['image']['region']['origin'][0]
#         offset_y = opdata['image']['region']['origin'][1]
#
#         xform = {
#             'scale' : [inverse_rel_width, inverse_rel_height],
#             'offset' : [offset_x, offset_y]
#             }
#
#         print xform
#
#
#         print w,h, opdata['image']['region']['size']
#
#         msg['xform'] = json.dumps(xform)
#
#
#         # json_data =
#
#         # print json_data
#
#         # job = q.enqueue(createFormRQ, json_data)
#
#         # import time
#         # while job.return_value is None:
#         #     time.sleep(0.5)
#
#
#         # msg['job'] = job.id
#         # msg['result'] = job.return_value
#
#     return json.dumps(msg)
#


# @app.route('/admin')
# def admin():
#     if g.user is not None:
#         print g.user.user_role
#
#     return render_template('admin.html')

# @app.route('/review/<image_id>')
# def simpleImageView(image_id):
#
#     # we actually don't use the image_id in flask, but angular will
#
#     if g.user is not None:
#         print g.user.user_role
#     return render_template('simpleimageview.html')

#
#
# @app.route('/test')
# def apiTest():
#     if g.user is not None:
#         print g.user.user_role
#     return render_template('apitest.html')




# def row2dict(row):
#     d = {}
#     for column in row.__table__.columns:
#         d[column.name] = getattr(row, column.name)
#
#     return d
#
#
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


@app.route('/segment', methods=['POST'])
def segment():

    import json

    msg = {}
    msg['status'] = 'start'

    if request.method == 'POST':

        import cv2
        import numpy as np
        from numpy import unique, squeeze
        import Image
        import cStringIO
        import re
        import geojson
        from geojson import Polygon, Feature, FeatureCollection

        opdata = json.loads(request.data)

        print opdata


        imgstr = re.search(r'base64,(.*)', opdata['image']).group(1)
        tempimg = cStringIO.StringIO(imgstr.decode('base64'))
        tempimg.seek(0)
        cvimg = cv2.imdecode(np.asarray(bytearray(tempimg.read()), dtype=np.uint8), 1)
        # cv2.imwrite('inputimage.png', cvimg)

        # imgray = cv2.cvtColor(cvimg,cv2.COLOR_BGR2GRAY)
        imgray = cvimg[:,:,2]
        # cv2.imwrite('segment.png', imgray)

        all_cnts = []
        cntdict = {}

        return_data = []

        extent = opdata['extent']
        tr = extent[0]
        bl = extent[1]

        native_width = tr[0] - bl[0]
        native_height = -bl[1] + tr[1]

        x_scale = native_width / imgray.shape[1]
        y_scale = native_height / imgray.shape[0]

        def contourToGeoString(cnt):
            '''convert an opencv contour to a geojson-compatible representation'''

            t_string = []
            for pt in cnt:

                px = np.round(pt[0] * x_scale) + bl[0]
                py = -1*np.round(pt[1] * y_scale) + tr[1]

                t_string.append((float(px), float(py)))

            return t_string

        unique_labels = unique(imgray)

        print 'uniques %s' % (unique_labels)

        # we're going to make an assumption: only consider a single hole in a polygon

        for label in unique_labels:

            working_img = imgray.copy()
            working_img[working_img != label] = 0

            # CV_RETR_CCOMP retrieves all of the contours and organizes them into a two-level
            # hierarchy. At the top level, there are external boundaries of the components.
            # At the second level, there are boundaries of the holes. If there is another contour
            # inside a hole of a connected component, it is still put at the top level.

            contours, hierarchy  = cv2.findContours(working_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

            # hierarchy[i][0] , hiearchy[i][1] , hiearchy[i][2] , and hiearchy[i][3] are set
            # to 0-based indices in contours of the next and previous contours at the same
            # hierarchical level, the first child contour and the parent contour, respectively.
            # If for the contour i there are no next, previous, parent, or nested contours,
            # the corresponding elements of hierarchy[i] will be negative.

            for n, cnt in enumerate(contours):

                hei = hierarchy[0][n]
        #         print hei

                # create an array for this polygon
                if str(label) not in cntdict.keys():
                    cntdict[str(label)] = []

                if hei[3] >= 0:
                    print '%s: %d -> this contour has a parent: %d' % (label, n, hei[3])
                    # this contour has a parent, do not add it directly
                    pass


                elif hei[2] < 0:
                    # this contour has no children, just add it

                    outer_poly = (contourToGeoString(squeeze(cnt)))

        #             x_vals = np.round(ca[:,0] * x_scale) + bl[0]
        #             y_vals = -1*np.round(ca[:,1] * y_scale) + tr[1]

                    print '(add) %s: %d -> this contour (%d) has no children' % (label,n, len(outer_poly))


                    print outer_poly

                    geo = Polygon([outer_poly])
                    feat = Feature(geometry=geo, id=len(all_cnts))
                    feat['properties']['labelindex'] = str(label)


                    cntdict[str(label)].append(feat)
                    all_cnts.append(feat)

                else:
                    # contour's child is at contours[hei[2]]
                    # add this contour and it's child

                    outer_poly = contourToGeoString(squeeze(cnt))
                    inner_poly = contourToGeoString(squeeze(contours[hei[2]]))

                    print '(add) %s: %d -> this contour (%d) has a child: %d (%d)' % (label, n, len(outer_poly), hei[2], len(inner_poly))

                    geo = Polygon([outer_poly, inner_poly])

                    feat = Feature(geometry=geo, id=len(all_cnts))
                    feat['properties']['labelindex'] = str(label)

                    cntdict[str(label)].append(feat)

                    all_cnts.append(feat)


        for c in all_cnts:
            return_data.append(geojson.dumps(c))

        print 'There are %d features to return' % (len(return_data))

        msg['features'] = return_data

    return json.dumps(msg)




#
@app.route('/segmentold', methods=['GET', 'POST'])
def segmentold():

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

        cv2.imwrite('inputimage.png', cvimg)

        imgray = cv2.cvtColor(cvimg,cv2.COLOR_BGR2GRAY)
        imgray = imgray*255

        cv2.imwrite('segment.png', imgray)

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



# @app.route('/upload', methods=['POST'])
# def uploadFile():
#
#     return_arr = []
#
#     print request.files
#
#     for f in request.files:
#         file = request.files[f]
#         print file
#
#         if 'docx' in file.filename:
#
#             import os
#             save_path = '/vagrant/docx_templates/%s' % file.filename
#
#             file.save(save_path)
#             return_arr.append(save_path)
#
#     msg = {}
#     msg['status'] = 'success'
#     msg['result'] = return_arr
#
#     print msg
#
#     import json
#     return json.dumps(msg)


##### Get all users
#
#	/users
#
#If normal user, returns the logged in user
#If admin, returns all users
#
# @app.route('/users', methods=['GET'])
# def userEndPoint():
#
#     if g.user is not None:
#
#         if g.user.user_role == 'admin':
#
#
#             import json
#             result = User.query.all()
#             return_result = []
#
#             for row in result:
#                 dict_row = row2dict(row)
#                 return_result.append(dict_row)
#             return json.dumps(return_result)
#
#         else:
#
#             import json
#             result = User.query.filter_by(id=g.user.id)
#             return_result = []
#
#             for row in result:
#                 dict_row = row2dict(row)
#
#                 dict_row['user_oauth_token'] = 'redacted'
#                 dict_row['user_oauth_secret'] = 'redacted'
#
#                 return_result.append(dict_row)
#
#             return json.dumps(return_result)
#             #return jsonify(return_result)
#
#
#     else:
#
#         return '{}'
#
#
#
# ##### Get a single user description
# #
# #	/user/{user_id}
# #
# #If normal, returns a description of the user if self
# #If admin, returns a description of the user
#
# @app.route('/user/<int:user_index>', methods=['GET'])
# def getUser(user_index):
#
#     # verify logged in
#     if g.user is not None:
#         if request.method == 'GET':
#
#             # get this annotation if it exists, else return empty object
#             result = User.query.filter_by(id=user_index)
#             return_result = []
#
#             for row in result:
#                 dict_row = row2dict(row)
#                 return_result.append(dict_row)
#
#             return json.dumps(return_result)
#
#     return '{}'
#
#
# ##### Get task list for a user
# #
# #	/user/{user_id}/tasks
# #
# #If normal, returns task list if user is self
# #If admin, returns a task list for user
#
# @app.route('/user/<int:user_index>/tasks', methods=['GET'])
# def taskForUser(user_index):
#
#     # verify logged in
#     if g.user is not None:
#         if request.method == 'GET':
#
#             # get this annotation if it exists, else return empty object
#             result = TaskList.query.filter_by(user_id=user_index)
#
#             return_result = []
#             #print result.length
#
#             for row in result:
#                 dict_row = row2dict(row)
#                 return_result.append(dict_row)
#
#             return json.dumps(return_result)
#
#     return '{}'
#
# ##### Get annotation list for a user
# #
# #	/user/{user_id}/annotations
# #
# #If normal, returns annotation list if user is self
# #If admin, returns an annotation list for user
#
# @app.route('/user/<int:user_index>/annotations', methods=['GET'])
# def annotationsForUser(user_index):
#
#     # verify logged in
#     if g.user is not None:
#         if request.method == 'GET':
#
#
#             # get this annotation if it exists, else return empty object
#             result = Annotation.query.filter_by(user_id=user_index)
#
#             return_result = []
#
#             #print result.length
#
#             for row in result:
#                 dict_row = row2dict(row)
#                 return_result.append(dict_row)
#
#             return json.dumps(return_result)
#
#     return '{}'
#
#
#
#
# ##### Get all images
# #
# #	/images
# #
# #Returns a list of all images
#
# @app.route('/images', methods=['GET'])
# def allImagesEndPoint():
#
#     # verify logged in
#     if g.user is not None:
#
#         import json
#         result = Image.query.order_by(Image.id)
#
#         return_result = []
#         for row in result:
#             dict_row = row2dict(row)
#             contents = json.loads(dict_row['mskcc_details'])
#
#             # add some additional information to keep the db's in line
#             contents['DA_id'] = dict_row['id']
#             contents['DA_key'] = dict_row['mskcc_key']
#
#             return_result.append(contents)
#         return json.dumps(return_result)
#
#
#     return '{}'
#
#
#
#
#


#
#
#
#
# @app.route('/image/<int:image_index>', methods=['GET'])
# def getSingleImage(image_index):
#
#     if g.user is not None:
#
#         import json
#         result = Image.query.order_by(Image.id).filter_by(id=image_index)
#         return_result = []
#         for row in result:
#             dict_row = row2dict(row)
#             contents = json.loads(dict_row['mskcc_details'])
#
#             # add some additional information to keep the db's in line
#             contents['DA_id'] = dict_row['id']
#             contents['DA_key'] = dict_row['mskcc_key']
#
#             return_result.append(contents)
#         return json.dumps(return_result)
#
#     else:
#
#         return '{}'
#
#
# @app.route('/mskccimage/<key>', methods=['GET'])
# def getSingleImageByMSKCC(key):
#
#     if g.user is not None:
#
#         import json
#         result = Image.query.order_by(Image.id).filter_by(mskcc_key=key)
#         return_result = []
#         for row in result:
#             dict_row = row2dict(row)
#             contents = json.loads(dict_row['mskcc_details'])
#
#             # add some additional information to keep the db's in line
#             contents['DA_id'] = dict_row['id']
#             contents['DA_key'] = dict_row['mskcc_key']
#
#             return_result.append(contents)
#         return json.dumps(return_result)
#
#     else:
#
#         return '{}'
#
#
#
# ##### Get all annotations for an image
# #
# #	/image/{image_id}/annotations
# #
# #If normal user, returns annotations created by the user
# #If admin, returns all annotations for an image
#
# @app.route('/image/<int:image_index>/annotation', methods=['GET'])
# def annotationForImageEndPoint(image_index):
#
#     # verify logged in
#     if g.user is not None:
#         if request.method == 'GET':
#
#             print 'attempting to load annotation for image', image_index, g.user.id
#
#             # get this annotation if it exists, else return empty object
#             result = Annotation.query.filter_by(image_id=image_index).filter_by(user_id=g.user.id).first()
#
#             if result:
#                 # should be a single row
#                 result_dict = row2dict(result)
#                 return json.dumps(result_dict)
#
#             else:
#
#                 result_dict = {}
#                 result_dict['status'] = 'not found'
#                 return json.dumps(result_dict)
#
#
#     return '{}'
#
#
#
# #### Get all annotations
# #
# #	/annotations
# #
# #If normal user, returns annotations for all images created by user
# #If admin, returns all annotations for all images
#
# @app.route('/annotations', methods=['GET'])
# def allAnnotations():
#
#         # verify logged in
#     if g.user is not None:
#
#         import json
#         result = Annotation.query.all()
#         return_result = []
#         for row in result:
#             dict_row = row2dict(row)
#             #contents = { int(dict_row['id']) : json .loads(dict_row['details']) }
#
#
#             return_result.append(dict_row)
#         return json.dumps(return_result)
#
#     else:
#         return '{}'
#
#
# ##### Get single annotation
# #
# #	/annotation/{annotation_id}
# #
# #If normal user, returns annotation if created by user
# #If admin, returns annotation
#
# @app.route('/annotation/<int:annotation_index>', methods=['GET', 'POST', 'DELETE'])
# def annotationEndPoint(annotation_index):
#
#     # verify logged in
#     if g.user is not None:
#         if request.method == 'GET':
#             # get this annotation if it exists, else return empty object
#             result = Annotation.query.filter_by(id=annotation_index).first()
#
#             if result:
#                 # should be a single row
#                 result_dict = row2dict(result)
#                 return json.dumps(result_dict)
#
#
#
#     return '{}'
#
#




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
#Returns a json response.
@app.route('/annotation/', methods=['POST'])
def annotationCreateEndPoint():

    # verify logged in
    if g.user is not None:

        response_dict = {}

        if request.method == 'POST':

            json_data = json.loads(request.data)

            # print json_data

            image_data = json_data['image']
            image_from_db = image_collection.find_one({'record_id': image_data['record_id']})

            if image_from_db:

                # create an annotation

                annotation = {}

                annotation['image_record_id'] = image_data['record_id']
                annotation['user_id'] = json_data['user_id']
                annotation['annotation'] = json_data['annotation']

                annotation_id = annotation_collection.insert(annotation)

                if 'annotation' not in image_from_db.keys():
                    image_from_db['annotation'] = []

                # print 'annotations:'
                # print image_from_db['annotation']

                # downcast to string otherwise we won't be able to grab it via our API
                image_from_db['annotation'].append(str(annotation_id))

                image_collection.save(image_from_db)



                response_dict['status'] = 'Annotation saved successfully'

            else:

                response_dict['stauts'] = "Database error, could not save annotation"

        else:

            response_dict['status'] = 'Invalid method'

        return json.dumps(response_dict)

    else:
        return '{}'



##### Get a subset of images
#
#	/images/{start}/{count}
#
# Returns a subset ({count}) of images, starting at {start}

@app.route('/images/<int:start_index>/<int:count>/', methods=['GET'])
def imageEndPoint(start_index, count):

    if g.user is not None:
        import json

        # result = image_collection.find({}, {'_id': False}, limit=count, skip=start_index).sort("Study_num", 1)
        query = {"study_id": { "$regex" : ".*uda.*" }}
        filter = {'_id': False}


        result = image_collection.find(query, filter, limit=count, skip=start_index).sort("Study_num", 1)


        # {"study_id" : {$regex : ".*uda.*"}}).count()

        return json.dumps(list(result))

    else:

        return '{}'

##### Get a subset of images
#
#	/images/{start}/{count}
#
# Returns a subset ({count}) of images, starting at {start}
@app.route('/fill', methods=['GET', 'POST'])
def fill():

    msg = {}
    msg['status'] = 'start'

    if request.method == 'GET':
        pass
    elif request.method == 'POST':

        # result = fillImage.delay(json.loads(request.data))

        result = fillImage2(json.loads(request.data))

        msg['result'] = result

    return json.dumps(msg)




@app.before_request
def before_request():

    # print session

    g.user = None
    if 'id' in session:
        g.user = user_collection.find_one({'id' : session['id']})

        # g.user = User.query.get(session['id'])

    # print 'user:'
    # print g.user


@app.after_request
def after_request(response):


    # db_session.remove()


    return response




@app.route('/review')
def review():

    result = add.delay(4, 1)

    # if g.user is not None:
    #     print g.user
    return render_template('review.html')


@app.route('/details')
def details():

    # if g.user is not None:
    #     print g.user
    return render_template('details.html')



@app.route('/')
def index():

    # result = add.delay(4, 4)

    # if g.user is not None:
    #     print g.user

    return render_template('index-rev4.html')


@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/guest')
def loginAsGuest():

    g.user = user_collection.find_one({'id': '007'})

    session['id'] = str(g.user['id'])

    return redirect(request.referrer or url_for('index'))


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

    user_data['last_oauth'] = resp['access_token']
    user_data['last_secret'] = resp['id_token']

    # print user_data
    #
    user = user_collection.find_one({'email': user_data['email']})

    # user = User.query.filter_by(user_email=user_data['email']).first()

    # if it's their first time, add them to the database
    if user is None:

        print 'no user found in mongo'

        user = user_collection.insert(user_data)
        # user = User(user_data['email'])
        # db_session.add(user)

        # print user
    #
    # now set their most recent auth values
    # user.oauth_token = resp['access_token']
    # user.oauth_secret = resp['id_token']

    # db_session.commit()

    # finally set, their user id as a session variable (this is the primary key in the users DB)
    # it is used to resolve the user prior to each request (wow this app is DB read heavy)
    session['id'] = str(user['id'])

    # print 'saving session id as %s' % session['id']

    flash('You were signed in')

    return redirect(next_url)





def main():

    app.debug = True

    app.run()


if __name__ == '__main__':
    main()
