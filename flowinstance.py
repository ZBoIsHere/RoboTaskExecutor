import json

class RoboFlowInstance:
    def __init__(self, flow_id = 'flow_id', flow_name = 'flow_name', flow_instance_id = 'flow_instance_id', robot_id = 'robot_id'):
        self.flow_id = flow_id
        self.flow_name = flow_name
        self.flow_instance_id = flow_instance_id
        self.robot_id = robot_id
        self.task_instances = []

class RoboTaskInstance:
    def __init__(self, task_id = 'task_id', task_name = 'task_name', task_instance_id = 'task_instance_id', type = 'type', info = 'info'):
        self.task_id = task_id
        self.task_name = task_name
        self.task_instance_id = task_instance_id
        self.type = type
        self.info = info

def json2FlowInstance(rfiJson):
    rfiMap = json.loads(rfiJson)
    rfi = RoboFlowInstance()
    rfi.flow_id = rfiMap['flow_id']
    rfi.flow_name = rfiMap['flow_name']
    rfi.flow_instance_id = rfiMap['flow_instance_id']
    rfi.robot_id = rfiMap['robot_id']
    for rtiMap in rfiMap['robotaskinstances']:
        rti = RoboTaskInstance()
        rti.task_id = rtiMap['task_id']
        rti.task_name = rtiMap['task_name']
        rti.task_instance_id = rtiMap['task_instance_id']
        rti.type = rtiMap['type']
        rti.info = json.loads(rtiMap['info'])
        rfi.task_instances.append(rti)
    return rfi
