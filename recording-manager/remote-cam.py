#!/bin/env python3
import threading
import time
from time import sleep
from typing import List
import requests
from requests_futures.sessions import FuturesSession
from flask import Flask, escape, request, send_from_directory, redirect
import datetime
import os
from socket import *
import random
app = Flask(__name__)
from peer_management import get_peers

#peers: List[str] = []
port = 5000

time_sec: int = 30
modes = {
    0: {
        "w": 1920,
        "h": 1080,
        "fps": 30,
    },
    1: {
        "w": 3280,
        "h": 2464,
        "fps": 15,
    },
    2: {
        "w": 3280,
        "h": 2464,
        "fps": 15,
    },
    3: {
        "w": 3280,
        "h": 2464,
        "fps": 15,
    },
    4: {
        "w": 1640,
        "h": 1232,
        "fps": 40,
    },
    5: {
        "w": 1640,
        "h": 922,
        "fps": 40,
    },
    6: {
        "w": 1280,
        "h": 720,
        "fps": 90,
    },
    7: {
        "w": 640,
        "h": 480,
        "fps": 120,
    }
}

raw_words = {
    '00': ['aardvark', 'adroitness'],
    '01': ['absurd', 'adviser'],
    '02': ['accrue', 'aftermath'],
    '03': ['acme', 'aggregate'],
    '04': ['adrift', 'alkali'],
    '05': ['adult', 'almighty'],
    '06': ['afflict', 'amulet'],
    '07': ['ahead', 'amusement'],
    '08': ['aimless', 'antenna'],
    '09': ['Algol', 'applicant'],
    '0A': ['allow', 'Apollo'],
    '0B': ['alone', 'armistice'],
    '0C': ['ammo', 'article'],
    '0D': ['ancient', 'asteroid'],
    '0E': ['apple', 'Atlantic'],
    '0F': ['artist', 'atmosphere'],
    '10': ['assume', 'autopsy'],
    '11': ['Athens', 'Babylon'],
    '12': ['atlas', 'backwater'],
    '13': ['Aztec', 'barbecue'],
    '14': ['baboon', 'belowground'],
    '15': ['backfield', 'bifocals'],
    '16': ['backward', 'bodyguard'],
    '17': ['banjo', 'bookseller'],
    '18': ['beaming', 'borderline'],
    '19': ['bedlamp', 'bottomless'],
    '1A': ['beehive', 'Bradbury'],
    '1B': ['beeswax', 'bravado'],
    '1C': ['befriend', 'Brazilian'],
    '1D': ['Belfast', 'breakaway'],
    '1E': ['berserk', 'Burlington'],
    '1F': ['billiard', 'businessman'],
    '20': ['bison', 'butterfat'],
    '21': ['blackjack', 'Camelot'],
    '22': ['blockade', 'candidate'],
    '23': ['blowtorch', 'cannonball'],
    '24': ['bluebird', 'Capricorn'],
    '25': ['bombast', 'caravan'],
    '26': ['bookshelf', 'caretaker'],
    '27': ['brackish', 'celebrate'],
    '28': ['breadline', 'cellulose'],
    '29': ['breakup', 'certify'],
    '2A': ['brickyard', 'chambermaid'],
    '2B': ['briefcase', 'Cherokee'],
    '2C': ['Burbank', 'Chicago'],
    '2D': ['button', 'clergyman'],
    '2E': ['buzzard', 'coherence'],
    '2F': ['cement', 'combustion'],
    '30': ['chairlift', 'commando'],
    '31': ['chatter', 'company'],
    '32': ['checkup', 'component'],
    '33': ['chisel', 'concurrent'],
    '34': ['choking', 'confidence'],
    '35': ['chopper', 'conformist'],
    '36': ['Christmas', 'congregate'],
    '37': ['clamshell', 'consensus'],
    '38': ['classic', 'consulting'],
    '39': ['classroom', 'corporate'],
    '3A': ['cleanup', 'corrosion'],
    '3B': ['clockwork', 'councilman'],
    '3C': ['cobra', 'crossover'],
    '3D': ['commence', 'crucifix'],
    '3E': ['concert', 'cumbersome'],
    '3F': ['cowbell', 'customer'],
    '40': ['crackdown', 'Dakota'],
    '41': ['cranky', 'decadence'],
    '42': ['crowfoot', 'December'],
    '43': ['crucial', 'decimal'],
    '44': ['crumpled', 'designing'],
    '45': ['crusade', 'detector'],
    '46': ['cubic', 'detergent'],
    '47': ['dashboard', 'determine'],
    '48': ['deadbolt', 'dictator'],
    '49': ['deckhand', 'dinosaur'],
    '4A': ['dogsled', 'direction'],
    '4B': ['dragnet', 'disable'],
    '4C': ['drainage', 'disbelief'],
    '4D': ['dreadful', 'disruptive'],
    '4E': ['drifter', 'distortion'],
    '4F': ['dropper', 'document'],
    '50': ['drumbeat', 'embezzle'],
    '51': ['drunken', 'enchanting'],
    '52': ['Dupont', 'enrollment'],
    '53': ['dwelling', 'enterprise'],
    '54': ['eating', 'equation'],
    '55': ['edict', 'equipment'],
    '56': ['egghead', 'escapade'],
    '57': ['eightball', 'Eskimo'],
    '58': ['endorse', 'everyday'],
    '59': ['endow', 'examine'],
    '5A': ['enlist', 'existence'],
    '5B': ['erase', 'exodus'],
    '5C': ['escape', 'fascinate'],
    '5D': ['exceed', 'filament'],
    '5E': ['eyeglass', 'finicky'],
    '5F': ['eyetooth', 'forever'],
    '60': ['facial', 'fortitude'],
    '61': ['fallout', 'frequency'],
    '62': ['flagpole', 'gadgetry'],
    '63': ['flatfoot', 'Galveston'],
    '64': ['flytrap', 'getaway'],
    '65': ['fracture', 'glossary'],
    '66': ['framework', 'gossamer'],
    '67': ['freedom', 'graduate'],
    '68': ['frighten', 'gravity'],
    '69': ['gazelle', 'guitarist'],
    '6A': ['Geiger', 'hamburger'],
    '6B': ['glitter', 'Hamilton'],
    '6C': ['glucose', 'handiwork'],
    '6D': ['goggles', 'hazardous'],
    '6E': ['goldfish', 'headwaters'],
    '6F': ['gremlin', 'hemisphere'],
    '70': ['guidance', 'hesitate'],
    '71': ['hamlet', 'hideaway'],
    '72': ['highchair', 'holiness'],
    '73': ['hockey', 'hurricane'],
    '74': ['indoors', 'hydraulic'],
    '75': ['indulge', 'impartial'],
    '76': ['inverse', 'impetus'],
    '77': ['involve', 'inception'],
    '78': ['island', 'indigo'],
    '79': ['jawbone', 'inertia'],
    '7A': ['keyboard', 'infancy'],
    '7B': ['kickoff', 'inferno'],
    '7C': ['kiwi', 'informant'],
    '7D': ['klaxon', 'insincere'],
    '7E': ['locale', 'insurgent'],
    '7F': ['lockup', 'integrate'],
    '80': ['merit', 'intention'],
    '81': ['minnow', 'inventive'],
    '82': ['miser', 'Istanbul'],
    '83': ['Mohawk', 'Jamaica'],
    '84': ['mural', 'Jupiter'],
    '85': ['music', 'leprosy'],
    '86': ['necklace', 'letterhead'],
    '87': ['Neptune', 'liberty'],
    '88': ['newborn', 'maritime'],
    '89': ['nightbird', 'matchmaker'],
    '8A': ['Oakland', 'maverick'],
    '8B': ['obtuse', 'Medusa'],
    '8C': ['offload', 'megaton'],
    '8D': ['optic', 'microscope'],
    '8E': ['orca', 'microwave'],
    '8F': ['payday', 'midsummer'],
    '90': ['peachy', 'millionaire'],
    '91': ['pheasant', 'miracle'],
    '92': ['physique', 'misnomer'],
    '93': ['playhouse', 'molasses'],
    '94': ['Pluto', 'molecule'],
    '95': ['preclude', 'Montana'],
    '96': ['prefer', 'monument'],
    '97': ['preshrunk', 'mosquito'],
    '98': ['printer', 'narrative'],
    '99': ['prowler', 'nebula'],
    '9A': ['pupil', 'newsletter'],
    '9B': ['puppy', 'Norwegian'],
    '9C': ['python', 'October'],
    '9D': ['quadrant', 'Ohio'],
    '9E': ['quiver', 'onlooker'],
    '9F': ['quota', 'opulent'],
    'A0': ['ragtime', 'Orlando'],
    'A1': ['ratchet', 'outfielder'],
    'A2': ['rebirth', 'Pacific'],
    'A3': ['reform', 'pandemic'],
    'A4': ['regain', 'Pandora'],
    'A5': ['reindeer', 'paperweight'],
    'A6': ['rematch', 'paragon'],
    'A7': ['repay', 'paragraph'],
    'A8': ['retouch', 'paramount'],
    'A9': ['revenge', 'passenger'],
    'AA': ['reward', 'pedigree'],
    'AB': ['rhythm', 'Pegasus'],
    'AC': ['ribcage', 'penetrate'],
    'AD': ['ringbolt', 'perceptive'],
    'AE': ['robust', 'performance'],
    'AF': ['rocker', 'pharmacy'],
    'B0': ['ruffled', 'phonetic'],
    'B1': ['sailboat', 'photograph'],
    'B2': ['sawdust', 'pioneer'],
    'B3': ['scallion', 'pocketful'],
    'B4': ['scenic', 'politeness'],
    'B5': ['scorecard', 'positive'],
    'B6': ['Scotland', 'potato'],
    'B7': ['seabird', 'processor'],
    'B8': ['select', 'provincial'],
    'B9': ['sentence', 'proximate'],
    'BA': ['shadow', 'puberty'],
    'BB': ['shamrock', 'publisher'],
    'BC': ['showgirl', 'pyramid'],
    'BD': ['skullcap', 'quantity'],
    'BE': ['skydive', 'racketeer'],
    'BF': ['slingshot', 'rebellion'],
    'C0': ['slowdown', 'recipe'],
    'C1': ['snapline', 'recover'],
    'C2': ['snapshot', 'repellent'],
    'C3': ['snowcap', 'replica'],
    'C4': ['snowslide', 'reproduce'],
    'C5': ['solo', 'resistor'],
    'C6': ['southward', 'responsive'],
    'C7': ['soybean', 'retraction'],
    'C8': ['spaniel', 'retrieval'],
    'C9': ['spearhead', 'retrospect'],
    'CA': ['spellbind', 'revenue'],
    'CB': ['spheroid', 'revival'],
    'CC': ['spigot', 'revolver'],
    'CD': ['spindle', 'sandalwood'],
    'CE': ['spyglass', 'sardonic'],
    'CF': ['stagehand', 'Saturday'],
    'D0': ['stagnate', 'savagery'],
    'D1': ['stairway', 'scavenger'],
    'D2': ['standard', 'sensation'],
    'D3': ['stapler', 'sociable'],
    'D4': ['steamship', 'souvenir'],
    'D5': ['sterling', 'specialist'],
    'D6': ['stockman', 'speculate'],
    'D7': ['stopwatch', 'stethoscope'],
    'D8': ['stormy', 'stupendous'],
    'D9': ['sugar', 'supportive'],
    'DA': ['surmount', 'surrender'],
    'DB': ['suspense', 'suspicious'],
    'DC': ['sweatband', 'sympathy'],
    'DD': ['swelter', 'tambourine'],
    'DE': ['tactics', 'telephone'],
    'DF': ['talon', 'therapist'],
    'E0': ['tapeworm', 'tobacco'],
    'E1': ['tempest', 'tolerance'],
    'E2': ['tiger', 'tomorrow'],
    'E3': ['tissue', 'torpedo'],
    'E4': ['tonic', 'tradition'],
    'E5': ['topmost', 'travesty'],
    'E6': ['tracker', 'trombonist'],
    'E7': ['transit', 'truncated'],
    'E8': ['trauma', 'typewriter'],
    'E9': ['treadmill', 'ultimate'],
    'EA': ['Trojan', 'undaunted'],
    'EB': ['trouble', 'underfoot'],
    'EC': ['tumor', 'unicorn'],
    'ED': ['tunnel', 'unify'],
    'EE': ['tycoon', 'universe'],
    'EF': ['uncut', 'unravel'],
    'F0': ['unearth', 'upcoming'],
    'F1': ['unwind', 'vacancy'],
    'F2': ['uproot', 'vagabond'],
    'F3': ['upset', 'vertigo'],
    'F4': ['upshot', 'Virginia'],
    'F5': ['vapor', 'visitor'],
    'F6': ['village', 'vocalist'],
    'F7': ['virus', 'voyager'],
    'F8': ['Vulcan', 'warranty'],
    'F9': ['waffle', 'Waterloo'],
    'FA': ['wallet', 'whimsical'],
    'FB': ['watchword', 'Wichita'],
    'FC': ['wayside', 'Wilmington'],
    'FD': ['willow', 'Wyoming'],
    'FE': ['woodlark', 'yesteryear'],
    'FF': ['Zulu', 'Yucatan']
}

