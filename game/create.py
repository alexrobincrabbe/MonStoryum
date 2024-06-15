'''
contains functions to create all of the game elements,
rooms,
monsters,
features,
items.
'''
#my class imports
from game.room import Room
from game.monster import Monster, Dragon, Player
from game.feature import Feature
from game.items import Armor,Weapon,Potion,Key

#my function imports
from game.clear import clear_console

def create_rooms() -> list:
    '''
    function to create the game rooms.
    creates all monsters, items, and features in room, creates player object.
    '''
     #create items
    #armor
    no_armor, rusty_armour, leather_armor, plate_armor, dragonscale_armor, \
    scales, stone_skin = create_armor()
    #weapons
    fists, dagger, club, sword, silver_sword, dragon_lance, \
    stinger, claws, bite, stone_fists = create_weapons()
    #potions
    healing_potion, super_healing_potion, agility_potion, strength_potion \
    = create_potions()
    #keys
    rusty_key, bronze_key, silver_key, golden_key, gold_medallion \
    = create_keys()

    #initialise player
    name = choose_name()
    player=Player(name, "A warrior", 20, 1, 1, no_armor, fists,[],"")
    player.hp=20
    player.start_hp=20

    #create monsters
    #talk to response
    g_speak = "it is probably swearing at you, but you don't understand goblish"
    dg_details = "The goblin looks very drunk"
    g_details = "goblins are funny looking creatures"
    gc_details = "it looks taller than the other goblins, and is brandishing a longer \
                weapon. It is clad in fine leather armor"
    t_speak = "it grunts at you"
    t_details = "Looks big, stupid and angry. It is carrying a big club."
    s_speak = "it hisses at you"
    s_details = "it is creepy"
    sg_speak = "it remains silent"
    sg_details ="it is a living statue, made of pure stone"
    d_details = "it is huge and scaly"
    d_speak = ""
    w_details = "it has really big teeth"
    w_speak = "it is not a talking wolf"
    #goblins
    goblins =[]
    for i in range (5):
        goblins.append(Monster("goblin", g_details, 10, 1, 0, no_armor,dagger,[],g_speak))
    goblin_captain = Monster("goblin captain",gc_details, 13, 1, 0, leather_armor,sword,[],g_speak)
    drunk_goblin=Monster("goblin",dg_details, 10, 1, -10, no_armor,dagger,[rusty_key],g_speak)
    #spiders
    spiders=[]
    for i in range(5):
        spiders.append(Monster("spider",s_details, 1,0,0,no_armor,stinger,[],s_speak))
    #trolls
    trolls = []
    for i in range (3):
        trolls.append(Monster("troll",t_details, 20, 2, -4, no_armor,club,[],t_speak))
    #wolves
    wolves=[]
    for i in range(2):
        wolves.append(Monster("wolf", w_details, 20,0,0, no_armor,bite, [], w_speak))
    #stone guardian
    stone_guardian = Monster("stone guardian", sg_details, 50, 0, 0, stone_skin,stone_fists,\
                             [golden_key],sg_speak)
    #dragon
    dragon=Dragon("dragon", d_details,100,0,0,scales,claws,[gold_medallion],d_speak)

    #create features
    wooden_chest_0=Feature("wooden chest","the chest is rickety and smells damp",\
                            [healing_potion],False)
    bronze_chest=Feature("bronze chest","the chest is dusty", \
                         [healing_potion,strength_potion, agility_potion],True)
    silver_chest=Feature("silver chest","the chest is smooth and shiny", \
                         [silver_sword,healing_potion],True)
    golden_chest=Feature("golden chest","the chest has strange markings on it", \
                         [dragonscale_armor,super_healing_potion,super_healing_potion],True)
    spider_egg=Feature("egg","it is wet and slimy",[],False)
    spider_egg_2=Feature("egg","it is wet and slimy",[bronze_key],False)
    well=Feature("well", "You can't see the bottom",[rusty_armour],False)
    wooden_chest = Feature("wooden chest","goblins like to store their stuff in chests", \
                           [super_healing_potion],False)
    table = Feature ("table", "it has goblin brew stains all over it",[silver_key],False)
    bag_of_potions = Feature("bag of potions","someone just left this lying around here", \
                             [healing_potion,healing_potion,healing_potion],False)

    #create room descriptions
    room_descriptions, room_descriptions_visited = create_room_descriptions()

    #create rooms
    #populate rooms with monsters
    monsters=[
        [drunk_goblin],#1
        [trolls[0]],#2
        [],#3
        [spider for spider in spiders],#4
        [],#5
        [dragon],#6
        [goblins[0],goblins[1],goblin_captain],#7
        [trolls[1],goblins[2],goblins[3]],#8
        [trolls[2], goblins[4],wolves[0],wolves[1]],#9
        [],#10
        [stone_guardian]#11
    ]
    #populate rooms with features
    features=[
        [],#1
        [],#2
        [wooden_chest_0, bronze_chest, silver_chest, golden_chest],#3
        [spider_egg,spider_egg_2,spider_egg],#4
        [well],#5
        [],#6
        [wooden_chest],#7
        [table],#8
        [],#9
        [bag_of_potions],#10
        []#11
        ]
    #populate rooms with items
    items=[
        [],#1
        [],#2
        [],#3
        [],#4
        [],#5
        [],#6
        [],#7
        [],#8
        [plate_armor],#9
        [],#10
        [dragon_lance]#11
    ]
    #create the rooms
    rooms=[]
    for i in range(11):
        rooms.append (Room(room_descriptions[i],room_descriptions_visited[i], \
                           player,monsters[i],items[i],features[i]))

    rooms[0].door="locked"
    rooms[0].key_name="prison_door"
    rooms[0].monster_action = True
    rooms[0].battle_started = True

    return rooms

