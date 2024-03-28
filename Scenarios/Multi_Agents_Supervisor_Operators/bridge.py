


import numpy as np
import math
import random
import socket
import json

#from bluerov2_bridge.bluerov_node import BlueRov

class MobileCommonInterface:
    
    def move_to(self, coordinates):
        pass

    def get_position(self):
        pass

    def get_battery(self):
        pass

    def reset_battery(self):
        pass

class UXVSimpleSimImplementation(MobileCommonInterface):
    """
        This class was created to build the bridge between functions/algorithms used to control 
        Bluerov2 and the Deep Reinforcement Learning script that makes decisions. Use this class
        to have a simplified version without ArduSub simulation.
    """

    def __init__(self):
       self.x = 0
       self.y = 0 
        

    def get_pos(self):
        #print("simple get pose  : ",self.x,self.y)
        return self.x,self.y
   
    def set_pos(self,new_pose):
        #print("simple set pose  : ", new_pose)
        self.x = new_pose[0]
        self.y = new_pose[1]
    def get_info(self) :  
        return "Je suis une implémentation simple"
    
class Bluerov2RealImplementation(MobileCommonInterface):
    
    """
        This class was created to build the bridge between functions/algorithms used to control 
        Bluerov2 and the Deep Reinforcement Learning script that makes decisions. Use this class 
        if you are using ArduSub and Unity.
    """

    def __init__(self,port_n):

        self.current_position = np.zeros(3)

        self.ip_port = 14550 + port_n
        n_bluerov = port_n
        self.bluerov = BlueRov(device='udp:localhost:'+str(self.ip_port),nbr_bluerov=n_bluerov)
        print(self.ip_port)

    def move_to(self, coordinates):
        #print("Bluerov2RealImplementation move_to: ",coordinates)
        
        goal = [coordinates[0] * 10, coordinates[1] * 10, -20 ]
        self.bluerov.do_rali(goal)

        curren_pos  = self.bluerov.get_position()
        self.current_position[0], self.current_position[1] = curren_pos[0], curren_pos[1]
       


    def get_pos(self):
        return self.bluerov.get_position()
    
    def set_pos(self,new_pose):
        #print("Bluerov2RealImplementation set_pos: ",new_pose[0],new_pose[1])
        self.move_to(new_pose)

        
    def get_info(self) :  
        return "Je suis une implémentation real"




class UnitySimImplementation(MobileCommonInterface):
    def __init__(self) :
        self.x = 0
        self.y = 0
        self.port = 20000 + 1
        self.ip_adress = 'localhost'

    def get_position(self):
        #self.x,self,y = robot.get_position()
        return self.x,self.y
    

    
    def set_pos(self, new_pose):
    
        self.x = new_pose[0]
        self.y = new_pose[1]

        data = {"x": self.x , "y": 0, "z": self.y, "pitch": 0, "yaw": 0, "roll": 0}

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            server_address = (self.ip_adress, self.port)
            client_socket.connect(server_address)
            json_data = json.dumps(data)
            client_socket.sendall(json_data.encode())


    def get_info(self) :  
        return "I'm an instance of UnitySim Implementation"





class UXV:
    def __init__(self, implementation="simple",ip_port=0):
        """
            implementation : choose if you use Bluerov2 or not ("bluerov2" or "simple")
        """
        if implementation == "simple":
            self.implementation = UXVSimpleSimImplementation()
        elif implementation == "real":
            print("in uxv real")
            self.implementation = Bluerov2RealImplementation(ip_port)
        elif implementation == "unity" : 
            self.implementation = UnitySimImplementation()
        else : 
            raise ValueError("Incorrect implementation value. Choose 'bluerov2' or 'simple'.")

    def get_pos(self):
        #print("UXV get_pos ")
        return self.implementation.get_pos()
     
    def set_pos(self,new_pose):
        #print("UXV set_pos : " , new_pose[0],new_pose[1])
        return self.implementation.set_pos(new_pose)
    def get_info(self) : 
        return self.implementation.get_info()