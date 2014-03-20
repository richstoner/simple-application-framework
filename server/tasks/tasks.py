from celery import Celery

import cv2
import urllib
import numpy as np
import json
import Image
import cStringIO
import re


c = Celery('tasks', backend='amqp', broker='amqp://')

class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)

@c.task(name='tasks.add')
def add(x, y):
    print 'hello task'
    return x + y


@c.task(name='tasks.fillImage')
def fillImage(params):

#todo implement a smart url-based hashing cache

    # loading image from url into memory, first as np array then opencv image
    req = urllib.urlopen(params['image']['url'])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr,-1) # 'load it as it is'

    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    lo = int(params['tolerance'])
    hi = int(params['tolerance'])
    connectivity = 4
    flags = connectivity
    flags |= cv2.FLOODFILL_FIXED_RANGE

    seed_pt = (int(params['click']['relative'][0] * w), int(params['click']['relative'][1] * h))

    print 'seed', seed_pt

    cv2.floodFill(img, mask, seed_pt, (255,190,00), (lo,lo,lo), (hi,hi,hi), flags)
    contours = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    class NumPyArangeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist() # or map(int, obj)
            return json.JSONEncoder.default(self, obj)

    # print len(contours[0][0])

    outer = json.dumps(contours[0][0], cls=NumPyArangeEncoder)
    # inner = json.dumps(contours[0][1], cls=NumPyArangeEncoder)

    del img, mask

    return_msg = {}
    return_msg['contour'] = {
        'outer' : outer
        # 'inner' : inner
    }

    # the points are now relative to the subimage we've obtained them from
    # so we need to scale it back up

    # divide subimage actual by what it is natively
    inverse_rel_width = w / float(params['image']['region']['size'][0])
    inverse_rel_height = h / float(params['image']['region']['size'][1])

    # inverse_rel_height = 1
    # inverse_rel_width = 1


    offset_x = params['image']['region']['origin'][0]
    offset_y = params['image']['region']['origin'][1]

    xform = {
        'scale' : [inverse_rel_width, inverse_rel_height],
        'offset' : [offset_x, offset_y]
        }

    # print xform
    # print w,h, opdata['image']['region']['size']

    return_msg['xform'] = json.dumps(xform)


    # json_data =

    # print json_data

    # job = q.enqueue(createFormRQ, json_data)

    # import time
    # while job.return_value is None:
    #     time.sleep(0.5)


    # msg['job'] = job.id
    # msg['result'] = job.return_value

    return return_msg




@c.task
def segmentImage(input_parameters):
    """ This function takes an input URL, seed point, and tolerance and produces a pointlist of the outer most contour
    """


    msg = {}
    msg['status'] = 'start'

    if request.method == 'GET':
        print 'get test'

    elif request.method == 'POST':
        # import pprint
        # pprint.pprint(json.loads(request.data))

        opdata = json.loads(request.data)


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



        print len(contours[0][0])

        contour_string = json.dumps(cnt_list, cls=NumPyArangeEncoder)

        print contour_string

        msg['contourstr'] = contour_string


    return json.dumps(msg)

