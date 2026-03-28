"""
╔══════════════════════════════════════════════════╗
║   S N A K E  ·  MYTHIC  EDITION  v9             ║
║   Weather · Boss Fights · Smart Prey            ║
╚══════════════════════════════════════════════════╝
"""
import pygame, random, sys, math, colorsys
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

COLS,ROWS=30,28; CELL=25; PANEL=250
W=COLS*CELL; H=ROWS*CELL; SW=W+PANEL; SH=H+96
UP=(0,-1);DOWN=(0,1);LEFT=(-1,0);RIGHT=(1,0)
OPP={UP:DOWN,DOWN:UP,LEFT:RIGHT,RIGHT:LEFT}
BASE_SPD=7; MAX_SPD=20

# ── Colours ──────────────────────────────────────
# ── Chibi palette ──────────────────────────────
BG=(8,10,18);PT=(12,14,24);PB=(16,18,30);CB=(14,16,28);CB2=(18,20,34)
BDR=(35,40,65);BDH=(55,65,105)
# Ground — warm grass chibi style
TD=(18,52,22);TM=(22,62,26);TL=(28,72,32);TE=(14,44,16)
AP=(222,46,46);APD=(176,24,24);APS=(255,125,125);STEM=(66,38,10);LF=(44,128,44)
STC=(255,190,32);STH=(255,235,125);WHT=(255,255,255);DIM=(58,66,88);DIM2=(34,42,62)
GOLD=(255,192,34);ACC=(60,180,100);AC2=(40,136,70);DNG=(208,48,48)
NFO=(60,144,212);NGN=(46,226,96);SCC=(218,222,232)


PS="shield";PV="speed";PM="magnet";PX="multi"
PG="ghost";PF="freeze";PL="slow";PN="nuke"
PZ="spd_cap";PW="time_warp";PH="heal"
PD="dash";PR="shrink";PB2="score3";PP="phase"   # new PUs

PU_COL={PS:(80,200,255),PV:(255,180,40),PM:(220,80,255),PX:(80,255,140),
        PG:(180,180,255),PF:(80,220,255),PL:(100,220,180),PN:(255,100,60),
        PZ:(255,160,80),PW:(160,80,255),PH:(80,255,160),
        PD:(255,120,255),PR:(120,255,220),PB2:(255,220,60),PP:(180,255,180)}
PU_ICO={PS:"DERQA",    PV:"SIR3A",   PM:"MAGNIT",  PX:"x2 NQT",
        PG:"GHOUL",    PF:"JLID",    PL:"BTTI",    PN:"NUKE",
        PZ:"HBES",     PW:"WQFA",    PH:"BRAS",
        PD:"DASH",     PR:"SQOL",    PB2:"x3 NQT", PP:"KHAYEL"}
# Darija legend:
# DERQA=Shield درقة | SIR3A=Speed سرعة | MAGNIT=Magnet | x2/x3 NQT=نقاط×2/3
# GHOUL=Ghost غول | JLID=Freeze جليد | BTTI=Slow بطي | NUKE=نيوك
# HBES=Speed Cap حبس | WQFA=TimeWarp وقفة | BRAS=Heal براس
# DASH=داش | SQOL=Shrink سقل | KHAYEL=Phase خايل
PU_DUR={PS:7000,PV:5000,PM:7000,PX:9000,PG:5000,PF:4500,PL:6000,PN:1,
        PZ:8000,PW:6000,PH:1,PD:1,PR:1,PB2:8000,PP:6000}

# ── SKILLS — passive upgrades bought with skill points ──
SKILLS=[
  # id            Darija name        Darija desc                     cost  col
  {"id":"combo_keep",  "name":"Daker l-Combo",  "desc":"Combo ma-ymutch bsre3a, +1 thanya",   "cost":3,"col":(255,200,50)},
  {"id":"start_len",   "name":"Bda Kbir",        "desc":"Katbda b-toul 5 (3wad 3)",            "cost":3,"col":(80,220,120)},
  {"id":"prey_time",   "name":"Sabr mezyan",     "desc":"3endek +5 thwayni bach tchdoh",       "cost":4,"col":(255,140,80)},
  {"id":"pu_longer",   "name":"Khzzen l-Qwa",   "desc":"Kol power-up kayb9a 30% akter",       "cost":5,"col":(160,100,255)},
  {"id":"score_bonus", "name":"Zid n-Nqat",     "desc":"+2 nqta zayda f kol akla",            "cost":4,"col":(255,220,60)},
  {"id":"dash_cd",     "name":"Dash Sir3",       "desc":"DASH katji bktir f l-map",            "cost":5,"col":(255,120,255)},
  {"id":"shield_wall", "name":"Droa l-Jdar",    "desc":"Shield kayhmi men l-jdran wald",       "cost":6,"col":(80,200,255)},
  {"id":"ghost_food",  "name":"3in l-Ghoul",    "desc":"Katshof l-makla f l-dlam",             "cost":5,"col":(180,180,255)},
]

THEMES=[
    ("Forest",  (75,206,106),(47,153,72),(31,116,50),(18,80,32),  (188,210,152),(135,255,168)),
    ("Ocean",   (38,158,228),(22,108,178),(14,78,138),(8,50,98),  (158,208,238),(130,218,255)),
    ("Magma",   (228,88,38),(178,52,18),(138,36,10),(98,22,4),    (238,178,128),(255,178,128)),
    ("Amethyst",(178,58,228),(128,28,178),(90,14,138),(58,6,100), (208,158,238),(228,168,255)),
    ("Gold",    (228,188,38),(178,138,18),(138,98,8),(98,65,2),   (238,218,158),(255,238,148)),
    ("Ice",     (158,218,244),(108,168,214),(78,128,185),(48,90,155),(208,233,246),(198,238,255)),
    ("Ruby",    (224,44,44),(174,20,20),(134,8,8),(94,2,2),       (232,172,172),(255,168,168)),
    ("Void",    (88,48,188),(58,28,148),(38,14,110),(22,4,78),    (168,148,218),(198,168,255)),
    ("Toxic",   (128,228,48),(88,178,28),(58,138,14),(34,98,4),   (198,228,148),(188,255,128)),
    ("Copper",  (188,108,48),(138,72,22),(98,48,8),(65,28,2),     (228,188,148),(255,198,138)),
]

# Weather types
WN="none"; WR="rain"; WS="snow"; WL="lightning"
WEATHER_DUR=45000  # 45s per weather

# Boss definitions
BOSSES={
    5:  {"name":"Stone Warden","col":(140,100,60),"hp":8, "atk":"rocks"},
    10: {"name":"Storm Eye",   "col":(80,160,255),"hp":12,"atk":"lightning"},
    15: {"name":"Frost King",  "col":(160,220,255),"hp":16,"atk":"freeze"},
}
BOSS_KILL_PU={5:PN, 10:PL, 15:PF}  # power-up that damages boss

# ── Game Modes ──────────────────────────────────────
MODE_MENU   = "menu"      # main menu: 3 big buttons
MODE_STAGE  = "stage_sel" # stage grid
MODE_FREE   = "free"      # free play running
MODE_GAME   = "game"      # stage game running

HAZARD_NONE      = "none"
HAZARD_VORTEX    = "vortex"
HAZARD_PORTAL    = "portal"
HAZARD_DARK      = "dark"
HAZARD_MIRROR    = "mirror"
HAZARD_SPEEDTRAP = "speed"
HAZARD_GRAVITY   = "gravity"
HAZARD_ELECTRIC  = "electric"
HAZARD_MAZE      = "maze"

# ── Helper to build stage ────────────────────────
def _S(id,name,col,spd,wx,boss,hz,target,desc):
    return {"id":id,"name":name,"col":col,"spd":spd,"wx":wx,
            "boss":boss,"hz":hz,"target":target,"desc":desc}

STAGES=[
 # ── ACT 1: Tutorial (1-5) ─────────────────────────────────────────────
 _S(1, "The Meadow",     (70,200,90),  1.00, WN, None, HAZARD_NONE,     80,  "Open fields. No tricks. Learn the ropes."),
 _S(2, "Puddle Path",    (55,130,220), 1.05, WR, None, HAZARD_NONE,    120,  "Rain falls. Ground is slippery."),
 _S(3, "Mushroom Ring",  (200,100,255),1.00, WN, None, HAZARD_SPEEDTRAP,140, "Gold mushrooms boost your speed — careful."),
 _S(4, "Frost Plains",   (160,215,255),0.90, WS, None, HAZARD_NONE,    160,  "Everything slows in the cold."),
 _S(5, "Stone Keep",     (160,120,75), 1.15, WN, 5,    HAZARD_NONE,    200,  "First boss: Stone Warden. Use NUKE."),

 # ── ACT 2: Confusion (6-10) ─────────────────────────────────────────────
 _S(6, "Mirror Lake",    (200,140,255),1.05, WN, None, HAZARD_MIRROR,  200,  "Controls reversed. Left is right. Up is down."),
 _S(7, "Dark Swamp",     (50,130,70),  1.15, WR, None, HAZARD_DARK,    220,  "Darkness patches hide your path."),
 _S(8, "Spin Canyon",    (100,200,255),1.10, WN, None, HAZARD_VORTEX,  240,  "Vortex zones rotate your direction 90°."),
 _S(9, "Twin Portals",   (255,160,60), 1.20, WN, None, HAZARD_PORTAL,  260,  "Enter a portal, exit somewhere else entirely."),
 _S(10,"Storm Summit",   (100,165,255),1.25, WL, None, HAZARD_NONE,    300,  "Lightning blinds you. Move between flashes."),

 # ── ACT 3: Pressure (11-15) ─────────────────────────────────────────────
 _S(11,"Electric Bog",   (255,220,50), 1.25, WR, None, HAZARD_ELECTRIC,300,  "Electric fences spawn in the rain. Deadly."),
 _S(12,"Gravity Pit",    (255,80,120), 1.30, WN, None, HAZARD_GRAVITY, 320,  "Gravity drags you down. You must fight it."),
 _S(13,"Blizzard Pass",  (200,230,255),1.20, WS, None, HAZARD_VORTEX,  340,  "Ice vortex + blizzard. Plan every move."),
 _S(14,"Dark Mirrors",   (180,100,255),1.25, WN, None, HAZARD_DARK,    360,  "Darkness AND reversed controls. Brutal."),
 _S(15,"Thunder Dome",   (100,165,255),1.40, WL, 10,   HAZARD_ELECTRIC,400,  "Storm Eye + electric fences. Use SLOW."),

 # ── ACT 4: Chaos (16-20) ─────────────────────────────────────────────
 _S(16,"Maze Ruins",     (80,200,160), 1.35, WN, None, HAZARD_MAZE,    420,  "Energy walls shift every 6 seconds."),
 _S(17,"Portal Storm",   (255,140,40), 1.40, WL, None, HAZARD_PORTAL,  440,  "Portals everywhere in a lightning storm."),
 _S(18,"Speed Maze",     (255,200,30), 1.45, WN, None, HAZARD_MAZE,    460,  "Speed traps inside a shifting energy maze."),
 _S(19,"Void Mirrors",   (160,80,255), 1.45, WN, None, HAZARD_MIRROR,  480,  "Mirror controls in the maze. No escape."),
 _S(20,"Gravity Storm",  (255,80,80),  1.50, WL, None, HAZARD_GRAVITY, 520,  "Lightning + gravity. Pure reflex needed."),

 # ── ACT 5: Nightmare (21-25) ─────────────────────────────────────────────
 _S(21,"Frozen Maze",    (160,215,255),1.40, WS, None, HAZARD_MAZE,    560,  "Energy maze in a blizzard. Ultra slow."),
 _S(22,"Dark Vortex",    (50,50,80),   1.50, WN, None, HAZARD_VORTEX,  580,  "Spin zones in total darkness."),
 _S(23,"Portal Gravity", (200,80,255), 1.55, WN, None, HAZARD_PORTAL,  600,  "Portals that send you in a gravity well."),
 _S(24,"Electric Mirror",(255,220,50), 1.55, WN, None, HAZARD_ELECTRIC,640,  "Reversed controls + electric fences."),
 _S(25,"Frost King Lair",(200,230,255),1.45, WS, 15,   HAZARD_VORTEX,  700,  "Frost King + ice vortex + blizzard."),

 # ── ACT 6: Endgame (26-30) ─────────────────────────────────────────────
 _S(26,"The Abyss",      (40,40,80),   1.60, WL, None, HAZARD_DARK,    750,  "Total darkness in a lightning storm."),
 _S(27,"Chaos Engine",   (255,60,60),  1.65, WN, None, HAZARD_MAZE,    800,  "Maze shifts every 4 seconds. No mercy."),
 _S(28,"All Hazards",    (255,140,0),  1.60, WR, None, HAZARD_ELECTRIC,840,  "Electric + rain + speed traps. Everything."),
 _S(29,"Final Storm",    (100,150,255),1.70, WL, None, HAZARD_GRAVITY, 880,  "Gravity + lightning storm. Last warm-up."),
 _S(30,"THE FINALE",     (255,200,30), 1.75, WL, 15,   HAZARD_MAZE,    999,  "Energy maze. Frost King. Lightning storm. END."),

 # ── ACT 7: REBIRTH (31-35) — new tricks ──────────────────────────────
 _S(31,"Neon Jungle",    (0,255,150),  1.50, WR, None, HAZARD_PORTAL,  680,  "Portals inside a dense wall maze. Think fast."),
 _S(32,"Crystal Caves",  (180,100,255),1.55, WS, None, HAZARD_VORTEX,  720,  "Vortex + ice + wall labyrinth. Disorienting."),
 _S(33,"The Garden",     (100,220,80), 1.45, WN, None, HAZARD_NONE,    760,  "Beautiful barriers. No hazard. Pure speed."),
 _S(34,"Acid Rain",      (180,255,50), 1.65, WR, None, HAZARD_ELECTRIC,800,  "Electric fences + rain in a tight arena."),
 _S(35,"Shadow Labyrinth",(80,60,180), 1.60, WN, None, HAZARD_DARK,    850,  "Darkness + maze walls. Can you see anything?"),

 # ── ACT 8: MASTER (36-40) — everything combined ─────────────────────
 _S(36,"Void Maze",      (40,20,80),   1.70, WN, None, HAZARD_MAZE,    900,  "Maze walls shift every 4 seconds. No mercy."),
 _S(37,"Gravity Grid",   (255,60,160), 1.70, WN, None, HAZARD_GRAVITY, 940,  "Gravity + walls. The grid fights you."),
 _S(38,"The Gauntlet",   (255,100,20), 1.75, WL, None, HAZARD_ELECTRIC,980,  "Electric + lightning + brutal wall layout."),
 _S(39,"Chaos Nexus",    (200,50,255), 1.80, WL, None, HAZARD_PORTAL,  999,  "Portal storm inside a prison of walls."),
 _S(40,"ETERNAL SNAKE",  (255,220,0),  1.85, WL, 15,   HAZARD_MAZE,   1200,  "The ultimate. All hazards. Final boss. No return."),
]

# ── Stage ground themes ──────────────────────────
STAGE_GROUND={
    1:"grass",2:"grass",3:"grass",4:"ice",5:"sand",
    6:"void",7:"sand",8:"lava",9:"purple",10:"sand",
    11:"lava",12:"purple",13:"ice",14:"void",15:"lava",
    16:"void",17:"sand",18:"void",19:"purple",20:"lava",
    21:"ice",22:"void",23:"purple",24:"lava",25:"ice",
    26:"void",27:"void",28:"lava",29:"purple",30:"void",
    31:"sand",32:"ice",33:"grass",34:"lava",35:"purple",
    36:"void",37:"sand",38:"lava",39:"ice",40:"void",
}

# ── Stage barrier patterns ───────────────────────
# Each entry is a list of wall segments: (x,y,len,horiz)
# Barriers are pre-baked solid walls on the grid
def _barrier(x,y,ln,hz=True):
    cells=set()
    for k in range(ln):
        if hz: cells.add((x+k,y))
        else:  cells.add((x,y+k))
    return cells

STAGE_BARRIERS={
    # Stage 1 — no barriers (tutorial)
    1: set(),
    # Stage 2 — 2 short walls
    2: _barrier(8,8,4)|_barrier(18,18,4),
    # Stage 3 — mirror layout
    3: _barrier(5,7,3)|_barrier(22,7,3)|_barrier(5,20,3)|_barrier(22,20,3),
    # Stage 4 — cross shape centre
    4: _barrier(12,8,6)|_barrier(12,18,6)|_barrier(8,12,14,False),
    # Stage 5 — box arena
    5: _barrier(6,6,4)|_barrier(20,6,4)|_barrier(6,18,4)|_barrier(20,18,4),
    # Stage 6 — 3 horizontal walls
    6: _barrier(4,7,8)|_barrier(18,12,8)|_barrier(4,19,8),
    # Stage 7 — zigzag
    7: _barrier(3,5,5)|_barrier(8,10,5)|_barrier(17,14,5)|_barrier(22,19,5),
    # Stage 8 — spiral arms
    8: _barrier(5,5,10)|_barrier(5,5,10,False)|_barrier(20,20,5)|_barrier(20,15,5,False),
    # Stage 9 — tight corridor
    9: _barrier(3,10,10)|_barrier(17,17,10)|_barrier(13,3,6,False)|_barrier(13,19,6,False),
    # Stage 10 — diamond
   10: _barrier(10,4,5)|_barrier(6,8,4,False)|_barrier(20,8,4,False)|_barrier(8,20,10),
   # Stage 11-20 — increasingly complex
   11: _barrier(2,6,12)|_barrier(16,20,12),
   12: _barrier(6,2,18,False)|_barrier(6,2,18,False),
   13: _barrier(4,7,8)|_barrier(4,19,8)|_barrier(18,7,8)|_barrier(18,19,8)|_barrier(11,12,4,False),
   14: _barrier(8,4,6)|_barrier(8,4,6,False)|_barrier(16,4,6)|_barrier(16,16,6,False),
   15: _barrier(5,5,5)|_barrier(5,5,8,False)|_barrier(20,5,5)|_barrier(20,5,8,False)|_barrier(5,20,5)|_barrier(20,12,5,False),
   16: _barrier(10,3,10)|_barrier(10,23,10)|_barrier(3,10,8,False)|_barrier(24,10,8,False),
   17: _barrier(7,7,16)|_barrier(7,7,10,False)|_barrier(7,16,16),
   18: (_barrier(3,6,6)|_barrier(21,6,6)|_barrier(3,20,6)|_barrier(21,20,6)|
        _barrier(12,3,4,False)|_barrier(12,20,4,False)),
   19: (_barrier(8,5,10)|_barrier(8,22,10)|_barrier(3,8,5,False)|_barrier(3,13,5,False)|
        _barrier(24,8,5,False)|_barrier(24,13,5,False)),
   20: (_barrier(5,5,20)|_barrier(5,5,18,False)|_barrier(5,22,20)|_barrier(24,5,18,False)),
   # Stage 21-30
   21: (_barrier(4,4,8)|_barrier(18,4,8)|_barrier(4,22,8)|_barrier(18,22,8)|
        _barrier(11,11,4)|_barrier(11,11,6,False)),
   22: (_barrier(3,3,24)|_barrier(3,3,22,False)|_barrier(3,24,24)|_barrier(26,3,22,False)),
   23: (_barrier(6,6,4)|_barrier(12,6,4)|_barrier(18,6,4)|
        _barrier(6,13,4)|_barrier(12,13,4)|_barrier(18,13,4)|
        _barrier(6,20,4)|_barrier(12,20,4)|_barrier(18,20,4)),
   24: (_barrier(8,3,5,False)|_barrier(8,3,14)|_barrier(8,16,14)|
        _barrier(22,3,5,False)|_barrier(22,16,5,False)),
   25: (_barrier(4,4,6)|_barrier(20,4,6)|_barrier(4,4,6,False)|_barrier(25,4,6,False)|
        _barrier(4,18,6)|_barrier(20,18,6)|_barrier(4,22,6,False)|_barrier(25,18,6,False)|
        _barrier(12,10,6)|_barrier(12,10,8,False)),
   # Stage 26-30 — brutal layouts
   26: (_barrier(3,3,24)|_barrier(3,3,10,False)|_barrier(3,12,24)|_barrier(3,21,24)|
        _barrier(3,12,10,False)),
   27: (_barrier(7,4,16)|_barrier(7,4,20,False)|_barrier(7,23,16)|_barrier(22,4,20,False)),
   28: (_barrier(5,5,6)|_barrier(5,5,5,False)|_barrier(19,5,6)|_barrier(19,5,5,False)|
        _barrier(5,18,6)|_barrier(5,22,5,False)|_barrier(19,18,6)|_barrier(19,22,5,False)|
        _barrier(11,11,8)|_barrier(11,11,6,False)),
   29: (_barrier(4,3,22)|_barrier(4,3,22,False)|_barrier(4,24,22)|_barrier(25,3,22,False)|
        _barrier(8,7,14)|_barrier(8,7,14,False)|_barrier(8,20,14)|_barrier(21,7,14,False)),
   30: (_barrier(3,3,24)|_barrier(3,3,22,False)|_barrier(3,24,24)|_barrier(26,3,22,False)|
        _barrier(7,7,16)|_barrier(7,7,14,False)|_barrier(7,20,16)|_barrier(22,7,14,False)|
        _barrier(11,11,8)|_barrier(11,11,6,False)),
   # Stage 31-40
   31: _barrier(6,4,18)|_barrier(6,22,18)|_barrier(3,4,18,False)|_barrier(24,4,18,False),
   32: (_barrier(5,5,7)|_barrier(5,5,8,False)|_barrier(18,5,7)|_barrier(18,5,8,False)|
        _barrier(5,15,7)|_barrier(5,22,8,False)|_barrier(18,15,7)|_barrier(18,22,8,False)),
   33: (_barrier(4,4,8)|_barrier(4,4,20,False)|_barrier(4,23,8)|_barrier(11,4,8)|
        _barrier(18,4,8)|_barrier(18,4,20,False)|_barrier(18,23,8)),
   34: (_barrier(8,3,14)|_barrier(8,3,22,False)|_barrier(8,24,14)|_barrier(21,3,22,False)|
        _barrier(11,8,8)|_barrier(11,8,10,False)|_barrier(11,17,8)|_barrier(18,8,10,False)),
   35: (_barrier(3,3,24)|_barrier(3,3,22,False)|_barrier(3,24,24)|_barrier(26,3,22,False)|
        _barrier(6,6,18)|_barrier(6,6,16,False)|_barrier(6,21,18)|_barrier(23,6,16,False)|
        _barrier(9,9,12)|_barrier(9,9,10,False)),
   36: (_barrier(4,4,22)|_barrier(4,4,20,False)|_barrier(4,23,22)|_barrier(25,4,20,False)|
        _barrier(8,8,14)|_barrier(8,8,12,False)|_barrier(8,19,14)|_barrier(21,8,12,False)),
   37: (_barrier(5,3,5)|_barrier(12,3,5)|_barrier(18,3,5)|
        _barrier(5,3,8,False)|_barrier(12,3,8,False)|_barrier(18,3,8,False)|
        _barrier(5,10,5)|_barrier(12,10,5)|_barrier(18,10,5)|
        _barrier(5,17,5)|_barrier(12,17,5)|_barrier(18,17,5)|
        _barrier(5,17,8,False)|_barrier(12,17,8,False)|_barrier(18,17,8,False)),
   38: (_barrier(6,6,18)|_barrier(6,6,16,False)|_barrier(6,21,18)|_barrier(23,6,16,False)|
        _barrier(10,10,10)|_barrier(10,10,8,False)|_barrier(10,17,10)|_barrier(19,10,8,False)|
        _barrier(13,13,4)|_barrier(13,13,2,False)),
   39: (_barrier(3,3,24)|_barrier(3,3,22,False)|_barrier(3,24,24)|_barrier(26,3,22,False)|
        _barrier(7,7,16)|_barrier(7,7,14,False)|_barrier(7,20,16)|_barrier(22,7,14,False)|
        _barrier(11,11,8)|_barrier(11,11,6,False)|_barrier(11,16,8)|_barrier(18,11,6,False)),
   40: set(),  # stage 40: no barriers but max everything else
}

