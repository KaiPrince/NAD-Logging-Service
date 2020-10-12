import React, { useEffect, useState } from 'react';

import { ThemeProvider, createMuiTheme } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import CssBaseline from '@material-ui/core/CssBaseline';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const baseTheme = createMuiTheme({
  overrides: {
    MuiCssBaseline: {
      '@global': {
        body: {
          margin: 0
        },
      },
    },
  }
});

const appTheme = theme => ({
  ...theme,
  overrides: {
    MuiGrid: {
      container: {
        justifyContent: 'center'
      },
      item: {
        [theme.breakpoints.up('sm')]: {
          width: '30%',
          minHeight: '500px'
        },
        border: '1px solid black',
        padding: '2em'
      }
    }
  }
});

export default function () {
  const [results, setResults] = useState(null);

  const performTest = async (params) => {
    console.log(`running test ${params.testName}`);

    // await sleep(3000)
    // Throw new error if something out of our control has happened, will stop all tests
    // throw new Error()

    try {
      const result = await fetch('http://localhost:5000/log', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
      });

      return `success during ${params.testName} (${result.status})`;
    } catch (exception) {
      return `error during ${params.testName}: ${exception}`;
    }
  };

  const performAllTests = () => {
    Promise.all([
      {
        testName: 'test1',
        message: 'test log 1',
        logLevel: '1',
        applicationId: '0x01',
        authToken: '0x01',
        dateTime: new Date(),
      },
      {
        testName: 'test2',
        message: 'test log 2',
        logLevel: '2',
        applicationId: '0x01',
        authToken: '0x01',
        dateTime: new Date(),
      }
    ].map(performTest))
      .then((results) => {
        setResults(results);
        console.log(results);
      })
      .catch((err) => {
        // An error in the client
        console.log('real bad error during test man');
      });

    console.log('start testing');
  };

  useEffect(() => {
    performAllTests();
  }, []);

  return (
    <div>
      <ThemeProvider theme={baseTheme}>
        <CssBaseline />
        <ThemeProvider theme={appTheme}>
          <Grid container>
            <Grid item>
              RUN ALL TEST
              <br />
              {results ? (
                <>
                  {results.map(result => <div>{result}</div>)}
                </>
              ) : 'no results'}
            </Grid>
            <Grid item>
              RUN CUSTOM TEST
            </Grid>
            <Grid item>
              REGISTER SERVICE
            </Grid>
          </Grid>
        </ThemeProvider>
      </ThemeProvider>
    </div>
  );
}