selected_mode = 6
'''
@app.before_first_request
def activate_job():
    def send_broadcast():
        while True:
            hostname = gethostname()
            ip_address = gethostbyname(hostname)
            s = socket(AF_INET, SOCK_DGRAM)
            s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            s.sendto(ip_address.encode(), ('255.255.255.255', 42069))
            time.sleep(3)

    def receive_broadcast():
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', 42069))
        m = s.recvfrom(1024)
        register(m[0].decode())

    threading.Thread(target=receive_broadcast).start()
    threading.Thread(target=send_broadcast).start()

@app.route('/register/<path:ip>')
def register(ip: str):
    r = requests.get('http://{}:{}'.format(ip, port))
    if r.status_code == requests.codes.ok:
        if ip not in peers:
            peers.append(ip)
            for peer in peers:
                r = requests.get('http://{}:{}/register/{}'.format(peer, port, ip))
                if not r.status_code == requests.codes.ok:
                    peers.remove(peer)
    return hello
'''


@app.route('/ls')
def ls():
    dir = os.listdir(os.path.join(os.getcwd(), "vid"))
    out = '<h1>All saved videos</h1><br /><a href="/"><h3>Go back home</h3></a>'
    for file in dir:
        out += "<p><h3><a href='/vid/{filename}'>{filename}</a></h3></p>".format(filename=file)
    return out


