#!/usr/bin/env python3

# lbal-seed v20210716a

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

# [type][rarity][group][i]
# detecting symbols vs. items relies on IDS being sorted (except Pool Ball variants so that we can give them special treatment when rolling)
IDS = [[[[
  'anchor',
  'banana_peel',
  'bounty_hunter',
  'bubble',
  'coal',
  'coin',
  'cultist',
  'd3',
  'dwarf',
  'flower',
  'key',
  'lockbox',
  'miner',
  'ore',
  'pearl',
  'present',
  'seed',
  'shiny_pebble',
  'toddler',
  'urn',
], [
  'banana',
  'beer',
  'candy',
  'cheese',
  'cherry',
  'egg',
  'milk',
], [
  'bee',
  'cat',
  'crab',
  'crow',
  'dog',
  'goldfish',
  'goose',
  'magpie',
  'monkey',
  'mouse',
  'owl',
  'oyster',
  'snail',
  'turtle',
]], [[
  'bar_of_soap',
  'big_ore',
  'big_urn',
  'billionaire',
  'bronze_arrow',
  'buffing_powder',
  'clubs',
  'coconut',
  'd5',
  'diamonds',
  'essence_capsule',
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
  'spades',
  'target',
  'tedium_capsule',
  'thief',
  'void_stone',
], [
  'chemical_seven',
  'coconut_half',
  'orange',
  'peach',
  'plum',
  'void_fruit',
  'wine',
], [
  'bear',
  'chick',
  'rabbit',
  'sloth',
  'void_creature',
  'wolf',
]], [[
  'amethyst',
  'archaeologist',
  'bartender',
  'beastmaster',
  'beehive',
  'card_shark',
  'chef',
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
  'pear',
  'strawberry',
], [
  'chicken',
  'cow',
]], [[
  'diamond',
  'golden_arrow',
  'highlander',
  'mega_chest',
  'midas_bomb',
  'pirate',
  'wildcard',
], [
  'watermelon',
], [
  'eldritch_beast',
]]], [[[
  'pool_ball',
  'adoption_papers',
  'birdhouse',
  'black_pepper',
  'blue_pepper',
  'brown_pepper',
  'checkered_flag',
  'cyan_pepper',
  'egg_carton',
  'fifth_ace',
  'fish_bowl',
  'frying_pan',
  'grave_robber',
  'gray_pepper',
  'green_pepper',
  'guillotine',
  'happy_hour',
  'jackolantern',
  'kyle_the_kernite',
  'lime_pepper',
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
  'rain_cloud',
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
  'flush',
  'fruit_basket',
  'goldilocks',
  'lefty_the_rabbit',
  'lemon',
  'lint_roller',
  'looting_glove',
  'piggy_bank',
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
  'dishwasher',
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
  'popsicle',
  'telescope',
]]]]

