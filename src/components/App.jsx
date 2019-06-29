import React from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import Story from './Story';
import Player from './Player';

export default () => (
  <div>
    <HashRouter>
      <Switch>
        <Route path="/story" component={Story} />
        <Route path="/player" component={Player} />
      </Switch>
    </HashRouter>
  </div>
);