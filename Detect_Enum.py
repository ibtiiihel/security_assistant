#########hostEnumeration.py

import os
import platform
import subprocess
from tqdm import tqdm

def ping(host):
    if platform.system().lower() == "windows":
        response = subprocess.run(['ping', '-n', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        response = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return response.stdout

def scan_network(ip_range , progress_callback=None):
    active_machines = []
    total_machines = 55
    with tqdm(total=total_machines, desc="Scanning network", unit="host") as pbar:
        for i in range(1, total_machines):
            target_ip = f"{ip_range}.{i}"
            if "1 received" in ping(target_ip):
                active_machines.append(target_ip)
            pbar.update(1)
            if progress_callback:
                progress_callback(int((i / total_machines) * 100)) 
    return active_machines
  
if __name__ == "__main__":
    network = "192.168.234"  # Change this to your network's IP range

    active_machines = scan_network(network)

    if active_machines:
        print("Active machines on the network:")
        for machine in active_machines:
            print(machine)
    else:
        print("No active machines found on the network.")

######osDetection.py

from scapy.all import IP, ICMP, sr1

def send_icmp_packet(target_ip):
    # Create an ICMP Echo Request packet
    packet = IP(dst=target_ip) / ICMP()

    # Send the packet and receive a response
    response = sr1(packet, timeout=2, verbose=False)

    # Print the response details
    if response:
        response.show()
        return response
    else :
        return None

def detect_os(dest_ip):
    # Send ICMP Echo Request
    response = send_icmp_packet(dest_ip)
    if response is None:
        return f"No response received from {dest_ip}"

    # Receive ICMP Echo Reply
    ttl = response[IP].ttl

    # Analyze the TTL value to make an educated guess about the OS
    if ttl is not None:
        if ttl <= 64:
            return f"The host {dest_ip} is likely running a Unix-like operating system."
        elif ttl > 64:
            return f"The host {dest_ip} is likely running a Windows operating system."
        else:
            return f"OS detection for {dest_ip} failed."
    else:
        return f"Failed to receive ICMP reply from {dest_ip}"
if __name__ == "__main__":
    target_ip = "192.168.48.54"  # Replace with the target IP address
    detect_os(target_ip)
 
########portsEnumeration.py

import socket
from tqdm import tqdm

def check_port_status(host, port):
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(2)
      s.connect((host,port))
      return "open"
  except ConnectionRefusedError:
    return 'closed'
  except socket.timeout:
    return 'filtered'

def scan_ports(host):
  start_port = 79
  end_port = 8080
  open_ports = []
  print(f"scanning ports on {host} from {start_port} to {end_port} ...")
  with tqdm(total=end_port-start_port, desc="Scanning ports", unit="port") as pbar:
    for port in range(start_port, end_port+1):
      status = check_port_status(host, port)
      if status == 'open' or status == "filtered":
        open_ports.append([port,status])
      pbar.update(1)
  return open_ports

if __name__ == "__main__":
  host = "192.168.234.6"
  open_ports = scan_ports(host)
  if open_ports:
    print("Open ports on the machine:")
    for port,status in open_ports:
      print(f"Port {port} : {status}")
  else:
    print("No open ports found on this machine.")


#####################################Scan.py
import subprocess

def identify_services(host):
  
    try:

        scan_result = subprocess.run(['C:\\Program Files (x86)\\Nmap\\nmap.exe', '-sV', host], capture_output=True, text=True, check=True)
        
        # Parsing the output to extract service information
        services = {}
        for line in scan_result.stdout.split('\n'):
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                port = parts[0]
                service = ' '.join(parts[2:])
                services[port] = service
        
        return services
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during nmap scan: {e}")
        return {}
example_host = '192.168.0.1'  # Example IP address
identified_services = identify_services(example_host)
print(identified_services)    
##################################Détection vulnérabilité 
import re

def nmap_vulnerability_scan(target, result_browser):
    try:
        # Exécute la commande nmap avec le script de détection de vulnérabilités
        scan_result = subprocess.run(['C:\\Program Files (x86)\\Nmap\\nmap.exe', '--script', 'vuln', target], capture_output=True, text=True, check=True)
        
        # Analyse la sortie de la commande pour extraire les informations sur les vulnérabilités
        vulnerabilities = re.findall(r'\d+/(\w+)/\w+\s+\|\s+(\S+)\s+', scan_result.stdout)

        if vulnerabilities:
            result_text = "Vulnérabilités détectées:\n"
            for service, vulnerability in vulnerabilities:
                result_text += f"Service: {service}, Vulnérabilité: {vulnerability}\n"
        else:
            result_text = "Aucune vulnérabilité détectée."

        # Affichez les résultats dans la zone de texte spécifiée
        result_browser.setPlainText(result_text)

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande Nmap : {e}")
        
if __name__ == "__main__":
    target_ip = '192.168.1.1'  # Remplacez cela par l'adresse IP de votre cible
    nmap_vulnerability_scan(target_ip)



