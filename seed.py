#!/usr/bin/env python3
import os
import sys
from random import Random
from ast import literal_eval # limited eval for literals only

DICT = { 'common': 0, 'uncommon': 1, 'rare': 2, 'very_rare': 3 }

# cumulative
ODDS = [[
  [0, 0, 0],
  [0, 0, 0.1],
  [0, 0.01, 0.21],
  [0, 0.01, 0.26],
  [0.005, 0.02, 0.31],
  [0.005, 0.02, 0.32],
], [
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0.1],
  [0, 0.025, 0.225],
  [0, 0.025, 0.275],
  [0.0125, 0.05, 0.35],
]]

# [type][rarity][is_lunch][i]
# detecting symbols vs. items relies on IDS being sorted (except Pool Ball variants so that we can give them special treatment when rolling)
IDS = [[[[
  'anchor',
  'banana_peel',
  'bee',
  'bounty_hunter',
  'bubble',
  'cat',
  'coal',
  'coin',
  'crab',
  'crow',
  'cultist',
  'd3',
  'dog',
  'dwarf',
  'flower',
  'goldfish',
  'goose',
  'key',
  'lockbox',
  'magpie',
  'miner',
  'monkey',
  'mouse',
  'ore',
  'owl',
  'oyster',
  'pearl',
  'rabbit',
  'seed',
  'shiny_pebble',
  'snail',
  'toddler',
  'turtle',
  'urn',
], [
  'banana',
  'beer',
  'candy',
  'cheese',
  'cherry',
  'egg',
  'milk',
]], [[
  'bar_of_soap',
  'bear',
  'big_ore',
  'big_urn',
  'billionaire',
  'bronze_arrow',
  'buffing_powder',
  'chick',
  'clubs',
  'coconut',
  'd5',
  'diamonds',
  'golem',
  'hearts',
  'hex_of_destruction',
  'hex_of_draining',
  'hex_of_emptiness',
  'hex_of_hoarding',
  'hex_of_midas',
  'hex_of_tedium',
  'hex_of_thievery',
  'hooligan',
  'hustler',
  'item_capsule',
  'lucky_capsule',
  'matryoshka_doll_1',
  'ninja',
  'pinata',
  'rabbit_fluff',
  'rain',
  'rarity_capsule',
  'removal_capsule',
  'reroll_capsule',
  'safe',
  'sapphire',
  'sloth',
  'spades',
  'target',
  'tedium_capsule',
  'thief',
  'void_creature',
  'void_stone',
  'wolf',
], [
  'chemical_seven',
  'coconut_half',
  'orange',
  'peach',
  'plum',
  'wine',
]], [[
  'archaeologist',
  'bartender',
  'beastmaster',
  'beehive',
  'card_shark',
  'chef',
  'chicken',
  'cow',
  'dame',
  'diver',
  'emerald',
  'farmer',
  'frozen_fossil',
  'general_zaroff',
  'joker',
  'king_midas',
  'magic_key',
  'mine',
  'moon',
  'mrs_fruit',
  'robin_hood',
  'ruby',
  'silver_arrow',
  'spirit',
  'sun',
  'tomb',
  'treasure_chest',
  'witch',
], [
  'apple',
  'golden_egg',
  'honey',
  'martini',
  'omelette',
  'strawberry',
]], [[
  'diamond',
  'eldritch_beast',
  'golden_arrow',
  'highlander',
  'mega_chest',
  'midas_bomb',
  'pirate',
  'wildcard',
], [
  'watermelon',
]]], [[[
  'pool_ball',
  'black_pepper',
  'blue_pepper',
  'checkered_flag',
  'cyan_pepper',
  'egg_carton',
  'fish_bowl',
  'frying_pan',
  'grave_robber',
  'gray_pepper',
  'green_pepper',
  'guillotine',
  'happy_hour',
  'jackolantern',
  'kyle_the_kernite',
  'lockpick',
  'lucky_cat',
  'lucky_seven',
  'lunchbox',
  'maxwell_the_bear',
  'mining_pick',
  'ninja_and_mouse',
  'nori_the_rabbit',
  'oswald_the_monkey',
  'pink_pepper',
  'pizza_the_cat',
  'purple_pepper',
  'quigley_the_wolf',
  'red_pepper',
  'reroll',
  'ricky_the_banana',
  'shedding_season',
  'swear_jar',
  'symbol_bomb_small',
  'tax_evasion',
  'treasure_map',
  'wanted_poster',
  'watering_can',
  'white_pepper',
  'yellow_pepper',
]], [[
  'horseshoe',
  'anthropology_degree',
  'barrel_o_dwarves',
  'birdhouse',
  'black_cat',
  'blue_suits',
  'capsule_machine',
  'cardboard_box',
  'cleaning_rag',
  'coin_on_a_string',
  'comfy_pillow',
  'compost_heap',
  'conveyor_belt',
  'cursed_katana',
  'dwarven_anvil',
  'fertilizer',
  'fifth_ace',
  'flush',
  'fruit_basket',
  'goldilocks',
  'lefty_the_rabbit',
  'lemon',
  'lint_roller',
  'looting_glove',
  'piggy_bank',
  'rain_cloud',
  'red_suits',
  'ritual_candle',
  'rusty_gear',
  'shattered_mirror',
  'shrine',
  'symbol_bomb_big',
  'time_machine',
  'triple_coins',
  'x_ray_machine',
  'zaroffs_contract',
]], [[
  'bowling_ball',
  'bag_of_holding',
  'booster_pack',
  'chicken_coop',
  'chili_powder',
  'clear_sky',
  'coffee',
  'devils_deal',
  'holy_water',
  'lucky_carrot',
  'lucky_dice',
  'oil_can',
  'protractor',
  'quiver',
  'recycling',
  'sunglasses',
  'swapping_device',
  'symbol_bomb_very_big',
  'undertaker',
  'void_portal',
]], [[
  'four_leaf_clover',
  'ancient_lizard_blade',
  'copycat',
  'frozen_pizza',
  'golden_carrot',
  'telescope',
]]]]