@app.route('/vid/<path:path>')
def send_vid(path):
    print(path)
    return send_from_directory('vid', path)

@app.route('/time/add/<int:time>/')
def time_add(time:int):
    global time_sec
    time_sec += time
    return redirect("/")

@app.route('/time/sub/<int:time>/')
def time_sub(time: int):
    global time_sec
    if time_sec - time > 0:
        return time_add(-time)
    else:
        time_sec = 10
        return redirect("/")
@app.route('/rec/<int:time>/')
def start_rec(time: int):
    vid_file_name = 'vid/Battledork_{:%Y-%m-%d__%H-%M-%S}.h264'.format(datetime.datetime.now())

    return '''
    <h1>Recording of {}s successful</h1><p>&nbsp;</p>
    <a href='/{}'><h3>Download</h3></a>
    <p>&nbsp;</p>
    <a href='/'><h3>Go back home</h3></a>'''.format(time, vid_file_name)

@app.route('/rec/<int:time>/<path:filename>/<int:mode>/')
def record(time: int, filename, mode: int):
    video_command = f'raspivid -o vid/{filename} -md {mode} -w {modes.get(mode).get("w")} -h {modes.get(mode).get("h")} -fps {modes.get(mode).get("fps")} -t {time * 1000}'
    if modes.get(mode).get("fps") > 120:
        video_command += ' -ex off'
    print(video_command)
    os.system(video_command)
    return video_command

