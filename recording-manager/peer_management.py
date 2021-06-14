import ipaddress
from typing import List
import os

# Enter IP subnet (/24) here with last part as zero
peer_subnet_start = ipaddress.IPv4Address("192.168.43.0")

#Enter the last part of each peer here
peers = [
    253,
    48,
    63,
    87
]

def get_peers() -> List[str]:
    return list(map(lambda x: str(peer_subnet_start + x), peers))

def upload():
    for peer in get_peers():
        up_command = f"scp -r ../recording-manager/ pi@{peer}:~"
        print(up_command)
        os.system(up_command)

if __name__ == '__main__':
    upload()