# for convenience, return 0 for symbol vs. 1 for item
def is_item(s):
  for lll in IDS[0]:
    for ll in lll:
      n = len(ll)
      lo = 0
      hi = n - 1
      i = (lo + hi) // 2
      if ll[i] < s:
        lo = i + 1
      else:
        hi = i
      while lo != hi:
        i = (lo + hi) // 2
        if ll[i] < s:
          lo = i + 1
        else:
          hi = i
      if ll[lo] == s:
        return 0
  return 1

RNG_TYPE = [
  2147483647, # 0: seed
  None, # 1: symbol rarity
  len(IDS[0][0][0]) + len(IDS[0][0][1]), # 2: common symbol
  len(IDS[0][1][0]) + len(IDS[0][1][1]), # 3: uncommon symbol
  len(IDS[0][2][0]) + len(IDS[0][2][1]), # 4: rare symbol
  len(IDS[0][3][0]) + len(IDS[0][3][1]), # 5: very_rare symbol
  len(IDS[0][0][1]), # 6: common lunchbox symbol
  len(IDS[0][1][1]), # 7: uncommon lunchbox symbol
  len(IDS[0][2][1]), # 8: rare lunchbox symbol (very_rare lunchbox is always watermelon)
  None, # 9: chance to replace symbol common due to cursed_katana or rain_cloud
  None, # 10: item rarity
  len(IDS[1][0][0]), # 11: common item
  len(IDS[1][1][0]), # 12: uncommon item
  len(IDS[1][2][0]), # 13: rare item
  len(IDS[1][3][0]), # 14: very_rare item
  None, # 15: lunchbox rarity
]
THRESHOLD = 625 # deserializing getstate() output involves parsing 625 integers, so it can be faster to count the number of state advances after seeding

SEED = [sys.argv[1]]
STATE = None
RNG = [None for n in RNG_TYPE]

if os.path.isfile(SEED[0] + '.dat'):
  s = None
  with open(SEED[0] + '.dat') as f:
    s = f.read()
  STATE = literal_eval(s)
else:
  STATE = [0 for n in RNG_TYPE]

def save():
  for k in range(len(RNG_TYPE)):
    rng = RNG[k]
    if rng is not None:
      s = STATE[k]
      if type(s) != int or s > THRESHOLD:
        STATE[k] = rng.getstate()
  s = repr(STATE)
  with open(SEED[0] + '.dat', 'w') as f:
    f.write(s)

def random_seed():
  if RNG[0] is None:
    RNG[0] = Random(SEED[0])
  return RNG[0].randrange(RNG_TYPE[0])

def random_float(k):
  rng = RNG[k]
  s = STATE[k]
  if type(s) == int:
    if rng is None:
      while len(SEED) < k + 1:
        SEED.append(random_seed())
      rng = Random(SEED[k])
      for i in range(s):
        rng.random()
      RNG[k] = rng
    STATE[k] += 1
  elif rng is None:
    rng = Random(0)
    rng.setstate(s)
    RNG[k] = rng
  return rng.random()

def random_int(k):
  n = RNG_TYPE[k]
  rng = RNG[k]
  s = STATE[k]
  if type(s) == int:
    if rng is None:
      while len(SEED) < k + 1:
        SEED.append(random_seed())
      rng = Random(SEED[k])
      for i in range(s):
        rng.randrange(n)
      RNG[k] = rng
    STATE[k] += 1
  elif rng is None:
    rng = Random(0)
    rng.setstate(s)
    RNG[k] = rng
  return rng.randrange(n)