@app.route('/recall')
def start_parallel():
    session = FuturesSession()
    random_words: List[str] = random.choice(list(raw_words.values()))
    filename = f"Battledork_{time_sec}s_{random_words[0]}-{random_words[1]}__{datetime.datetime.today().strftime('%Y-%m-%d+%H:%M:%S')}"
    reqs = []
    time.sleep(5)
    for i, peer in enumerate(get_peers()):
        req = session.get(f"http://{peer}:5000/rec/{time_sec}/{filename}__{i}.mp4/{selected_mode}/")
        reqs.append(req)
    done_out = ""
    for req in reqs:
        done_out += str(req.result())
    return f"Started peers: {get_peers()}, Results: {done_out}"



@app.route('/img/<int:mode>')
def get_img(mode = 6):
    img_tmp_name = 'tmp_img.jpg'
    #os.system(f"rm ./img/{img_tmp_name}")
    img_command = f'raspistill -t 500 -o ./img/{img_tmp_name} -q 20 -w {modes.get(mode).get("w")} -h {modes.get(mode).get("h")} -md {mode}'
    print(img_command)
    os.system(img_command)
    #time.sleep(1)
    return send_from_directory('img', img_tmp_name)

@app.route("/viewer/<path:video>")
def viewer(video):
    prev = ""
    for i, peer in enumerate(get_peers()):
        vpath = list(str(video))
        vpath[-5] = str(i)
        peer_path = ''.join(vpath)
        prev += f'<video src="http://{peer}:5000/vid/{peer_path}" controls preload="metadata" style="float: left; width: 30%; margin-right: 1%; margin-bottom: 0.5em;">video error</video>'
    return prev

