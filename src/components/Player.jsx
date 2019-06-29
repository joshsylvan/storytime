import React, { Fragment, useEffect, useState } from 'react';
import { connectToServer } from '../util/api';

const GAME_STATES = {
  INTRO: 0,
  LOBBY: 1,
  NARRATOR: 2,
  INPUT: 3,
  CHOICE: 4,
  WAITING: 5,
};

export default () => {
  const [name, setName] = useState();
  const [storyName, setStoryName] = useState();
  const [socket, setSocket] = useState();
  const [gameState, setGameState] = useState(GAME_STATES.INTRO);
  const [input, setInput] = useState({});
  const [choice, setChoice] = useState({});

  const onEvent = (soc) => {
    soc.on('lobby', (data) => {
      if (!storyName) {
        setGameState(GAME_STATES.LOBBY);
        setStoryName(data.honorific);
      }
    });
    soc.on('narrator', (data) => {
      setGameState(GAME_STATES.NARRATOR);
    });
    soc.on('input', (data) => {
      console.log(data);
      setGameState(GAME_STATES.INPUT);
      setInput({
        question: data.question,
        input: '',
      });
    });
    soc.on('choice', (data) => {
      setGameState(GAME_STATES.CHOICE);
      setChoice({
        question: data.question,
        choices: data.choices,
        choice: '',
      });
    });
  };

  const onClick = () => {
    const soc = connectToServer(null, onEvent, null);
    setSocket(soc);
    soc.emit('intro', { name });
  };

  const onNext = (type, string) => {
    const body = {
      type,
      data: string,
    };
    socket.emit('next', { body });
    setGameState(GAME_STATES.WAITING);
  }

  const onStartGame = () => {
    socket.emit('start');
  };

  useEffect(() => {
    return () => {
      if (socket) socket.close();
    };
  }, []);

  let content;
  switch (gameState) {
    case GAME_STATES.INTRO:
      content = (
        <div>
          PLAYER WHAT IS YOUR NAME?
        <input
            onChange={(e) => setName(e.target.value)}
            type="text"
          />
          <button onClick={onClick}>JOIN STORY</button>
        </div>
      );
      break;
    case GAME_STATES.LOBBY:
      content = (
        <div>
          <h1>{`${name}, ${storyName}`}</h1>
          IN THE LOBBY
          <button onClick={onStartGame}>Start Game</button>
        </div>
      );
      break;
    case GAME_STATES.NARRATOR:
      content = (
        <div>
          <h1>{`${name}, ${storyName}`}</h1>
          <p>The narrator is speeking...</p>
        </div>
      );
      break;
    case GAME_STATES.INPUT:
      content = (
        <div>
          <h1>{input.question}</h1>
          <input type="text" onChange={(e) => setInput({ ...input, input: e.target.value })} />
          <button onClick={() => onNext('input', input.input)}>Submit</button>
        </div>
      );
      break;
    case GAME_STATES.CHOICE:
      content = (
        <div>
          <h1>{choice.question}</h1>
          {choice.choices.map(item => (
            <button onClick={() => onNext('choice', item)}>{item}</button>
          ))}
        </div>
      );
      break;
    case GAME_STATES.WAITING:
      content = (
        <div>
          <h1>{`${name}, ${storyName}`}</h1>
          <p>Waiting for player responses...</p>
        </div>
      );
      break;
  }
  console.log(gameState);
  return (
    <Fragment>
      {content}
    </Fragment>
  );
};
