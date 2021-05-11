import React from 'react';
import { QueryClientProvider, QueryClient } from 'react-query';
import { Switch, Route, BrowserRouter } from 'react-router-dom';

import PageLayout from '../../common/layout/PageLayout';
import Stops from '../stops/Stops';
import Routeh from '../routes/Route';
import Routes from '../routes/Routes';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <PageLayout>
          <Switch>
            <Route exact component={Routes} path={['/', '/routes']} />
            <Route exact component={Routeh} path={'/routes/:id'} />
            <Route exact component={Stops} path="/stops" />
          </Switch>
        </PageLayout>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
