"""
Storage interface
"""

import time
import datetime
import couchdb.client
import json
from models import User,Board,Pin,Counttrack
from bottle import request


class Storage(object):
    def __init__(self):
        # initialize our storage, data is a placeholder
        self.data = {}
        # for demo
        self.data['created'] = time.ctime()


    def start_server(self):
        """
        The method is used to initialize the database instances and make them accessable elsewhere
        """
        global couch
        couch = couchdb.Server()  # Assuming localhost:5984
        global userdb
        if couch.__contains__('mydb'):
            userdb = couch['mydb']
        else:
            userdb = couch.create('mydb')

        global boarddb
        if couch.__contains__('boarddb'):
            boarddb = couch['boarddb']
        else:
            boarddb = couch.create('boarddb')

        global pindb
        if couch.__contains__('pindb'):
            pindb = couch['pindb']
        else:
            boarddb = couch.create('pindb')

        global countdb
        if couch.__contains__('counttrack'):
            countdb = couch['counttrack']
        else:
            countdb = couch.create('counttrack')
        #usercount = countdb['user']

        """
            Initialize the meta data count if it does not exist
        """
        user = "user"
        board = "board"
        pin = "pin"
        if not user in countdb:
            print "user doc does not exist"
            userdoc = {'entity':user, 'count':0}
            countdb[user]=userdoc
        usercount=countdb[user]
        if not board in countdb:
            print "board doc does not exist"
            boarddoc = {'entity':board, 'count':0}
            countdb[board]=boarddoc
        boardcount=countdb[board]
        if not pin in countdb:
            print "pin count does not exists"
            userdoc = {'entity':pin, 'count':0}
            countdb[pin]=userdoc
        pincount=countdb[pin]

    def get_next_id(self, entity):
        countobj = Counttrack.load(countdb,entity)
        if not(countobj is None):
            return countobj.count+1
        else:
            return 0


    def get_all_boards(self):
        """
        Returns a list of all boards
        """
        allboards=[]
        try:
            for bid in boarddb:
                singleboard = {}
                singleboard['board_id']=boarddb[bid].get('_id')
                singleboard['board_name']=boarddb[bid].get('board_name')
                allboards.append(singleboard)
            return allboards
        except:
            return  False

    def get_all_pins(self):
        """
        Returns a List of All Pins
        """
        allpins=[]
        try:
            for pid in pindb:
                singlepin={}
                singlepin['pin_id']=pindb[pid].get('_id')
                singlepin['pin_name']=pindb[pid].get('pin_name')
                singlepin['pin_url']=request.urlparts.scheme+"://"+request.urlparts.netloc+"/"+pindb[pid].get('pin_url')
                allpins.append(singlepin)
            return allpins
        except:
            return False

    def get_user_info(self,user_id):
        """
        Returns the user info of a particular user possessing user_id
        """
        result={}
        multipleboards=[]
        try:
            if user_id in userdb:
                for bid in boarddb:
                    if boarddb[bid].get("user_id")==user_id:
                        singleboard={}
                        singleboard['board_id']=boarddb[bid].get('_id')
                        singleboard['board_name']=boarddb[bid].get('board_name')
                        multipleboards.append(singleboard)
                result['boards']=multipleboards
                result['name']=userdb[user_id].get('name')
                return result
            else:
                return False
        except:
            return False



    def get_board(self,board_id):
        """
        Returns All the pins in a particular board with board_id
        """
        try:
            board=Board.load(boarddb,board_id)
            result={}
            result['board_id']=board_id
            result['board_name']=board.board_name
            pins=[]
            for pin_item in board.pins:
                pin2=Pin.load(pindb,pin_item.pin_id)
                pin={}
                pin['pin_id']=pin_item.pin_id
                pin['pin_name']=pin2.pin_name
                pin['pin_url']=request.urlparts.scheme+"://"+request.urlparts.netloc+"/"+pin2.pin_url
                pins.append(pin)
            result['pins']=pins
            return result
        except:
            return False


    def get_pin(self,pin_id):
      """
        Returns Pin item with information of user id,pin id, pin name, pin url and comments
      """
      try:
         pin=Pin.load(pindb,pin_id)
         pin_item={}
         pin_item['pin_id']=pin_id
         pin_item['pin_name']=pin.pin_name
         pin_item['pin_url']=request.urlparts.scheme+"://"+request.urlparts.netloc+"/"+pin.pin_url
         comments=[]
         for comments_item in pin.comments:
             comment={}
             comment['user_id']=comments_item.user_id
             comment['comment']=comments_item.comment
             comments.append(comment)
         pin_item['comments']=comments
         return pin_item
      except:
          return False

    def fetch_pin(self,pin_id):
      """
      Returns a pin corresponding to a particular pin_id
      """
      try:
         pin=Pin.load(pindb,pin_id)
         return pin
      except:
          return "error:pin does not exist"

    def save_comment(self, pin,user_id):
        """
        This method saves a comments
        """
        if user_id in userdb:
            try:
                pin.store(pindb)
                return "Comment Added"
            except:
                return False
        else:
            return False


    def insert_registration(self, user):
        """
        This method returns user_id on successful registration or False on unsuccessful attempt
        """
        try:
            user_id= self.get_next_id("user")
            #check if user already exists
            for iad in userdb:
                print "user.username",user.username
                if (userdb[iad].get('username') == user.username):
                    return False

            #store new user
            newuser = {'name': user.name, 'username':user.username, 'password':user.password}
            userdb[str(user_id)]=newuser

            #update user count
            usercount = Counttrack.load(countdb,"user")
            usercount.count=user_id
            usercount.store(countdb)

            return user_id
        except:
            return False

    def checklogin(self, username, password):
        """
        This method returns user_id on successful login or returns False on unsuccessful attempt
        """
        for iad in userdb:
            if (userdb[iad].get('username') == username) and (userdb[iad].get('password') == password):
                return userdb[iad].id
        return False

    def create_pin(self,pin):
        """
        This method returns pin_id on successful pin creation and returns False on unsuccessful attempt
        """
        if pin.user_id in userdb:
            try:
               #store the new pin
               pin_id = self.get_next_id("pin")
               newpin = {"pin_name":pin.pin_name, "user_id":pin.user_id, "pin_url":pin.pin_url, "comments":[]}
               pindb[str(pin_id)] = newpin
               #increment pin count in metadata
               pincount = Counttrack.load(countdb,"pin")
               pincount.count=pin_id
               pincount.store(countdb)
               return str(pin_id)
            except:
                return False
        else:
             return False



    def create_board(self,board):
        """
        This method returns board_id on successful board creation and returns False on unsuccessful attempt
        """
        if board.user_id in userdb:
            try:
               board_id = self.get_next_id("board")
               newboard = {"board_name":board.board_name, "user_id":board.user_id, "pins":[], "board_type":"public"}
               boarddb[str(board_id)] = newboard

               #increment board count in metadata
               boardcount = Counttrack.load(countdb,"board")
               boardcount.count=board_id
               boardcount.store(countdb)
               return str(board_id)
            except:
                return False
        else:
            return False

    def delete_board(self,user_id,board_id):
        if user_id in userdb:
            try:
                #board=Board.load(userdb,board_id)
                board = boarddb[board_id]
                if(board is not None and board['user_id']== user_id):
                    boarddb.delete(boarddb[board_id])
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def attach_pin(self,user_id,pin_id,board_id):
        """
        This method returns "pin Attached" on successful operation and False on unsuccessful attempts.
        This method attaches a particular pin with pin_id to a board with board_id
        """
        if board_id in boarddb and user_id in userdb:
            try:
                board=Board.load(boarddb,board_id)
                if board['user_id']==user_id:
                    board.pins.append(pin_id=pin_id)
                    board.store(boarddb)
                    return "Pin Attached"
                else:
                    return False
            except:
                return False
        else:
            return False