def choose_name() -> str:
    '''
    prompts player to input a name of maximum 10 characters.
    returns name
    '''
    clear_console()
    name = input("please choose your name: ")
    if len(name) > 10:
        print("maximum of 10 characters")
        choose_name()
    else:
        return name

def create_armor() -> tuple:
    '''
    intialises all objects of Armor class used in the game
    '''
    no_armor = Armor("none","none", 0, 0)
    rusty_armour= Armor("rusty armor", "it has seen better days",2,-1)
    leather_armor = Armor("leather armor", "it is light, and offers some protection",3,0)
    plate_armor = Armor("plate armor", "it is heavy, but offers good protection",5,-1)
    dragonscale_armor = Armor("dragonscale armor", "it glistens",11,1)
    scales = Armor("none", "none",10,0)
    stone_skin = Armor("none", "none", 5, -2)
    return no_armor, rusty_armour, leather_armor, plate_armor, dragonscale_armor, \
            scales, stone_skin

def create_weapons() -> tuple:
    '''
    initialises all objects of Weapon class used in the game
    '''
    fists = Weapon("fists", "none", [1,2], 0)
    dagger = Weapon("dagger", "a small stabby weapon", [1,6], 1)
    club = Weapon("club", "a large blunt weapon", [2,10], -1)
    sword = Weapon("sword","a fine steel sword",[1,10],2)
    silver_sword = Weapon("silver sword","a shiny silver sword",[2,12],3)
    dragon_lance = Weapon("dragon lance", "it glistens", [10,25],4)
    stinger = Weapon("stinger", "none", [1,1], 0)
    claws = Weapon("claws","none",[20,30],5)
    bite= Weapon("bite","none",[4,9],4)
    stone_fists = Weapon("fists", "none", [5,15],4)
    return fists, dagger, club, sword, silver_sword, dragon_lance, \
            stinger, claws, bite, stone_fists