# for convenience, return 0 for symbol vs. 1 for item
def is_item(s):
  for lll in IDS[0]:
    for ll in lll:
      n = len(ll)
      lo = 0
      hi = n - 1
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
  len(IDS[0][0][0]) + len(IDS[0][0][1]) + len(IDS[0][0][2]), # 2: common symbol
  len(IDS[0][1][0]) + len(IDS[0][1][1]) + len(IDS[0][1][2]), # 3: uncommon symbol
  len(IDS[0][2][0]) + len(IDS[0][2][1]) + len(IDS[0][2][2]), # 4: rare symbol
  len(IDS[0][3][0]) + len(IDS[0][3][1]) + len(IDS[0][3][2]), # 5: very_rare symbol
  len(IDS[0][0][1]), # 6: common lunchbox symbol
  len(IDS[0][1][1]), # 7: uncommon lunchbox symbol
  len(IDS[0][2][1]), # 8: rare lunchbox symbol (very_rare is always watermelon)
  len(IDS[0][0][2]), # 9: common adoption_papers symbol
  len(IDS[0][1][2]), # 10: uncommon adoption_papers symbol
  len(IDS[0][2][2]), # 11: rare adoption_papers symbol (very_rare is always eldritch_beast)
  None, # 12: item rarity
  len(IDS[1][0][0]), # 13: common item
  len(IDS[1][1][0]), # 14: uncommon item
  len(IDS[1][2][0]), # 15: rare item
  len(IDS[1][3][0]), # 16: very_rare item
  len(IDS[1][0][0]) + len(IDS[1][1][0]) + len(IDS[1][2][0]) + len(IDS[1][3][0]), # 17: essence
  None, # 18: lunchbox rarity
  None, # 19: adoption_papers rarity
]
THRESHOLD = 625 # deserializing getstate() output involves parsing 625 integers, so it can be faster to count and replay state advances after seeding

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
        if len(item) <= 8 or item[-8:] != '_essence':
          DICT[item] = True
        elif item == 'lucky_seven_essence':
          DICT['chemical_seven'] = True
          extras += 1
    start = line.index('"item_types":[', end) + 14
    end = line.index(']', start)
    if end != start:
      for item in [s[1:-1] for s in line[start:end].split(',')]:
        DICT[item] = True
        if item == 'cursed_katana':
          DICT['ninja'] = True
          extras += 1
        elif item == 'rain_cloud':
          DICT['rain'] = True
          extras += 1
    continue

  start = line.find('"saved_card_types":["')
  if start == -1:
    sys.stdout.write(line)
    continue
  pos = start + 20
  end = line.index(']', pos + 2)

  ss = line[pos:end].split(',', 2)
  c = len(ss)
  t = is_item(ss[0][1:-1])
  rng = (1, 12)[t]
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
      initial = True
      for rarity in [s[1:-1] for s in line[r_start:r_end].split(',', 2)]:
        if initial:
          if rarity == 'essence':
            t = 2
            break
          initial = False
        rr.append(DICT[rarity])
      if t != 2 and line.find('"or_better":true', 0, start) != -1:
        rr_min = rr
        rr = []
  if t != 2:
    if t == 0:
      r_start = line.find('"symbols":{"rare":', 0, start)
      if r_start != -1:
        r_start += 18
        unluck /= float(line[r_start:line.index(',', r_start)])
      r_start = line.find('"forced_group":"', 0, start)
      if r_start != -1:
        t = 3 if line[r_start+16:r_start+21] == 'food"' else 4
        rng = t + 15
    if t == 0 and extras != 0:
      numer = extras
      denom = extras + RNG_TYPE[2]
      while len(rr) < c:
        x = random_float(rng) * unluck
        if x < odds[0]:
          rr.append(3)
        elif x < odds[1]:
          rr.append(2)
        elif x < odds[2]:
          rr.append(1)
        elif numer != 0 and (x - odds[2]) * denom < (unluck - odds[2]) * numer:
          if numer == 3:
            rr.append(int(x * 59049) % 3 - 3) # use a low-order "digit"
          elif numer == 2:
            if 'chemical_seven' not in DICT or -3 in rr:
              rr.append(int(x * 16384) % 2 - 2)
            elif 'rain' not in DICT or -1 in rr:
              rr.append(int(x * 32768) % 2 - 3)
            elif int(x * 65536) % 2 == 0:
              rr.append(-1)
            else:
              rr.append(-3)
          elif 'chemical_seven' not in DICT or -3 in rr:
            if 'rain' not in DICT or -1 in rr:
              rr.append(-2)
            else:
              rr.append(-1)
          else:
            rr.append(-3)
          numer -= 1
          denom -= 1
        else:
          rr.append(0)
          denom -= 1
    elif t == 3 and 'chemical_seven' in DICT:
      numer = 1
      denom = extras + RNG_TYPE[6]
      while len(rr) < c:
        x = random_float(rng) * unluck
        if x < odds[0]:
          rr.append(3)
        elif x < odds[1]:
          rr.append(2)
        elif x < odds[2]:
          rr.append(1)
        elif numer != 0 and (x - odds[2]) * denom < (unluck - odds[2]) * numer:
          rr.append(-3)
          numer = 0
        else:
          rr.append(0)
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
      if r == -3:
        ss.append('chemical_seven')
        continue
      if r == -2:
        ss.append('ninja')
        continue
      if r == -1:
        ss.append('rain')
        continue
      nolunch = IDS[0][r][0]
      lnl = len(nolunch)
      while True:
        s = None
        i = random_int(r + 2)
        if i < lnl:
          s = nolunch[i]
        else:
          lunch = IDS[0][r][1]
          if i < lnl + len(lunch):
            s = 'watermelon' if r == 3 else lunch[random_int(r + 6)]
          else:
            s = 'eldritch_beast' if r == 3 else IDS[0][r][2][random_int(r + 9)]
        if s not in DICT:
          ss.append(s)
          DICT[s] = True
          break
  elif t == 1:
    for r in rr:
      result = IDS[1][r][0][0]
      for i in range(THRESHOLD):
        s = IDS[1][r][0][random_int(r + 13)]
        if s not in DICT:
          result = s
          break
      ss.append(result)
      DICT[result] = True
  elif t == 2:
    items = IDS[1][0][0] + IDS[1][1][0] + IDS[1][2][0] + IDS[1][3][0]
    i = 0
    while i < 3:
      s = items[random_int(17)] + '_essence'
      if s not in DICT:
        ss.append(s)
        DICT[s] = True
        i += 1
  else:
    for r in rr:
      if r == -3:
        ss.append('chemical_seven')
        continue
      while True:
        if r == 3:
          very_rare = IDS[0][3][t - 2][0]
          if very_rare not in DICT:
            ss.append(very_rare)
            DICT[very_rare] = True
            break
          s = IDS[0][2][t - 2][random_int(t * 3 - 1)]
        else:
          s = IDS[0][r][t - 2][random_int(t * 3 - 3 + r)]
        if s not in DICT:
          ss.append(s)
          DICT[s] = True
          break

  sys.stdout.write(line[:pos+1]) # copy first quotation mark
  sys.stdout.write('","'.join(ss))
  sys.stdout.write(line[end-1:]) # copy last quotation mark

save()
