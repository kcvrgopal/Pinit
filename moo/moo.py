
import json
import os
import time
import socket
from data.storage import Storage
from data.models import User,Board,Pin
# bottle framework
from bottle import request, response, route, error, static_file

# moo
from classroom import Room
# virtual classroom implementation
room = None
# Global Database variable
global db
db=Storage()

#
def setup(base,conf_fn):
   print '\n**** service initialization ****\n'
   global room
   room = Room(base,conf_fn)

@error(404)
def error404(error):
    """
    This method returns 'Nothing here, sorry' when there is any error in the URL
    """
    return 'Nothing here, sorry'

@route('/v1/reg',method='POST')
def register_user():
    """
    This method registers a user with the data provided and returns corresponding response
    """
    fmt=__format(request)
    if request.content_type=="application/json":
        username=request.json['username']
        name=request.json['name']
        password=request.json['password']
    else:
        username = request.forms.get("username")
        name = request.forms.get("name")
        password = request.forms.get("password")
    user = User(name=name, username=username, password=password)
    result = db.insert_registration(user)
    if result:
        response._status_line= "201 Created"
        response_to_user={"status": response._status_line, "success":True, "message":"Created","user_id":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line= "500 Internal Server Error"
        response_to_user={"status": response._status_line,"success":False,"message":"Could Not Process Request!!!"}
        return format_checker(response_to_user,fmt)


@route('/v1/login',method='POST')
def login_user():
    """
    This method Logs a user in with the data provided and returns corresponding response
    """
    fmt=__format(request)
    if request.content_type=="application/json":
        username=request.json["username"]
        password=request.json["password"]
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
    login_result = db.checklogin(username,password)

    if login_result:
        response_to_user={"status":response._status_line,"success":True,"user_id":login_result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="401 Unauthorized"
        response_to_user={"status":response._status_line,"message":login_result}
        return format_checker(response_to_user,fmt)

@route('/v1/user/:user_id/board',method='POST')
def create_board(user_id):
    """
    This method Creates a board with the user_id provided and returns corresponding response
    """
    fmt=__format(request)
    if request.content_type=="application/json":
        board_name=request.json['boardname']
    else:
        board_name=request.POST.get('boardname')
    board=Board(user_id=user_id,board_name=board_name)
    result=db.create_board(board)
    if result:
        response._status_line="201 Created"
        response_to_user={"status":response._status_line,"success":True,"board_id":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="401 Unauthorized"
        response_to_user={"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)

@route('/v1/user/:user_id/boards/:board_id',method='DELETE')
def delete_board(user_id,board_id):
    """
    This method Deletes a board with the user_id and board_id provided and returns corresponding response
    """
    fmt=__format(request)
    result = db.delete_board(user_id,board_id)
    if result:
        response._status_line= "200 OK"
        response_to_user={"status":response._status_line,"success":result,"message": "Resource Deleted Successfully"}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="401 Unauthorized "
        response_to_user= {"status":response._status_line,"success":result,"message":"Unauthorized"}
        return format_checker(response_to_user,fmt)


@route('/v1/boards', method='GET')
def get_all_boards():
    """
    This method returns all the boards
    """
    fmt=__format(request)
    result=db.get_all_boards()
    if result:
        response_to_user={"status":response._status_line,"success":True,"boards":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="500 Internal Server Error"
        response_to_user={"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)

@route('/v1/boards/:board_id', method='GET')
def get_board(board_id):
    """
    This method returns a board with the particular board_id
    """
    fmt=__format(request)
    result=db.get_board(board_id)
    if result:
        response_to_user= {"status":response._status_line,"success":True,"board":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="500 Internal Server Error"
        response_to_user= {"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)

@route('/v1/user/:user_id/pin',method='POST')
def create_pin(user_id):
    """
    This method Creates a pin with the user_id provided and returns corresponding response
    """
    fmt=__format(request)
    user_id=user_id;
    pin_name=request.POST.get('name')
    upload = request.files.get('tack')
    #save_path = "./static"
    save_path = "images"
    name,ext = os.path.splitext(upload.filename)
    upload.filename=name+"_"+str(int(time.time()))+ext
    upload.save(save_path)
    pin_url= save_path+"/"+upload.filename
    pin=Pin(user_id=user_id,pin_name=pin_name,pin_url=pin_url)
    result=db.create_pin(pin)
    if result:
        response._status_line="201 Created"
        response_to_user={"status":response._status_line,"success":True,"pin_id":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="401 Unauthorized"
        response_to_user={"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)



@route('/v1/user/:user_id/board/:board_id',method='PUT')
def attach_pin(user_id,board_id):
    """
    This method attaches a pin to a board with the user_id, pin_id and board_id provided
    and returns corresponding response
    """
    fmt=__format(request)
    pin_id=request.POST.get('pin_id')
    result=db.attach_pin(user_id,pin_id,board_id)
    if result:
        response._status_line="200 OK"
        response_to_user={"status":response._status_line,"success":True,"message":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="401 Unauthorized"
        response_to_user={"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)


@route('/v1/pins',method='GET')
def get_all_pins():
    """
    This method returns all pins
    """
    fmt=__format(request)
    result=db.get_all_pins()
    if result:
        response_to_user={"status":response._status_line,"success":True,"pins":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="500 Internal Server Error"
        response_to_user= {"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)


@route('/v1/pin/:pin_id',method='GET')
def get_pin(pin_id):
    """
    This method returns a board with the pin_id provided
    """
    fmt=__format(request)
    result = db.get_pin(pin_id)
    if result:
        response_to_user= {"status":response._status_line,"success":True,"pin":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="500 Internal Server Error"
        response_to_user={"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)


@route('/v1/user/:user_id/pin/:pin_id',method='POST')
def add_comment(user_id,pin_id):
    """
    This method creates a comment with the data provided and returns corresponding response
    """
    fmt=__format(request)
    pin=db.fetch_pin(pin_id)
    if request.content_type=="application/json":
        comment= request.json['comment']
    else:
        comment=request.POST.get('comment')
    pin.comments.append(user_id=user_id, comment=comment)
    result=db.save_comment(pin,user_id)
    if result:
        response_to_user= {"status":response._status_line,"success":True,"message":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="500 Internal Server Error"
        response_to_user= {"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)



@route('/v1/user/:user_id',method='GET')
def get_user_info(user_id):
    """
    This method the information of the user with the user_id provided
    """
    fmt=__format(request)
    result=db.get_user_info(user_id)
    if result:
        response_to_user= {"status":response._status_line,"success":True,"message":result}
        return format_checker(response_to_user,fmt)
    else:
        response._status_line="500 Internal Server Error"
        response_to_user= {"status":response._status_line,"success":False}
        return format_checker(response_to_user,fmt)


# setup the configuration for our service
@route('/')
def root():
   return 'welcome  to Pin It!!!'

#
#

#
# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
def __format(request):
   types = request.headers.get("Accept",'')
   subtypes = types.split(",")
   for st in subtypes:
      sst = st.split(';')
      if sst[0] == "text/html":
         return "html"
      elif sst[0] == "text/plain":
         return "text"
      elif sst[0] == "application/json":
         return "json"
      elif sst[0] == "application/xml":
         return "xml"
      elif sst[0] == "*/*":
         return "json"

   # default
   return "json"


@route('/images/<filepath:path>')
def server_static(filepath):
    """
    This method  returns the image
    """
    return static_file(filepath, root='images')


def format_checker(message,format):
    """
    This method returns the respective format requested by the client
    """
    if format == "html" :
        return '<html><body>'+convert_to_text(message)+'</body></html>'
    elif format == "xml":
        return convert_to_xml(message)
    elif format == "text":
        return convert_to_text(message)
    else:
        return message


def convert_to_xml(json_obj, line_padding=""):
    """
    This method converts json to xml
    """
    result_list = list()
    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(convert_to_xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(convert_to_xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)

def convert_to_text(json_obj, line_padding=""):
    """
    This method converts json to plain text
    """
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(convert_to_text(sub_elem,"\t"+ line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s %s :" % ("\n"+line_padding, tag_name))
            result_list.append(convert_to_text(sub_obj,line_padding))

        return "".join(result_list)

    return "%s%s" % (line_padding, json_obj)