def create_potions() -> tuple:
    '''
    initialises all objects of Potion class used in the game
    '''
    healing_potion = Potion("healing potion","it is red and smells fruity", "hp",10)
    super_healing_potion = Potion("super healing potion","really potent stuff", "hp",20)
    agility_potion = Potion("agility potion", "it is green and sticky","agility",3)
    strength_potion = Potion("strength potion", "orange and bubbly", "strength",2)
    return healing_potion, super_healing_potion, agility_potion, strength_potion

def create_keys() -> tuple:
    '''
    initialises all objects of Key class used in the game
    '''
    rusty_key=Key("rusty key","It smells of goblin brew","prison_door")
    bronze_key=Key("bronze key","It is dusty","bronze chest")
    silver_key=Key("silver key","It is shiny","silver chest")
    golden_key=Key("golden key","It has strange markings","golden chest")
    gold_medallion = Key("gold medallion", "it is proof that you killed the dragon", "none")
    return rusty_key, bronze_key, silver_key, golden_key, gold_medallion

def create_room_descriptions() -> tuple[list,list]:
    '''
    create the descriptions used for the room.details attribute
    '''
    room_descriptions = [
        "Regaining consciousness, you open your eyes and realise you are in a dark, "
        "dank-smelling dungeon. From the faint sounds above you, you realise you are " 
        "in the depths of the citadel, controlled by the evil sorceress queen, Achlys. "
        "It dawns on you that by wrongfully imprisoning you, Achlys has removed the "
        "last obstacle to her malicious schemes. You must find a way to escape, "
        "though you know that her loyal monsters will fight you to the death. "
        "The innocent citizens of Greystorm will be counting on you to "
        "save them. "
        "You hear clumsy, heavy footsteps approaching your cell, "
        "the door creaks open and an evidently inebriated goblin stumbles in. "
        "You reach for your weapon but…your scabbard is empty. "
        "He begins to berate you, but you don't know what he's saying - "
        "you don't speak Goblish. "
        "He lunges towards you and you see a dagger in his gnarly hand: ",#1

        "You lurch out of your cell and find yourself in the guard quarters. "
        "You are confronted by a large troll. He glares angrily at you.",#2

        "Leaving the troll's lifeless body behind, you enter a small room. "
        "You hear water dripping. In the dim light, cast by a torch high "
        "up on the wall, you spy four chests; one wooden, one bronze, one "
        "silver, one gold..",#3

        "You stagger down a narrow corridor and spot a gap in the walls. "
        "You feel your way carefully through the gap, along jagged rock "
        "walls until you edge your way into an opening. You feel "
        "something enshroud your face, sticking to you, pulling at you. "
        "You reach out with your hands and desperately rip it away. You "
        "look down and see three big white egg sacs. They seem to be wriggling. "
        "You look up and see thick webs and dark shapes moving hurriedly "
        "across the ceiling. Dozens of glowing, hungry eyes are fixed on you.", #4

        "Climbing a few roughly hewn steps you see ahead of you a shaft of light "
        "shining down upon an old stone well. \n"
        "An anvil sits on a stone pile next to the well and discarded bottles are "
        "strewn about the floor. A stack of buckets has been knocked over and left "
        "where they fell. \n"
        "Goblins and trolls are not renowned for their housekeeping! \n"
        "As you approach, something inside the well catches your eye "
        "- is that metal?",#5

        "You find yourself in another cavern, this time it's huge. You look up and "
        "wonder if those are stars you see. \n"
        "You can hear something flying above you, circling - probably  birds, you say to yourself. "
        "Spanning the centre of the cavern is a grand bridge made of cut stone. Torches line one "
        "side and appear to go on forever, glowing in the darkness, dimly lighting the path. "
        "You can't see where it leads - a mighty, thick fog is blocking the view. Anything could "
        "be lurking inside. \n You gingerly edge closer to the low wall of the bridge and peer "
        "over at the blackness below you. The air feels electric, alive. \n"
        "It occurs to you that this bridge is incredibly large, even for trolls. "
        "You try not to think about what that might mean, but it is a thought that sticks with "
        "you as you continue on your way.\n \n"
        "You suddenly hear a slow, rhythmic sound and, as you're getting closer to the source, "
        "it's becoming so loud it's making the bridge rumble. \n"
        "It's like the stone is snoring…you can feel the air tremble around you as it breathes "
        "in and out. A sudden realisation as the monster comes into sight…"
        "the rumours of terrorised citizens were true. Dragons still exist! \n"
        "You stare at the dragon in amazement as a flicker of fire escapes its nostrils. \n"
        "Then a huge yellow eye snaps open and gazes back at you.",#6

        "You hurry past the dragon, down a passageway. You dash through the next "
        "unlocked door you find and are met by a trio of goblins, one appears to "
        "be in charge. They grunt at you.",#7

        "As you turn the corner, you hear guffawing and the snorts of Goblish being"
        "spoken and the grunts of a troll. You see them, quaffing a dark brew, two "
        "goblins and a troll sitting at a table, their drinks spilling as they see you. "
        "They appear startled - and then irritated - that you've disturbed their fun.",#8

        "The room is deadly silent but you are unnerved by the feeling that you're not "
        "alone. Taking a few careful steps forward, you hear the slow scraping sound of "
        "metal against concrete. \n"
        "Two deep growls echo together, bouncing off the walls. They vibrate through your"
        " body and the hair on the back of your neck stands on end. \n"
        "Then you see them, waiting for you. \n"
        "They must have heard you coming…because this goblin and troll have their weapons "
        "ready in-hand….and have a couple of massive, ferocious wolves guarding them. " 
        "The hairy beasts raise their hackles…and stare into your soul, circling, they "
        "appear to be starving…saliva drips from their snarling mouths. They are ready "
        "to pounce, just waiting for the order. \n"
        "The troll lumbers forward as the goblin lets out an ungodly screeching sound." 
        "You see a flash of teeth and claws",#9

        "What is this I see before me? Somebody has left an ornately embroidered bag "
        "full of potions just lying here. It looks very out of place…perhaps you are "
        "going to need these?",#10

        "Pushing open a door that is much heavier than the others, daylight dazzles "
        "you. Shielding your eyes, you see a hulking shape ahead of you, blocking "
        "the exit to this hellish place. You have fought so hard and freedom is so close. "
        "A Stone Guardian stomps towards you."#11 
    ]

    room_descriptions_visited = [
        "You are in a foul-smelling cell. There is a door to the east.",#1

        "You are in a dimly lit cave. It smells like trolls have been living here for "
        "a long time",#2

        "room 3",#3

        "You are in the spiders' nest…watch where you walk…those egg sacs look like "
        "they are wriggling!",#4

        "A shaft of light shines down upon an old stone well. "
        "An anvil sits on a stone pile next to the well and discarded bottles are "
        "strewn about the floor. A stack of buckets has been knocked over and left "
        "where they fell. \n"   
        "Goblins and trolls are not renowned for their housekeeping! \n  "
        "Something is splashing about in that well…best not draw attention to yourself.",#5

        "Spanning the centre of the familiar cavern is a grand bridge made of cut stone. "
        "Torches line one side and appear to go on forever, glowing in the darkness, dimly "
        "lighting the path. You can't see where it leads - a mighty, thick fog is blocking "
        "the view. Anything could be lurking inside.",#6

        "This looks like the guards' quarters",#7

        "The stench of sweet booze lingers in the room, - that stuff is potent! "
        "The chairs and table are knocked over, "
        "there is broken glass everywhere.", #8

        "What a mess! Patches of red-stained fur all over. Those wolves are almost as "
        "frightening in death as they were when alive. Their gigantic fangs are still "
        "sharp, someone might slip in the blood and land on those!",#9

        "You are in some kind of storage room",#10

        "This is the last room before freedom. Daylight dazzles your eyes."#11
        ]
    return room_descriptions, room_descriptions_visited