# Clean barriers — remove out-of-bounds cells and cells too close to centre
def _clean_barrier(cells,margin=2):
    centre=(COLS//2,ROWS//2)
    return {(x,y) for x,y in cells
            if margin<=x<COLS-margin and margin<=y<ROWS-margin
            and abs(x-centre[0])+abs(y-centre[1])>4}

STAGE_BARRIERS={k:_clean_barrier(v) for k,v in STAGE_BARRIERS.items()}

# ── Fonts ─────────────────────────────────────────
def _f(sz,bold=False):
    for n in ["Segoe UI","Ubuntu","DejaVu Sans","Arial"]:
        try:
            f=pygame.font.SysFont(n,sz,bold=bold)
            if f: return f
        except: pass
    return pygame.font.Font(None,sz)

FXL=_f(44,True);FT=_f(34,True);FB=_f(28,True)
FM=_f(18,True);FS=_f(13);FXS=_f(11);FXX=_f(10)

# ── Helpers ───────────────────────────────────────
def hsv(h,s=1.,v=1.):
    r,g,b=colorsys.hsv_to_rgb(h%1.,s,v)
    return(int(r*255),int(g*255),int(b*255))
def lc(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def cl(v): return max(0,min(255,int(v)))
def asurf(w,h): return pygame.Surface((max(1,w),max(1,h)),pygame.SRCALPHA)
def tc(surf,txt,fnt,col,cx,cy):
    t=fnt.render(str(txt),True,col)
    surf.blit(t,(cx-t.get_width()//2,cy-t.get_height()//2))
def glow_tc(surf,txt,fnt,col,cx,cy,layers=3):
    dark=tuple(cl(c*.18) for c in col)
    for g in range(layers,0,-1):
        t=fnt.render(str(txt),True,dark)
        for dx,dy in[(-g,0),(g,0),(0,-g),(0,g),(-g,-g),(g,g),(-g,g),(g,-g)]:
            surf.blit(t,(cx-t.get_width()//2+dx,cy-t.get_height()//2+dy))
    tc(surf,txt,fnt,col,cx,cy)
def rbox(surf,rect,col,r=8,brd=None,bw=1,a=255):
    s=asurf(rect[2],rect[3])
    pygame.draw.rect(s,(*col[:3],a),(0,0,rect[2],rect[3]),border_radius=r)
    if brd: pygame.draw.rect(s,(*brd[:3],a),(0,0,rect[2],rect[3]),border_radius=r,width=bw)
    surf.blit(s,(rect[0],rect[1]))
def rbox_g(surf,rect,ct,cb,r=8,brd=None,bw=1):
    s=asurf(rect[2],rect[3])
    for y in range(rect[3]):
        c=lc(ct,cb,y/max(1,rect[3]-1))
        pygame.draw.line(s,(*c,255),(0,y),(rect[2],y))
    ms=asurf(rect[2],rect[3])
    pygame.draw.rect(ms,(255,255,255,255),(0,0,rect[2],rect[3]),border_radius=r)
    s.blit(ms,(0,0),special_flags=pygame.BLEND_RGBA_MIN)
    if brd: pygame.draw.rect(s,(*brd[:3],255),(0,0,rect[2],rect[3]),border_radius=r,width=bw)
    surf.blit(s,(rect[0],rect[1]))
def nbar(surf,x,y,w,h,val,mx,col,r=4):
    pygame.draw.rect(surf,(9,12,20),(x,y,w,h),border_radius=r)
    if val>0 and mx>0:
        fw=max(0,int(w*min(val,mx)/mx))
        if fw>0:
            pygame.draw.rect(surf,col,(x,y,fw,h),border_radius=r)
            g=asurf(fw+12,h+12)
            pygame.draw.rect(g,(*col,25),(0,0,fw+12,h+12),border_radius=r+4)
            surf.blit(g,(x-6,y-6))
def cglow(surf,cx,cy,r,col,a=55):
    s=asurf(r*2+8,r*2+8)
    pygame.draw.circle(s,(*col[:3],a),(r+4,r+4),r)
    surf.blit(s,(cx-r-4,cy-r-4))

# ── Sound ─────────────────────────────────────────
def _synth(freq=440,dur=0.08,vol=0.13,wave="sine",env=(0.01,0.02,0.7,0.05),
           harmonics=None,pitch_sweep=None,vibrato=None):
    sr=44100;n=int(sr*dur);buf=bytearray(n*4)
    at=int(sr*env[0]);dc=int(sr*env[1]);su=env[2];rel=int(sr*env[3])
    ss=at+dc;se=max(ss,n-rel)
    for i in range(n):
        t=i/sr
        if i<at: e=i/max(1,at)
        elif i<ss: e=1.-(1.-su)*(i-at)/max(1,dc)
        elif i<se: e=su
        else: e=su*max(0,1-(i-se)/max(1,rel))
        f=freq+(pitch_sweep*t if pitch_sweep else 0)
        if vibrato: f+=vibrato[0]*math.sin(2*math.pi*vibrato[1]*t)
        ph=2*math.pi*f*t
        if wave=="sine": v=math.sin(ph)
        elif wave=="sqr": v=1. if math.sin(ph)>0 else -1.
        elif wave=="tri": v=2*abs(2*(t*f-math.floor(t*f+.5)))-1
        elif wave=="saw": v=2*(t*f-math.floor(t*f+.5))
        else: v=math.sin(ph)
        if harmonics:
            for hf,hv in harmonics: v+=hv*math.sin(2*math.pi*f*hf*t)
            v/=(1+sum(abs(hv) for _,hv in harmonics))
        s=max(-32768,min(32767,int(32767*vol*v*e)))
        buf[4*i]=s&0xFF;buf[4*i+1]=(s>>8)&0xFF;buf[4*i+2]=s&0xFF;buf[4*i+3]=(s>>8)&0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))

def _build_snd():
    d={}
    try:
        d["eat1"]=_synth(523,.11,.12,"sine",harmonics=[(2,.22)],env=(.003,.012,.5,.09))
        d["eat2"]=_synth(659,.10,.12,"sine",harmonics=[(2,.28)],env=(.003,.010,.5,.08),pitch_sweep=55)
        d["eat3"]=_synth(784,.12,.13,"sine",harmonics=[(2,.32),(4,.10)],env=(.003,.010,.6,.09),pitch_sweep=45)
        d["bon"]=_synth(1047,.14,.13,"sine",harmonics=[(2,.45),(3,.18)],env=(.005,.015,.5,.10),vibrato=(10,5))
        d["lvl"]=_synth(660,.22,.14,"tri",harmonics=[(2,.55),(3,.25)],env=(.008,.018,.7,.12),pitch_sweep=180)
        d["die"]=_synth(110,.42,.17,"sqr",harmonics=[(0.5,.4)],env=(.005,.04,.3,.36),pitch_sweep=-50)
        d["strt"]=_synth(528,.11,.12,"sine",harmonics=[(2,.28)],env=(.004,.010,.6,.08))
        d["pick"]=_synth(760,.08,.11,"sine",harmonics=[(2,.25)],env=(.003,.007,.5,.07))
        d["prey"]=_synth(880,.16,.13,"tri",harmonics=[(2,.3),(3,.1)],env=(.003,.010,.6,.12),pitch_sweep=180,vibrato=(8,6))
        d["thunder"]=_synth(60,.55,.22,"sqr",harmonics=[(0.5,.6),(2,.3)],env=(.002,.01,.4,.5),pitch_sweep=-30)
        d["boss_hit"]=_synth(200,.18,.18,"sqr",harmonics=[(2,.4)],env=(.002,.008,.5,.17),pitch_sweep=-80)
        d["boss_die"]=_synth(440,.6,.20,"tri",harmonics=[(2,.5),(3,.25)],env=(.01,.02,.6,.55),pitch_sweep=220)
        d["boss_warn"]=_synth(300,.28,.15,"sine",harmonics=[(2,.35)],env=(.01,.02,.5,.24),vibrato=(18,5))
        d["escaped"]=_synth(220,.22,.14,"sqr",harmonics=[(0.5,.4)],env=(.003,.01,.4,.20),pitch_sweep=-55)
        d[PS]=_synth(800,.10,.11,"sine",harmonics=[(3,.2)],env=(.004,.010,.5,.08),vibrato=(4,7))
        d[PV]=_synth(1200,.07,.11,"saw",env=(.002,.004,.5,.06),pitch_sweep=280)
        d[PM]=_synth(440,.12,.11,"tri",harmonics=[(0.5,.3)],env=(.008,.018,.5,.09))
        d[PX]=_synth(660,.10,.12,"sine",harmonics=[(2,.45),(4,.18)],env=(.004,.010,.6,.08))
        d[PG]=_synth(320,.14,.10,"sine",harmonics=[(0.5,.45),(3,.1)],env=(.015,.025,.4,.11))
        d[PF]=_synth(200,.17,.12,"sine",harmonics=[(3,.38),(5,.18)],env=(.008,.018,.5,.13),vibrato=(18,4))
        d[PL]=_synth(350,.15,.11,"tri",harmonics=[(2,.28)],env=(.008,.025,.4,.11),pitch_sweep=-70)
        d[PN]=_synth(80,.50,.18,"sqr",harmonics=[(0.5,.55),(2,.28)],env=(.004,.010,.6,.42),pitch_sweep=-35)
        d[PZ]=_synth(520,.13,.12,"sine",harmonics=[(3,.3)],env=(.003,.008,.5,.10),pitch_sweep=-120)
        d[PW]=_synth(300,.20,.14,"tri",harmonics=[(0.5,.4),(2,.2)],env=(.008,.018,.5,.16),pitch_sweep=-80,vibrato=(6,3))
        d[PH]=_synth(660,.15,.13,"sine",harmonics=[(2,.4),(4,.15)],env=(.004,.010,.6,.12),pitch_sweep=100,vibrato=(10,5))
        d[PD]=_synth(880,.09,.14,"saw",harmonics=[(2,.3)],env=(.001,.003,.5,.08),pitch_sweep=400)  # DASH: whoosh
        d[PR]=_synth(440,.12,.12,"tri",harmonics=[(2,.35)],env=(.003,.010,.5,.10),pitch_sweep=-180) # SHRINK: shrink
        d[PB2]=_synth(784,.15,.14,"sine",harmonics=[(2,.45),(3,.2)],env=(.004,.012,.6,.11),pitch_sweep=60,vibrato=(12,5))
        d[PP]=_synth(360,.18,.12,"sine",harmonics=[(0.5,.5),(3,.15)],env=(.010,.020,.4,.14),vibrato=(20,3))  # PHASE
    except: pass
    return d

SE=_build_snd()
for fb in[("eat2","eat1"),("eat3","eat1")]:
    if fb[0] not in SE and fb[1] in SE: SE[fb[0]]=SE[fb[1]]
def sfx(k):
    if k in SE:
        try: SE[k].play()
        except: pass

# ── Particles ─────────────────────────────────────
class Spark:
    __slots__=["x","y","vx","vy","life","decay","r","col"]
    def __init__(self,x,y,col,sp=1.,big=False):
        a=random.uniform(0,2*math.pi);s=random.uniform(1.2,5.5)*sp
        self.x=float(x);self.y=float(y);self.vx=math.cos(a)*s;self.vy=math.sin(a)*s
        self.life=1.;self.decay=random.uniform(.024,.062)
        self.r=random.randint(3,9) if big else random.randint(2,4)
        self.col=tuple(cl(c) for c in col[:3])
    def update(self):
        self.x+=self.vx;self.y+=self.vy;self.vy+=.09;self.vx*=.97
        self.life-=self.decay;return self.life>0
    def draw(self,surf):
        a=int(255*max(0,self.life));r=max(1,self.r)
        g=asurf(r*4+2,r*4+2)
        pygame.draw.circle(g,(*self.col,a//4),(r*2+1,r*2+1),r*2)
        surf.blit(g,(int(self.x-r*2-1),int(self.y-r*2-1)))
        s=asurf(r*2,r*2);pygame.draw.circle(s,(*self.col,a),(r,r),r)
        surf.blit(s,(int(self.x-r),int(self.y-r)))

class FloatTxt:
    __slots__=["x","y","txt","col","life","vy","big"]
    def __init__(self,x,y,txt,col,big=False):
        self.x=float(x);self.y=float(y);self.txt=str(txt)
        self.col=tuple(cl(c) for c in col[:3])
        self.life=1.;self.vy=-2.6 if big else -2.1;self.big=big
    def update(self): self.y+=self.vy;self.vy*=.92;self.life-=.018;return self.life>0
    def draw(self,surf):
        a=int(255*max(0,self.life));fnt=FB if self.big else FM
        t=fnt.render(self.txt,True,self.col)
        s=asurf(t.get_width()+2,t.get_height()+2);s.blit(t,(1,1));s.set_alpha(a)
        surf.blit(s,(int(self.x-t.get_width()//2),int(self.y)))

class Ring:
    __slots__=["x","y","r","life","col","w"]
    def __init__(self,x,y,col,w=2):
        self.x=x;self.y=y;self.r=6;self.life=1.
        self.col=tuple(cl(c) for c in col[:3]);self.w=w
    def update(self): self.r+=16;self.life-=.048;return self.life>0
    def draw(self,surf):
        a=int(150*max(0,self.life));r=max(1,self.r)
        s=asurf(r*2+8,r*2+8)
        pygame.draw.circle(s,(*self.col,a),(r+4,r+4),r,self.w)
        surf.blit(s,(self.x-r-4,self.y-r-4))

class EatBurst:
    def __init__(self,cx,cy,col): self.cx=cx;self.cy=cy;self.col=col;self.t=0.
    def update(self,dt): self.t+=dt*.005;return self.t<1.
    def draw(self,surf):
        t=self.t;c=self.col
        if t<.5:
            p=t/.5;r=int(4+20*p);a=int(210*(1-p))
            if a>4:
                s=asurf(r*2+4,r*2+4)
                pygame.draw.circle(s,(*c,a),(r+2,r+2),r,2)
                surf.blit(s,(self.cx-r-2,self.cy-r-2))
        else:
            p=(t-.5)/.5;r=int(24+10*p);a=int(70*(1-p))
            if a>4:
                s=asurf(r*2+4,r*2+4)
                pygame.draw.circle(s,(*c,a),(r+2,r+2),r,1)
                surf.blit(s,(self.cx-r-2,self.cy-r-2))
        if t<.25:
            p=t/.25;a=int(180*(1-p));r2=int(3*(1-p))+1
            if a>6:
                fs=asurf(r2*2+2,r2*2+2)
                pygame.draw.circle(fs,(*c,a),(r2+1,r2+1),r2)
                surf.blit(fs,(self.cx-r2-1,self.cy-r2-1))

# ── Rain Drop ─────────────────────────────────────
class RainDrop:
    def __init__(self):
        self.x=float(random.randint(PANEL,PANEL+W))
        self.y=float(random.randint(96-40,96+H))
        self.spd=random.uniform(8,18)
        self.len=random.randint(6,18)
        self.a=random.randint(40,110)
    def update(self):
        self.y+=self.spd
        if self.y>96+H+20:
            self.x=float(random.randint(PANEL,PANEL+W))
            self.y=float(random.randint(96-60,96-10))
    def draw(self,surf):
        s=asurf(4,self.len+4)
        pygame.draw.line(s,(180,210,255,self.a),(1,0),(3,self.len))
        surf.blit(s,(int(self.x)-2,int(self.y)-2))

# ── Snow Flake ────────────────────────────────────
class SnowFlake:
    def __init__(self):
        self.x=float(random.randint(PANEL,PANEL+W))
        self.y=float(random.randint(96-40,96+H))
        self.spd=random.uniform(1,3)
        self.drift=random.uniform(-.5,.5)
        self.r=random.randint(2,5)
        self.a=random.randint(80,200)
        self.phase=random.uniform(0,2*math.pi)
    def update(self,T):
        self.y+=self.spd
        self.x+=self.drift+math.sin(T*2+self.phase)*.4
        if self.y>96+H+20:
            self.x=float(random.randint(PANEL,PANEL+W))
            self.y=float(random.randint(96-60,96-10))
        if self.x<PANEL: self.x=float(PANEL+W)
        if self.x>PANEL+W: self.x=float(PANEL)
    def draw(self,surf):
        s=asurf(self.r*2+2,self.r*2+2)
        pygame.draw.circle(s,(220,235,255,self.a),(self.r+1,self.r+1),self.r)
        surf.blit(s,(int(self.x)-self.r-1,int(self.y)-self.r-1))

# ── Lightning Bolt (visual) ───────────────────────
class LightningBolt:
    def __init__(self):
        self.reset()
    def reset(self):
        self.segs=[]
        x=random.randint(PANEL+50,PANEL+W-50); y=96
        self.segs.append((x,y))
        while y<96+H-30:
            x+=random.randint(-30,30); y+=random.randint(18,40)
            x=max(PANEL+5,min(PANEL+W-5,x))
            self.segs.append((x,y))
        self.life=1.; self.active=True
    def update(self,dt):
        self.life-=dt*.006
        if self.life<=0: self.active=False
    def draw(self,surf):
        if not self.active or len(self.segs)<2: return
        a=int(220*max(0,self.life))
        for i in range(len(self.segs)-1):
            x1,y1=self.segs[i]; x2,y2=self.segs[i+1]
            # glow
            gs=asurf(abs(x2-x1)+20,abs(y2-y1)+20)
            ox=min(x1,x2)-10; oy=min(y1,y2)-10
            pygame.draw.line(surf,(180,200,255,a//5),(x1,y1),(x2,y2),8)
            pygame.draw.line(surf,(220,230,255,a//2),(x1,y1),(x2,y2),3)
            pygame.draw.line(surf,(255,255,255,a),(x1,y1),(x2,y2),1)

# ── Weather System ────────────────────────────────
class Weather:
    def __init__(self):
        self.kind=WN
        self.timer=WEATHER_DUR
        self.transition=0.  # 0→1 fade in
        self.rain=[RainDrop() for _ in range(120)]
        self.snow=[SnowFlake() for _ in range(80)]
        self.bolts=[]
        self.bolt_t=0.; self.bolt_cd=random.uniform(5,12)  # seconds between bolts
        self.flash=0.   # screen white flash
        self.blind=0.   # darkness overlay
        self.slip=False # rain slippery
        self.frozen=False
        self.next_weather=WN
        self.warn_t=0.  # warning before change

    def set(self,kind):
        self.kind=kind; self.timer=WEATHER_DUR; self.transition=0.
        self.slip=(kind==WR); self.frozen=(kind==WS)
        self.bolts=[]; self.bolt_t=0.

    @property
    def spd_mult(self):
        if self.kind==WS: return .82
        return 1.

    @property
    def active(self): return self.kind!=WN

    def update(self,dt,T):
        self.timer-=dt
        if self.transition<1.: self.transition=min(1.,self.transition+dt*.001)
        if self.flash>0: self.flash=max(0,self.flash-dt*.008)
        if self.blind>0: self.blind=max(0,self.blind-dt*.004)
        if self.timer<=0:
            choices=[WN,WR,WS,WL]
            choices=[c for c in choices if c!=self.kind]
            self.set(random.choice(choices))
        # rain update
        if self.kind==WR:
            for r in self.rain: r.update()
        # snow update
        if self.kind==WS:
            for s in self.snow: s.update(T)
        # lightning update
        if self.kind==WL:
            self.bolt_t+=dt*.001
            if self.bolt_t>=self.bolt_cd:
                self.bolt_t=0.; self.bolt_cd=random.uniform(4,10)
                b=LightningBolt(); self.bolts.append(b)
                self.flash=1.; self.blind=.7
                sfx("thunder")
            self.bolts=[b for b in self.bolts if (b.update(dt) or True) and b.active]

    def draw_bg(self,surf,T):
        """Draw weather effects behind snake"""
        alpha=int(255*min(1.,self.transition))
        if self.kind==WR:
            for r in self.rain: r.draw(surf)
            # rain tint
            ov=asurf(W,H); ov.fill((10,20,40,int(38*self.transition))); surf.blit(ov,(PANEL,96))
        if self.kind==WS:
            # snow tint – bright
            ov=asurf(W,H); ov.fill((200,220,255,int(22*self.transition))); surf.blit(ov,(PANEL,96))
            for s in self.snow: s.draw(surf)
        if self.kind==WL:
            for b in self.bolts: b.draw(surf)
            if self.flash>0:
                ov=asurf(W,H); ov.fill((255,255,255,int(self.flash*130))); surf.blit(ov,(PANEL,96))
            if self.blind>0:
                ov=asurf(W,H); ov.fill((0,0,5,int(self.blind*170))); surf.blit(ov,(PANEL,96))

    def draw_hud(self,surf,T):
        if self.kind==WN: return
        icons={WR:"🌧 RAIN — slippery",WS:"❄ SNOW — slow",WL:"⚡ STORM — blind"}
        cols={WR:(100,160,255),WS:(180,220,255),WL:(255,240,100)}
        txt=icons.get(self.kind,""); col=cols.get(self.kind,WHT)
        pulse=abs(math.sin(T*2))
        tc(surf,txt,FXS,tuple(cl(c*(0.6+0.4*pulse)) for c in col),PANEL+W-110,SH-18)
        # weather timer bar
        frac=max(0,self.timer/WEATHER_DUR)
        nbar(surf,PANEL+W-195,SH-8,180,4,frac,1.,col,2)

# ── Boss ──────────────────────────────────────────
class Boss:
    def __init__(self,level,ox,oy):
        info=BOSSES[level]
        self.level=level; self.name=info["name"]
        self.col=info["col"]; self.max_hp=info["hp"]; self.hp=info["hp"]
        self.atk=info["atk"]; self.kill_pu=BOSS_KILL_PU[level]
        # Position: wanders the grid
        self.pos=(random.randint(4,COLS-5),random.randint(4,ROWS-5))
        self.mv_t=0.; self.mv_spd=3.0  # base — increases with score
        self.phase=random.uniform(0,2*math.pi)
        self.alive=True; self.enter_t=0.  # 0→1 entrance anim
        self.atk_t=0.; self.atk_cd=random.uniform(2.5,5)  # attack cooldown sec
        self.projectiles=[]  # kept for compat
        self.warn_zones=[]  # {pos, life, max}
        self.warn_t=3.      # 3s warning before appearing
        self.anger=0.        # 0→1 based on low hp
        self.ox=ox; self.oy=oy

    @property
    def done(self): return not self.alive

    def take_hit(self,game_score=0):
        self.hp-=1
        if self.hp<=0: self.alive=False
        hp_anger=1-self.hp/self.max_hp
        # Also gets angrier based on game score (max +0.3 bonus anger)
        score_anger=min(0.3, game_score/1500.0)
        self.anger=min(1.0, hp_anger+score_anger)

    def _move(self,snake,solid):
        """Wanders — avoids snake body, mild chasing"""
        hx,hy=snake[0]; bx,by=self.pos
        # Move away from snake if too close (distance < 5)
        dist=abs(hx-bx)+abs(hy-by)
        opts=[(d,((bx+d[0])%COLS,(by+d[1])%ROWS)) for d in[UP,DOWN,LEFT,RIGHT]]
        opts=[(d,p) for d,p in opts if p not in solid and p not in set(snake)]
        if not opts: return
        if dist<5:
            # flee
            opts.sort(key=lambda x:-(abs(x[1][0]-hx)+abs(x[1][1]-hy)))
        else:
            # wander randomly
            random.shuffle(opts)
        self.pos=opts[0][1]

    def _chase(self,snake,solid):
        """Higher level bosses hunt the snake head via BFS"""
        from collections import deque
        start=self.pos; target=snake[0]
        if start==target: return
        blocked=solid-{start}
        q=deque([(start,[start])]); vis={start}
        while q:
            cur,path=q.popleft()
            for d in[UP,DOWN,LEFT,RIGHT]:
                nx=((cur[0]+d[0])%COLS,(cur[1]+d[1])%ROWS)
                if nx in vis: continue
                if nx in blocked: continue
                vis.add(nx); np2=path+[nx]
                if nx==target:
                    self.pos=np2[1] if len(np2)>1 else start
                    return
                q.append((nx,np2))
        # fallback: wander
        self._move(snake,solid)

    def _attack(self,snake,solid,texts,sparks,rings):
        """
        Warning zones: flashing red cells that appear for 1.5s.
        If snake head enters one = hit. No physical blockers.
        """
        hx,hy=snake[0]
        if self.atk=="rocks":
            # 3-4 warning zones around snake, NOT on head
            n=random.randint(3,4+int(self.anger*2))
            for _ in range(n*8):
                if len(self.warn_zones)>=n: break
                rx=hx+random.randint(-4,4); ry=hy+random.randint(-4,4)
                rx=max(1,min(COLS-2,rx)); ry=max(1,min(ROWS-2,ry))
                if (rx,ry)==(hx,hy): continue
                if (rx,ry) not in [z["pos"] for z in self.warn_zones]:
                    self.warn_zones.append({"pos":(rx,ry),"life":1500.,"max":1500.})
        elif self.atk=="lightning":
            # Strike: 2 random cross patterns
            for _ in range(2):
                rx=random.randint(2,COLS-3); ry=random.randint(2,ROWS-3)
                for dx in range(-1,2):
                    self.warn_zones.append({"pos":((rx+dx)%COLS,ry),"life":1200.,"max":1200.})
                for dy in range(-1,2):
                    if dy!=0:
                        self.warn_zones.append({"pos":(rx,(ry+dy)%ROWS),"life":1200.,"max":1200.})
            cx2=PANEL+W//2; cy2=96+H//2
            for _ in range(3): rings.append(Ring(cx2,cy2,(100,180,255),w=3))
        elif self.atk=="freeze":
            # Freeze: ring of zones around snake
            for ang_i in range(8):
                ang=ang_i*math.pi/4
                rx=int(hx+math.cos(ang)*3)%COLS
                ry=int(hy+math.sin(ang)*3)%ROWS
                self.warn_zones.append({"pos":(rx,ry),"life":1800.,"max":1800.})

    def update(self,dt,snake,solid,texts,sparks,rings,weather):
        if not self.alive: return False
        if self.warn_t>0:
            self.warn_t-=dt*.001
            return False
        if self.enter_t<1.: self.enter_t=min(1.,self.enter_t+dt*.002)
        self.mv_t+=dt*.001
        # Speed increases with anger AND game difficulty
        eff_spd=self.mv_spd*(1+self.anger*.8)
        if self.mv_t>=1/max(0.5,eff_spd):
            self.mv_t=0
            # Always chase — no random wandering for hard bosses
            chase_prob=0.55+self.anger*.45
            if self.level>=10: chase_prob=0.85+self.anger*.15
            if random.random()<chase_prob:
                self._chase(snake,solid)
            else:
                self._move(snake,solid)
        self.atk_t+=dt*.001
        hit_player=False
        if self.atk_t>=self.atk_cd:
            self.atk_t=0.; self.atk_cd=max(1.5,random.uniform(3-self.anger*1.2,5-self.anger*2))
            self._attack(snake,solid,texts,sparks,rings)
            sfx("boss_warn")
            hx,hy=snake[0]
            cx2=self.ox+hx*CELL+CELL//2; cy2=self.oy+hy*CELL+CELL//2
            if self.atk=="lightning":
                for _ in range(35): sparks.append(Spark(cx2,cy2,(100,180,255),sp=1.5,big=True))
                for _ in range(3): rings.append(Ring(cx2,cy2,(100,180,255),w=3))
                texts.append(FloatTxt(cx2,cy2-28,"STRUCK!",( 100,180,255),big=True))
                hit_player=True
            elif self.atk=="freeze":
                hit_player="stun"
        # Warn zones: count down, check if snake head enters
        hx2,hy2=snake[0]; new_wz=[]
        for z in self.warn_zones:
            z["life"]-=dt
            if z["life"]>0:
                # Hit when zone is ACTIVE (life < 40% of max = strike phase)
                strike_phase=z["life"]<z["max"]*.4
                if strike_phase and z["pos"]==(hx2,hy2):
                    hit_player=True
                else:
                    new_wz.append(z)
        self.warn_zones=new_wz
        return hit_player

    def get_solid(self):
        return set()  # No physical obstacles from boss

    def draw(self,surf,T):
        if not self.alive or self.warn_t>0: return
        bx,by=self.pos
        cx=self.ox+bx*CELL+CELL//2; cy=self.oy+by*CELL+CELL//2
        sc=self.enter_t; col=self.col
        r=int((CELL//2+4)*sc)
        if r<2: return
        # Anger colour shift
        acol=lc(col,(220,60,60),self.anger*.7)
        # Glow
        gr=int((r+8+6*abs(math.sin(T*3+self.phase)))*(1+self.anger*.5))
        cglow(surf,cx,cy,gr,acol,int(40+30*self.anger))
        # Body
        bs=asurf(r*2+4,r*2+4)
        pygame.draw.circle(bs,(*acol,220),(r+2,r+2),r)
        # Spikes (rotating)
        n_spikes=6+int(self.anger*4)
        for i in range(n_spikes):
            ang=T*1.2+i*2*math.pi/n_spikes+self.phase
            sx=cx+int(math.cos(ang)*(r+6)); sy=cy+int(math.sin(ang)*(r+6))
            sx2=cx+int(math.cos(ang)*(r-2)); sy2=cy+int(math.sin(ang)*(r-2))
            pygame.draw.line(surf,acol,(sx2,sy2),(sx,sy),2)
        # Face
        pygame.draw.circle(surf,(10,10,10),(cx,cy),r)
        pygame.draw.circle(surf,acol,(cx,cy),r-1)
        # Eyes — glowing red
        er=max(2,r//4)
        for ex_off in[-r//3,r//3]:
            ex=cx+ex_off; ey=cy-r//6
            pygame.draw.circle(surf,(255,50,50),(ex,ey),er)
            pygame.draw.circle(surf,(255,180,180),(ex,ey),max(1,er//2))
        # Name tag
        if self.enter_t>0.8:
            nt=FXX.render(self.name,True,acol)
            ns=asurf(nt.get_width()+4,nt.get_height()+2); ns.blit(nt,(2,1)); ns.set_alpha(200)
            surf.blit(ns,(cx-nt.get_width()//2-2,cy-r-16))
        # HP bar
        bar_w=CELL*3; bar_x=cx-bar_w//2; bar_y=cy+r+4
        pygame.draw.rect(surf,(20,8,8),(bar_x,bar_y,bar_w,5),border_radius=2)
        fw=int(bar_w*self.hp/self.max_hp)
        if fw>0:
            bc=lc((255,60,60),(255,200,60),self.hp/self.max_hp)
            pygame.draw.rect(surf,bc,(bar_x,bar_y,fw,5),border_radius=2)
        # Warning zones — clear visual phases
        for z in self.warn_zones:
            zx,zy=z["pos"]; life_f=z["life"]/z["max"]
            rx2=self.ox+zx*CELL; ry2=self.oy+zy*CELL
            cx_r=rx2+CELL//2; cy_r=ry2+CELL//2
            strike=(life_f<0.38)
            if strike:
                # RED STRIKE — danger, get out!
                pulse=abs(math.sin(T*16))
                col_z=(255,30,30)
                a_z=int(180+65*pulse)
                ws=asurf(CELL,CELL)
                pygame.draw.rect(ws,(*col_z,a_z),(0,0,CELL,CELL),border_radius=3)
                # X mark
                pygame.draw.line(ws,(255,200,200,230),(3,3),(CELL-3,CELL-3),2)
                pygame.draw.line(ws,(255,200,200,230),(CELL-3,3),(3,CELL-3),2)
                surf.blit(ws,(rx2,ry2))
                cglow(surf,cx_r,cy_r,CELL//2+5,col_z,int(90+55*pulse))
            else:
                # YELLOW WARNING — time to move
                pulse=abs(math.sin(T*6))
                urgency=1-life_f  # more urgent as time runs out
                col_z=(255,int(200-urgency*100),20)
                a_z=int(55+80*pulse+urgency*60)
                ws=asurf(CELL,CELL)
                pygame.draw.rect(ws,(*col_z,a_z),(1,1,CELL-2,CELL-2),border_radius=5)
                # Warning triangle
                pts=[(CELL//2,4),(4,CELL-4),(CELL-4,CELL-4)]
                pygame.draw.polygon(ws,(*col_z,int(130*pulse+urgency*100)),pts)
                surf.blit(ws,(rx2,ry2))
                if urgency>0.5:
                    cglow(surf,cx_r,cy_r,CELL//2+3,col_z,int(40*pulse))

    def draw_warn(self,surf,T):
        if self.warn_t<=0 or self.warn_t>3: return
        frac=self.warn_t/3.
        cx2=PANEL+W//2; cy2=96+H//2
        pulse=abs(math.sin(T*6))
        col=tuple(cl(c*(0.5+0.5*pulse)) for c in self.col)
        glow_tc(surf,f"⚠ {self.name} INCOMING ⚠",FT,col,cx2,cy2-60,4)
        tc(surf,f"Use {PU_ICO[self.kill_pu]} power-up to damage it!",FM,DIM,cx2,cy2-20)
        # countdown
        tc(surf,f"{int(self.warn_t)+1}",FXL,col,cx2,cy2+30)

# ── Prey (v2 — smarter) ───────────────────────────
class Prey:
    """
    Haro wst l map — ma kaymshich l 7it.
    Kayhreb mnk dima. 15 sec tnchdoh = points.
    Itla3 l combo ila fetek.
    """
    LIFE=15000
    # Note: skill "prey_time" adds 5000ms — applied in Game._spawn_prey()

    def __init__(self,pos,col):
        self.pos=pos; self.col=col; self.life=self.LIFE; self.alive=True
        self.mv_t=0
        # Speed: slow when far, fast when panicking
        self.spd=4          # moves/sec base (easy to chase from far)
        self.flee_spd=5.5   # moves/sec when fleeing (catchable with effort)
        self.phase=random.uniform(0,2*math.pi)
        self.fleeing=False
        self.escape_noted=False
        # No wall target — wanders map center
        # Pick a random MODE_MENU zone in the middle 60% of the map
        self.wander_t=0.
        self.wander_target=self._new_wander()
        self.has_pu=random.random()>.45
        self.pu_kind=random.choice([PS,PV,PX,PM,PZ,PW,PH,PD,PR,PB2,PP]) if self.has_pu else None

    def _new_wander(self):
        """Pick a random cell in the centre zone (not walls)"""
        mx=random.randint(COLS//5, COLS*4//5)
        my=random.randint(ROWS//5, ROWS*4//5)
        return (mx, my)

    @property
    def done(self): return not self.alive or self.life<=0

    def _next_step(self,snake,solid):
        """Simple: flee from head if close, else wander. Only avoid solid obstacles."""
        hx,hy=snake[0]; px,py=self.pos
        dist=abs(hx-px)+abs(hy-py)
        # Only blocked by solid obstacles — NOT by snake body
        blocked=solid
        opts=[]
        for d in[UP,DOWN,LEFT,RIGHT]:
            nx=((px+d[0])%COLS,(py+d[1])%ROWS)
            # avoid walls (border cells) and solid obstacles
            if nx[0]<=0 or nx[0]>=COLS-1: continue
            if nx[1]<=0 or nx[1]>=ROWS-1: continue
            if nx in blocked: continue
            opts.append(nx)
        if not opts:
            # nowhere to go — try including walls
            for d in[UP,DOWN,LEFT,RIGHT]:
                nx=((px+d[0])%COLS,(py+d[1])%ROWS)
                if nx not in blocked: opts.append(nx)
        if not opts: return (px,py)
        if self.fleeing:
            # Flee: far from head AND avoid snake body
            body=set(snake[:8])
            def flee_score(p):
                d_head=abs(p[0]-hx)+abs(p[1]-hy)
                d_body=min((abs(p[0]-sx)+abs(p[1]-sy) for sx,sy in body),default=0)
                return d_head+d_body*.7
            opts.sort(key=lambda p:-flee_score(p))
            return opts[0]
        else:
            # Wander: move toward wander_target
            if self.pos==self.wander_target or random.random()<.04:
                self.wander_target=self._new_wander()
            tx,ty=self.wander_target
            opts.sort(key=lambda p: abs(p[0]-tx)+abs(p[1]-ty))
            return opts[0]

    def update(self,dt,snake,solid,weather_spd=1.):
        if self.done: return
        self.life-=dt
        hx,hy=snake[0]; px,py=self.pos
        dist=abs(hx-px)+abs(hy-py)
        self.fleeing=(dist<=6)
        cur_spd=(self.flee_spd if self.fleeing else self.spd)*weather_spd
        self.mv_t+=dt
        if self.mv_t>=1000/max(1,cur_spd):
            self.mv_t=0
            self.pos=self._next_step(snake,solid)

    def draw(self,surf,ox,oy,T):
        if self.done: return
        px,py=self.pos
        cx=ox+px*CELL+CELL//2; cy=oy+py*CELL+CELL//2
        frac=max(0,self.life/self.LIFE)
        # Pulse faster when time running out
        pulse_rate=9+6*(1-frac)
        pulse=1.+.18*abs(math.sin(T*pulse_rate+self.phase))
        r=max(7,int(CELL//2.2*pulse))

        # Colour: bright when calm, reddish when panicking
        if self.fleeing:
            col=lc(self.col,(255,60,60),.65)
        else:
            col=lc(self.col,(255,180,80),max(0,1-frac*1.2))

        # Glow — bigger + brighter when fleeing
        glow_a=int(50+30*abs(math.sin(T*4))) if not self.fleeing else int(80+50*abs(math.sin(T*10)))
        cglow(surf,cx,cy,r+5+(4 if self.fleeing else 0),col,glow_a)

        # Shadow
        sh=asurf(r*2+2,4); pygame.draw.ellipse(sh,(0,0,0,40),(0,0,r*2+2,4))
        surf.blit(sh,(cx-r-1,cy+r-1))

        # Body
        bs=asurf(r*2+2,r*2+2)
        pygame.draw.circle(bs,(*col,215),(r+1,r+1),r)
        pygame.draw.circle(bs,(*WHT,55),(max(1,r+1-r//3),max(1,r+1-r//3)),max(1,r//3))
        surf.blit(bs,(cx-r-1,cy-r-1))

        # Eyes — look AWAY from snake when fleeing, look toward wander target otherwise
        ey_r=max(2,r//3)
        hx2,hy2=0,0  # will be set below
        try: hx2,hy2=self.wander_target
        except: pass
        if self.fleeing:
            # Scared: wide eyes, pupils look away from snake
            from pygame.locals import SRCALPHA
            hx_s=ox//CELL; hy_s=oy//CELL  # dummy
            # look away: opposite of snake direction
            # get snake head screen pos
            angle=math.atan2(py - (cy-oy)//CELL, px-(cx-ox)//CELL)+math.pi
        else:
            tx2,ty2=self.wander_target
            angle=math.atan2(ty2-py, tx2-px)

        for ex_off in[-r//3,r//3]:
            ex=cx+ex_off; ey=cy-r//5
            eye_r=ey_r+1 if self.fleeing else ey_r  # bigger eyes when scared
            es=asurf(eye_r*2+2,eye_r*2+2)
            pygame.draw.circle(es,(*WHT,220),(eye_r+1,eye_r+1),eye_r)
            surf.blit(es,(ex-eye_r-1,ey-eye_r-1))
            pupil_r=max(1,eye_r//2)
            pp2x=int(math.cos(angle)*eye_r*.4); pp2y=int(math.sin(angle)*eye_r*.4)
            pygame.draw.circle(surf,(10,10,10),(ex+pp2x,ey+pp2y),pupil_r)
            pygame.draw.circle(surf,WHT,(ex+pp2x-1,ey+pp2y-1),max(1,pupil_r//3))

        # Sweat drops when fleeing
        if self.fleeing:
            for si in range(3):
                sx=cx+r//2+si*5; sy=cy-r//3-si*4
                a_sw=int(200-si*40)
                swt=asurf(5,8)
                pygame.draw.ellipse(swt,(120,180,255,a_sw),(0,0,4,7))
                surf.blit(swt,(sx,sy))
            # Panic lines (motion blur)
            for li in range(3):
                la=int(80-li*20); lr=r+8+li*3
                ls=asurf(lr*2+4,lr*2+4)
                pygame.draw.circle(ls,(*col,la),(lr+2,lr+2),lr,1)
                surf.blit(ls,(cx-lr-2,cy-lr-2))

        # Frown when <40% time
        if frac<.4:
            fa=int(200*(1-frac/.4))
            pygame.draw.arc(surf,(*col,fa),(cx-r//3,cy+r//6,r*2//3,r//3),math.pi,2*math.pi,2)

        # Power-up badge
        if self.has_pu and self.pu_kind:
            pc=PU_COL[self.pu_kind]
            cglow(surf,cx+r,cy-r,7,pc,70)
            badge=asurf(16,16); pygame.draw.circle(badge,(*pc,210),(8,8),7); surf.blit(badge,(cx+r-8,cy-r-8))
            pt=FXX.render(PU_ICO[self.pu_kind][:1],True,WHT)
            surf.blit(pt,(cx+r-pt.get_width()//2,cy-r-pt.get_height()//2))

        # Timer bar — above head, red flash at end
        bw=int(CELL*frac)
        if bw>1:
            if frac<.3:
                flash=abs(math.sin(T*12))
                bar_col=lc(DNG,WHT,flash*.5)
            else:
                bar_col=lc(DNG,self.col,frac)
            pygame.draw.rect(surf,(0,0,0,90),(ox+px*CELL,oy+py*CELL-6,CELL,4))
            pygame.draw.rect(surf,(*bar_col,200),(ox+px*CELL,oy+py*CELL-6,bw,4))

# ── Obstacle ──────────────────────────────────────
# ═══════════════════════════════════════════════════════
#  H A Z A R D   S Y S T E M
# ═══════════════════════════════════════════════════════

class HazardVortex:
    """Spinning zones — if snake head enters, direction rotates 90°"""
    def __init__(self):
        self.zones=[]   # list of {pos, spin, life}
        self.spawn_t=0.; self.spawn_cd=8.
    def reset(self):
        self.zones=[]; self.spawn_t=0.
    def update(self,dt,snake_set,solid):
        self.spawn_t+=dt*.001
        if self.spawn_t>=self.spawn_cd:
            self.spawn_t=0.; self.spawn_cd=random.uniform(6,12)
            for _ in range(50):
                x=random.randint(3,COLS-4); y=random.randint(3,ROWS-4)
                if (x,y) not in snake_set and (x,y) not in solid:
                    spin=random.choice([-1,1])  # -1=CCW, +1=CW
                    self.zones.append({"pos":(x,y),"spin":spin,"life":random.uniform(8,16),"T":0.})
                    break
        keep=[]
        for z in self.zones:
            z["life"]-=dt*.001; z["T"]+=dt*.001
            if z["life"]>0: keep.append(z)
        self.zones=keep
    def apply(self,head,dirn):
        """Returns new direction if head in vortex"""
        SPIN_CW ={UP:RIGHT,RIGHT:DOWN,DOWN:LEFT,LEFT:UP}
        SPIN_CCW={UP:LEFT,LEFT:DOWN,DOWN:RIGHT,RIGHT:UP}
        for z in self.zones:
            if z["pos"]==head:
                return SPIN_CW[dirn] if z["spin"]==1 else SPIN_CCW[dirn], True
        return dirn, False
    def draw(self,surf,ox,oy,T):
        for z in self.zones:
            x,y=z["pos"]; px=ox+x*CELL; py=oy+y*CELL
            frac=min(1.,z["life"]/3.)
            col=(100,200,255) if z["spin"]==1 else (255,140,100)
            a=int(60*frac*abs(math.sin(T*4+z["T"])))
            s=asurf(CELL,CELL); pygame.draw.rect(s,(*col,a),(0,0,CELL,CELL),border_radius=6)
            surf.blit(s,(px,py))
            # Spinning arrow
            ang=T*2*z["spin"]+z["T"]
            cr=CELL//2-3; cx2=px+CELL//2; cy2=py+CELL//2
            for i in range(4):
                a2=ang+i*math.pi/2
                x1=cx2+int(math.cos(a2)*cr); y1=cy2+int(math.sin(a2)*cr)
                x2=cx2+int(math.cos(a2+0.6)*(cr-4)); y2=cy2+int(math.sin(a2+0.6)*(cr-4))
                aa=int(120*frac*abs(math.sin(T*3)))
                if aa>10:
                    ls=asurf(SW,SH); pygame.draw.line(ls,(*col,aa),(x1,y1),(x2,y2),2)
                    surf.blit(ls,(0,0))


class HazardPortal:
    """Pairs of portals — enter one, exit the other"""
    def __init__(self):
        self.pairs=[]   # list of [(pos_a,col_a),(pos_b,col_b)]
        self.spawn_t=0.; self.spawn_cd=12.
        self.teleport_flash=0.
    def reset(self):
        self.pairs=[]; self.spawn_t=0.
    def _free_pos(self,taken):
        for _ in range(200):
            x=random.randint(2,COLS-3); y=random.randint(2,ROWS-3)
            if (x,y) not in taken: return (x,y)
        return None
    def update(self,dt,snake_set,solid):
        self.spawn_t+=dt*.001
        if self.spawn_t>=self.spawn_cd and len(self.pairs)<3:
            self.spawn_t=0.; self.spawn_cd=random.uniform(10,18)
            taken=snake_set|solid|{p for pair in self.pairs for p,_ in pair}
            pa=self._free_pos(taken)
            if pa:
                taken.add(pa); pb=self._free_pos(taken)
                if pb:
                    col=hsv(random.random(),.8,.9)
                    self.pairs.append([(pa,col),(pb,col)])
        # Expire old pairs
        for p in self.pairs:
            p[0]=list(p[0]); p[1]=list(p[1])
        # Keep up to 3
        if len(self.pairs)>3: self.pairs=self.pairs[-3:]
        if self.teleport_flash>0: self.teleport_flash-=dt*.005
    def apply(self,head):
        """Returns teleport destination or None"""
        for pair in self.pairs:
            (pa,ca),(pb,cb)=pair
            if head==pa: return pb
            if head==pb: return pa
        return None
    def draw(self,surf,ox,oy,T):
        for pair in self.pairs:
            for pos,col in pair:
                if not isinstance(pos,tuple): continue
                x,y=pos; px=ox+x*CELL; py=oy+y*CELL
                cx2=px+CELL//2; cy2=py+CELL//2
                r=int(CELL//2-1+2*abs(math.sin(T*3)))
                # Glow rings
                for ri in range(3):
                    a=int(40-ri*12); rr=r+ri*3
                    gs=asurf(rr*2+4,rr*2+4)
                    pygame.draw.circle(gs,(*col,a),(rr+2,rr+2),rr)
                    surf.blit(gs,(cx2-rr-2,cy2-rr-2))
                # Inner portal
                ps=asurf(CELL,CELL)
                pygame.draw.circle(ps,(*col,160),(CELL//2,CELL//2),r)
                # Swirl inside
                for i in range(6):
                    ang=T*3+i*math.pi/3
                    sx2=CELL//2+int(math.cos(ang)*(r-4))
                    sy2=CELL//2+int(math.sin(ang)*(r-4))
                    pygame.draw.circle(ps,(*WHT,60),(sx2,sy2),2)
                surf.blit(ps,(px,py))
        if self.teleport_flash>0:
            fov=asurf(W,H); fov.fill((*WHT,int(self.teleport_flash*180)))
            surf.blit(fov,(PANEL,96))


class HazardDark:
    """Dark patches that hide grid — move slowly"""
    def __init__(self):
        self.patches=[]
        self.spawn_t=0.
    def reset(self):
        n=random.randint(4,7)
        self.patches=[{"x":float(random.randint(2,COLS-3)),
                        "y":float(random.randint(2,ROWS-3)),
                        "r":random.randint(2,4),
                        "vx":random.uniform(-.04,.04),
                        "vy":random.uniform(-.04,.04),
                        "phase":random.uniform(0,math.pi*2)} for _ in range(n)]
    def update(self,dt,*a):
        for p in self.patches:
            p["x"]+=p["vx"]; p["y"]+=p["vy"]
            if p["x"]<2 or p["x"]>COLS-3: p["vx"]*=-1
            if p["y"]<2 or p["y"]>ROWS-3: p["vy"]*=-1
    def in_dark(self,gx,gy):
        for p in self.patches:
            if abs(gx-p["x"])+abs(gy-p["y"])<p["r"]+0.5:
                return True
        return False
    def draw(self,surf,ox,oy,T):
        for p in self.patches:
            cx2=int(ox+p["x"]*CELL+CELL//2); cy2=int(oy+p["y"]*CELL+CELL//2)
            r=int((p["r"]+.5)*CELL)
            pulse=.85+.12*math.sin(T*1.5+p["phase"])
            rr=int(r*pulse)
            ds=asurf(rr*2+4,rr*2+4)
            # Soft dark circle
            for ri in range(5):
                a=int(200*(1-ri/5)**2)
                pygame.draw.circle(ds,(0,0,0,a),(rr+2,rr+2),max(1,rr-ri*4))
            surf.blit(ds,(cx2-rr-2,cy2-rr-2))


class HazardSpeedtrap:
    """Gold cells — enter = instant speed boost for 2 moves"""
    def __init__(self):
        self.traps=[]
        self.active_boost=0  # moves remaining
    def reset(self):
        n=random.randint(5,9)
        taken=set()
        self.traps=[]
        for _ in range(n*10):
            if len(self.traps)>=n: break
            x=random.randint(2,COLS-3); y=random.randint(2,ROWS-3)
            if (x,y) not in taken:
                taken.add((x,y)); self.traps.append((x,y))
    def update(self,dt,*a):
        if self.active_boost>0: self.active_boost-=1
    def apply(self,head):
        if head in self.traps:
            self.traps=[t for t in self.traps if t!=head]
            self.active_boost=4  # 4 extra fast moves
            return True
        return False
    @property
    def boosting(self): return self.active_boost>0
    def draw(self,surf,ox,oy,T):
        for x,y in self.traps:
            px=ox+x*CELL; py=oy+y*CELL
            pulse=abs(math.sin(T*4+(x+y)*.5))
            a=int(80+60*pulse)
            ts=asurf(CELL,CELL)
            pygame.draw.rect(ts,(255,200,30,a),(1,1,CELL-2,CELL-2),border_radius=5)
            # Lightning bolt
            mx=CELL//2; my=CELL//2
            pts=[(mx,2),(mx-4,my),(mx+2,my),(mx-2,CELL-3),(mx+5,my-2),(mx-1,my-2)]
            pygame.draw.polygon(ts,(255,240,80,int(160*pulse)),pts)
            surf.blit(ts,(px,py))


class HazardGravity:
    """Constant pull in one direction — every N moves you drift"""
    def __init__(self):
        self.pull=DOWN   # gravity direction
        self.drift_t=0.
        self.drift_cd=3.0  # seconds between drift
        self.pull_col=(255,80,100)
        self.indicator_t=0.
    def reset(self):
        self.pull=random.choice([DOWN,LEFT,RIGHT])
        self.drift_cd=random.uniform(2.5,4.)
        self.drift_t=0.
    def update(self,dt,*a):
        self.drift_t+=dt*.001
        self.indicator_t+=dt*.001
    @property
    def should_drift(self):
        if self.drift_t>=self.drift_cd:
            self.drift_t=0.; return True
        return False
    @property
    def drift_frac(self): return min(1.,self.drift_t/self.drift_cd)
    def draw(self,surf,ox,oy,T):
        # Arrow border showing gravity direction
        col=self.pull_col
        arrows={DOWN:(PANEL+W//2,96+H-16,0,1),
                LEFT:(PANEL+16,96+H//2,-1,0),
                RIGHT:(PANEL+W-16,96+H//2,1,0)}
        if self.pull in arrows:
            ax,ay,dx2,dy2=arrows[self.pull]
            pulse=abs(math.sin(T*3))
            a2=int(80+60*pulse)
            # Draw arrow
            pts=[(ax+dx2*14,ay+dy2*14),
                 (ax+dy2*8-dx2*4,ay-dx2*8-dy2*4),
                 (ax-dy2*8-dx2*4,ay+dx2*8-dy2*4)]
            as2=asurf(SW,SH); pygame.draw.polygon(as2,(*col,a2),pts); surf.blit(as2,(0,0))
            # Progress bar showing when next drift is
            frac=self.drift_frac
            if frac>0.7:  # warn when approaching
                warn_a=int(100*(frac-.7)/.3)
                pygame.draw.rect(surf,(*col,warn_a),(PANEL+20,96+H-8,int((W-40)*frac),4),border_radius=2)


class HazardElectric:
    """Rows/cols of electric fence — move periodically"""
    def __init__(self):
        self.fences=[]   # list of {axis:'h'or'v', idx:int, life:float, max:float}
        self.spawn_t=0.; self.spawn_cd=5.
    def reset(self):
        self.fences=[]; self.spawn_t=0.
    def update(self,dt,*a):
        self.spawn_t+=dt*.001
        if self.spawn_t>=self.spawn_cd and len(self.fences)<4:
            self.spawn_t=0.; self.spawn_cd=random.uniform(4,7)
            axis=random.choice(['h','v'])
            if axis=='h': idx=random.randint(3,ROWS-4)
            else:         idx=random.randint(3,COLS-4)
            self.fences.append({"axis":axis,"idx":idx,"life":4000.,"max":4000.})
        keep=[]
        for f in self.fences:
            f["life"]-=dt
            if f["life"]>0: keep.append(f)
        self.fences=keep
    def is_live(self,gx,gy):
        """Returns True if cell is on a live fence (danger phase = life<40%)"""
        for f in self.fences:
            if f["life"]>f["max"]*.35: continue  # warning phase only
            if f["axis"]=='h' and gy==f["idx"]: return True
            if f["axis"]=='v' and gx==f["idx"]: return True
        return False
    def draw(self,surf,ox,oy,T):
        for f in self.fences:
            frac=f["life"]/f["max"]
            live=(frac<0.35)
            col=(255,50,50) if live else (255,220,50)
            a=int(130*abs(math.sin(T*(12 if live else 5))))
            if f["axis"]=='h':
                y=oy+f["idx"]*CELL
                fs=asurf(W,CELL); fs.fill((*col,a))
                surf.blit(fs,(ox,y))
                # Spark dots along fence
                if live:
                    for xi in range(0,W,CELL//2):
                        sa=int(200*abs(math.sin(T*15+xi*.3)))
                        cglow(surf,ox+xi,y+CELL//2,4,col,sa//3)
                        pygame.draw.circle(surf,WHT,(ox+xi,y+CELL//2),1)
            else:
                x=ox+f["idx"]*CELL
                fs=asurf(CELL,H); fs.fill((*col,a))
                surf.blit(fs,(x,oy))
                if live:
                    for yi in range(0,H,CELL//2):
                        sa=int(200*abs(math.sin(T*15+yi*.3)))
                        cglow(surf,x+CELL//2,oy+yi,4,col,sa//3)
                        pygame.draw.circle(surf,WHT,(x+CELL//2,oy+yi),1)


class HazardMaze:
    """Energy wall segments that shift every few seconds"""
    def __init__(self):
        self.walls=set()  # set of (x,y) cells blocked by energy
        self.shift_t=0.; self.shift_cd=6.
        self.flash_walls=[]  # walls about to appear (warning)
    def reset(self):
        self.walls=set(); self._generate(); self.shift_t=0.
    def _generate(self):
        """Generate a sparse maze-like pattern"""
        self.walls=set()
        # Random horizontal/vertical segments
        for _ in range(8):
            hz=random.choice([True,False])
            x=random.randint(3,COLS-6); y=random.randint(3,ROWS-6)
            ln=random.randint(3,6)
            for k in range(ln):
                if hz: self.walls.add((x+k,y))
                else:  self.walls.add((x,y+k))
    def solid_cells(self): return self.walls
    def update(self,dt,snake_set,*a):
        self.shift_t+=dt*.001
        if self.shift_t>=self.shift_cd:
            self.shift_t=0.
            # Generate new walls that don't overlap snake
            new_w=set()
            for _ in range(12):
                hz=random.choice([True,False])
                x=random.randint(3,COLS-6); y=random.randint(3,ROWS-6)
                ln=random.randint(3,5)
                for k in range(ln):
                    p=(x+k,y) if hz else (x,y+k)
                    if p not in snake_set: new_w.add(p)
            self.walls=new_w
    @property
    def shift_frac(self): return min(1.,self.shift_t/self.shift_cd)
    def draw(self,surf,ox,oy,T):
        warn=(self.shift_frac>0.8)
        for x,y in self.walls:
            px=ox+x*CELL; py=oy+y*CELL
            col=(100,200,255) if not warn else (255,150,50)
            pulse=abs(math.sin(T*3+(x+y)*.4))
            a=int(140+60*pulse)
            ws=asurf(CELL,CELL)
            pygame.draw.rect(ws,(*col,a),(0,0,CELL,CELL),border_radius=3)
            # inner glow
            pygame.draw.rect(ws,(*WHT,int(40*pulse)),(3,3,CELL-6,CELL-6),border_radius=2)
            surf.blit(ws,(px,py))
            cglow(surf,px+CELL//2,py+CELL//2,CELL//2+2,col,int(25*pulse))


def make_hazard(kind):
    """Factory — returns the right hazard object"""
    if kind==HAZARD_VORTEX:    return HazardVortex()
    if kind==HAZARD_PORTAL:    return HazardPortal()
    if kind==HAZARD_DARK:      return HazardDark()
    if kind==HAZARD_SPEEDTRAP: return HazardSpeedtrap()
    if kind==HAZARD_GRAVITY:   return HazardGravity()
    if kind==HAZARD_ELECTRIC:  return HazardElectric()
    if kind==HAZARD_MAZE:      return HazardMaze()
    return None


class PowerUp:
    def __init__(self,pos,kind): self.pos=pos;self.kind=kind;self.life=13000.;self.T=0.
    def update(self,dt): self.T+=dt*.001;self.life-=dt;return self.life>0
    def draw(self,surf,ox,oy):
        gx,gy=self.pos;cx=ox+gx*CELL+CELL//2;cy=oy+gy*CELL+CELL//2
        col=PU_COL[self.kind];r=int(CELL//2-1+2.5*abs(math.sin(self.T*3.2)))
        cglow(surf,cx,cy,r+7,col,int(26+14*abs(math.sin(self.T*2.4))))
        s=asurf(r*2+2,r*2+2)
        pygame.draw.circle(s,(*col,205),(r+1,r+1),r)
        pygame.draw.circle(s,(*WHT,60),(max(1,r+1-r//3),max(1,r+1-r//3)),max(1,r//3))
        surf.blit(s,(cx-r-1,cy-r-1))
        frac=max(0,self.life/13000)
        if frac<.98:
            ar=r+5;ars=asurf(ar*2+2,ar*2+2)
            pygame.draw.arc(ars,(*col,135),(1,1,ar*2,ar*2),-math.pi/2,-math.pi/2+frac*2*math.pi,2)
            surf.blit(ars,(cx-ar-1,cy-ar-1))
        t2=FXX.render(PU_ICO[self.kind],True,col)
        ts=asurf(t2.get_width()+4,t2.get_height()+2);ts.blit(t2,(2,1));ts.set_alpha(188)
        surf.blit(ts,(cx-t2.get_width()//2-2,cy+r+3))

# ── Background ────────────────────────────────────
class Meteor:
    def __init__(self): self._reset()
    def _reset(self):
        self.x=float(random.randint(PANEL,PANEL+W));self.y=float(random.randint(96,96+H//3))
        self.vx=random.uniform(3.5,8.);self.vy=random.uniform(1.2,3.5)
        self.life=1.;self.tail=random.randint(16,36)
        self.col=random.choice([(255,255,220),(200,220,255),(255,210,180)])
        self.active=False;self.wait=random.uniform(4,14);self.wt=0.
    def update(self,dt):
        if not self.active:
            self.wt+=dt*.001
            if self.wt>=self.wait: self.active=True
            return
        self.x+=self.vx;self.y+=self.vy;self.life-=.026
        if self.life<=0 or self.x>PANEL+W+50: self._reset()
    def draw(self,surf):
        if not self.active: return
        a=int(215*max(0,self.life))
        for i in range(self.tail):
            t=i/self.tail;ta=int(a*(1-t)**2)
            if ta<4: continue
            tx=int(self.x-self.vx*i*.8);ty=int(self.y-self.vy*i*.8)
            r=max(1,int(2*(1-t)));s=asurf(r*2+2,r*2+2)
            pygame.draw.circle(s,(*self.col,ta),(r+1,r+1),r);surf.blit(s,(tx-r-1,ty-r-1))

class NebulaPatch:
    def __init__(self):
        self.x=float(random.randint(PANEL+50,PANEL+W-50));self.y=float(random.randint(96+50,96+H-50))
        self.hue=random.random();self.r=random.randint(55,130);self.alpha=random.randint(4,12)
        self.dx=random.uniform(-.035,.035);self.dy=random.uniform(-.025,.025);self.phase=random.uniform(0,2*math.pi)
    def update(self,dt):
        self.x+=self.dx;self.y+=self.dy;self.hue=(self.hue+dt*.000016)%1.
        if self.x<PANEL+10 or self.x>PANEL+W-10: self.dx*=-1
        if self.y<96+10 or self.y>96+H-10: self.dy*=-1
    def draw(self,surf,T):
        col=hsv(self.hue,.72,.55);pulse=1+.25*math.sin(T*.38+self.phase)
        r=int(self.r*pulse);s=asurf(r*2+4,r*2+4)
        for i in range(4):
            ri=r*(1-i/4);ai=int(self.alpha*(1-i/4)**1.5)
            if ai>0: pygame.draw.circle(s,(*col,ai),(r+2,r+2),int(ri))
        surf.blit(s,(int(self.x)-r-2,int(self.y)-r-2))

class StarField:
    def __init__(self):
        self.stars=[{"x":float(random.randint(PANEL,PANEL+W)),"y":float(random.randint(96,96+H)),
                     "r":random.choice([1,1,1,2]),"phase":random.uniform(0,2*math.pi),
                     "speed":random.uniform(.18,.75),"col":random.choice([WHT,(200,220,255),(255,220,180),(180,255,200)])}
                    for _ in range(170)]
        self.meteors=[Meteor() for _ in range(4)];self.nebulae=[NebulaPatch() for _ in range(7)]
    def update(self,dt):
        for m in self.meteors: m.update(dt)
        for n in self.nebulae: n.update(dt)
    def draw(self,surf,T):
        for n in self.nebulae: n.draw(surf,T)
        for st in self.stars:
            # Chibi: brighter twinkle with 4-point star shape
            t_val=abs(math.sin(T*st["speed"]+st["phase"]))
            a=int(t_val*180+40)
            r=st["r"]; s=asurf(r*2+2,r*2+2)
            pygame.draw.circle(s,(*st["col"],a),(r+1,r+1),r)
            surf.blit(s,(int(st["x"])-r-1,int(st["y"])-r-1))
            # Twinkle cross for bright stars
            if r>1 and t_val>0.7:
                ta=int((t_val-0.7)/.3*140)
                sx2=int(st["x"]); sy2=int(st["y"])
                pygame.draw.line(surf,(*WHT,ta),(sx2-r-2,sy2),(sx2+r+2,sy2),1)
                pygame.draw.line(surf,(*WHT,ta),(sx2,sy2-r-2),(sx2,sy2+r+2),1)
        for m in self.meteors: m.draw(surf)

class Aurora:
    def __init__(self):
        self.bands=[{"hue":random.random(),"y":float(random.randint(96+55,96+H-115)),
                     "vy":random.uniform(-.09,.09),"w":random.randint(W//3,W),"alpha":random.randint(5,14)}
                    for _ in range(6)]
    def update(self,dt):
        for b in self.bands:
            b["y"]+=b["vy"]
            if b["y"]<96+28 or b["y"]>96+H-28: b["vy"]*=-1
            b["hue"]=(b["hue"]+dt*.00002)%1.
    def draw(self,surf,T):
        for b in self.bands:
            # Chibi: more saturated, brighter aurora
            col=hsv(b["hue"],.65,.55)
            a=int(b["alpha"]*(1.4+.4*math.sin(T*.48+b["hue"]*10)))
            bw=b["w"]; s=asurf(bw,56)
            for dy in range(28):
                fa=int(a*(1-(dy/28)**1.4))
                if fa>0:
                    pygame.draw.line(s,(*col,fa),(0,dy),(bw,dy))
                    pygame.draw.line(s,(*col,fa),(0,55-dy),(bw,55-dy))
            surf.blit(s,(PANEL+(W-bw)//2,int(b["y"])-28))

# ── Baked surfaces ────────────────────────────────
# Ground themes per stage — set by _apply_ground_theme()
_GROUND_THEME={"light":(22,62,26),"dark":(9,28,12),"alt":(18,52,22),"line":(14,44,16)}

def bake_ground(theme="grass"):
    """Bake a stage-themed ground. theme: grass|sand|ice|void|lava|purple"""
    random.seed(42); s=pygame.Surface((W,H))
    themes={
        "grass": {"a":(20,58,24),"b":(25,68,28),"line":(14,44,16),"dot":(30,80,34)},
        "sand":  {"a":(90,70,30),"b":(100,80,36),"line":(75,58,22),"dot":(110,88,40)},
        "ice":   {"a":(40,70,100),"b":(50,82,115),"line":(32,58,88),"dot":(60,92,130)},
        "void":  {"a":(12,8,28),"b":(16,11,36),"line":(8,6,20),"dot":(22,14,48)},
        "lava":  {"a":(60,18,8),"b":(72,22,10),"line":(48,14,6),"dot":(88,28,12)},
        "purple":{"a":(38,14,62),"b":(46,18,74),"line":(28,10,50),"dot":(56,22,88)},
    }
    t=themes.get(theme,themes["grass"])
    for gx in range(COLS):
        for gy in range(ROWS):
            checker=(gx+gy)%2
            base=t["a"] if checker==0 else t["b"]
            n=random.randint(-3,3)
            c=tuple(cl(b+n) for b in base)
            pygame.draw.rect(s,c,(gx*CELL,gy*CELL,CELL,CELL))
    # Subtle grid
    for gx in range(COLS+1):
        pygame.draw.line(s,t["line"],(gx*CELL,0),(gx*CELL,H),1)
    for gy in range(ROWS+1):
        pygame.draw.line(s,t["line"],(0,gy*CELL),(W,gy*CELL),1)
    # Corner dots — chibi style
    for gx in range(COLS):
        for gy in range(ROWS):
            if random.random()<0.18:
                px=gx*CELL+random.randint(3,CELL-3)
                py=gy*CELL+random.randint(3,CELL-3)
                pygame.draw.circle(s,t["dot"],(px,py),1)
    random.seed(); return s

def bake_sl(w,h,a=9):
    s=asurf(w,h)
    for y in range(0,h,2): pygame.draw.line(s,(0,0,0,a),(0,y),(w,y))
    return s
def bake_vig(w,h,st=78):
    s=asurf(w,h)
    for i in range(36):
        a=int(st*(1-i/36)**1.9);pygame.draw.rect(s,(0,0,0,a),(i,i,w-i*2,h-i*2),1)
    return s
def bake_panel(w,h):
    s=pygame.Surface((w,h))
    for y in range(h): c=lc(PT,PB,y/h);pygame.draw.line(s,c,(0,y),(w,y))
    return s

def bake_free_ground():
    """Chibi warm teal/purple ground for free play — easy on the eyes"""
    random.seed(99); s=pygame.Surface((W,H))
    for gx in range(COLS):
        for gy in range(ROWS):
            # Warm teal checker
            checker=(gx+gy)%2
            if checker==0: base=(20,55,70)
            else:          base=(24,64,80)
            n=random.randint(-2,2)
            c=tuple(cl(b+n) for b in base)
            pygame.draw.rect(s,c,(gx*CELL,gy*CELL,CELL,CELL))
    # Grid — subtle warm teal
    for gx in range(COLS+1):
        pygame.draw.line(s,(16,44,58),(gx*CELL,0),(gx*CELL,H),1)
    for gy in range(ROWS+1):
        pygame.draw.line(s,(16,44,58),(0,gy*CELL),(W,gy*CELL),1)
    # Soft glow dots — lavender
    for _ in range(100):
        px=random.randint(2,W-3); py=random.randint(2,H-3)
        c=(cl(random.randint(45,65)),cl(random.randint(70,95)),cl(random.randint(90,115)))
        pygame.draw.circle(s,c,(px,py),1)
    random.seed(); return s

# ═════════════════════════════════════════════════
#  G A M E
# ═════════════════════════════════════════════════
class Game:
    def __init__(self):
        self.screen=pygame.display.set_mode((SW,SH))
        pygame.display.set_caption("SNAKE  ·  Mythic Edition  v9")
        self.clock=pygame.time.Clock()
        self.ground=bake_ground()
        self.free_ground=bake_free_ground()
        self.sl=bake_sl(W,H,8);self.vig=bake_vig(W,H,76)
        self.pbg=bake_panel(PANEL,SH);self.psl=bake_sl(PANEL,SH,5)
        self.aurora=Aurora();self.stars=StarField()
        self.weather=Weather()
        self.hi=0;self.state="menu";self.T=0.;self.RT=0.
        self.dust=[(random.randint(PANEL,SW),random.randint(0,SH),random.uniform(0,2*math.pi),random.uniform(.3,1.)) for _ in range(95)]
        self.ff=[(float(random.randint(PANEL+8,PANEL+W-8)),float(random.randint(96+8,96+H-8)),random.uniform(0,2*math.pi),random.uniform(.4,1.5)) for _ in range(30)]
        self.mode=MODE_MENU
        self.stage_idx=0        # selected stage (0-9)
        self.free_play=False
        self.stage_complete=False
        self.stage_weather=WN
        self.stage_spd_mult=1.0
        self.stage_score_target=300
        self.stage_boss_level=None
        self.hazard=None
        self.mirror_active=False
        self.stage_walls=set()
        self.ground_theme="grass"
        self.stage_score_target=200  # score to complete a stage
        self.unlocked=1         # stages 0..unlocked-1 are available
        self._full_reset(); self.demo=self._make_demo()

    def _full_reset(self):
        self.powerups=[];self.preys=[]
        self.sparks=[];self.texts=[];self.rings=[];self.bursts=[]
        mid=(COLS//2,ROWS//2)
        if "start_len" in getattr(self,"skills_owned",set()):
            self.snake=[mid]+[(mid[0]-k,mid[1]) for k in range(1,5)]
        else:
            self.snake=[mid,(mid[0]-1,mid[1]),(mid[0]-2,mid[1])]
        self.dir=RIGHT;self.ndir=RIGHT
        self.score=0;self.level=1;self.eats=0
        self.combo=0;self.combo_t=0;self.max_combo=0
        self.bonus=None;self.bonus_t=0
        self.food=self._sfood()
        self.mv_t=0;self.shake=0;self.trail_h=.33
        self.theme_idx=0;self.theme=THEMES[0];self.prev_theme=THEMES[0];self.theme_t=1.0
        self.pus={PS:0,PV:0,PM:0,PX:0,PG:0,PF:0,PL:0,PZ:0,PW:0,PP:0,PB2:0,PD:0,PR:0}
        self.pu_spawn_t=random.randint(10000,16000);self.slow_f=1.0
        self.freeze_stun=0
        self.stage_complete=False
        self.stage_weather=WN
        self.stage_spd_mult=1.0
        self.stage_score_target=300
        self.stage_boss_level=None
        self.hazard=None
        self.mirror_active=False
        self.stage_walls=set()
        self.ground_theme="grass"
        self.boss=None;self.boss_killed=set()
        self.slip_dir=None;self.slip_t=0  # rain slippery effect
        self.weather=Weather()
        self.skill_pts=0
        self.skills_owned=set()
        self.high_scores=[]  # Track high scores
        self.game_stats={"games_played":0,"total_score":0,"best_stage":0}
        self.powerup_stats={k:0 for k in PU_COL.keys()}  # Track power-up usage

    def _sc(self,gp): return(PANEL+gp[0]*CELL+CELL//2,96+gp[1]*CELL+CELL//2)

    def _sfood(self,extra=None):
        bl=set(self.snake)|getattr(self,"stage_walls",set())
        for p in self.powerups: bl.add(p.pos)
        for p in self.preys: bl.add(p.pos)
        if self.bonus is not None: bl.add(self.bonus)
        if extra: bl|=extra
        for _ in range(3000):
            p=(random.randint(1,COLS-2),random.randint(1,ROWS-2))
            if p not in bl: return p
        for gx in range(COLS):
            for gy in range(ROWS):
                if(gx,gy) not in bl: return(gx,gy)
        return(0,0)


    def _solid(self):
        s=set(getattr(self,"stage_walls",set()))
        if self.boss: s|=self.boss.get_solid()
        if self.hazard and isinstance(self.hazard,HazardMaze):
            s|=self.hazard.solid_cells()
        return s

    def _spd(self):
        b=min(BASE_SPD+(self.level-1),MAX_SPD)
        if self.pus[PZ]>0: b=min(b,10)  # SPD CAP: never faster than 10
        if self.pus[PV]>0: b=min(b+4,MAX_SPD)
        if self.pus[PL]>0: self.slow_f=max(.4,self.slow_f-.002)
        else: self.slow_f=min(1.,self.slow_f+.004)
        w=self.weather.spd_mult
        return max(2,int(b*self.slow_f*w))

    def _check_boss_spawn(self):
        """Spawn boss at levels 5, 10, 15"""
        if self.level in BOSSES and self.level not in self.boss_killed and self.boss is None:
            ox,oy=PANEL,96
            self.boss=Boss(self.level,ox,oy)
            sfx("boss_warn")
            cx2=PANEL+W//2; cy2=96+H//2
            col=BOSSES[self.level]["col"]
            self.texts.append(FloatTxt(cx2,cy2-80,f"⚠ {BOSSES[self.level]['name']} AWAKENS!",col,big=True))

    def _make_demo(self):
        demos=[]
        for _ in range(6):
            x=random.randint(2,COLS-6);y=random.randint(2,ROWS-6)
            d=random.choice([UP,DOWN,LEFT,RIGHT])
            demos.append({"body":[(x-k,y) for k in range(6)],"dir":d,"t":0,"hue":random.random()})
        return demos

    def _start_free(self):
        """Start free play mode"""
        self.free_play=True; self._full_reset()
        self.state="running"; self.mode=MODE_FREE; sfx("strt")

    def _advance_stage(self):
        """After completing a stage — unlock next, go to stage select"""
        N=len(STAGES)-1
        if self.stage_idx<N:
            self.stage_idx=min(self.stage_idx+1,self.unlocked-1)
        self.mode=MODE_STAGE

    def _start_stage(self,idx):
        st=STAGES[idx]; self.free_play=False
        self._full_reset()
        self.state="running"; self.mode=MODE_GAME; self.free_play=False
        self.stage_weather=st["wx"]
        if st["wx"]!=WN: self.weather.set(st["wx"])
        self.stage_spd_mult=st["spd"]
        self.stage_score_target=st["target"]
        self.stage_boss_level=st.get("boss")
        self._last_click_stage=-1
        self.mirror_active=(st["hz"]==HAZARD_MIRROR)
        hz_kind=st.get("hz",HAZARD_NONE)
        if hz_kind not in(HAZARD_NONE,HAZARD_MIRROR):
            self.hazard=make_hazard(hz_kind)
            if self.hazard: self.hazard.reset()
        else:
            self.hazard=None
        # Load stage barriers
        self.boss_score_scale=1.0  # updated each frame
        sid=st["id"]
        raw=STAGE_BARRIERS.get(sid,set())
        self.stage_walls=raw.copy()
        # Rebake ground with stage theme
        gtheme=STAGE_GROUND.get(sid,"grass")
        self.ground=bake_ground(gtheme)
        self.ground_theme=gtheme

    def run(self):
        while True:
            dt=self.clock.tick(60)
            self.T+=dt*.001;self.RT+=dt*.0004
            self.aurora.update(dt);self.stars.update(dt)
            self._events();self._update(dt);self._render()
            pygame.display.flip()

    def _events(self):
        DM={pygame.K_UP:UP,pygame.K_w:UP,pygame.K_DOWN:DOWN,pygame.K_s:DOWN,
            pygame.K_LEFT:LEFT,pygame.K_a:LEFT,pygame.K_RIGHT:RIGHT,pygame.K_d:RIGHT}
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()

            # ──────────────────────────────────────────────────
            #  MOUSE
            # ──────────────────────────────────────────────────
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                mx,my=ev.pos

                if self.mode==MODE_MENU:
                    # Skills buy click
                    if getattr(self,"skill_menu",False):
                        self._handle_skill_click(mx,my)
                    else:
                        cx=PANEL+W//2; cy=96+H//2
                        bw=280; bh=54; bx=cx-bw//2
                        if bx<=mx<=bx+bw:
                            if cy-60<=my<=cy-60+bh:   self.mode=MODE_STAGE
                            elif cy+10<=my<=cy+10+bh: self._start_free()
                            elif cy+80<=my<=cy+80+bh: pygame.quit(); sys.exit()
                        # Skills button
                        if PANEL+W-160<=mx<=PANEL+W-10 and 96+H-36<=my<=96+H-6:
                            self.skill_menu=True

                elif self.mode==MODE_STAGE:
                    cols=5; cw=128; ch=72; gap=7
                    x0=(PANEL+W//2)-(cols*cw+(cols-1)*gap)//2; y0=96+54
                    for i in range(len(STAGES)):
                        sx=x0+(i%cols)*(cw+gap); sy=y0+(i//cols)*(ch+gap)
                        if sx<=mx<=sx+cw and sy<=my<=sy+ch and i<self.unlocked:
                            if getattr(self,'_last_stage_click',(-1,0))[0]==i:
                                # double click = start
                                self._start_stage(i); sfx("strt")
                            else:
                                self.stage_idx=i
                                self._last_stage_click=(i,self.T)
                    # Free play btn bottom right
                    if PANEL+W-175<=mx<=PANEL+W-15 and 96+H-40<=my<=96+H-8:
                        self._start_free()

                elif self.mode in(MODE_GAME,MODE_FREE):
                    cx=PANEL+W//2; cy=96+H//2
                    if self.state=="dead":
                        # Retry button
                        if cx-100<=mx<=cx+100 and cy+78<=my<=cy+122:
                            if self.mode==MODE_FREE:
                                self._start_free()
                            else:
                                self.mode=MODE_STAGE
                    elif self.stage_complete:
                        # Continue button
                        if cx-120<=mx<=cx+120 and cy+134<=my<=cy+180:
                            self._advance_stage()

            # ──────────────────────────────────────────────────
            #  KEYBOARD
            # ──────────────────────────────────────────────────
            if ev.type==pygame.KEYDOWN:
                k=ev.key

                # ── Main Menu ─────────────────────────────────
                if self.mode==MODE_MENU:
                    if k in(pygame.K_1,pygame.K_s): self.mode=MODE_STAGE
                    if k in(pygame.K_2,pygame.K_f): self._start_free()
                    if k==pygame.K_ESCAPE:          pygame.quit(); sys.exit()
                    if k in(pygame.K_SPACE,pygame.K_RETURN): self.mode=MODE_STAGE

                # ── Stage Select ──────────────────────────────
                elif self.mode==MODE_STAGE:
                    if k in(pygame.K_RIGHT,pygame.K_d):
                        self.stage_idx=min(self.stage_idx+1,min(self.unlocked-1,len(STAGES)-1))
                    if k in(pygame.K_LEFT,pygame.K_a):
                        self.stage_idx=max(self.stage_idx-1,0)
                    if k in(pygame.K_DOWN,): # down = next row (+5)
                        self.stage_idx=min(self.stage_idx+5,min(self.unlocked-1,len(STAGES)-1))
                    if k in(pygame.K_UP,):   # up = prev row (-5)
                        self.stage_idx=max(self.stage_idx-5,0)
                    if k in(pygame.K_SPACE,pygame.K_RETURN):
                        self._start_stage(self.stage_idx); sfx("strt")
                    if k==pygame.K_f: self._start_free()
                    if k==pygame.K_ESCAPE: self.mode=MODE_MENU

                # ── In-game (stages or free play) ─────────────
                elif self.mode in(MODE_GAME,MODE_FREE):
                    if k in DM and self.state=="running":
                        nd=DM[k]
                        if getattr(self,"mirror_active",False): nd=OPP.get(nd,nd)
                        if nd!=OPP.get(self.dir): self.ndir=nd
                    if k in(pygame.K_SPACE,pygame.K_RETURN):
                        if self.stage_complete:
                            self._advance_stage()
                        elif self.state=="dead":
                            if self.mode==MODE_FREE: self._start_free()
                            else: self.mode=MODE_STAGE
                    if k in(pygame.K_p,pygame.K_ESCAPE):
                        if self.state=="running":  self.state="paused"
                        elif self.state=="paused":
                            if getattr(self,"skill_menu",False): self.skill_menu=False
                            else: self.mode=MODE_MENU; self.state="running"
                    if k==pygame.K_s and self.state=="paused":
                        self.skill_menu=not getattr(self,"skill_menu",False)
                    if k==pygame.K_s and self.mode==MODE_MENU:
                        self.skill_menu=not getattr(self,"skill_menu",False)
                    # Buy skill with number keys in skill menu
                    if getattr(self,"skill_menu",False) and pygame.K_1<=k<=pygame.K_8:
                        idx=k-pygame.K_1
                        if idx<len(SKILLS):
                            sk=SKILLS[idx]
                            if (sk["id"] not in getattr(self,"skills_owned",set())
                                    and getattr(self,"skill_pts",0)>=sk["cost"]):
                                self.skills_owned.add(sk["id"])
                                self.skill_pts-=sk["cost"]
                                sfx("lvl")

    def _update(self,dt):
        if self.shake>0: self.shake-=1
        if self.combo_t>0:
            self.combo_t-=dt
            if self.combo_t<=0: self.combo=0
        if self.theme_t<1.: self.theme_t=min(1.,self.theme_t+dt*.003)
        for k in list(self.pus):
            if self.pus[k]>0: self.pus[k]=max(0,self.pus[k]-dt)
        self.sparks=[p for p in self.sparks if p.update()]
        self.texts=[t for t in self.texts if t.update()]
        self.rings=[r for r in self.rings if r.update()]
        self.bursts=[b for b in self.bursts if b.update(dt)]
        ss=set(self.snake);solid=self._solid()
        self.powerups=[p for p in self.powerups if p.update(dt)]
        tw=0.35 if self.pus.get(PW,0)>0 else 1.0  # TIME WARP: all entities at 35% speed
        w_spd=(self.weather.spd_mult if self.weather else 1.)*tw
        for pr in self.preys: pr.update(dt*tw,self.snake,solid,w_spd)
        for pr in self.preys:
            if pr.life<=0 and pr.alive and not getattr(pr,'escape_noted',False):
                pr.escape_noted=True
                # Timer ran out: prey escaped, lose combo
                px_e,py_e=pr.pos
                cx_e=PANEL+px_e*CELL+CELL//2; cy_e=96+py_e*CELL+CELL//2
                self.texts.append(FloatTxt(cx_e,cy_e,"GOT AWAY!",DNG,big=True))
                if self.combo>0:
                    self.texts.append(FloatTxt(cx_e,cy_e+26,f"COMBO LOST ×{self.combo}",(200,60,60)))
                self.combo=0; self.combo_t=0
                sfx("escaped"); self.shake=max(self.shake,5)
        self.preys=[p for p in self.preys if not p.done]
        if self.mode in(MODE_MENU,MODE_STAGE):
            self._upd_demo(dt); self.weather.update(dt,self.T); return
        if self.mode not in(MODE_GAME,MODE_FREE): return
        if self.stage_complete: return  # freeze on complete
        if self.state!="running": return
        self.weather.update(dt,self.T)
        # Update active hazard
        if self.hazard:
            ss2=set(self.snake)
            solid2=self._solid()
            self.hazard.update(dt,ss2,solid2)
            # Speed trap boost
            if isinstance(self.hazard,HazardSpeedtrap):
                self.hazard.update(1,ss2,solid2)  # decrement boost counter each frame
        # Boss update
        if self.boss:
            if self.boss.done:
                col=self.boss.col; cx2=PANEL+W//2; cy2=96+H//2
                for _ in range(120): self.sparks.append(Spark(cx2,cy2,col,sp=2.,big=True))
                for _ in range(8): self.rings.append(Ring(cx2,cy2,col,w=4))
                pts_boss=300+self.boss.level*50
                self.score+=pts_boss; self.hi=max(self.hi,self.score)
                self.texts.append(FloatTxt(cx2,cy2-50,f"BOSS SLAIN! +{pts_boss}",col,big=True))
                sfx("boss_die")
                self.boss_killed.add(self.boss.level)
                self.boss=None
            else:
                # Scale boss speed with score
                if self.boss: self.boss.mv_spd=3.0+min(2.5,self.score/400.0)
                boss_hit=self.boss.update(dt,self.snake,solid,self.texts,self.sparks,self.rings,self.weather)
                if boss_hit==True:
                    # Lightning or rock hit — shield saves, else die
                    if self.pus[PS]>0:
                        self.pus[PS]=0; self.shake=14; sfx("pick")
                        hx2,hy2=self.snake[0]; cx3,cy3=self._sc((hx2,hy2))
                        self.texts.append(FloatTxt(cx3,cy3,"SHIELD SAVED!",PU_COL[PS],big=True))
                        for _ in range(30): self.sparks.append(Spark(cx3,cy3,PU_COL[PS],big=True))
                    else:
                        hx2,hy2=self.snake[0]; cx3,cy3=self._sc((hx2,hy2))
                        self.texts.append(FloatTxt(cx3,cy3,"BOSS HIT YOU!",DNG,big=True))
                        self._die(); return
                elif boss_hit=="stun":
                    # Freeze stun: lock direction for 2s
                    self.freeze_stun=max(getattr(self,"freeze_stun",0),2000)
                    hx2,hy2=self.snake[0]; cx3,cy3=self._sc((hx2,hy2))
                    self.texts.append(FloatTxt(cx3,cy3,"FROZEN!!",(160,220,255),big=True))
        if self.bonus is not None:
            self.bonus_t-=dt
            if self.bonus_t<=0: self.bonus=None
        self.pu_spawn_t-=dt
        if self.pu_spawn_t<=0:
            self.pu_spawn_t=random.randint(10000,16000)
            pool=[PS,PV,PM,PX,PG,PF,PL,PN,PZ,PW,PH,PD,PR,PB2,PP]
            if "dash_cd" in getattr(self,"skills_owned",set()):
                pool=pool+[PD,PD]  # dash appears more often
            self.powerups.append(PowerUp(self._sfood(),random.choice(pool)))
        if self.pus[PM]>0 and self.food:
            hx,hy=self.snake[0];fx,fy=self.food
            if abs(hx-fx)+abs(hy-fy)<=4: self._eat_food();return
        self.mv_t+=dt
        # Freeze stun from Frost King
        if hasattr(self,"freeze_stun") and self.freeze_stun>0:
            self.freeze_stun-=dt
            self.ndir=self.dir  # can't turn
        if self.mv_t<1000/self._spd(): return
        self.mv_t=0; self.dir=self.ndir
        hx,hy=self.snake[0]; dx,dy=self.dir
        # Rain slippery
        if self.weather.kind==WR and self.weather.slip and random.random()<.35:
            dx,dy=self.dir
        # Gravity drift — override direction
        if self.hazard and isinstance(self.hazard,HazardGravity):
            if self.hazard.should_drift:
                gdx,gdy=self.hazard.pull
                dx,dy=gdx,gdy
                self.texts.append(FloatTxt(PANEL+W//2,96+H//2-24,"GRAVITY!",self.hazard.pull_col))
        head=((hx+dx)%COLS,(hy+dy)%ROWS)
        # Vortex spin
        if self.hazard and isinstance(self.hazard,HazardVortex):
            new_dir2,spun=self.hazard.apply(head,self.dir)
            if spun:
                self.dir=new_dir2; self.ndir=new_dir2
                cx2,cy2=self._sc(head)
                self.texts.append(FloatTxt(cx2,cy2,"SPIN!",( 100,200,255)))
        # Portal teleport
        if self.hazard and isinstance(self.hazard,HazardPortal):
            dest=self.hazard.apply(head)
            if dest:
                head=dest; self.hazard.teleport_flash=1.
                self.shake=max(self.shake,6); sfx("pick")
        # Electric fence kill
        if self.hazard and isinstance(self.hazard,HazardElectric):
            if self.hazard.is_live(head[0],head[1]):
                if self.pus[PS]>0:
                    self.pus[PS]=0; self.shake=10; sfx("pick")
                    cx2,cy2=self._sc(head)
                    self.texts.append(FloatTxt(cx2,cy2,"SHIELD SAVED!",PU_COL[PS],big=True))
                else:
                    self._die(); return
        if head in set(self.snake[:-1]):
            if self.pus.get(PP,0)>0: pass  # PHASE: no self-collision
            else: self._die(); return
        if head in solid:
            if self.pus.get(PP,0)>0: pass  # PHASE: walk through walls
            elif self.pus[PS]>0:
                # Skill: shield_wall also blocks stage walls
                self.pus[PS]=0;self.shake=8;sfx("pick")
                col=PU_COL[PS];cx2,cy2=self._sc(head)
                for _ in range(18): self.sparks.append(Spark(cx2,cy2,col,big=True))
                self.texts.append(FloatTxt(cx2,cy2,"BLOCKED!",col,big=True))
                for _ in range(2): self.rings.append(Ring(cx2,cy2,col))
            elif self.pus[PG]>0: pass
            else: self._die();return
        if head==self.food: self._eat_food();return
        if self.bonus and head==self.bonus:
            pts=50*min(self.combo+1,5)
            if self.pus[PX]>0: pts*=2
            self.combo=min(self.combo+2,10);self.combo_t=3200;self.max_combo=max(self.max_combo,self.combo)
            self.bonus=None;cx2,cy2=self._sc(head)
            for _ in range(50): self.sparks.append(Spark(cx2,cy2,GOLD,big=True))
            for _ in range(2): self.rings.append(Ring(cx2,cy2,GOLD))
            self.texts.append(FloatTxt(cx2,cy2,f"+{pts} ★",GOLD,big=True))
            sfx("bon");self.score+=pts;self.hi=max(self.hi,self.score)
            self.snake=[head]+self.snake;self.trail_h=(self.trail_h+.003)%1.;return
        # Prey catch
        for pr in list(self.preys):
            if head==pr.pos:
                frac=max(0,pr.life/pr.LIFE)
                pts=int(150*frac/10)*10;pts=max(20,pts)
                if self.pus[PX]>0: pts*=2
                pr.alive=False;cx2,cy2=self._sc(head)
                for _ in range(50): self.sparks.append(Spark(cx2,cy2,pr.col,sp=1.4,big=True))
                for _ in range(3): self.rings.append(Ring(cx2,cy2,pr.col,w=3))
                self.texts.append(FloatTxt(cx2,cy2,f"+{pts} CAUGHT!",pr.col,big=True))
                sfx("prey"); self.score+=pts; self.hi=max(self.hi,self.score)
                # Give power-up if prey had one
                if pr.has_pu and pr.pu_kind:
                    self.pus[pr.pu_kind]=PU_DUR[pr.pu_kind]
                    pcol=PU_COL[pr.pu_kind]
                    self.texts.append(FloatTxt(cx2,cy2-28,f"+{PU_ICO[pr.pu_kind]}!",pcol,big=True))
                    for _ in range(20): self.sparks.append(Spark(cx2,cy2,pcol,big=True))
                break
        # Speed trap pickup
        if self.hazard and isinstance(self.hazard,HazardSpeedtrap):
            if self.hazard.apply(head):
                cx2,cy2=self._sc(head)
                self.texts.append(FloatTxt(cx2,cy2,"SPEED TRAP!⚡",(255,200,30),big=True))
                for _ in range(20): self.sparks.append(Spark(cx2,cy2,(255,200,30),big=True))
                sfx("pick")
        # PU pickup
        for pu in list(self.powerups):
            if head==pu.pos:
                self._collect_pu(pu); self.powerups.remove(pu); break
        # Boss collision — head enters boss cell OR boss enters head cell
        if self.boss and self.boss.warn_t<=0 and self.boss.alive:
            boss_hit_me=(head==self.boss.pos)
            # Also check any body segment near boss (full contact)
            boss_adjacent=self.boss and any(abs(s[0]-self.boss.pos[0])+abs(s[1]-self.boss.pos[1])<=1
                               for s in self.snake[:3])
            if boss_hit_me:
                if self.pus.get(PP,0)>0:
                    pass  # PHASE: walk through boss
                elif self.pus[PS]>0:
                    self.pus[PS]=0; self.shake=16; sfx("pick")
                    bcol=self.boss.col; cx2,cy2=self._sc(head)
                    self.texts.append(FloatTxt(cx2,cy2,"DERQA SALVATIK!",PU_COL[PS],big=True))
                    for _ in range(35): self.sparks.append(Spark(cx2,cy2,PU_COL[PS],big=True))
                    for _ in range(3): self.rings.append(Ring(cx2,cy2,PU_COL[PS],w=3))
                else:
                    cx2,cy2=self._sc(head)
                    self.texts.append(FloatTxt(cx2,cy2,"L-WE7CH DRBEK!",DNG,big=True))
                    self._die(); return
        self.snake=[head]+self.snake[:-1];self.trail_h=(self.trail_h+.003)%1.

    def _eat_food(self):
        self.eats+=1
        self.combo=min(self.combo+1,10)
        ct_bonus=1000*("combo_keep" in getattr(self,"skills_owned",set()))
        self.combo_t=3200+ct_bonus;self.max_combo=max(self.max_combo,self.combo)
        mult=min(self.combo,8)
        base_pts=10+2*("score_bonus" in getattr(self,"skills_owned",set()))
        pts=base_pts*mult
        if self.pus[PX]>0: pts*=2
        if self.pus.get(PB2,0)>0: pts*=3
        pl=self.level
        self.prev_theme=self.theme;self.theme_idx=(self.theme_idx+1)%len(THEMES)
        self.theme=THEMES[self.theme_idx];self.theme_t=0.;hc=self.theme[1]
        cx2,cy2=self._sc(self.food)
        self.bursts.append(EatBurst(cx2,cy2,hc))
        for _ in range(20+self.combo*5): self.sparks.append(Spark(cx2,cy2,hc,big=True))
        for _ in range(1+self.combo//4): self.rings.append(Ring(cx2,cy2,hc))
        self.shake=max(self.shake,2+self.combo//2)
        if self.combo>=5: sfx("eat3")
        elif self.combo>=2: sfx("eat2")
        else: sfx("eat1")
        lbl=f"+{pts}"
        if self.pus[PX]>0: lbl+=" ×2!"
        if self.combo>=3: lbl+=f"  ×{self.combo}!"
        self.texts.append(FloatTxt(cx2,cy2,lbl,GOLD if self.combo>=3 else SCC,big=self.combo>=3))
        if self.eats%4==0: self.bonus=self._sfood();self.bonus_t=7500
        if self.eats%4==0 and len([p for p in self.preys if not p.done])==0:
            pcol=hsv(random.random(),.82,.92)
            pr=Prey(self._sfood(),pcol)
            # Skill: sabr mezyan adds 5s
            if "prey_time" in getattr(self,"skills_owned",set()):
                pr.life+=5000  # instance override — class LIFE unchanged
            # Difficulty: prey gets faster with score
            diff=min(1.0, self.score/800.0)
            pr.spd=max(4, pr.spd + diff*3)       # max spd 7
            pr.flee_spd=max(5.5, pr.flee_spd + diff*3.5)  # max flee 9
            self.preys.append(pr)
        self.score+=pts;self.level=1+self.score//80;self.hi=max(self.hi,self.score)
        # Stage complete check
        if (not self.free_play and not self.stage_complete
                and self.score>=self.stage_score_target):
            self.stage_complete=True
            N2=len(STAGES)-1
            if self.stage_idx<N2: self.unlocked=max(self.unlocked,self.stage_idx+2)
            # Award skill points based on stage difficulty
            sp_earned=1+(self.stage_idx//5)
            self.skill_pts+=sp_earned
            cx4=PANEL+W//2; cy4=96+H//2
            self.texts.append(FloatTxt(cx4,cy4-60,f"+{sp_earned} SKILL PTS",(255,220,60),big=True))
            cx2=PANEL+W//2; cy2=96+H//2
            self.texts.append(FloatTxt(cx2,cy2-40,"STAGE COMPLETE!",GOLD,big=True))
            for _ in range(8): self.rings.append(Ring(cx2,cy2,GOLD,w=4))
            for _ in range(80): self.sparks.append(Spark(cx2,cy2,GOLD,sp=2.,big=True))
            sfx("boss_die")
        if self.level>pl:
            sfx("lvl");self._lvl_fx()
            self._check_boss_spawn()
        hx,hy=self.snake[0];dx,dy=self.dir
        head=((hx+dx)%COLS,(hy+dy)%ROWS)
        self.snake=[head]+self.snake
        self.food=self._sfood();self.trail_h=(self.trail_h+.003)%1.

    def _collect_pu(self,pu):
        kind=pu.kind;col=PU_COL[kind];cx2,cy2=self._sc(pu.pos)
        for _ in range(32): self.sparks.append(Spark(cx2,cy2,col,big=True))
        for _ in range(2): self.rings.append(Ring(cx2,cy2,col))
        self.texts.append(FloatTxt(cx2,cy2,PU_ICO[kind],col,big=True))
        sfx(kind if kind in SE else "pick")
        # Boss damage check
        if self.boss and self.boss.warn_t<=0 and kind==self.boss.kill_pu:
            self.boss.take_hit(self.score)
            bcol=self.boss.col; bx,by=self.boss.pos
            bcx=PANEL+bx*CELL+CELL//2; bcy=96+by*CELL+CELL//2
            for _ in range(40): self.sparks.append(Spark(bcx,bcy,bcol,sp=1.5,big=True))
            self.texts.append(FloatTxt(bcx,bcy-20,f"HIT! {self.boss.hp}/{self.boss.max_hp}",bcol,big=True))
            sfx("boss_hit");self.shake=10
        if kind==PH:
            # HEAL: remove last 3 segments (shrink snake)
            if len(self.snake)>4:
                remove=min(3,len(self.snake)-3)
                self.snake=self.snake[:-remove]
                self.texts.append(FloatTxt(cx2,cy2-28,f"-{remove} segs HEALED",col,big=True))
                for _ in range(25): self.sparks.append(Spark(cx2,cy2,col,big=True))
        elif kind==PZ:
            self.pus[PZ]=PU_DUR[PZ]
            self.texts.append(FloatTxt(cx2,cy2-28,"SPEED CAPPED!",col,big=True))
        elif kind==PW:
            self.pus[PW]=PU_DUR[PW]
            self.texts.append(FloatTxt(cx2,cy2-28,"TIME WARP!",col,big=True))
            for _ in range(5): self.rings.append(Ring(cx2,cy2,col,w=3))
        elif kind==PN:
            if self.boss: self.boss.warn_zones=[]
            self.texts.append(FloatTxt(cx2,cy2-28,"BOSS NUKED!",col,big=True))
            for _ in range(6): self.rings.append(Ring(cx2,cy2,col,w=4))
        elif kind==PD:
            # DASH: teleport snake 3 cells forward instantly
            hx3,hy3=self.snake[0]; dx3,dy3=self.dir
            solid3=self._solid()
            new_head=self.snake[0]
            for step in range(3):
                nh=((hx3+dx3*(step+1))%COLS,(hy3+dy3*(step+1))%ROWS)
                if nh not in solid3 and nh not in set(self.snake[:-1]):
                    new_head=nh
            if new_head!=self.snake[0]:
                self.snake=[new_head]+self.snake[:-1]
                self.shake=max(self.shake,8)
                for _ in range(30): self.sparks.append(Spark(cx2,cy2,col,sp=1.8,big=True))
                for _ in range(3):  self.rings.append(Ring(cx2,cy2,col,w=3))
                self.texts.append(FloatTxt(cx2,cy2-28,"DASH!",col,big=True))
                sfx("strt")
        elif kind==PR:
            # SHRINK: cut last 30% of snake (min 3)
            cut=max(0,len(self.snake)-max(3,int(len(self.snake)*.7)))
            if cut>0:
                self.snake=self.snake[:-cut]
                self.texts.append(FloatTxt(cx2,cy2-28,f"SHRINK -{cut}",col,big=True))
                for _ in range(25): self.sparks.append(Spark(cx2,cy2,col,big=True))
        elif kind==PB2:
            # x3 SCORE: 8 seconds triple points
            self.pus[PB2]=PU_DUR[PB2]
            self.texts.append(FloatTxt(cx2,cy2-28,"x3 SCORE!",col,big=True))
            for _ in range(6): self.rings.append(Ring(cx2,cy2,col,w=3))
        elif kind==PP:
            # PHASE: pass through walls AND own body for 6s
            self.pus[PP]=PU_DUR[PP]
            self.texts.append(FloatTxt(cx2,cy2-28,"PHASE!",col,big=True))
            for _ in range(5): self.rings.append(Ring(cx2,cy2,col,w=2))
        else:
            dur=PU_DUR.get(kind,5000)
            # Skill: Power Hoarder extends duration
            if "pu_longer" in getattr(self,"skills_owned",set()):
                dur=int(dur*1.3)
            self.pus[kind]=dur
            if kind==PF:
                for _ in range(4): self.rings.append(Ring(PANEL+W//2,96+H//2,col))

    def _die(self):
        self.state="dead";self.shake=26;self.hi=max(self.hi,self.score);sfx("die")
        hc=self.theme[1]
        for seg in self.snake[:16]:
            cx2,cy2=self._sc(seg)
            for _ in range(16): self.sparks.append(Spark(cx2,cy2,hc,big=True))
        for _ in range(5): self.rings.append(Ring(PANEL+W//2,96+H//2,DNG))

    def _upd_demo(self,dt):
        for sn in self.demo:
            sn["t"]+=dt
            if sn["t"]>200:
                sn["t"]=0;d=sn["dir"]
                if random.random()<.28:
                    ch=[dd for dd in[UP,DOWN,LEFT,RIGHT] if dd!=OPP.get(d)]
                    d=random.choice(ch);sn["dir"]=d
                hx,hy=sn["body"][0];head=((hx+d[0])%COLS,(hy+d[1])%ROWS)
                sn["body"]=[head]+sn["body"][:-1]
            sn["hue"]=(sn["hue"]+dt*.0002)%1.

    def _lvl_fx(self):
        cx2=PANEL+W//2;cy2=96+H//2
        for _ in range(7): self.rings.append(Ring(cx2,cy2,hsv(random.random(),.7,1.)))
        for _ in range(110):
            gx=random.randint(0,COLS-1);gy=random.randint(0,ROWS-1)
            cx3,cy3=self._sc((gx,gy));self.sparks.append(Spark(cx3,cy3,hsv(random.random(),.9,1.),big=True))

    # ══════════════════ RENDER ════════════════════
    def _render(self):
        sx=random.randint(-3,3) if self.shake>0 else 0
        sy=random.randint(-3,3) if self.shake>0 else 0
        ox=PANEL+sx;oy=96+sy
        surf=pygame.Surface((SW,SH));surf.fill(BG)
        self.stars.draw(surf,self.T);self.aurora.draw(surf,self.T)
        self._draw_atm(surf)
        if self.mode in(MODE_GAME,MODE_FREE):
            self._draw_panel(surf);self._draw_hud(surf)
        g_surf=self.free_ground if getattr(self,"free_play",False) else self.ground
        surf.blit(g_surf,(ox,oy))
        # Snow ground tint
        if self.weather.kind==WS:
            gt=asurf(W,H);gt.fill((200,220,255,int(18*self.weather.transition)));surf.blit(gt,(ox,oy))
        if self.mode in(MODE_MENU,MODE_STAGE):
            pass  # menu/stage draws its own overlay
        else:
            # Draw walls
            self._draw_walls(surf,ox,oy)
            # Draw active hazard (behind food/snake)
            if self.hazard:
                self.hazard.draw(surf,ox,oy,self.T)
            self._draw_food(surf,ox,oy)
            for pu in self.powerups: pu.draw(surf,ox,oy)
            for pr in self.preys: pr.draw(surf,ox,oy,self.T)
            if self.boss: self.boss.draw(surf,self.T)
            self._draw_snake(surf,ox,oy)
            # Weather on top of snake
            self.weather.draw_bg(surf,self.T)
            for b in self.bursts: b.draw(surf)
            for r in self.rings: r.draw(surf)
            for p in self.sparks: p.draw(surf)
            for t in self.texts: t.draw(surf)
            # Boss warning overlay
            if self.boss and self.boss.warn_t>0:
                self.boss.draw_warn(surf,self.T)
            if self.pus.get(PZ,0)>0:
                hx3,hy3=self.snake[0]
                scx3=PANEL+hx3*CELL+CELL//2+sx; scy3=96+hy3*CELL+CELL//2+sy
                cglow(surf,scx3,scy3,CELL//2+6,PU_COL[PZ],int(28+14*abs(math.sin(self.T*3))))
            if self.pus[PS]>0:
                hx,hy=self.snake[0];scx=PANEL+hx*CELL+CELL//2+sx;scy=96+hy*CELL+CELL//2+sy
                pr2=int(CELL//2+4+2.5*abs(math.sin(self.T*5)));col=PU_COL[PS]
                cglow(surf,scx,scy,pr2,col,int(34+16*abs(math.sin(self.T*4))))
                sa=asurf(pr2*2+4,pr2*2+4)
                pygame.draw.circle(sa,(*col,38),(pr2+2,pr2+2),pr2)
                pygame.draw.circle(sa,(*col,105),(pr2+2,pr2+2),pr2,2)
                surf.blit(sa,(scx-pr2-2,scy-pr2-2))
            if self.pus[PG]>0:
                go=asurf(W,H);go.fill((*PU_COL[PG],int(11+8*abs(math.sin(self.T*3)))));surf.blit(go,(PANEL+sx,96+sy))
            if self.pus.get(PP,0)>0:
                # PHASE: cyan tint + grid flicker
                ph=asurf(W,H); ph.fill((*PU_COL[PP],int(14+10*abs(math.sin(self.T*5)))));surf.blit(ph,(PANEL+sx,96+sy))
            if self.pus[PF]>0:
                fo=asurf(W,H);fo.fill((*PU_COL[PF],int(12+6*abs(math.sin(self.T*4)))));surf.blit(fo,(PANEL+sx,96+sy))
            if self.pus.get(PW,0)>0:
                # TIME WARP: purple slow-motion vignette on edges
                tw_ov=asurf(W,H)
                for edge in range(12):
                    ea=int(18*(1-edge/12))
                    pygame.draw.rect(tw_ov,(*PU_COL[PW],ea),(edge,edge,W-edge*2,H-edge*2),1)
                surf.blit(tw_ov,(PANEL+sx,96+sy))
                # Slow-mo label
                pulse2=abs(math.sin(self.T*2))
                wc=tuple(cl(c*(0.6+0.4*pulse2)) for c in PU_COL[PW])
                tc(surf,"⏱ TIME WARP",FXS,wc,PANEL+W//2,96+H-18)
        self._draw_ff(surf)
        surf.blit(self.sl,(PANEL,96));surf.blit(self.vig,(PANEL,96))
        pygame.draw.rect(surf,BDR,(PANEL,96,W,H),2);pygame.draw.rect(surf,BDH,(PANEL+1,97,W-2,H-2),1)
        self.weather.draw_hud(surf,self.T)
        if   self.mode==MODE_MENU:   self._draw_main_menu(surf)
        elif self.mode==MODE_STAGE:  self._draw_stage_sel(surf)
        elif self.state=="dead":     self._ov_dead(surf)
        elif self.state=="paused":   self._ov_pause(surf)
        elif self.stage_complete and self.mode in(MODE_GAME,MODE_FREE):
            self._ov_stage_complete(surf)
        # Skill menu overlays everything
        if getattr(self,"skill_menu",False):
            self._draw_skill_menu(surf)
        self.screen.blit(surf,(0,0))

    def _draw_atm(self,surf):
        for(px,py,phase,br) in self.dust:
            a=int(br*52*abs(math.sin(self.T*.48+phase)))
            if a>5:
                r=1 if br<.6 else 2;ds=asurf(r*4,r*4)
                pygame.draw.circle(ds,(182,210,188,a),(r*2,r*2),r);surf.blit(ds,(int(px)-r*2,int(py)-r*2))

    def _draw_ff(self,surf):
        for i,(fx,fy,phase,spd) in enumerate(self.ff):
            nx=fx+math.sin(self.T*spd+phase)*.54;ny=fy+math.cos(self.T*spd*.7+phase)*.40
            self.ff[i]=(nx,ny,phase,spd);blink=abs(math.sin(self.T*spd*2+phase))
            if blink>.25:
                a=int(blink*155);col=(186,255,126)
                cglow(surf,int(nx),int(ny),4,col,int(a*.18))
                dot=asurf(6,6);pygame.draw.circle(dot,(*col,a),(3,3),2);surf.blit(dot,(int(nx)-3,int(ny)-3))

    def _draw_panel(self,surf):
        # Gradient bg
        surf.blit(self.pbg,(0,0)); surf.blit(self.psl,(0,0))
        for i in range(5):
            a=cl(35*(1-i/5)); eg=asurf(2,SH); eg.fill((*NGN,a)); surf.blit(eg,(PANEL-2+i,0))
        pygame.draw.line(surf,(18,22,36),(PANEL-1,0),(PANEL-1,SH),1)

        cx=PANEL//2; hue=self.RT%1.; ac=hsv(hue,.72,1.)
        p=9; W2=PANEL-p*2; sep=(18,24,40)

        def card(y,h,col,r=8):
            """Draws a dark card with a left accent stripe"""
            bg=(cl(col[0]*.10),cl(col[1]*.10),cl(col[2]*.10))
            rbox_g(surf,(p,y,W2,h),
                   (cl(col[0]*.12),cl(col[1]*.12),cl(col[2]*.12)),
                   (cl(col[0]*.06),cl(col[1]*.06),cl(col[2]*.06)),r,sep,1)
            pygame.draw.rect(surf,col,(p,y,3,h),border_radius=2)

        def div(y):
            pygame.draw.line(surf,sep,(p,y),(PANEL-p,y),1)

        # ── TITLE ──────────────────────────────────────
        glow_tc(surf,"SNAKE",FXL,ac,cx,24,5)
        lw=100; lx=cx-lw//2
        pygame.draw.line(surf,(18,22,38),(lx,56),(lx+lw,56),1)
        dx=int(lx+(lw*((self.T*.3)%1.)))
        cglow(surf,dx,56,4,ac,28); pygame.draw.circle(surf,ac,(dx,56),2)
        tc(surf,"MYTHIC  EDITION",FXX,hsv(hue,.14,.28),cx,66)

        y=76
        # ── SCORE ──────────────────────────────────────
        card(y,68,ac)
        tc(surf,"SCORE",FXS,(55,65,90),cx,y+12)
        glow_tc(surf,str(self.score),FT,WHT,cx,y+44,3)
        y+=74

        # ── BEST · LEVEL · LEN ─────────────────────────
        cw=(W2-6)//3
        for xi,(lbl,val,col) in enumerate([
            ("BEST", str(self.hi),  GOLD),
            ("LVL",  str(self.level),ACC),
            ("LEN",  str(len(self.snake)),NFO)]):
            x=p+xi*(cw+3)
            card(y,42,col,7)
            tc(surf,lbl,FXX,tuple(cl(c*.55) for c in col),x+cw//2,y+10)
            tc(surf,val,FM,col,x+cw//2,y+30)
        y+=48

        # ── XP BAR ─────────────────────────────────────
        xf=(self.score%80)/80; xc=hsv((hue+.12)%1.,.82,1.)
        pygame.draw.rect(surf,(9,11,20),(p,y,W2,8),border_radius=4)
        fw=max(0,int(W2*xf))
        if fw>3:
            pygame.draw.rect(surf,xc,(p,y,fw,8),border_radius=4)
            sx=min(p+fw-5,p+W2-9)
            sh=asurf(9,8); pygame.draw.rect(sh,(*WHT,45),(0,0,9,8),border_radius=3); surf.blit(sh,(sx,y))
        tc(surf,f"next lv  {int(xf*100)}%",FXX,(38,46,68),cx,y+16)
        y+=26

        # ── SKIN ───────────────────────────────────────
        th=self.theme; thc=th[1]
        card(y,30,thc,7)
        tc(surf,th[0],FM,thc,cx,y+15)
        sw2=W2//len(THEMES)
        for ki,kth in enumerate(THEMES):
            kc=kth[1]; ks=asurf(sw2-1,3)
            pygame.draw.rect(ks,(*kc,230 if ki==self.theme_idx else 45),(0,0,sw2-1,3),border_radius=1)
            surf.blit(ks,(p+ki*sw2,y+27))
        y+=34; div(y); y+=5

        # ── WEATHER ────────────────────────────────────
        wc_m={WR:(55,125,255),WS:(145,205,255),WL:(255,215,55),WN:(32,40,62)}
        wn_m={WR:"🌧  RAIN",WS:"❄  SNOW",WL:"⚡  STORM",WN:"clear"}
        ws_m={WR:"slippery",WS:"−48% speed",WL:"strikes!",WN:""}
        wk=self.weather.kind; wc=wc_m[wk]
        pw=abs(math.sin(self.T*2.4)); wcp=tuple(cl(c*(0.62+0.38*pw)) for c in wc)
        card(y,38,wc,7)
        tc(surf,wn_m[wk],FM,wcp,cx,y+12)
        if ws_m[wk]: tc(surf,ws_m[wk],FXX,(48,56,78),cx,y+28)
        wf=max(0,self.weather.timer/45000)
        nbar(surf,p,y+35,W2,2,wf,1.,wc,2)
        y+=42; div(y); y+=5

        # ── BOSS ───────────────────────────────────────
        if self.boss and self.boss.warn_t<=0:
            bc=self.boss.col; ang=self.boss.anger
            bca=lc(bc,(220,35,35),ang*.7)
            pb=abs(math.sin(self.T*(3+ang*3))); bcp=tuple(cl(c*(0.58+0.42*pb)) for c in bca)
            card(y,54,bca)
            tc(surf,f"⚔ {self.boss.name}",FM,bcp,cx,y+12)
            nbar(surf,p,y+24,W2,7,self.boss.hp,self.boss.max_hp,bca,4)
            tc(surf,f"HP {self.boss.hp}/{self.boss.max_hp}",FXX,bca,cx-22,y+39)
            pk=self.boss.kill_pu
            tc(surf,f"➤ {PU_ICO[pk]}",FXX,PU_COL[pk],cx+22,y+39)
            y+=60
        elif self.level in BOSSES and self.level not in self.boss_killed:
            bc=BOSSES[self.level]["col"]; pb2=abs(math.sin(self.T*2.8))
            card(y,30,bc,7)
            bcp2=tuple(cl(c*(0.5+0.5*pb2)) for c in bc)
            tc(surf,f"⚠ {BOSSES[self.level]['name']}",FXS,bcp2,cx,y+10)
            bk=BOSS_KILL_PU[self.level]
            tc(surf,f"prepare {PU_ICO[bk]}",FXX,PU_COL[bk],cx,y+23)
            y+=36
        div(y); y+=5

        # ── PREY ───────────────────────────────────────
        alive=[pr for pr in self.preys if not pr.done]
        if alive:
            pr=alive[0]; pcol=pr.col; frac=max(0,pr.life/pr.LIFE)
            cc2=lc(pcol,DNG,.5) if pr.fleeing else pcol
            card(y,50,cc2)
            lbl3="🏃 FLEEING!" if pr.fleeing else "🐾 PREY!"
            tc(surf,lbl3,FM,cc2,cx,y+12)
            if frac<.33:
                bc3=lc(DNG,pcol,abs(math.sin(self.T*9))*.5)
            else:
                bc3=lc(DNG,pcol,frac)
            nbar(surf,p,y+24,W2,6,pr.life,pr.LIFE,bc3,3)
            secs=max(0,int(pr.life/1000))
            stxt=f"{secs}s ⚠" if secs<=4 else f"{secs}s"
            tc(surf,stxt,FXX,bc3,cx-(20 if pr.has_pu and pr.pu_kind else 0),y+38)
            if pr.has_pu and pr.pu_kind:
                tc(surf,f"+{PU_ICO[pr.pu_kind]}",FXX,PU_COL[pr.pu_kind],cx+26,y+38)
            y+=56
        else:
            tc(surf,"prey: every 4 eats",FXX,(28,36,56),cx,y+8); y+=18
        div(y); y+=5

        # ── ACTIVE POWERS ──────────────────────────────
        active=[(k,self.pus.get(k,0),PU_DUR.get(k,5000)) for k in[PS,PV,PM,PX,PG,PF,PL,PZ,PW,PP,PB2] if self.pus.get(k,0)>0]
        if active:
            tc(surf,"POWERS",FXX,(40,48,70),cx,y+6); y+=14
            for pi,(kind,rem,mxd) in enumerate(active[:4]):
                col2=PU_COL[kind]; py2=y+pi*25
                card(py2,21,col2,5)
                nbar(surf,p,py2+15,W2,3,rem,mxd,col2,2)
                tc(surf,PU_ICO[kind],FXX,col2,cx,py2+6)
            y+=len(active[:4])*25+8
            div(y); y+=5

        # ── COMBO ──────────────────────────────────────
        if self.combo>=2:
            cc4=hsv((self.RT+.33)%1.,.95,1.); pa=cl(65+55*abs(math.sin(self.T*5)))
            card(y,46,cc4,10)
            gl=asurf(W2,46); pygame.draw.rect(gl,(*cc4,pa),(0,0,W2,46),border_radius=10)
            surf.blit(gl,(p,y))
            tc(surf,"COMBO",FXX,cc4,cx,y+8)
            glow_tc(surf,f"x{self.combo}",FT,cc4,cx,y+30,3)
            y+=52

        # ── FOOTER ─────────────────────────────────────
        div(SH-54)
        for i,(t2,c2) in enumerate([
            ("WASD  move",(30,38,58)),
            ("P pause  ·  ESC quit",(30,38,58)),
            ("right PU defeats boss",(38,65,38))]):
            tc(surf,t2,FXX,c2,cx,SH-46+i*15)

    def _draw_hud(self,surf):
        for y in range(96):
            c=lc((6,8,16),(3,5,10),y/96)
            pygame.draw.line(surf,c,(PANEL,y),(PANEL+W,y))
        cx=PANEL+W//2; hue=self.RT%1.
        # Mode badge — top left
        if getattr(self,"free_play",False):
            mc=(60,200,110)
            rbox(surf,(PANEL+8,3,96,18),(8,18,12),9,(25,60,35),1)
            pygame.draw.rect(surf,mc,(PANEL+8,3,3,18),border_radius=2)
            tc(surf,"FREE PLAY",FXX,mc,PANEL+56,12)
        elif hasattr(self,"stage_idx") and self.stage_idx<len(STAGES):
            st4=STAGES[self.stage_idx]; sc4=st4["col"]
            rbox(surf,(PANEL+8,3,96,18),(cl(sc4[0]*.12),cl(sc4[1]*.12),cl(sc4[2]*.12)),9,
                 (cl(sc4[0]*.35),cl(sc4[1]*.35),cl(sc4[2]*.35)),1)
            pygame.draw.rect(surf,sc4,(PANEL+8,3,3,18),border_radius=2)
            tc(surf,f"STAGE {st4['id']}",FXX,sc4,PANEL+56,12)

        # Bottom separator glow
        sep_c=hsv(hue,.6,.5)
        for i in range(3):
            a=cl(45*(1-i/3))
            s2=asurf(W,1); s2.fill((*sep_c,a)); surf.blit(s2,(PANEL,93+i))
        pygame.draw.line(surf,(14,18,32),(PANEL,95),(PANEL+W,95),1)

        # ── LEFT: Weather ─────────────────────────────
        wc_m={WR:(55,125,255),WS:(145,205,255),WL:(255,215,55),WN:(30,40,65)}
        wn_m={WR:"🌧  RAIN",WS:"❄  SNOW",WL:"⚡  STORM",WN:""}
        wk=self.weather.kind
        if wk!=WN:
            wc=wc_m[wk]; pw=abs(math.sin(self.T*2.5))
            wcp=tuple(cl(c*(0.55+0.45*pw)) for c in wc)
            tc(surf,wn_m[wk],FM,wcp,PANEL+60,22)
            wf=max(0,self.weather.timer/45000)
            pygame.draw.rect(surf,(10,14,24),(PANEL+14,34,96,4),border_radius=2)
            if wf>0: pygame.draw.rect(surf,wc,(PANEL+14,34,int(96*wf),4),border_radius=2)

        # ── CENTRE: Level + XP ────────────────────────
        n=min(self.level,22)
        if n>0:
            dw=n*13+(n-1)*3; dx0=cx-dw//2
            for i in range(n):
                dc=hsv((hue+i*.05)%1.,.88,.96)
                bx=dx0+i*16; by=20
                # glow behind dot
                gs=asurf(14,14); pygame.draw.circle(gs,(*dc,22),(7,7),7); surf.blit(gs,(bx-7,by-7))
                pygame.draw.circle(surf,dc,(bx,by),4)
                pygame.draw.circle(surf,(*WHT,160),(bx-1,by-1),1)
        # Level label
        lc3=hsv(hue,.45,.55)
        tc(surf,f"LEVEL  {self.level}",FS,lc3,cx,48)
        # XP bar — full width, thin
        xf=(self.score%80)/80; xc=hsv((hue+.12)%1.,.85,1.)
        pygame.draw.rect(surf,(8,10,20),(PANEL+16,60,W-32,5),border_radius=3)
        fw2=max(0,int((W-32)*xf))
        if fw2>3:
            pygame.draw.rect(surf,xc,(PANEL+16,60,fw2,5),border_radius=3)
            # shimmer dot
            shx=min(PANEL+16+fw2-5, PANEL+W-20)
            sc3=asurf(10,5); pygame.draw.rect(sc3,(*WHT,60),(0,0,10,5),border_radius=3)
            surf.blit(sc3,(shx,60))

        # ── COMBO bar ─────────────────────────────────
        if self.combo>0 and self.state=="running":
            cc=hsv(hue,.94,1.)
            cb_x=PANEL+16; cb_w=W-32
            pygame.draw.rect(surf,(8,10,20),(cb_x,70,cb_w,6),border_radius=3)
            fw3=max(0,int(cb_w*self.combo/10))
            if fw3>2: pygame.draw.rect(surf,cc,(cb_x,70,fw3,6),border_radius=3)
            tc(surf,f"COMBO  x{self.combo}",FS,cc,cx,82)

        # ── RIGHT: Prey arrow ─────────────────────────
        alive=[pr for pr in self.preys if not pr.done]
        if alive and self.state=="running":
            pr=alive[0]; ppx,ppy=pr.pos; hx2,hy2=self.snake[0]
            angle=math.atan2(ppy-hy2,ppx-hx2)
            # Arrow base position: right side of HUD
            arx=PANEL+W-52; ary=28
            arx2=arx+int(math.cos(angle)*16); ary2=ary+int(math.sin(angle)*10)
            col2=pr.col; aa=int(150+85*abs(math.sin(self.T*5)))
            # Arrow triangle
            pts=[(arx2+int(math.cos(angle)*13),ary2+int(math.sin(angle)*13)),
                 (arx2+int(math.cos(angle+2.5)*6),ary2+int(math.sin(angle+2.5)*6)),
                 (arx2+int(math.cos(angle-2.5)*6),ary2+int(math.sin(angle-2.5)*6))]
            as2=asurf(SW,SH); pygame.draw.polygon(as2,(*col2,aa),pts); surf.blit(as2,(0,0))
            lbl2="🏃" if pr.fleeing else "PREY"
            pt2=FXX.render(lbl2,True,(*col2,aa))
            ls=asurf(pt2.get_width()+2,pt2.get_height()+2)
            ls.blit(pt2,(1,1)); ls.set_alpha(aa)
            surf.blit(ls,(arx2-pt2.get_width()//2,ary2+14))

    def _draw_walls(self,surf,ox,oy):
        """Draw stage barrier walls — chibi tile style"""
        walls=getattr(self,"stage_walls",set())
        if not walls: return
        gt=getattr(self,"ground_theme","grass")
        # Wall colour per theme
        wc_map={
            "grass": (55,130,60),"sand":(160,120,40),"ice":(80,140,200),
            "void":  (60,40,120),"lava":(180,60,20),"purple":(100,50,180),
        }
        wc=wc_map.get(gt,(60,80,60))
        whi=tuple(min(255,c+60) for c in wc)  # highlight
        wdk=tuple(max(0,c-40) for c in wc)    # shadow

        # Pre-check neighbours for connected drawing
        def has(dx,dy,cx,cy): return (cx+dx,cy+dy) in walls

        for (gx,gy) in walls:
            px=ox+gx*CELL; py=oy+gy*CELL
            # Base tile
            ws=pygame.Surface((CELL,CELL)); ws.fill(wdk)
            # Top face (lighter)
            pygame.draw.rect(ws,wc,(0,0,CELL,CELL-3))
            # Top highlight strip
            pygame.draw.rect(ws,whi,(0,0,CELL,4))
            # Left highlight
            pygame.draw.rect(ws,whi,(0,0,3,CELL))
            # Bottom shadow
            pygame.draw.rect(ws,wdk,(0,CELL-4,CELL,4))
            # Right shadow
            pygame.draw.rect(ws,wdk,(CELL-4,0,4,CELL))
            # Inner darker centre
            pygame.draw.rect(ws,(max(0,wdk[0]-10),max(0,wdk[1]-10),max(0,wdk[2]-10)),
                             (4,4,CELL-8,CELL-8))
            # Shine dot (chibi highlight)
            pygame.draw.circle(ws,whi,(5,5),3)
            # Pixel border
            pygame.draw.rect(ws,(min(255,whi[0]+20),min(255,whi[1]+20),min(255,whi[2]+20)),
                             (0,0,CELL,CELL),1)
            surf.blit(ws,(px,py))
            # Glow aura on exposed sides
            if not has(-1,0,gx,gy):
                for i in range(3):
                    a=int(30*(1-i/3))
                    gs=asurf(3,CELL); gs.fill((*whi,a)); surf.blit(gs,(px-3+i,py))
            if not has(0,-1,gx,gy):
                for i in range(3):
                    a=int(30*(1-i/3))
                    gs=asurf(CELL,3); gs.fill((*whi,a)); surf.blit(gs,(px,py-3+i))

    def _draw_food(self,surf,ox,oy):
        if not self.food: return
        # ghost_food skill: draw food even through dark hazard
        dark_hz2=self.hazard if self.hazard and isinstance(self.hazard,HazardDark) else None
        ghost_food_skill="ghost_food" in getattr(self,"skills_owned",set())
        pulse=abs(math.sin(self.T*2.8))*2.5
        fx,fy=self.food; cx=ox+fx*CELL+CELL//2; cy=oy+fy*CELL+CELL//2
        r=int(CELL//2-1+pulse)  # bigger
        # Outer glow rings (double)
        gr=r+int(6+4*abs(math.sin(self.T*2.8)))
        cglow(surf,cx,cy,gr+6,(255,60,60),18)
        cglow(surf,cx,cy,gr,AP,42)
        # Shadow
        sh=asurf(r*2+6,7); pygame.draw.ellipse(sh,(0,0,0,55),(0,0,r*2+6,7))
        surf.blit(sh,(cx-r-3,cy+r-2))
        # Body layers
        pygame.draw.circle(surf,(140,20,20),(cx,cy),max(1,r))       # dark base
        pygame.draw.circle(surf,AP,(cx,cy),max(1,r-1))              # main red
        pygame.draw.circle(surf,(255,100,100),(cx,cy),max(1,r-2))   # mid
        pygame.draw.circle(surf,APS,(cx-max(1,r//3),cy-max(1,r//3)),max(1,r//3))  # shine
        # Stem
        pygame.draw.line(surf,STEM,(cx,cy-r),(cx+2,cy-r-7),2)
        # Leaf
        lox=int(math.sin(self.T*1.6)*1.5)
        pygame.draw.ellipse(surf,LF,(cx+lox,cy-r-8,10,5))
        pygame.draw.ellipse(surf,(60,160,60),(cx+lox+1,cy-r-7,6,3))
        # Magnet ring
        if self.pus[PM]>0:
            cglow(surf,cx,cy,r+10,PU_COL[PM],int(40+20*abs(math.sin(self.T*4))))
        # Bonus star
        if self.bonus:
            bx2,by2=self.bonus; bcx=ox+bx2*CELL+CELL//2; bcy=oy+by2*CELL+CELL//2
            br=int(CELL//2+1+pulse); gc=hsv((self.RT*2.4)%1.,.8,1.)
            cglow(surf,bcx,bcy,br+8,gc,55)
            cglow(surf,bcx,bcy,br+2,gc,90)
            rot=self.T*1.5; pts=[]
            for i in range(10):
                a=-math.pi/2+rot+i*2*math.pi/10
                rad=br if i%2==0 else br//2+2
                pts.append((bcx+int(rad*math.cos(a)),bcy+int(rad*math.sin(a))))
            if len(pts)>=3:
                pygame.draw.polygon(surf,STC,pts)
                pygame.draw.polygon(surf,STH,pts,2)

    def _seg_col(self,i,n):
        tr=i/max(n-1,1);t2=self.theme_t;th=self.theme;pth=self.prev_theme
        ci=1 if i==0 else(2 if i%3==0 else(3 if i%3==1 else 4))
        fade=1-tr*.80
        cur=tuple(cl(c*fade) for c in th[ci]);prev=tuple(cl(c*fade) for c in pth[ci])
        return lc(prev,cur,t2)

    def _draw_snake(self,surf,ox,oy):
        n=len(self.snake)
        if n==0: return
        dark_hz=self.hazard if self.hazard and isinstance(self.hazard,HazardDark) else None
        combo_mode=self.combo>=3; ghost=self.pus[PG]>0
        for i in range(n-1,-1,-1):
            gx,gy=self.snake[i]; tr=i/max(n-1,1)
            if combo_mode:
                h=(self.trail_h+i*.055)%1.
                color=tuple(cl(c*(1-tr*.75)) for c in hsv(h,.82,.92))
            else:
                color=self._seg_col(i,n)
            if self.weather.kind==WS:
                color=lc(color,(180,210,240),self.weather.transition*.22)
            # Head slightly bigger, tail tapers
            if i==0:   pad=1;  rad=10
            elif i==1: pad=1;  rad=9
            else:      pad=max(2,2+int(tr*2.5)); rad=max(3,9-int(tr*5))
            rx=ox+gx*CELL+pad; ry=oy+gy*CELL+pad
            rw=CELL-pad*2; rh=CELL-pad*2
            if rw<=0 or rh<=0: continue
            if ghost:
                gs=asurf(rw,rh)
                pygame.draw.rect(gs,(*color,95),(0,0,rw,rh),border_radius=rad)
                surf.blit(gs,(rx,ry))
            else:
                # Drop shadow
                sha=cl(28*(1-tr*.8))
                if sha>3:
                    ss=asurf(rw,5); pygame.draw.ellipse(ss,(0,0,0,sha),(0,0,rw,5))
                    surf.blit(ss,(rx,ry+rh-2))
                # Main body
                # Dark hazard — dim cells in dark zones
                draw_col=color
                if dark_hz and dark_hz.in_dark(gx,gy):
                    draw_col=tuple(max(0,c//5) for c in color)
                pygame.draw.rect(surf,draw_col,(rx,ry,rw,rh),border_radius=rad)
                # Inner highlight (top-left)
                hi_col=tuple(cl(min(255,c+40)) for c in color)
                hi_s=asurf(rw-4,rh-4)
                pygame.draw.ellipse(hi_s,(*hi_col,28),(0,0,rw-4,rh-4))
                surf.blit(hi_s,(rx+2,ry+2))
                # Belly stripe
                if rh>7:
                    belly=self.theme[5] if not combo_mode else (200,220,160)
                    bh2=max(2,rh//3)
                    bs=asurf(max(1,rw-6),bh2)
                    pygame.draw.rect(bs,(*lc(color,belly,.28),52),(0,0,max(1,rw-6),bh2),border_radius=2)
                    surf.blit(bs,(rx+3,ry+rh-bh2-2))
                # Scale shimmer every other segment
                if i>0 and i%3==0 and rw>7:
                    sc=asurf(rw,rh)
                    pygame.draw.ellipse(sc,(*WHT,9),(2,2,rw-4,rh-4))
                    surf.blit(sc,(rx,ry))
        hx,hy=self.snake[0];dx,dy=self.dir
        hrx=ox+hx*CELL+1;hry=oy+hy*CELL+1;hrw=CELL-2;hrh=CELL-2
        if not ghost:
            ss=asurf(hrw,5);pygame.draw.ellipse(ss,(0,0,0,40),(0,0,hrw,5));surf.blit(ss,(hrx,hry+hrh-2))
        sc2=self.theme[6];pygame.draw.rect(surf,sc2,(hrx+3,hry+3,max(1,hrw//3),max(1,hrh//3)),border_radius=2)
        if   dx==1:  e1=(ox+hx*CELL+CELL-7,oy+hy*CELL+8);     e2=(ox+hx*CELL+CELL-7,oy+hy*CELL+CELL-8)
        elif dx==-1: e1=(ox+hx*CELL+7,     oy+hy*CELL+8);     e2=(ox+hx*CELL+7,     oy+hy*CELL+CELL-8)
        elif dy==-1: e1=(ox+hx*CELL+8,     oy+hy*CELL+7);     e2=(ox+hx*CELL+CELL-8,oy+hy*CELL+7)
        else:        e1=(ox+hx*CELL+8,     oy+hy*CELL+CELL-7);e2=(ox+hx*CELL+CELL-8,oy+hy*CELL+CELL-7)
        for ex,ey in(e1,e2):
            pygame.draw.circle(surf,(8,8,8),(ex,ey),4);pygame.draw.circle(surf,(255,213,33),(ex,ey),3)
            pygame.draw.circle(surf,(4,4,4),(ex,ey),2);pygame.draw.circle(surf,WHT,(ex+1,ey-1),1)
        if int(self.T*4)%4<2:
            tbx=ox+hx*CELL+CELL//2+dx*(CELL//2-1);tby=oy+hy*CELL+CELL//2+dy*(CELL//2-1)
            pygame.draw.line(surf,(202,15,15),(tbx,tby),(tbx+dx*6+dy*3,tby+dy*6+dx*3),1)
            pygame.draw.line(surf,(202,15,15),(tbx,tby),(tbx+dx*6-dy*3,tby+dy*6-dx*3),1)

    def _draw_demo(self,surf,ox,oy):
        for sn in self.demo:
            for i,(gx,gy) in enumerate(sn["body"]):
                a=cl(72*(1-i/max(len(sn["body"])-1,1)));col=hsv(sn["hue"],.52,.34)
                s=asurf(CELL-4,CELL-4);pygame.draw.rect(s,(*col,a),(0,0,CELL-4,CELL-4),border_radius=5)
                surf.blit(s,(ox+gx*CELL+2,oy+gy*CELL+2))

    def _ov_bg(self,surf,a=208):
        ov=asurf(W,H);ov.fill((3,5,9,a));surf.blit(ov,(PANEL,96))

    # ═══════════════════════════════════════════════
    #  H O M E   S C R E E N
    # ═══════════════════════════════════════════════
    def _handle_skill_click(self,mx,my):
        cx=PANEL+W//2; sy0=96+H//2-120
        sw=320; sh=50; sx=cx-sw//2
        for i,sk in enumerate(SKILLS):
            by2=sy0+i*(sh+6)
            if sx<=mx<=sx+sw and by2<=my<=by2+sh:
                if (sk["id"] not in self.skills_owned
                        and self.skill_pts>=sk["cost"]):
                    self.skills_owned.add(sk["id"])
                    self.skill_pts-=sk["cost"]
                    sfx("lvl")
            # Close button
        if PANEL+W-60<=mx<=PANEL+W-10 and 96+10<=my<=96+40:
            self.skill_menu=False

    def _draw_skill_menu(self,surf):
        """Overlay skill shop"""
        cx=PANEL+W//2; cy=96+H//2
        mx,my=pygame.mouse.get_pos()
        # Dim background
        ov=asurf(W,H); ov.fill((2,3,8,235)); surf.blit(ov,(PANEL,96))
        # Title
        glow_tc(surf,"DKKAN L-MHARAT",FT,GOLD,cx,cy-168,4)
        sp=getattr(self,"skill_pts",0)
        tc(surf,f"Nqat l-Mhara: {sp}",FB,GOLD,cx,cy-138)
        tc(surf,"Rbhom men stages — akter s3oba = akter nqat",FXS,(50,62,80),cx,cy-118)
        # Skill cards
        sw=340; sh=50; sx=cx-sw//2; sy0=cy-100
        for i,sk in enumerate(SKILLS):
            by2=sy0+i*(sh+5)
            owned=sk["id"] in getattr(self,"skills_owned",set())
            can_buy=not owned and sp>=sk["cost"]
            hov=(sx<=mx<=sx+sw and by2<=my<=by2+sh)
            col=sk["col"]
            # Card
            if owned:
                rbox_g(surf,(sx,by2,sw,sh),(cl(col[0]*.15),cl(col[1]*.15),cl(col[2]*.15)),
                       (cl(col[0]*.08),cl(col[1]*.08),cl(col[2]*.08)),8,
                       tuple(cl(c*.6) for c in col),2)
                pygame.draw.rect(surf,col,(sx,by2,4,sh),border_radius=2)
                tc(surf,"✓ OWNED",FXS,col,sx+sw-36,by2+sh//2)
            elif can_buy and hov:
                gs=asurf(sw+14,sh+14)
                pygame.draw.rect(gs,(*col,35),(0,0,sw+14,sh+14),border_radius=10)
                surf.blit(gs,(sx-7,by2-7))
                rbox_g(surf,(sx,by2,sw,sh),(cl(col[0]*.20),cl(col[1]*.20),cl(col[2]*.20)),
                       (cl(col[0]*.10),cl(col[1]*.10),cl(col[2]*.10)),8,
                       tuple(cl(c*.8) for c in col),2)
                pygame.draw.rect(surf,col,(sx,by2,4,sh),border_radius=2)
            else:
                alpha=0.10 if not can_buy else 0.13
                rbox(surf,(sx,by2,sw,sh),
                     (cl(col[0]*alpha),cl(col[1]*alpha),cl(col[2]*alpha)),8,
                     tuple(cl(c*(0.3 if not can_buy else 0.45)) for c in col),1)
                pygame.draw.rect(surf,tuple(cl(c*(.5 if can_buy else .3)) for c in col),
                                 (sx,by2,4,sh),border_radius=2)
            # Content
            lc2=col if (owned or can_buy) else tuple(cl(c*.4) for c in col)
            tc(surf,sk["name"],FM,lc2,sx+120,by2+15)
            tc(surf,sk["desc"],FXX,tuple(cl(c*.6) for c in lc2),sx+120,by2+32)
            # Cost
            cost_c=GOLD if can_buy else (tuple(cl(c*.5) for c in GOLD) if not owned else (40,50,30))
            tc(surf,("✓" if owned else f"{sk['cost']} pts"),FXS,cost_c,sx+sw-22,by2+sh//2)
            # Number key hint
            tc(surf,f"{i+1}",FXX,(35,42,58),sx+14,by2+sh//2)
        # Close button
        close_hov=(PANEL+W-60<=mx<=PANEL+W-10 and 96+10<=my<=96+40)
        rbox(surf,(PANEL+W-58,96+12,46,28),(18,22,34),8,
             (60,80,120) if close_hov else (30,36,54),1)
        tc(surf,"ESC",FXS,(80,110,160) if close_hov else (50,65,90),PANEL+W-35,96+26)

    def _draw_main_menu(self,surf):
        cx=PANEL+W//2; cy=96+H//2
        hue=self.RT%1.; mx,my=pygame.mouse.get_pos()

        # ── Background layers ─────────────────────────
        ov=asurf(W,H); ov.fill((2,4,12,225)); surf.blit(ov,(PANEL,96))
        self._draw_demo(surf,PANEL,96)
        ov2=asurf(W,H); ov2.fill((2,4,12,145)); surf.blit(ov2,(PANEL,96))

        # Scanline effect for retro feel
        for y in range(0,H,4):
            sl=asurf(W,1); sl.fill((0,0,0,18)); surf.blit(sl,(PANEL,96+y))

        # ── GIANT RAINBOW TITLE ───────────────────────
        title="SNAKE"
        char_w=52; total_tw=len(title)*char_w; tx0=cx-total_tw//2+4
        for ci,ch in enumerate(title):
            ch_hue=(hue+ci*0.12)%1.
            cc=hsv(ch_hue,.85,1.)
            # Drop shadow
            sh=tuple(max(0,c//5) for c in cc)
            t=FXL.render(ch,True,sh)
            for r in range(5,0,-1):
                surf.blit(t,(tx0+ci*char_w-t.get_width()//2+r,cy-178+r))
            # Outline
            t2=FXL.render(ch,True,(10,10,20))
            for dx,dy in[(-2,0),(2,0),(0,-2),(0,2)]:
                surf.blit(t2,(tx0+ci*char_w-t2.get_width()//2+dx,cy-178+dy))
            # Main letter
            tm=FXL.render(ch,True,cc)
            surf.blit(tm,(tx0+ci*char_w-tm.get_width()//2,cy-178))
            # Shine dot on letter
            shine_a=int(160*abs(math.sin(self.T*2+ci*.8)))
            sd=asurf(8,8); pygame.draw.circle(sd,(*WHT,shine_a),(4,4),4)
            surf.blit(sd,(tx0+ci*char_w-4,cy-174))

        # Subtitle with typewriter shimmer
        sub="M Y T H I C   E D I T I O N"
        sub_hue=(hue+0.5)%1.
        tc(surf,sub,FM,hsv(sub_hue,.30,.50),cx,cy-115)

        # Animated separator
        sw=int(100+50*abs(math.sin(self.T*1.3)))
        sep_c=hsv(hue,.7,1.)
        pygame.draw.rect(surf,sep_c,(cx-sw//2,cy-100,sw,3),border_radius=2)
        # Moving dot on separator
        dot_x=int(cx-sw//2+(sw*((self.T*.6)%1.)))
        cglow(surf,dot_x,cy-99,6,sep_c,40)
        pygame.draw.circle(surf,sep_c,(dot_x,cy-99),4)

        # ── 3 MAIN BUTTONS (world-class style) ────────
        bw=300; bh=58; bx=cx-bw//2
        buttons=[
            (cy-58, hsv(hue,.75,1.),       "▶  STAGES",      f"{self.unlocked}/40 unlocked", True),
            (cy+16, (50,210,110),            "⚡  FREE PLAY",   "No limits, no pressure",       False),
            (cy+90, (180,55,55),             "✕  QUIT",         "",                              False),
        ]
        for (by2,bcol,lbl,sub2,is_main) in buttons:
            hov=(bx<=mx<=bx+bw and by2<=my<=by2+bh)
            scale=1.0+(0.015 if hov else 0.0)
            sw2=int(bw*scale); sh2=int(bh*scale)
            sxb=cx-sw2//2; syb=by2-int((sh2-bh)//2)

            # Outer glow
            ga=int(55 if hov else (35 if is_main else 18))
            pulse_g=abs(math.sin(self.T*(2.5 if is_main else 1.5)))
            ga=int(ga*(0.7+0.3*pulse_g))
            gl=asurf(sw2+24,sh2+24)
            pygame.draw.rect(gl,(*bcol,ga),(0,0,sw2+24,sh2+24),border_radius=sh2//2+8)
            surf.blit(gl,(sxb-12,syb-12))

            # Button bg
            at=0.28 if hov else (0.20 if is_main else 0.15)
            ab=0.14 if hov else (0.10 if is_main else 0.07)
            rbox_g(surf,(sxb,syb,sw2,sh2),
                   (cl(bcol[0]*at),cl(bcol[1]*at),cl(bcol[2]*at)),
                   (cl(bcol[0]*ab),cl(bcol[1]*ab),cl(bcol[2]*ab)),
                   sh2//2,
                   tuple(cl(c*(0.95 if hov else 0.55)) for c in bcol),2)
            # Left accent bar (thicker for main)
            bw3=5 if is_main else 3
            pygame.draw.rect(surf,bcol,(sxb,syb,bw3,sh2),border_radius=3)
            # Shine strip on top
            shine=asurf(sw2-bw3-4,sh2//2)
            pygame.draw.rect(shine,(*WHT,18 if hov else 10),(0,0,sw2-bw3-4,sh2//2),border_radius=sh2//4)
            surf.blit(shine,(sxb+bw3+2,syb+2))

            # Label
            lc_p=abs(math.sin(self.T*2.5)) if is_main else 0.8
            lc_col=tuple(cl(c*(0.72+0.28*lc_p)) for c in bcol)
            lf=FB if is_main else FM
            glow_tc(surf,lbl,lf,lc_col,cx+(20 if sub2 else 0),syb+sh2//2-(9 if sub2 else 0),2 if hov else 1)
            if sub2:
                tc(surf,sub2,FXX,tuple(cl(c*.48) for c in bcol),cx+20,syb+sh2//2+12)

        # ── Act progress strip ─────────────────────────
        n_un=getattr(self,"unlocked",1)
        act_now=(n_un-1)//5+1
        ap_y=cy+160
        # Act icons
        act_cols=[(70,200,90),(55,130,220),(200,140,255),(160,215,255),(160,120,75),
                  (50,130,70),(255,160,60),(100,165,255)]
        act_w=52; act_total=8*act_w; act_x0=cx-act_total//2
        for ai in range(8):
            ax=act_x0+ai*act_w; done=((ai+1)*5<=n_un)
            curr=(ai+1==act_now)
            ac=act_cols[ai]
            # Circle
            ar=15 if curr else 12
            pygame.draw.circle(surf,ac if done or curr else (20,24,36),(ax+act_w//2,ap_y),ar)
            if done:
                pygame.draw.circle(surf,WHT,(ax+act_w//2,ap_y),ar,2)
                tc(surf,"✓",FXX,WHT,ax+act_w//2,ap_y)
            elif curr:
                pulse_a=abs(math.sin(self.T*3))
                pygame.draw.circle(surf,tuple(cl(c*(0.6+0.4*pulse_a)) for c in ac),
                                   (ax+act_w//2,ap_y),ar,2)
                tc(surf,f"{ai+1}",FXX,ac,ax+act_w//2,ap_y)
            else:
                tc(surf,f"{ai+1}",FXX,(30,36,52),ax+act_w//2,ap_y)
            # Connector
            if ai<7:
                lc3=(30,38,56) if not done else act_cols[ai]
                pygame.draw.line(surf,lc3,(ax+act_w//2+ar,ap_y),(ax+act_w-1,ap_y),2)

        tc(surf,f"Act {act_now}/8  ·  Stage {n_un}/40",FXX,(40,50,72),cx,ap_y+20)
        if self.hi>0: tc(surf,f"Best score: {self.hi}",FXX,(38,46,66),cx,ap_y+36)
        tc(surf,"SPACE stages  ·  F free play  ·  S skills  ·  ESC quit",FXX,(28,34,52),cx,ap_y+54)
        # Skills button — bottom right of game area
        sk_pts=getattr(self,"skill_pts",0)
        sk_hov_m=(PANEL+W-160<=mx<=PANEL+W-10 and 96+H-36<=my<=96+H-6)
        sk_col=(255,220,60) if sk_pts>0 else (50,58,80)
        rbox(surf,(PANEL+W-158,96+H-34,148,28),(10,12,20),8,
             tuple(cl(c*.45) for c in sk_col) if sk_hov_m else tuple(cl(c*.25) for c in sk_col),1)
        tc(surf,f"S  DKKAN  ({sk_pts} nqt)",FXX,sk_col,PANEL+W-84,96+H-20)

    def _draw_stage_sel(self,surf):
        cx=PANEL+W//2; cy=96+H//2; hue=self.RT%1.
        mx,my=pygame.mouse.get_pos()

        # Background
        ov=asurf(W,H); ov.fill((2,3,8,218)); surf.blit(ov,(PANEL,96))
        self._draw_demo(surf,PANEL,96)
        ov2=asurf(W,H); ov2.fill((2,3,8,150)); surf.blit(ov2,(PANEL,96))

        # Title + nav hint
        tc(surf,"SELECT  STAGE",FT,hsv(hue,.5,.72),cx,96+22)
        tc(surf,"← → ↑ ↓  navigate  ·  SPACE / click  play  ·  F  free play  ·  ESC  back",
           FXX,(32,40,58),cx,96+42)

        # Grid — 8 rows × 5 cols = 40 stages
        cols=5; rows=8
        cw=128; ch=72; gap=7
        total_w=cols*cw+(cols-1)*gap
        x0=(PANEL+W//2)-total_w//2
        y0=96+54

        hover_idx=-1
        for i,st in enumerate(STAGES):
            row=i//cols; col2=i%cols
            sx=x0+col2*(cw+gap); sy=y0+row*(ch+gap)
            locked=(i>=getattr(self,"unlocked",1))
            sel=(i==self.stage_idx)
            hov=(sx<=mx<=sx+cw and sy<=my<=sy+ch)
            if hov and not locked: hover_idx=i
            col=st["col"]

            if locked:
                rbox(surf,(sx,sy,cw,ch),(5,7,12),6,(14,18,28),1)
                tc(surf,"🔒",FM,(24,30,44),sx+cw//2,sy+28)
                tc(surf,f"{i+1}",FXX,(18,24,36),sx+10,sy+12)
            else:
                bt=(cl(col[0]*.15),cl(col[1]*.15),cl(col[2]*.15))
                bb=(cl(col[0]*.07),cl(col[1]*.07),cl(col[2]*.07))
                alpha_brd=0.70 if sel else (0.45 if hov else 0.22)
                brd=tuple(cl(c*alpha_brd) for c in col)
                bw2=2 if (sel or hov) else 1
                rbox_g(surf,(sx,sy,cw,ch),bt,bb,7,brd,bw2)
                # Top stripe
                pygame.draw.rect(surf,col,(sx,sy,cw,3),border_radius=2)
                # Hover/select glow
                if sel or hov:
                    ga=45 if sel else 25
                    gls=asurf(cw+14,ch+14)
                    pygame.draw.rect(gls,(*col,ga),(0,0,cw+14,ch+14),border_radius=9)
                    surf.blit(gls,(sx-7,sy-7))
                # Stage number
                tc(surf,f"{i+1}",FXS,col,sx+10,sy+12)
                # Stage name (short)
                name=st["name"]
                if len(name)>14: name=name[:13]+"."
                tc(surf,name,FXX,col,sx+cw//2,sy+30)
                # Icon row
                hz=st.get("hz",HAZARD_NONE)
                hz_ico={HAZARD_VORTEX:"🌀",HAZARD_PORTAL:"🔵",HAZARD_DARK:"🌑",
                         HAZARD_MIRROR:"⟺",HAZARD_SPEEDTRAP:"⚡",HAZARD_GRAVITY:"↓",
                         HAZARD_ELECTRIC:"⚡⚡",HAZARD_MAZE:"⬛",HAZARD_NONE:""}
                wi2={WN:"",WR:"🌧",WS:"❄",WL:"⚡"}
                icons=[ic for ic in [hz_ico.get(hz,""),wi2.get(st["wx"],""),"⚔" if st.get("boss") else ""] if ic]
                irow="  ".join(icons)
                if irow: tc(surf,irow,FXX,col,sx+cw//2,sy+ch-12)

        # ── Detail card for selected/hovered stage ──────
        show_idx=hover_idx if hover_idx>=0 else self.stage_idx
        if 0<=show_idx<len(STAGES):
            st=STAGES[show_idx]; col=st["col"]
            dy=y0+rows*(ch+gap)+4
            dw=W-40; dh=62; dx2=PANEL+20
            rbox_g(surf,(dx2,dy,dw,dh),
                   (cl(col[0]*.14),cl(col[1]*.14),cl(col[2]*.14)),
                   (cl(col[0]*.07),cl(col[1]*.07),cl(col[2]*.07)),
                   10,(cl(col[0]*.38),cl(col[1]*.38),cl(col[2]*.38)),1)
            pygame.draw.rect(surf,col,(dx2,dy,4,dh),border_radius=2)
            tc(surf,f"Stage {st['id']}  ·  {st['name']}",FM,col,cx,dy+14)
            tc(surf,st["desc"],FS,(75,90,112),cx,dy+32)
            hz=st.get("hz",HAZARD_NONE)
            hz_name={HAZARD_NONE:"No hazard",HAZARD_VORTEX:"Vortex zones",
                      HAZARD_PORTAL:"Portals",HAZARD_DARK:"Darkness",
                      HAZARD_MIRROR:"Mirror controls",HAZARD_SPEEDTRAP:"Speed traps",
                      HAZARD_GRAVITY:"Gravity pull",HAZARD_ELECTRIC:"Electric fences",
                      HAZARD_MAZE:"Energy maze"}
            wi3={WN:"Clear",WR:"Rain",WS:"Snow",WL:"Storm"}
            boss_txt=f"  ·  Boss: {BOSSES[st['boss']]['name']}" if st.get("boss") else ""
            stats=f"×{st['spd']} speed  ·  {wi3[st['wx']]}  ·  {hz_name.get(hz,'')}  ·  Target {st['target']} pts{boss_txt}"
            tc(surf,stats,FXX,(50,62,84),cx,dy+50)

        # ── Free Play button (bottom right) ─────────────
        fp_x=PANEL+W-170; fp_y=96+H-38
        hov_fp=(fp_x<=mx<=fp_x+160 and fp_y<=my<=fp_y+32)
        rbox(surf,(fp_x,fp_y,160,32),(8,12,22),8,
             (55,80,130) if hov_fp else (32,42,68),1)
        tc(surf,"F  —  FREE PLAY",FXS,(80,120,190) if hov_fp else (55,78,120),fp_x+80,fp_y+16)

    def _ov_stage_complete(self,surf):
        ov=asurf(W,H); ov.fill((2,4,10,205)); surf.blit(ov,(PANEL,96))
        cx=PANEL+W//2; cy=96+H//2; hue=self.RT%1.
        st=STAGES[self.stage_idx]; col=st["col"]
        pulse=abs(math.sin(self.T*2.8))
        cp=tuple(cl(c*(0.6+0.4*pulse)) for c in col)

        # Sparks ongoing
        if random.random()<.25:
            for _ in range(3):
                sx=random.randint(PANEL+20,PANEL+W-20)
                sy=random.randint(96+20,96+H-20)
                self.sparks.append(Spark(sx,sy,col,sp=1.5,big=True))

        # Big animated title
        glow_tc(surf,"STAGE COMPLETE",FT,cp,cx,cy-118,6)

        # Stage name
        tc(surf,st["name"],FB,col,cx,cy-82)
        pygame.draw.rect(surf,col,(cx-60,cy-70,120,2),border_radius=1)

        # Stats card
        cw=340; ch=120
        rbox_g(surf,(cx-cw//2,cy-60,cw,ch),
               (cl(col[0]*.14),cl(col[1]*.14),cl(col[2]*.14)),
               (cl(col[0]*.07),cl(col[1]*.07),cl(col[2]*.07)),
               14,(cl(col[0]*.42),cl(col[1]*.42),cl(col[2]*.42)),2)
        pygame.draw.rect(surf,col,(cx-cw//2,cy-60,4,ch),border_radius=2)
        # Stats
        hw3=(cw-40)//3
        pairs=[("SCORE",str(self.score),GOLD),
               ("LEVEL",str(self.level),ACC),
               ("COMBO",f"×{self.max_combo}" if self.max_combo>1 else "—",col)]
        for pi,(lbl,val,vc) in enumerate(pairs):
            px3=cx-cw//2+20+pi*(hw3+10); py3=cy-60
            tc(surf,lbl,FXX,(60,72,92),px3+hw3//2,py3+22)
            glow_tc(surf,val,FB,vc,px3+hw3//2,py3+54,2)

        # Next stage preview
        if self.stage_idx<9:
            nxt=STAGES[self.stage_idx+1]; nc=nxt["col"]
            ny=cy+70
            rbox(surf,(cx-200,ny,400,52),(cl(nc[0]*.10),cl(nc[1]*.10),cl(nc[2]*.10)),
                 10,(cl(nc[0]*.32),cl(nc[1]*.32),cl(nc[2]*.32)),1)
            pygame.draw.rect(surf,nc,(cx-200,ny,3,52),border_radius=2)
            tc(surf,f"NEXT: Stage {nxt['id']}  ·  {nxt['name']}",FM,nc,cx,ny+18)
            tc(surf,nxt["desc"],FXX,(55,68,88),cx,ny+36)

        # Continue button
        # Next stage progress (how many left in act)
        act=(self.stage_idx//5)+1
        tc(surf,f"Act {act}  ·  Stage {self.stage_idx+1}/40",FXX,(45,55,75),cx,cy+118)
        bw=240; bh=46
        rbox_g(surf,(cx-bw//2,cy+134,bw,bh),
               (cl(col[0]*.18),cl(col[1]*.18),cl(col[2]*.18)),
               (cl(col[0]*.09),cl(col[1]*.09),cl(col[2]*.09)),
               bh//2,(cl(col[0]*.70),cl(col[1]*.70),cl(col[2]*.70)),2)
        tc(surf,"SPACE  —  CONTINUE",FM,cp,cx,cy+157)

    def _ov_menu(self,surf):
        self._ov_bg(surf,218)
        cx=PANEL+W//2; cy=96+H//2; hue=self.RT%1.; c1=hsv(hue,.68,1.)
        # Title
        glow_tc(surf,"SNAKE",FXL,c1,cx,cy-132,6)
        uw=int(65+28*abs(math.sin(self.T*1.6)))
        pygame.draw.rect(surf,hsv((hue+.5)%1.,.8,1.),(cx-uw//2,cy-98,uw,2),border_radius=1)
        tc(surf,"MYTHIC  EDITION",FXS,hsv(hue,.16,.40),cx,cy-83)
        # START pill
        bw=216; bh=46; bx=cx-bw//2; by=cy-44
        rbox_g(surf,(bx,by,bw,bh),
               (cl(c1[0]*.13),cl(c1[1]*.13),cl(c1[2]*.13)),
               (cl(c1[0]*.07),cl(c1[1]*.07),cl(c1[2]*.07)),
               bh//2,(cl(c1[0]*.65),cl(c1[1]*.65),cl(c1[2]*.65)),2)
        ps=abs(math.sin(self.T*2.6))
        c1p=tuple(cl(c*(0.68+0.32*ps)) for c in c1)
        glow_tc(surf,"SPACE  —  START",FM,c1p,cx,cy-21,2)
        # Feature rows
        rows=[
            ("🌧  Rain  ·  ❄ Snow  ·  ⚡ Storm",(70,130,255)),
            ("⚔  Boss every 5 levels",          (220,145,55)),
            ("🐾  Catch the prey in 15s",        (75,200,115)),
            ("11 power-ups  ·  10 skins",        (160,80,255)),
        ]
        for ri,(rtxt,rcol) in enumerate(rows):
            ry=cy+10+ri*30
            # subtle pill bg
            pw2=180
            rbox(surf,(cx-pw2//2,ry-1,pw2,22),(cl(rcol[0]*.08),cl(rcol[1]*.08),cl(rcol[2]*.08)),
                 11,(cl(rcol[0]*.30),cl(rcol[1]*.30),cl(rcol[2]*.30)),1)
            tc(surf,rtxt,FS,rcol,cx,ry+10)
        # Boss cheatsheet
        for bi,(blv,bpu) in enumerate([(5,PN),(10,PL),(15,PF)]):
            bname=BOSSES[blv]["name"]
            tc(surf,f"Lv{blv} {bname}  →  {PU_ICO[bpu]}",FXX,
               tuple(cl(c*.75) for c in PU_COL[bpu]),cx,cy+140+bi*14)

    def _ov_dead(self,surf):
        self._ov_bg(surf,218)
        cx=PANEL+W//2; cy=96+H//2; thc=self.theme[1]
        glow_tc(surf,"GAME OVER",FT,DNG,cx,cy-132,5)
        # stats card
        cw=310; ch=158
        rbox_g(surf,(cx-cw//2,cy-92,cw,ch),(11,14,24),(7,9,16),14,
               (22,28,44),1)
        pygame.draw.rect(surf,DNG,(cx-cw//2,cy-92,3,ch),border_radius=2)
        tc(surf,"SCORE",FXS,(58,68,92),cx,cy-74)
        glow_tc(surf,str(self.score),FT,WHT,cx,cy-44,3)
        pygame.draw.line(surf,(20,26,42),(cx-cw//2+14,cy-16),(cx+cw//2-14,cy-16),1)
        hw3=(cw-28)//2
        tc(surf,"BEST",FXX,(68,62,32),cx-hw3//2,cy-4)
        tc(surf,str(self.hi),FM,GOLD,cx-hw3//2,cy+18)
        tc(surf,"LEVEL",FXX,(32,68,42),cx+hw3//2,cy-4)
        tc(surf,str(self.level),FM,ACC,cx+hw3//2,cy+18)
        if self.max_combo>1:
            tc(surf,f"max combo  x{self.max_combo}",FS,GOLD,cx,cy+48)
        tc(surf,f"skin:  {self.theme[0]}",FXX,thc,cx,cy+66)
        # retry button
        bw2=196; bh2=42
        rbox_g(surf,(cx-bw2//2,cy+82,bw2,bh2),(10,28,14),(6,18,8),bh2//2,AC2,2)
        glow_tc(surf,"SPACE  —  RETRY",FM,ACC,cx,cy+103,1)

    def _ov_pause(self,surf):
        self._ov_bg(surf,202);cx=PANEL+W//2;cy=96+H//2
        rbox_g(surf,(cx-184,cy-60,368,120),(10,13,20),(7,9,14),10,BDR,1)
        glow_tc(surf,"PAUSED",FT,ACC,cx,cy-20,3)
        tc(surf,"SPACE  resume",FS,ACC,cx,cy+18)
        tc(surf,"ESC  main menu   ·   S  skills",FS,DIM,cx,cy+36)
        sp2=getattr(self,"skill_pts",0)
        if sp2>0:
            tc(surf,f"✦ {sp2} nqta dyal l-mhara — doz 3la S",FXS,GOLD,cx,cy+56)

if __name__=="__main__":
    Game().run()