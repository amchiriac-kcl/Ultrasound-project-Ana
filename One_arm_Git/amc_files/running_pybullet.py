import pybullet as p
import pybullet_data
import time
from pathlib import Path

# Connect to physics server (GUI for visualization)
p.connect(p.GUI)

# Set search path to find built-in URDFs (optional but useful)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load a plane (optional ground)


# Load your URDF file
script_dir = Path(__file__).resolve().parent # The directory of this script
urdf_path = script_dir.parent / "Housden created STL and URDF 5/RightArm.urdf"
robot_id = p.loadURDF(str(urdf_path), basePosition=[0, 0, 1])


 # Coord frames for base and each link
for i in range(-1, p.getNumJoints(robot_id)):
    if i == -1:
        pos, orn = p.getBasePositionAndOrientation(robot_id)
    else:
        pos, orn = p.getLinkState(robot_id, i)[:2]

    p.addUserDebugLine(pos, [pos[0]+0.1, pos[1], pos[2]], [1,0,0], 2)  # X (red)
    p.addUserDebugLine(pos, [pos[0], pos[1]+0.1, pos[2]], [0,1,0], 2)  # Y (green)
    p.addUserDebugLine(pos, [pos[0], pos[1], pos[2]+0.1], [0,0,1], 2)  # Z (blue)

#label links
num_joints = p.getNumJoints(robot_id)

# Base link (-1)
base_pos, _ = p.getBasePositionAndOrientation(robot_id)
p.addUserDebugText(
    "Link: base",
    base_pos,
    textColorRGB=[1, 1, 1],
    textSize=1.2
)

# All child links
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    link_name = info[12].decode("utf-8")  # link name

    link_state = p.getLinkState(robot_id, i)
    pos = link_state[0]  # world position of link frame

    p.addUserDebugText(
        f"Link: {link_name}",
        pos,
        textColorRGB=[1, 1, 0],
        textSize=1.2
    )

# Sliders for camera control
pos, _ = p.getBasePositionAndOrientation(robot_id)

yaw = p.addUserDebugParameter("Yaw", -180, 180, 50)
pitch = p.addUserDebugParameter("Pitch", -89, 0, -30)
dist = p.addUserDebugParameter("Distance", 0.1, 5, 1.5)

#Run simulation with camera control
for _ in range(100000):
    y = p.readUserDebugParameter(yaw)
    pch = p.readUserDebugParameter(pitch)
    d = p.readUserDebugParameter(dist)

    pos, _ = p.getBasePositionAndOrientation(robot_id)

    p.resetDebugVisualizerCamera(d, y, pch, pos)

    p.stepSimulation()
    time.sleep(1/240)

p.disconnect()