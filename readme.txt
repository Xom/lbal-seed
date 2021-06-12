lbal-seed: Seeded runs for Luck Be A Landlord

I. What is a seeded run?
II. What are lbal-seed's requirements?
III. How to use lbal-seed?
IV. How does lbal-seed work?
V. Explain the seeding algorithm.
VI. How to use lbal-seed on Windows?

I'm Xom#7240 in Discord. I welcome your questions, bug reports, feedback, and seeded run results!

Demonstration video coming soon. In the meantime, look for recordings of me using lbal-seed at https://twitch.tv/xomnom

===========================================================

I. What is a seeded run?

A seed is a value used to initialize a RNG. By re-using a seed, the same sequence of random outcomes can be re-created. lbal-seed applies a seeded RNG to symbol and item rolls; the same seed will always generate the same rolls until luck modifiers are acquired (details later in this FAQ). lbal-seed doesn't affect spins or abilities; even with the same seed, their outcomes remain independently random across runs.

Use the same seed as a friend and see how you fare given the same rolls!

===========================================================

II. What are lbal-seed's requirements?

bash and python3 are required. OS X and most Linux distributions come with both. I'll discuss Windows later in this FAQ.

===========================================================

III. How to use lbal-seed?

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

IV. How does lbal-seed work?

seed.py is a python3 script that takes as input a LBAL.save and a seed string, and outputs a save that's identical except for the current roll (2-3 cards depending whether you have Shattered Mirror). It keeps track of its progress in files named SEEDSTRING.dat and SEEDSTRING.save, where SEEDSTRING is the seed string. (So any non-empty string can be a seed as long as it can be used in a filename. For convenience, auto-generated seeds have zz- as a prefix.) play.sh is a bash script that alternates endlessly between running LBAL and seed.py.

===========================================================

V. Explain the seeding algorithm.

It's the same-symbols algorithm in this post: https://discord.com/channels/213781388992708608/797256317109534720/851928830556766258
The behavior is statistically identical to the original game, assuming that the following odds table that I used is correct: https://discord.com/channels/213781388992708608/797256317109534720/852543163310932008
More details in this FAQ when I get around to it.

===========================================================

VI. How to use lbal-seed on Windows?

There are two possibilities. One is to use Windows Subsystem for Linux (WSL), which should work, though no one yet has tried and reported back to me. The other, of course, is to emulate Linux in a virtual machine.

For WSL, the big question is whether it can run the Linux version of LBAL. Otherwise, if you use the Windows executable, then play.sh won't be able to stop the game automatically, and you'll have to manually close the game at each roll. (I imagine that Alt+F4 or clicking the X is faster than the in-game menu.)

Again, I'm Xom#7240 in Discord. I welcome your questions, bug reports, feedback, seeded run results, and ESPECIALLY reports of using WSL!
