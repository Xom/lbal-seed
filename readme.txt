lbal-seed v20210716a: Seeded runs for Luck Be A Landlord

I. What is a seeded run?
II. What are lbal-seed's requirements?
III. Where to download lbal-seed?
IV. How to use lbal-seed?
V. How does lbal-seed work?
VI. KNOWN ISSUES
VII. Algorithm
VIII. What's that spreadsheet that Xom uses?

I'm Xom#7240 in Discord; see lbal-seed in action at https://twitch.tv/xomnom

I welcome your questions, bug reports, feedback, and seeded run stories!

===========================================================

I. What is a seeded run?

A seed is a value used to initialize a RNG. By re-using a seed, the same sequence of random outcomes can be re-created. lbal-seed applies a seeded RNG to symbol, item, and essence rolls; the same seed will always generate the same rolls until luck modifiers are acquired (details later in this FAQ). lbal-seed doesn't affect spins or abilities; even with the same seed, their outcomes remain independently random across runs.

Use the same seed as a friend and see how you fare given the same rolls!

===========================================================

II. What are lbal-seed's requirements?

bash and python3 are required. OS X and most Linux distributions come with both.

On Windows, there are three possibilities. One is to use Windows Subsystem for Linux (WSL), which should work, though no one yet has tried and reported back to me. (You could be the one! How about it?)

For WSL, the big question is whether it can run the Linux version of LBAL. Otherwise, if you use the Windows executable, then play.sh won't be able to stop the game automatically, and you'll have to manually close the game at each roll. (I imagine that Alt+F4 or clicking the X is faster than the in-game menu.)

The other possibilities are to emulate Linux in a virtual machine, or to install Linux on a USB drive to use when you want to play LBAL with lbal-seed.

===========================================================

III. Where to download lbal-seed?

lbal-seed lives at https://github.com/xom/lbal-seed

You can download the latest by clicking the green download button labeled "Code", then "Download ZIP".

(Which is a link to https://github.com/Xom/lbal-seed/archive/refs/heads/master.zip )

===========================================================

IV. How to use lbal-seed?

Before you start, make a backup of your LBAL.save in case something goes wrong.

In your command-line terminal, run play.sh, with the following parameters:
1. The location of LBAL's executable
2. The location of LBAL.save
3. Optionally, a seed string (otherwise the script will prompt you for one)

The format is thus:

./play.sh EXECLOCATION SAVELOCATION (SEEDSTRING)

On my computer, it goes:

./play.sh ~/.local/share/Steam/steamapps/common/Luck\ be\ a\ Landlord/Luck\ be\ a\ Landlord.x86_64 ~/.local/share/godot/app_userdata/Luck\ be\ a\ Landlord/LBAL.save (SEEDSTRING)

The script will run LBAL, and at each roll, it will stop LBAL, then run seed.py to edit the save, then reload LBAL for you to continue playing.

===========================================================

V. How does lbal-seed work?

seed.py is a python3 script that takes as input a LBAL.save and a seed string, and outputs a save that's identical except for the current roll (2-3 cards depending whether you have Shattered Mirror). It keeps track of its progress in files named SEEDSTRING.dat and SEEDSTRING.save, where SEEDSTRING is the seed string. (So any non-empty string can be a seed as long as it can be used in a filename. For convenience, auto-generated seeds have zz- as a prefix.) play.sh is a bash script that alternates endlessly between running LBAL and seed.py.

===========================================================

VI. KNOWN ISSUES

I've added a 0.2-second pause between stopping the game and running seed.py, because sometimes the game saves twice in immediate succession, resulting in a read error if I don't pause. If you see this problem again, please tell me so that I can increase the pause.

One known case is when Adoption Papers is used. I don't know about other rolling items. There's another known case for which I have the save file, but I don't know the distinguishing condition. In theory, it should never be necessary to save twice like this, but I don't feel like bothering the developer about this now; maybe later when the end of early access is nigh.

--

lbal-seed v20210716a fixes the previously incorrect handling of Cursed Katana and Rain Cloud. Previously, if you had Cursed Katana / Rain Cloud, the algorithm didn't skip Ninja / Rain in the uncommon sequence, which meant you could still get Ninja / Rain when you were supposed to get an uncommon, resulting in finding 1.35x as many Ninja / Rain as you were supposed to. (I thought I had implemented the skipping but apparently I didn't. I discovered and fixed it when extending the code for Lucky Seven Essence.)

===========================================================

VII. Algorithm

It's the same-symbols algorithm in this post: https://discord.com/channels/213781388992708608/797256317109534720/851928830556766258
The behavior is statistically identical to the original game, assuming that the following odds table that I used is correct: https://discord.com/channels/213781388992708608/797256317109534720/852543163310932008
More details in this FAQ when I get around to it.

===========================================================

VIII. What's that spreadsheet that Xom uses?

It calculates and projects gold-per-turn. It's not related to lbal-seed. It's a LibreOffice Calc spreadsheet with macros. If you'd like to recreate it in Excel, you can message me on Discord for help. The spreadsheet contains its own readme, and you can download it at https://xomboard.neocities.org/lbal.ods
