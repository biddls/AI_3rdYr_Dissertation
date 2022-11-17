# Project Evaluation

## Current thoughts
I feel like that a more stripped down version of what I was planning would be a good middle-ground. Just focusing on the path prediction of planes as the 2nd 1/2 of the project doesn't contribute massively to the "academic" portion of the dissertation.

> If by Christmas I don't have the data gathering portion of the project working properly then I will switch to Anichos' idea and do something with peer-to-peer none central drone planning where they act autonomously to maximise some score.

I feel like this option would give me the best opportunity to work on something that I'm very excited about while also being sufficiently relevant to a backup plan. If there is an opportunity to extend my work to fully incorporate the idealised scope then that is great, if I don't have enough time then I still have a fully fleshed out project.

## Project A specification
> For each agent `A`<sub>`p`</sub> at time `T`<sub>`n`</sub> predict the position of all agents `A` at time `T`<sub>`n+1`</sub> taking into account all other agents.

The data and eventual intended application of this will be before the game Digital Combat Simulator ([DCS](https://www.digitalcombatsimulator.com/en/))  by Eagle Dynamics. This will allow campaign creators to use a more intelligent system that can make predictions about the future state of the campaign that they are running. If there is enough time, I intend to create a path finding module that will allow for more intelligent pathing to be made available to all mission creators within the community.

## Project B specification

> For each agent `A`<sub>`d`</sub> make a move and send a message to each connected agent with the goal of maximising some reward `R` for the whole swarm for each time-step `T`<sub>`n`</sub> such that the maximum `R` is reached in the smallest possible `n`.

Creating a self adapting and independently behaving agent that communicates with surrounding agents to achieve some goal. This is done with the aim of exploring the differences between the top down control schema VS a peer-to-peer system. The evaluation of this will come down to a variety of factors: resiliency, efficacy, speed and any others factors that are decided upon at a later date.

