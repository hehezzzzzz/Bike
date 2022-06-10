import socket
import json
import UdpComms as U
import tempfile
import sys
import argparse
import threading
import time
import tkinter as tk
import subprocess
import functools
import signal

sys.path.append("../")
import PoseModule as PM

# TODO: I WILL CLEAN THIS UP!!!!!!
master = tk.Tk()
master.title("Freeride Controls")
master.resizable(0,0)

# lb1 = Label(master, text = "Run Controller Setup")
# lb2 = Label(master, text = "Start receiver")
# lc1 = Label(master, text = "Run Controller")
# lc2 = Label(master, text = "Run Pose")

# lb1.grid(row = 0, column = 0, sticky = W, pady = 2)
# lb2.grid(row = 1, column = 0, sticky = W, pady = 2)
# lc1.grid(row = 2, column = 0, sticky = W, pady = 2)
# lc2.grid(row = 3, column = 0, sticky = W, pady = 2)
c1Val = tk.IntVar()
c2Val = tk.IntVar()

c1 = tk.Checkbutton(master, text = "Run Controller", variable = c1Val)
c1.grid(row = 1, column = 0, sticky = tk.W)
c2 = tk.Checkbutton(master, text = "Run Pose", variable = c2Val)
c2.grid(row = 1, column = 1, sticky = tk.W)
# b1 = tk.Button(master, text = "Install controller", command = launch_init)
# b1.grid(row = 0, column = 0, sticky = tk.W+tk.E, columnspan = 2, pady=20)
# b2 = tk.Button(master, text = "Start receiver", command = lambda c=c1.get(), p=c2.get() : start_transmission(c, p))
# b2.grid(row = 2, column = 0, sticky = tk.W+tk.E, columnspan = 2)
def handler(sig, f):
    if (sig == signal.SIGINT):
        master.destroy()
        exit(1)

def launch_init():
    print("init")
    try:
        subprocess.call([r'.\first_time_setup.bat'])
    except subprocess.CalledProcessError as e:
        print(e)

def start_transmission():
    #signal.signal(signal.SIGINT, handler)
    cont = c1Val.get()
    pose = c2Val.get()
    print("hello")
    print(cont)
    print(pose)
    if (pose or cont):
        master.deiconify()
        sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True) # communication with Unity
        if pose:
            print("hi")
            t1 = threading.Thread(target=PM.main, daemon=True)
            t1.start()
        if cont:
            temp_dir = tempfile.gettempdir()
            try:
                with open(temp_dir + '/freeride_setup/mymac.txt', 'r') as file:
                    filedata = file.read()
            except OSError as e:
                print("MAC address file not found. Have you run the first time setup script?")
                time.sleep(5)
                master.destroy()
                exit()
            file.close()
            serv = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) # bluetooth connection to raspberry PI
            server_address = filedata.strip() # change this to your computer's bluetooth MAC address
            port = 5
            serv.bind((server_address, port))
            serv.settimeout(0.1)
            print("Awaiting controller connection...")
            serv.listen()
            prev_pose_data = 0
            while True:
                try:
                    client, addr = serv.accept()
                    while True:
                        bt_data = client.recv(3, socket.MSG_WAITALL) # ensure that entire output from IMU script is received
                        if not bt_data: break 
                        from_bt_string = bt_data.decode()

                        pose_data = sock.ReadReceivedData()
                        if pose_data != None:
                            prev_pose_data = pose_data

                        output_obj = {
                            "bt_data": int(bt_data),
                            "pose_data": int(prev_pose_data)
                        }

                        output_obj_str = json.dumps(output_obj)
                        sock.SendData(output_obj_str)
                        print(output_obj_str)

                        bt_data = None
                except socket.timeout as e:
                    continue
                except socket.error as e:
                    err = e.args[0]
                    print(e)
                    master.destroy()
                    exit(1)
                client.close()
                print('client disconnected')
                master.deiconify()
                break

# def callback():
#     start_transmission(c1Val.get(), c2Val.get())   
b1 = tk.Button(master, text = "Install controller", command = launch_init)
b1.grid(row = 0, column = 0, sticky = tk.W+tk.E, columnspan = 2, pady=20)
b2 = tk.Button(master, text = "Start receiver", command = start_transmission)
b2.grid(row = 2, column = 0, sticky = tk.W+tk.E, columnspan = 2)
# def launchpose(pose):
#     if pose:
#         t1 = threading.Thread(target=PM.main, daemon=True)
#         t1.start()

# def launchcontroller(cont):
#     if cont:
#         temp_dir = tempfile.gettempdir()
#         try:
#             with open(temp_dir + '/freeride_setup/mymac.txt', 'r') as file:
#                 filedata = file.read()
#         except OSError as e:
#             print("MAC address file not found. Have you run the first time setup script?")
#             exit()
#         print("Your bluetooth MAC address is: " + filedata)
#         file.close()
#         serv = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) # bluetooth connection to raspberry PI
#         server_address = filedata.strip() # change this to your computer's bluetooth MAC address
#         port = 5

#         # Initialization to add RFCOMM protocol to endpoint
#         serv = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) # bluetooth connection to raspberry PI
#         sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True) # communication with Unity
#         end_cv_sock = U.UdpComms(udpIP="127.0.0.1", portTX=8003, portRX=8004, enableRX=False, suppressWarnings=True) # communication with pose detection script
#         serv.bind((server_address, port))
#         serv.settimeout(0.1)
#         print("Awaiting controller connection...")
#         serv.listen()
#         prev_time = 0
#         prev_pose_data = 0
#         while True:
#             try:
#                 client, addr = serv.accept()
#                 while True:
#                     bt_data = client.recv(3, socket.MSG_WAITALL) # ensure that entire output from IMU script is received
#                     if not bt_data: break 
#                     from_bt_string = bt_data.decode()

