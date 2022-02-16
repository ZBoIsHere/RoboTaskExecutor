#!/usr/bin/python
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import flowinstance
import navitask
import taskstatus
import json
import robotcommander
import actionlib
import rospy
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
import rosgraph
import time

PORT_NUMBER = 8080

class taskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write('success access task executor\n'.encode())
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        rospy.logerr("POST request,\nPath: %s\nHeaders:\n%s\n",
                     str(self.path), str(self.headers))

        if 'roboflow' in self.path:
            rfi = flowinstance.json2FlowInstance(post_data.decode('utf8'))
            rospy.logerr("Start execute flow %s instance id %s", rfi.flow_name, rfi.flow_instance_id)
            flow = threading.Thread(target=flowExecutor, args=[rfi])
            flow.start()
        elif 'navitask' in self.path:
            np1 = navitask.json2MessageDomain(post_data.decode('utf8'))
            task = threading.Thread(target=naviTaskExecutor, args=[np1])
            task.start()
        else:
            np1 = navitask.json2MessageDomain(post_data.decode('utf8'))
            task = threading.Thread(target=naviTaskExecutor, args=[np1])
            task.start()

        ret = navitask.MessageSendResultDomain()
        ret.robot_id = 'robotidtodoadd'
        ret.status = taskstatus.SendSuccess
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(ret, default=lambda obj: obj.__dict__).encode())

def naviTaskExecutor(np):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = np.message.header.frame_id
    #goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = np.message.pose.pose.position.x
    goal.target_pose.pose.position.y = np.message.pose.pose.position.y
    goal.target_pose.pose.position.z = np.message.pose.pose.position.z
    goal.target_pose.pose.orientation.x = np.message.pose.pose.orientation.x
    goal.target_pose.pose.orientation.y = np.message.pose.pose.orientation.y
    goal.target_pose.pose.orientation.z = np.message.pose.pose.orientation.z
    goal.target_pose.pose.orientation.w = np.message.pose.pose.orientation.w

    client.send_goal(goal)

    state = client.wait_for_result()
    if state == actionlib.SimpleGoalState.PENDING:
        rospy.logerr("Action server not avil")
        rospy.signal_shutdown("Action server not avilable")
    else:
        ret = client.get_state()
        rospy.logwarn('task done : %s', ret.__str__())

def naviPointExecutor(task):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = task['frame_id']
    #goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = task['pose']['x']
    goal.target_pose.pose.position.y = task['pose']['y']
    goal.target_pose.pose.position.z = task['pose']['z']
    goal.target_pose.pose.orientation.x = task['orientation']['x']
    goal.target_pose.pose.orientation.y = task['orientation']['y']
    goal.target_pose.pose.orientation.z = task['orientation']['z']
    goal.target_pose.pose.orientation.w = task['orientation']['w']

    client.send_goal(goal)

    state = client.wait_for_result()
    if state == actionlib.SimpleGoalState.PENDING:
        rospy.logerr("Action server not avil")
        rospy.signal_shutdown("Action server not avilable")
    return state

def gaitSwitchExecutor(task):
    if task['target_gait']:
        robotcommander.robot_commander.sendSimple(25)
        return 'True'
    return 'False'

def flowExecutor(fi):
    rospy.logerr("Start execute flow %s task num %d", fi.flow_name, len(fi.task_instances))
    for i, v in enumerate(fi.task_instances):
        rospy.logerr("Start execute flow %s task index %d task info %s", fi.flow_name, i, v.info)
        if v.type == 'navi_point':
            state = naviPointExecutor(v.info['goal'])
            rospy.logerr("Execute flow %s task index %d task result %s", fi.flow_name, i, state)
        if v.type == 'gait_switch':
            gaitSwitchExecutor(v.info)
            rospy.logerr("Execute flow %s task index %d task result %s", fi.flow_name, i, state)

try:
    while True:
        if rosgraph.is_master_online():
            rospy.init_node('robo_task_executor')
            server = HTTPServer(('', PORT_NUMBER), taskHandler)
            rospy.logerr('Started task executor on port %d', PORT_NUMBER)
            server.serve_forever()
        else:
            rospy.logwarn('ROS MASTER is offline')
            time.sleep(5)

except KeyboardInterrupt:
    rospy.logerr('^C received, shutting down the web server')
    server.socket.close()