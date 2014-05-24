
import urllib,requests

host=raw_input("Enter Host:")
port=int((raw_input("Enter Port:")))

while(True):

    print "1.Register\n","2.Login\n","3.Create Board\n","4.Get Board\n","5.Get All Boards\n","6.Upload Pin\n","7.Get Pin\n","8.Get All Pins\n","9.Attach Pin\n","10.Get User Info\n","11.Add Comment\n","12.Delete Board\n"
    choice= int(raw_input("Enter your Choice"))

    if choice==1:
        username=raw_input("Enter your username")
        name=raw_input("Enter your name:")
        password=raw_input("Enter password:")
        url ='http://'+str(host)+':'+str(port)+'/v1/reg'
        print url
        data = {'username': username,
                'name':name,
                'password':password
                }
        #print username
        result = requests.post(url,data)
        print result.text

    elif choice==2:
        username=raw_input("Enter your username")
        password=raw_input("Enter password:")
        url = 'http://'+str(host)+':'+str(port)+'/v1/login'
        data = {
            'username': username,
            'password':password
            }
        result=requests.post(url,data)
        print result.text

    elif choice==3:
        user_id=raw_input("Enter your user_id")
        boardname=raw_input("Enter Board Name:")
        url = 'http://'+str(host)+':'+str(port)+'/v1/user/'+user_id+'/board'
        data = {
            'user_id': user_id,
            'boardname':boardname
             }
        result=requests.post(url,data)
        print result.text

    elif choice==4:
        board_id=raw_input("Enter your board_id")
        url = 'http://'+str(host)+':'+str(port)+'/v1/boards/'+ board_id
        result = requests.get(url)
        print result.text

    elif choice==5:
        url = 'http://'+str(host)+':'+str(port)+'/v1/boards'
        result = requests.get(url)
        print result.text
        print "5"

    elif choice==6:
        user_id=raw_input("Enter your user_id")
        name=raw_input("Enter tack Name:")
        tack=raw_input("Enter url of image:")
        print tack
        url='http://'+str(host)+':'+str(port)+'/v1/user/'+user_id+'/pin'
        #url = 'http://localhost:8000/v1/user/1/pin'
        path=tack
        files = {
                 'tack': (open(tack,'rb'))
            }
        data={'name':name}
        result=requests.post(url,files=files,data=data)
        print result.text
        print 6
    elif choice==7:
        pin_id=raw_input("Enter your pin_id")
        url = 'http://'+str(host)+':'+str(port)+'/v1/pin/'+ pin_id
        result = requests.get(url)
        print result.text
    elif choice==8:
        url = 'http://'+str(host)+':'+str(port)+'/v1/pins'
        result=requests.get(url)
        print result.text
    elif choice==9:
        user_id=raw_input("Enter user_id :")
        board_id=raw_input("Enter Board _id")
        pin_id=raw_input("Enter pin_id:")
        url = 'http://'+str(host)+':'+str(port)+'/v1/user/'+user_id+'/board/'+board_id
        data={
        'pin_id':pin_id
        }
        result=requests.put(url,data)
        print result.text
    elif choice==10:
        user_id=raw_input("Enter your user_id")
        url = 'http://'+str(host)+':'+str(port)+'/v1/user/'+ user_id
        result = requests.get(url)
        print result.text
    elif choice==11:
        user_id=raw_input("Enter user_id :")
        pin_id=raw_input("Enter pin_id:")
        comment=raw_input("Enter Comment:")
        url = 'http://'+str(host)+':'+str(port)+'/v1/user/'+user_id+'/pin/'+pin_id
        data={
            'comment':comment
        }
        result = requests.post(url, data)
        print result.text
    elif choice==12:
        user_id=raw_input("Enter user_id :")
        board_id=raw_input("Enter Board _id")
        url = 'http://'+str(host)+':'+str(port)+'/v1/user/'+user_id+'/boards/'+board_id
        result = requests.delete(url)
        print result.text
    else:
        print "Select correct option"

