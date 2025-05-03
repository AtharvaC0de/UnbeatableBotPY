# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from supremacy import helpers

# This is your team name
CREATOR = "ATHARVA_BOT"
#TankAngle=0.0


def tank_ai(tank, info, game_map):
    """
    Function to control tanks.
    """
#    global TankAngle
#    tank.set_heading(TankAngle)
#    TankAngle += 1.0
#    if TankAngle > 360.0:
#        TankAngle = 0.0
    if not tank.stopped:
        if (tank.get_distance(tank.owner.x, tank.owner.y) > 80) or tank.stuck:
            tank.stop()
        elif "target" in info:
            tank.goto(*info["target"])


def ship_ai(ship, info, game_map):
    """
    Function to control ships.
    """
    if not ship.stopped:
        if (ship.get_distance(ship.owner.x, ship.owner.y) > 140):
            ship.set_heading(np.random.random() * 360.0)
        if ship.stuck:
            if ship.get_distance(ship.owner.x, ship.owner.y) > 40:
                if len(info["bases"]) < 12:
                    ship.convert_to_base()
            else:
                ship.set_heading(np.random.random() * 360.0)


def jet_ai(jet, info, game_map):
    """
    Function to control jets.
    """
    if "target" in info:
        jet.goto(*info["target"])


class PlayerAi:
    """
    This is the AI bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.build_queue = helpers.BuildQueue(
            ["mine", "tank","ship", "tank", "ship" ,"jet", "mine", "tank", "ship", "jet", "jet"], cycle=True
        
        )
        self.TankAngle = 0.0  # Angle for tank movement

    def run(self, t: float, dt: float, info: dict, game_map: np.ndarray):
        """
         This is the main function that will be called by the game engine.
        """

        # Get information about my team
        myinfo = info[self.team]

        # Iterate through all my bases and process build queue
        for base in myinfo["bases"]:
            # Calling the build_queue will return the object that was built by the base.
            # It will return None if the base did not have enough resources to build.
            if base.mines == 3:
                self.build_queue = helpers.BuildQueue(
                ["mine", "ship", "tank","tank","tank","tank","tank","jet", "tank", "ship", "tank","tank","tank","tank","tank", "tank", "jet", "tank", "ship", "jet", "tank", "ship", "jet", "tank", "ship", "jet", "tank", "ship", "jet", "tank", "ship", "jet", "tank", "ship", "jet"], cycle=True)

            obj = self.build_queue(base)
            if (obj is not None) and (obj.kind == 'tank'):
                obj.set_heading(self.TankAngle)
                self.TankAngle += 10.0
                if self.TankAngle > 360.0:
                    self.TankAngle = 0.0

        # Try to find an enemy target
        # If there are multiple teams in the info, find the first team that is not mine
        if len(info) > 1:
            for name in info:
                if name != self.team:
                    # Target only bases
                    if "bases" in info[name]:
                        # Simply target the first base
                        t = info[name]["bases"][0]
                        myinfo["target"] = [t.x, t.y]
                        break

        # Control all my vehicles
        helpers.control_vehicles(
            info=myinfo, game_map=game_map, tank=tank_ai, ship=ship_ai, jet=jet_ai
        )
