import json

class MessageDomain:
    def __init__(self, robot_id = 'robot_id', type = 'control', command = 0):
        self.robot_id = robot_id
        self.type = type
        self.command = command
        self.message = MessageEntityDomain()

class MessageEntityDomain:
    def __init__(self):
        self.pose = PoseDomain()
        self.header = HeaderDomain()

class HeaderDomain:
    def __init__(self, frame_id = 'map'):
        self.stamp = StampDomain()
        self.frame_id = frame_id

class StampDomain:
    def __init__(self, sec = 0, nanosec = 0):
        self.sec = sec
        self.nanosec = nanosec

class PoseDomain:
    def __init__(self):
        self.pose = PoseEntityDomain()

class PoseEntityDomain:
    def __init__(self):
        self.position = PositionDomain()
        self.orientation = OrientationDomain()

class PositionDomain:
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z

class OrientationDomain:
    def __init__(self, x = 0.0, y = 0.0, z = 0.0, w = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

class MessageSendResultDomain:
    #def __init__(self, message_id = 'message_id', robot_id = 'robot_id', status = 'success'):
        #self.message_id = message_id
    def __init__(self, robot_id = 'robot_id', status = 'success'):
        self.robot_id = robot_id
        self.status = status

def json2MessageDomain(md):
    map = json.loads(md)
    np = MessageDomain()
    np.robot_id = map['robot_id']
    np.type = map['type']
    #np.command = map['command']
    np.message.header.stamp.sec = map['message']['header']['stamp']['sec']
    np.message.header.stamp.nanosec = map['message']['header']['stamp']['nanosec']
    np.message.header.frame_id = map['message']['header']['frame_id']
    np.message.pose.pose.position.x = map['message']['pose']['pose']['position']['x']
    np.message.pose.pose.position.y = map['message']['pose']['pose']['position']['y']
    np.message.pose.pose.position.z = map['message']['pose']['pose']['position']['z']
    np.message.pose.pose.orientation.x = map['message']['pose']['pose']['orientation']['x']
    np.message.pose.pose.orientation.y = map['message']['pose']['pose']['orientation']['y']
    np.message.pose.pose.orientation.z = map['message']['pose']['pose']['orientation']['z']
    np.message.pose.pose.orientation.w = map['message']['pose']['pose']['orientation']['w']
    return np
