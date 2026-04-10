import pybullet as p
import pybullet_data
import time
from pathlib import Path

# Connect to physics server (GUI for visualization)
p.connect(p.GUI)

# Set search path to find built-in URDFs (optional but useful)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load a plane (optional ground)
#plane_id = p.loadURDF("plane.urdf")

# Load your URDF file
script_dir = Path(__file__).resolve().parent # The directory of this script
urdf_path = script_dir.parent / "Housden created STL and URDF 5/RightArm.urdf"
robot_id = p.loadURDF(str(urdf_path), basePosition=[0, 0, 1])


# Run simulation
for _ in range(10000):
    p.stepSimulation()
    time.sleep(1/240)

p.disconnect()