#                     pose_data = sock.ReadReceivedData()
#                     if pose_data != None:
#                         prev_pose_data = pose_data

#                     output_obj = {
#                         "bt_data": int(bt_data),
#                         "pose_data": int(prev_pose_data)
#                     }

#                     output_obj_str = json.dumps(output_obj)
#                     sock.SendData(output_obj_str)
#                     print(output_obj_str)

#                     bt_data = None
#             except socket.timeout as e:
#                 err = e.args[0]
#                 print(e)
#                 continue
#             except socket.error as e:
#                 err = e.args[0]
#                 print(e)
#                 exit(1)


def main():
    # c1 = tk.Checkbutton(master, text = "Run Controller")
    # c1.grid(row = 1, column = 0, sticky = tk.W)
    # c2 = tk.Checkbutton(master, text = "Run Pose")
    # c2.grid(row = 1, column = 1, sticky = tk.W)
    # b1 = tk.Button(master, text = "Install controller", command = launch_init)
    # b1.grid(row = 0, column = 0, sticky = tk.W+tk.E, columnspan = 2, pady=20)
    # b2 = tk.Button(master, text = "Start receiver", command = lambda : callback)
    # b2.grid(row = 2, column = 0, sticky = tk.W+tk.E, columnspan = 2)
    signal.signal(signal.SIGINT, handler)
    tk.mainloop()




        # while True:
        #     bt_data = client.recv(3, socket.MSG_WAITALL) # ensure that entire output from IMU script is received
        #     if not bt_data: break 
        #     from_bt_string = bt_data.decode()

        #     pose_data = sock.ReadReceivedData()
        #     if pose_data != None:
        #         prev_pose_data = pose_data

        #     output_obj = {
        #         "bt_data": int(bt_data),
        #         "pose_data": int(prev_pose_data)
        #     }

        #     output_obj_str = json.dumps(output_obj)
        #     sock.SendData(output_obj_str)
        #     print(output_obj_str)

        #     bt_data = None
        #client.close()
        #print('client disconnected')
        #break







# parser = argparse.ArgumentParser(description='Launch without pose module')
# parser.add_argument('--poseoff', action='store_true')
# parser.add_argument('-controlleroff', action='store_true')

# args = vars(parser.parse_args())
# temp_dir = tempfile.gettempdir()
# try:
#     with open(temp_dir + '/freeride_setup/mymac.txt', 'r') as file:
#         filedata = file.read()
# except OSError as e:
#     print("MAC address file not found. Have you run the first time setup script?")
#     exit()

# # t1 = threading.Thread(target=PM.main, daemon=True)
# # t1.start()

# print("Your bluetooth MAC address is: " + filedata)
# file.close()

# server_address = filedata.strip() # change this to your computer's bluetooth MAC address
# port = 5

# # Initialization to add RFCOMM protocol to endpoint
# serv = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) # bluetooth connection to raspberry PI
# sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True) # communication with Unity
# end_cv_sock = U.UdpComms(udpIP="127.0.0.1", portTX=8003, portRX=8004, enableRX=False, suppressWarnings=True) # communication with pose detection script

# # Start pose detection script
# if not (args['poseoff']):
#     t1 = threading.Thread(target=PM.main, daemon=True)
#     t1.start()

# # Assigns a port for the server that listens to clients connecting to this port
# serv.bind((server_address, port))
# serv.settimeout(0.1)
# print("Awaiting controller connection...")
# serv.listen()
# prev_time = 0
# prev_pose_data = 0
# while True:
#     try:
#         client, addr = serv.accept()
#         while True:
#             bt_data = client.recv(3, socket.MSG_WAITALL) # ensure that entire output from IMU script is received
#             if not bt_data: break 
#             from_bt_string = bt_data.decode()

#             pose_data = sock.ReadReceivedData()
#             if pose_data != None:
#                 prev_pose_data = pose_data

#             output_obj = {
#                 "bt_data": int(bt_data),
#                 "pose_data": int(prev_pose_data)
#             }

#             output_obj_str = json.dumps(output_obj)
#             sock.SendData(output_obj_str)
#             print(output_obj_str)

#             bt_data = None
#     except socket.timeout as e:
#         err = e.args[0]
#         print(e)
#         continue
#     except socket.error as e:
#         err = e.args[0]
#         print(e)
#         exit(1)

#     # while True:
#     #     bt_data = client.recv(3, socket.MSG_WAITALL) # ensure that entire output from IMU script is received
#     #     if not bt_data: break 
#     #     from_bt_string = bt_data.decode()

#     #     pose_data = sock.ReadReceivedData()
#     #     if pose_data != None:
#     #         prev_pose_data = pose_data

#     #     output_obj = {
#     #         "bt_data": int(bt_data),
#     #         "pose_data": int(prev_pose_data)
#     #     }

#     #     output_obj_str = json.dumps(output_obj)
#     #     sock.SendData(output_obj_str)
#     #     print(output_obj_str)

#     #     bt_data = None
#     #client.close()
#     print('client disconnected')
#     break

if __name__ == "__main__":
	main()