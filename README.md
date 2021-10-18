# ROS-programming

requirement: python2

-RPLidar
ls /dev/tty* #search tty* 
catkin_make
source devel/setup.bash 
sudo chmod 666 /dev/ttyUSB*  #authorization
roslaunch rplidar_ros rplidar.launch 

-check
rostopic list
rostopic echo [/topic_name]
rqt_graph

-rviz
fixed name → laser
add→ by topic → laser scan 
laserscan → size → 0.07

https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=thumbdown&logNo=220385363246


-general way of creating package
catkin_create_package [pack_name]
cd  [pack_name]
mkdir scripts
cd scripts
gedit [file_name]  #file create
code #visual studio
'''
#! urs/bin/evn python  #neccessary to add before coding python in ros
import rospy
'''
chmod +x [file_name]  #authorization
cd ~/catkin_ws
catkin_make 

-rosrun
roscore
new tap
source devel/setup.bash  #setup
rosrun [pack_name] [file_name]


-linux serial
use python2 
sudo chmod 777 /dev/ttyUSB*
ser = serial.Serial('/dev/ttyUSB0', 115200)

-usb_cam
sudo apt install v4l-utils 를 통해 몇가지 카메라 관련 Ubuntu Package를 설치하시면 usb_cam을 활용하는데 더 큰 도움이 됩니다.
v4l2-ctl : v4l-utils의 가장 핵심이며 많이 사용하는 명령어입니다.
v4l2-ctl –list –device : 현재 연결되어 있는 모든 카메라를 index와 함께 출력해줍니다.
v4l2-ctl –list-formats : 현재 연결된 카메라의 출력 포맷을 출력해줍니다.

-ROS download using git
https://github.com/jetsonhacks/installROSXavier

-Linux IP connection
1. ip check
sudo apt get ifconfig
ifconfig

2. wifi setting
‘’’
address(pc_IP): 192.168.0.112 
netmask: 24 //or 255.255.255.0
gateway(router IP): 192.168.0.1
‘’’
sudo nano ~/.bashrc //or gedit ~/.bashrc
‘’’
112PC에서:
export ROS_MASTER_URI=http://192.168.1.112:11311   //마스터 IP
export ROS_IP=192.168.0.112     //현재pc IP 입력
111PC에서:
export ROS_MASTER_URI=http://192.168.1.112:11311   //마스터 IP
export ROS_IP=192.168.0.111     //현재pc IP 입력
‘’’
source ~/.bashrc     // or terminate terminal and reopen

3. ssh 
-112에서 111원격 제어
112: ssh wego@192.168.0.111
wego 비밀번호 입력 //wego는 111 PC이름
-111에서 112 원격 제어
111: ssh nvidia@192.168.0.112
nvidia 비밀번호 // nvidia는 112 PC이름

-Linux velodyne IP connection
Linux - settings - Network - IPv4 - Manual - wireshark(check destination: 192.168.1.100 source: 192.168.1.201) - (IP: 192.168.1.100 subnet mask: 255.255.255.0) - 192.168.1.201 웹 접속 (host:  192.168.1.100 sensor: 192.168.1.201)

