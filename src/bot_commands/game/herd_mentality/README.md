# How to Play Herd Mentality

## Introduction

This game is inspired by the board game named _Herd Mentality_. It's a fun and engaging game that encourages players to think like the majority. The goal is to match your answers with the most players to win.

---

## Objective

The objective of the game is to have the most points by the end of the game. Points are earned by matching your answers with the majority of players.

## Game Play

1. **Choose a Moderator**:

   - The moderator will read the questions and manage the game flow. (Normally Nox)

2. **Start Session**:

   - Use the `/herdmentality` command to start a new session.
   - Optionally, you can add the `without` parameter to exclude players from participating in the session.

3. **Start the Game**:

   - Use the `/hquiz` command to start a new round with a question.

4. **Answering**:

   - Players submit their answers secretly using the `/ha` command.

5. **Reveal Answers**:

   - The moderator reveals the answers using the `/hshow` command.

6. **Scoring**:

   - The moderator can add points to players using the `/haddpoint` command.
   - Alternatively, use the `/haddpointview` command to display buttons for adding points to players.

7. **Repeat**:
   - After adding points, the moderator can use the `/hresult` command to show current results and end the round.

## The Pink Cow

In _Herd Mentality_, the Pink Cow is a unique game mechanic that adds an interesting twist to the gameplay. Here’s how it works:

- **Receiving the Pink Cow**:
  - If a player’s answer is different from the majority of players, they receive the Pink Cow. This means that their answer did not match the most common response.
- **Consequences of Holding the Pink Cow**:

  - A player who holds the Pink Cow cannot win the game. While they can still accumulate points, they are effectively at a disadvantage compared to other players.
  - The Pink Cow serves as a reminder for players to think carefully about their answers, as unique answers can lead to receiving the cow.

- **Passing the Pink Cow**:

  - If a new player joins the game and provides an answer that is different from the existing answers, they will receive the Pink Cow from the current holder.
  - This mechanic encourages players to stay engaged and think strategically about their answers.

- **Goal**:
  - The ultimate goal is to avoid holding the Pink Cow while trying to match answers with the majority of players. Players should aim to think collectively to maximize their points and avoid the Pink Cow.

## Commands Overview

- **/herdmentality**: Start a new session. Optionally exclude players.
- **/hquiz**: Start a new round with a question.
- **/ha**: Submit an answer for the current question.
- **/hshow**: Show answers for the current question.
- **/haddpoint**: Add points to specified players by name.
- **/haddpointview**: Add points to players using buttons for interaction.
- **/hend**: End the current session and archive the scoreboard.
- **/hcow**: Assign the pink cow to a player in the session.
- **/hrule**: Explain the rules of Herd Mentality in Thai.

## Winning the Game

- The player with the most points at the end of the game is declared the winner.

## Tips for Success

- **Think Like the Group**: Try to predict what the majority will answer.
- **Avoid Unique Answers**: Unique answers do not earn points.
- **Stay Engaged**: Pay attention to the group's dynamics and trends.

## Conclusion

_Herd Mentality_ is a game of consensus and fun. It's perfect for parties and gatherings, encouraging players to think collectively. Enjoy the game and may the best herd win!

---

## Checklist

- [x] Start a new session using `/herdmentality` command.
- [x] Start a new round using `/hquiz` command.
- [x] Answer using `/ha` command.
- [x] Show answers using `/hshow` command.
- [x] Add points using `/haddpoint` command.
- [x] Add points using `/haddpointview` command.
- [x] End the session using `/hend` command.
- [x] Improve `/haddpoint` by changing from inserting player's name to using `discord.ui.View`.
- [x] Improve `/herdmentality` to start a new session by adding a `without` parameter for players not participating in the session.
- [x] Add interaction for submitting answers.
- [x] Adding COW!!

## Footnotes

Inspired by the original board game _Herd Mentality_.
