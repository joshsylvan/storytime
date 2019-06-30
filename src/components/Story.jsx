import React, { useState, useEffect } from 'react';
import { SpeechBlock } from '../entity/SpeechBlock';
import { connectToServer } from '../util/api';

const STORY_STATE = {
  LOBBY: 0,
  READING: 1,
  WAITING: 2,
};

export default () => {
  const [block, setBlock] = useState();
  const [socket, setSocket] = useState();
  const [players, setPlayers] = useState([]);
  const [gameState, setGameState] = useState();

  const onEvent = (soc) => {
    soc.on('lobby', (data) => {
      setPlayers(data.players);
    });
    soc.on('narrator', (data) => {
      // Handle the narrator lines
      setGameState(STORY_STATE.READING);
      setBlock(new SpeechBlock(data));
    });
    soc.on('speak', (data) => {
      // Handle the narrator lines
      console.log('asdasd');
      const utterThis = new SpeechSynthesisUtterance(data);
      window.speechSynthesis.speak(utterThis);
    });
  };

  const onDialogRead = () => {
    socket.emit('read_end');
    setGameState(STORY_STATE.WAITING);
  };

  useEffect(() => {
    // setBlock(new SpeechBlock(
    //   [
    //     'The year is 1945.',
    //     'Our heroes find themselves in Nazie Germany',
    //     'The Goal is simple.',
    //     'Kill Hitler.',
    //     'You are all a team of elite assassins',
    //     'Please dress appropriatly',
    //   ]
    // ));
    setSocket(connectToServer(null, onEvent, null));
    setGameState(STORY_STATE.LOBBY);
  }, []);


  const speek = () => {
    block.speek(onDialogRead);
  }

  useEffect(() => {
    console.dir(block);
    if (block) block.speek(onDialogRead);
  }, [block])

  let content;
  switch (gameState) {
    case STORY_STATE.LOBBY:
      content = (<div>
        {players.map(([name, title]) => (<h2>{`${name}, ${title}`}</h2>))}
        <button onClick={speek}>CLICK</button>
      </div>);
      break;
    case STORY_STATE.READING:
      content = JSON.stringify(block);
      break;
    case STORY_STATE.WAITING:
      content = 'waiting';
      break;
  }


  return (
    <div>
      {content}
    </div>
  );
};
