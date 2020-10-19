import React, { useEffect, useState } from 'react';

import { ThemeProvider, createMuiTheme } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import green from '@material-ui/core/colors/green';
import CssBaseline from '@material-ui/core/CssBaseline';

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const sampleTests = [
  {
    testName: 'test1',
    result: false,
    status: 'waiting', // DONE, WAITING, RUNNING
    message: 'test log 1',
    logLevel: '1',
    applicationId: '0x01',
    authToken: '0x01',
    processName: 'node.exe',
    processId: 1000,
    dateTime: new Date(),
  },
  {
    testName: 'test2',
    result: false,
    status: 'waiting', // DONE, WAITING, RUNNING
    message: 'test log 2',
    logLevel: '2',
    applicationId: '0x01',
    authToken: '0x01',
    processName: 'node.exe',
    processId: 1000,
    dateTime: new Date(),
  },
];

const baseTheme = createMuiTheme({
  overrides: {
    MuiCssBaseline: {
      '@global': {
        body: {
          margin: 0,
        },
      },
    },
  },
});

const appTheme = (theme) => ({
  ...theme,
  overrides: {
    MuiGrid: {
      container: {
        justifyContent: 'center',
      },
      item: {
        [theme.breakpoints.up('sm')]: {
          width: '30%',
          minHeight: '500px',
        },
        border: '1px solid black',
        padding: '2em',
      },
    },
    MuiTypography: {
      h1: {
        fontSize: '2em',
      },
    },
  },
});

export default function () {
  const [testRunning, setTestRunning] = useState(false);
  const [tests, setTests] = useState(sampleTests);

  const performTest = async (params) => {
    console.log('params: ', params);
    startTest(params.testName);
    await sleep(3000);
    // Throw new error if something out of our control has happened, will stop all tests
    // throw new Error()

    try {
      const result = await fetch('http://localhost:5000/logger/log', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': '0xABC',
        },
        body: JSON.stringify(params),
      });

      completeTest(params.testName, true);
      return `success during ${params.testName} (${result.status})`;
    } catch (exception) {
      completeTest(params.testName, false);
      return `error during ${params.testName}: ${exception}`;
    }
  };

  // TODO Improve this logic
  const renderTest = ({ testName, status, result }) => {
    const renderStatus = () => {
      switch (status) {
        case 'done':
          return result ? 'SUCCESS' : 'FAILURE';
        case 'waiting':
          if (testRunning) {
            return 'waiting to run...';
          }
          break;
        default:
          if (testRunning) {
            return <CircularProgress />;
          }
          return undefined;
      }
    };

    const testData = () => {};

    return (
      <div>
        {testName} {renderStatus()}
      </div>
    );
  };

  const completeTest = (testName, result) => {
    setTests(
      tests.map((item) => {
        if (item.testName === testName) {
          item.result = result;
          item.status = 'done';
        }
        return item;
      })
    );
  };

  const resetTests = async (testName) => {
    setTests(
      tests.map((item) => {
        item.result = null;
        item.status = 'waiting';
        return item;
      })
    );
  };

  const startTest = (testName) => {
    setTests(
      tests.map((item) => {
        if (item.testName === testName) {
          item.status = 'running';
        }

        return item;
      })
    );
  };

  const performAllTests = async () => {
    await resetTests();
    setTestRunning(true);
    for (const index in tests) {
      await performTest(tests[index]);
    }
    setTestRunning(false);
  };

  return (
    <div>
      <ThemeProvider theme={baseTheme}>
        <CssBaseline />
        <ThemeProvider theme={appTheme}>
          <Grid container>
            <Grid item>
              <Typography variant="h1">RUN SET OF LOG REQUESTS</Typography>
              <Button disabled={testRunning} onClick={performAllTests}>
                Start
              </Button>
              <br />
              {tests ? (
                <>
                  {tests.map((test) => (
                    <div>{renderTest(test)}</div>
                  ))}
                </>
              ) : (
                'no results'
              )}
            </Grid>
            <Grid item>
              <Typography variant="h1">RUN CUSTOM REQUEST</Typography>
            </Grid>
          </Grid>
        </ThemeProvider>
      </ThemeProvider>
    </div>
  );
}