@app.route("/preview/")
def preview():
    prev = ""
    for i, peer in enumerate(get_peers()):
        prev += '<img src="http://{}:5000/img/{}?{}" style="float: left; width: 30%; margin-right: 1%; margin-bottom: 0.5em;">'.format(peer, selected_mode, random.randint(1000000000,100000000000))
        if (i % 2) == 1:
            prev += '<p style="clear: both;">'
    prev += "<p>"
    for i in range(8):
        prev += f'<a href="/set/mode/{i}">{i}</a>&nbsp;'
    prev += f"</p><p><h3>{selected_mode}</h3></p>"
    return prev

@app.route('/set/mode/<int:mode>/')
def set_mode(mode: int):
    global selected_mode
    selected_mode = mode
    return redirect("/")

@app.route('/')
def hello():
    return f'''
    <h1>Battledork Recording Manager</h1>
    <p>&nbsp;</p>
    <a href='/ls'><h3>Show recorded files</h3></a>
    <p>&nbsp;</p>
    <h4>Selected mode: {selected_mode}</h4>
    <h4>Selected Time: {time_sec}s</h4>
    <h4>Peers: {get_peers()}</h4>
    <p>&nbsp;</p>
    <a href='/recall'>Record in parrallel</a>
    <p>&nbsp;</p>
    <a href='/time/sub/60'><h3>Sub 60s</h3></a>
    <a href='/time/sub/10'><h3>Sub 10s</h3></a>
    <a href='/time/add/10'><h3>Add 10s</h3></a>
    <a href='/time/add/60'><h3>Add 60s</h3></a>
    <a href='/'><h3></h3></a>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <a href="/preview">Preview Camera Images</a>
    <p>&nbsp;</p>
    <table>
    <thead>
    <tr>
    <th>Mode</th><th>Size</th><th>Aspect Ratio</th><th>Frame rates</th><th>FOV</th><th>Binning</th></tr>
    </thead>
    <tbody>
    <tr><td><a href="/set/mode/0">0</a></td><td>automatic selection</td><td></td><td></td><td></td><td></td></tr>
    <tr><td><a href="/set/mode/1">1</a></td><td>1920x1080</td><td>16:9</td><td>0.1-30fps</td><td>Partial</td><td>None</td></tr>
    <tr><td><a href="/set/mode/2">2</a></td><td>3280x2464</td><td>4:3</td><td>0.1-15fps</td><td>Full</td><td>None</td></tr>
    <tr><td><a href="/set/mode/3">3</a></td><td>3280x2464</td><td>4:3</td><td>0.1-15fps</td><td>Full</td><td>None</td></tr>
    <tr><td><a href="/set/mode/4">4</a></td><td>1640x1232</td><td>4:3</td><td>0.1-40fps</td><td>Full</td><td>2x2</td></tr>
    <tr><td><a href="/set/mode/5">5</a></td><td>1640x922</td><td>16:9</td><td>0.1-40fps</td><td>Full</td><td>2x2</td></tr>
    <tr><td><a href="/set/mode/6">6</a></td><td>1280x720</td><td>16:9</td><td>40-90fps</td><td>Partial</td><td>2x2</td></tr>
    <tr><td><a href="/set/mode/7">7</a></td><td>640x480</td><td>4:3</td><td>40-200fps<sup>1</sup></td><td>Partial</td><td>2x2</td></tr>
    </tbody>
    </table>
        '''
