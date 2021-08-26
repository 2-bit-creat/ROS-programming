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
