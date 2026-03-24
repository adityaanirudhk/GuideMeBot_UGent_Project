# GuideMeBot-Group3


Our project aims to develop an autonomous indoor Help Robot capable of guiding students (international, for example) or visitors around an indoor university building. For our project, we will focus on the ground floor of the iGent building, or a portion of this floor if the space is too large for WiFi signals to convey. The robot will interact through computer input to determine the destination, and then speak during navigation, with a microphone connected to a laptop resting on top of the TurtleBot. To choose a destination to go to, the user will press an input key corresponding to the desired location, with the computer displaying all possible locations and their respective keys. The robot will autonomously navigate to the chosen location, such as a specific classroom. Using ROS 2 navigation and localization packages, the TurtleBot will plan and execute safe paths, avoiding obstacles such as people or furniture. Obstacle avoidance will take place during navigation so that the robot will not run into anything that moves into its path, nor any obstacle pre-set in the environment. The robot will also communicate politely, confirming destinations before moving, and provide vocal feedback upon arrival. The robot will engage in small talk to ensure that the subject is following the robot’s navigation. This project demonstrates autonomous localization, navigation, obstacle avoidance, and human-robot social interaction.

## Features

- **Destination Selection**: Using a GUI
- **Autonomous Navigation**: Nav2-based path planning with obstacle avoidance
- **Conversational Interface**: Engaging small talk during navigation using LLM (OpenAI via DialogFlow)
- **Human Following Verification**: Monitors user responses to ensure they are following

## Hardware Requirements

- TurtleBot4 with Raspberry Pi
- RPLIDAR for static and dynamic obstacle detection and avoidance
- Laptop mounted on TurtleBot (for user interface and processing)

## Software Requirements

- Ubuntu 22.04
- ROS2 Humble
- Nav2 Navigation Stack
- Google Cloud Dialogflow (for conversation management)
- Whisper.cpp (for local speech recognition)
- Python 3.10+

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download Whisper model (required for speech recognition)
chmod +x download_whisper_model.sh
./download_whisper_model.sh
```

### 2. Build the Package

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select guide_me_bot
source install/setup.bash
```

### 3. Create and Save Your Map

```bash
# Start SLAM
ros2 launch turtlebot4_navigation slam.launch.py

# Save the map when done
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name:
  data: 'map_name'"
```

### 4. Configure Destinations

Edit `config/destinations.yaml` with your building's destinations.

### 5. Launch the Help Robot
If the map or the nav2 files are not given, the default map and params are used.

```bash
ros2 launch guide_me_bot guide_me_bot.launch.py map:=/path/to/your/map.yaml params_file:=/path/to/your/nav2.yaml
```

### Start the Navigation GUI

You can start the navigation GUI either via the provided launch file (recommended) or by starting the required nodes manually.

- Option A — start the full system (recommended):

```bash
ros2 launch guide_me_bot guide_me_bot.launch.py map:=/path/to/your/map.yaml
```

- Option B — start nodes separately (useful for debugging):

```bash
# start localization (map -> AMCL)
ros2 launch turtlebot4_navigation localization.launch.py map:=/path/to/your/map.yaml

# start Nav2 (planner, controller, recovery, etc.)
ros2 launch turtlebot4_navigation nav2.launch.py params_file:=/path/to/your/nav2.yaml

# optionally launch RViz view
ros2 launch turtlebot4_viz view_robot.launch.py

# run the GUI node
ros2 run guide_me_bot gui_navigator
```
The following is how the GUI would look:
<img width="1272" height="677" alt="image" src="https://github.com/user-attachments/assets/1932f4de-bf73-4cef-a4b0-6a232b99f579" />


RViz: use the `2D Pose Estimate` (or `Publish Pose`) tool to set the AMCL initial pose interactively.

Note about initial pose sources
- The GUI will (by default) publish a one-shot `/initialpose` using the `dock_pose` or `start_position` values from `config/destinations.yaml` shortly after startup. If you prefer to set the initial pose from RViz, you have two choices:
  - Start the GUI and then publish the `/initialpose` from RViz after the GUI's automatic publish happens — the last message on `/initialpose` wins, so your RViz pose will override the GUI's.
  - Edit or disable the GUI's delayed initial-pose publish in `guide_me_bot/gui_navigator.py` (the code schedules `_publish_initial_pose` after a short delay) so that only RViz provides the initial pose.

## Usage

Quick interactive usage (GUI):

- Select a destination from the GUI list (click an entry). 
- Click **START JOURNEY** to undock (if necessary) and begin navigation to the selected destination.
- Click **HALT** to cancel the current goal. Click **RETURN TO DOCK** to start the docking sequence.


Behavior notes:
- When docking, the GUI first navigates to a safe approach/staging pose offset from the dock, then calls the `Dock` action only when the dock becomes visible (to avoid driving onto the dock blindly).
- The robot will hold a conversation during navigation. If the user stops responding, the robot will return to the start/dock as configured.

## Connection to robot via Ethernet
We could not get this dual connection working properly, so do not necessarily expect these steps to work.

# i) TurtleBot4 + Internet (Windows 11 + WSL2 + ROS 2 Humble)
This setup keeps ROS 2 communication on a dedicated Ethernet link to the TurtleBot4 while keeping your laptop on eduroam for full internet access.[web:285]  
It also uses a Fast DDS Discovery Server so ROS 2 discovery works reliably from WSL2 without relying on multicast.[web:273]

# Windows 11: set the laptop Ethernet IPv4 manually
The TurtleBot4 Raspberry Pi Ethernet interface uses a static IP `192.168.185.3`, so your laptop Ethernet must be on the same `192.168.185.0/24` subnet.[web:285]  
On Windows 11, set the Ethernet adapter IPv4 to **Manual** and choose an address that is not `192.168.185.3` (example: `192.168.185.10`) with subnet mask `255.255.255.0`.[web:285]  
Leave the Ethernet **default gateway blank** so your internet continues to route via eduroam Wi‑Fi.[web:232]

# ii) Test connectivity (WSL2)

After plugging the Ethernet cable from your laptop to the TurtleBot4 Ethernet port, confirm you can reach the robot at `192.168.185.3`.[web:285]  
From WSL2:
`ping -c 3 192.168.185.3`
`ssh ubuntu@192.168.185.3`
SSH to `ubuntu@192.168.185.3` is the expected TurtleBot4 Ethernet access method.[web:298][web:285]

# iii) Configure ROS 2 discovery (Fast DDS)
Start a Fast DDS Discovery Server on the TurtleBot4 (server side).[web:273]  
`fastdds discovery -i 0`

On both a new the TurtleBot4 terminal **and** a WSL2 terminal, point ROS 2 to the discovery server using the TurtleBot4 Ethernet IP and the default discovery port (`11811`).[web:273][web:279]  
`export ROS_DISCOVERY_SERVER=192.168.185.3:11811`

This tells ROS 2 nodes to discover each other via the server instead of multicast.[web:273][web:279]


## Project Structure

```
guide_me_bot/
├── config/                  # Configuration files
├── dialogflow/              # Webhook setup
├── docs/                    # Documentation
├── guide_me_bot/            # nodes
├── launch/                  # Launch files
├── maps/                    # map files
└── README.md
```

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Usage Instructions](docs/USAGE.md)
- [LLM](docs/LLM.md)
- [Presentation](https://docs.google.com/presentation/d/1uv6pHERbWaDNXfGuaby_s6oUn21R8dKU9kio4Rsm-FA/edit?usp=sharing)

## License

MIT License
