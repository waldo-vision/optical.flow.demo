# visual-anticheat
A project that uses optical flow and machine learning to detect aimhacking in video clips from the game Apex Legends.

## The What
A new form of cheating in video games is using deep learning to implement an aim assist cheat.
This form of cheating is very hard to detect because no game hacking or modification is necessary, so anti-cheats can't detect it easily.

We're trying to combat this new kind of cheating by creating our own deep learning program to detect this behavior in video clips.
We're starting with only one game, Apex Legends, to focus our efforts.

## The How
Because deep learning aimhacks don't actually modify the game or computer in any way, the only way to detect this form of cheating is by observing the cheating behavior while spectating, or by analyzing the aiming data of a player. We don't have access to raw aim data for players, so our goal is to analyze the video directly using deep learning to detect aimhacking.
