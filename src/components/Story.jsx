import React, { useState, useEffect } from 'react';
import { SpeechBlock } from '../entity/SpeechBlock';
import { connectToServer } from '../util/api';

export default () => {
  const [block, setBlock] = useState();
  const [socket, setSocket] = useState();
  const [players, setPlayers] = useState();

  const onEvent = (soc) => {
    soc.on('lobby', (data) => {
      setPlayers(data.players);
      console.log(data);
    });
  };

  useEffect(() => {
    setBlock(new SpeechBlock(
      [
        'The year is 1945.',
        'Our heroes find themselves in Nazie Germany',
        'The Goal is simple. Kill Hitler',
      ]
    ));
    setSocket(connectToServer(null, onEvent, null));
  }, []);

  const speek = () => {
    block.speek();
  }

  return (
    <div>
      {JSON.stringify(players)}
      <button onClick={speek}>CLICK</button>
    </div>
  );
};
