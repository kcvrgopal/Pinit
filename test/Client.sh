#!/bin/bash

echo "Enter the host"
read host
echo "Enter Port"
read port
c="y"
while [ "$c" == "y" ]
do
printf " 1.Register\n 2.Login\n 3.Create Board\n 4.Get Board\n 5.Get All Boards\n 6.Upload Pin\n 7.Get Pin\n 8.Get All Pins\n 9.Attach Pin\n 10.Get User Info\n 11.Add Comment\n 12.Delete Board\n"

read val
case "$val" in

1)  echo "username"
    read username
    echo "name"
    read name
    echo "password"
    read password
    u="http://$host:$port/v1/reg"
curl -i -H "Accept: application/json" -H "Content-type:application/json" -d '
{"username":"'"${username}"'","name":"'"${name}"'","password":"'"${password}"'"}'  "${u}"
    ;;
2)  echo "username"
    read username
    echo "password"
    read password
    u="http://$host:$port/v1/login"
curl -i -H "Accept: application/json" -H "Content-type:application/json" -d '
{"username":"'"${username}"'","password":"'"${password}"'"}'  "${u}"    
    ;;
3)  echo "userid"
    read userid
    echo "boardname"
    read boardname
    u="http://$host:$port/v1/user/$userid/board"
curl -i -H "Accept: application/json" -H "Content-type:application/json" -d '
{"boardname":"'"${boardname}"'"}'  "${u}"
    ;;
4)  echo "boardid"
    read boardid
    u="http://$host:$port/v1/boards/$boardid"
    curl -i -H "Content-type:application/json" "${u}"
    ;;
5)  u="http://$host:$port/v1/boards"
    curl -i -H "Content-type:application/json" "${u}"
    ;;
6)  echo "Enter tack name"
    read name
    echo "Enter tack url"
    read address
echo "Enter userid"
read user_id
    tack="@\"$address\""
    echo $tack
u="http://$host:$port/v1/user/$user_id/pin"
curl -i -F name="$name" -F tack="$tack" "${u}"
    ;;
7)  echo "pinid"
    read pinid
    u="http://$host:$port/v1/pin/$pinid"
    curl -i -H "Content-type:application/json" "${u}"
    ;;
8)  u="http://$host:$port/v1/pins"
    curl -i -H "Content-type:application/json" "${u}"
    ;;
9)  echo "userid"
    read userid
    echo "boardid"
    read boardid
    echo "pinid"
    read pin_id
	echo "$pin_id"
    u="http://$host:$port/v1/user/$userid/board/$boardid"
curl -i -H "Content-type:application/json" -X PUT -d '{"pin_id":"'"${pin_id}"'"}' "${u}"

    ;;
10) echo "userid"
    read userid 
    u="http://$host:$port/v1/user/$userid"
    curl -i -H "Content-type:application/json" "${u}"
   ;;
11)  echo "userid"
    read userid
    echo "pinid"
    read pinid
    echo "comment"
    read comment
    u="http://$host:$port/v1/user/$userid/pin/$pinid"
curl -i -H "Accept: application/json" -H "Content-type:application/json" -d '{"comment":"'"${comment}"'"}'  "${u}"
    ;;
12)  echo "userid"
    read userid
    echo "boardid"
    read boardid
    u="http://$host:$port/v1/user/$userid/boards/$boardid"
curl -i -H "Content-type:application/json" -X DELETE "${u}"
    ;;
*) echo "Try again"
   ;;
esac
printf "\nDo you want to continue?" 
read c
echo $c
done