extras = -1

for line in sys.stdin:
  if extras == -1:
    sys.stdout.write(line)
    start = line.find('"destroyed_item_types":[')
    if start == -1:
      # Occurrence of "highlander" before items means highlander in inventory
      if '"highlander"' in line:
        DICT['highlander'] = True
      continue
    extras = 0
    start += 24
    end = line.index(']', start)
    if end != start:
      for item in [s[1:-1] for s in line[start:end].split(',')]:
        DICT[item] = True
    start = line.index('"item_types":[', end) + 14
    end = line.index(']', start)
    if end != start:
      for item in [s[1:-1] for s in line[start:end].split(',')]:
        DICT[item] = True
        if item == 'cursed_katana' or item == 'rain_cloud':
          extras += 1
    continue

  start = line.find('"saved_card_types":[')
  if start == -1:
    sys.stdout.write(line)
    continue
  pos = start + 20
  end = line.index(']', pos)
  if end == pos:
    sys.stdout.write(line)
    continue

  ss = line[pos:end].split(',', 2)
  c = len(ss)
  t = is_item(ss[0][1:-1])
  rng = (1, 10)[t]
  month_start = line.index('"times_rent_paid":', end) + 18
  month = int(line[month_start:line.index(',', month_start)])
  odds = ODDS[t][min(month, 5)]
  unluck = 1.0

  rr = []
  rr_min = None
  r_start = line.find('"forced_rarity":[', 0, start)
  if r_start != -1:
    r_start += 17
    r_end = line.index(']', r_start)
    if r_end != r_start:
      for rarity in [s[1:-1] for s in line[r_start:r_end].split(',', 2)]:
        rr.append(DICT[rarity])
      if line.find('"or_better":true', 0, start) != -1:
        rr_min = rr
        rr = []
  if t == 0:
    r_start = line.find('"symbols":{"rare":', 0, start)
    if r_start != -1:
      r_start += 18
      unluck /= float(line[r_start:line.index(',', r_start)])
    if line.find('"forced_group":"food"', 0, start) != -1:
      t = 2
      rng = 15
  if t == 0 and extras != 0:
    cc = RNG_TYPE[2]
    cd = extras
    while len(rr) < c:
      x = random_float(rng) * unluck
      if x < odds[0]:
        rr.append(3)
      elif x < odds[1]:
        rr.append(2)
      elif x < odds[2]:
        rr.append(1)
      elif cd == 0:
        rr.append(0)
      else:
        x = random_float(9) * (cc + cd)
        if x < cd:
          if cd != extras:
            rr.append(-2 if -1 in rr else -1)
          elif x >= 1 or 'rain_cloud' not in DICT:
            rr.append(-1)
          else:
            rr.append(-2)
          cd -= 1
        else:
          rr.append(0)
          cc -= 1
  else:
    while len(rr) < c:
      x = random_float(rng) * unluck
      if x < odds[0]:
        rr.append(3)
      elif x < odds[1]:
        rr.append(2)
      elif x < odds[2]:
        rr.append(1)
      else:
        rr.append(0)
  if rr_min:
    for i in range(len(rr_min)):
      if rr_min[i] > rr[i] and rr_min[i] > 0:
        rr[i] = rr_min[i]

  ss = []
  if t == 0:
    for r in rr:
      if r == -1:
        ss.append('ninja')
        continue
      if r == -2:
        ss.append('rain')
        continue
      nolunch = IDS[0][r][0]
      while True:
        s = None
        i = random_int(r + 2)
        if i < len(nolunch):
          s = nolunch[i]
        elif r == 3:
          s = 'watermelon'
        else:
          s = IDS[0][r][1][random_int(r + 6)]
        if s not in DICT:
          ss.append(s)
          DICT[s] = True
          break
  elif t == 1:
    for r in rr:
      while True:
        i = random_int(r + 11)
        s = IDS[1][r][0][i]
        if i == 0 or s not in DICT:
          ss.append(s)
          DICT[s] = True
          break
  else:
    for r in rr:
      while True:
        if r == 3:
          if 'watermelon' not in DICT:
            ss.append('watermelon')
            DICT['watermelon'] = True
            break
          s = IDS[0][2][1][random_int(8)]
        else:
          s = IDS[0][r][1][random_int(r + 6)]
        if s not in DICT:
          ss.append(s)
          DICT[s] = True
          break

  sys.stdout.write(line[:pos+1]) # copy first quotation mark
  sys.stdout.write('","'.join(ss))
  sys.stdout.write(line[end-1:]) # copy last quotation mark

save()
