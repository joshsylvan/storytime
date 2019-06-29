import React, { Fragment, useEffect, useState } from 'react';
import { connectToServer } from '../util/api';

const GAME_STATES = {
  INTRO: 0,
  LOBBY: 1,
};

export default () => {
  const [name, setName] = useState();
  const [storyName, setStoryName] = useState();
  const [socket, setSocket] = useState();
  const [gameState, setGameState] = useState(GAME_STATES.INTRO);

  const onEvent = (soc) => {
    soc.on('lobby', (data) => {
      if (!storyName) {
        setGameState(GAME_STATES.LOBBY);
        setStoryName(data.honorific);
      }
    });
  };

  const onClick = () => {
    const soc = connectToServer(null, onEvent, null);
    setSocket(soc);
    soc.emit('intro', { name });
  };

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
  }

  return (
    <Fragment>
      {content}
    </Fragment>
  );
};
