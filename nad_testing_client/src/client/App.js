import React, { useEffect, useState } from 'react';

import { ThemeProvider, createMuiTheme } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import DoneIcon from '@material-ui/icons/Done';
import ArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import ArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import ClearIcon from '@material-ui/icons/Clear';
import CssBaseline from '@material-ui/core/CssBaseline';

const url = 'http://localhost:5000/logger/log';

const sampleTests = [
  {
    result: undefined,
    resultObj: undefined,
    status: 'waiting', // DONE, WAITING, RUNNING
    message: 'The app has crashed unexpectedly.',
    logLevel: 'CRITICAL',
    applicationName: 'BingoBangoBongo',
    processName: 'node.exe',
    processId: 6545,
    dateTime: new Date(2020, 1, 1),
    extra: { userId: 5, endpoint: '/users/5' },
    authToken: "eyy35t4m5vtk489k7vtk5ivk8ct74",
    url
  },
  {
    result: undefined,
    actualResult: undefined,
    status: 'waiting', // DONE, WAITING, RUNNING
    message: 'User authenticated successfully.',
    logLevel: 'INFO',
    applicationName: 'BingoBangoBongo',
    processName: 'node.exe',
    processId: 1337,
    dateTime: new Date(2020, 5, 16),
    extra: { userId: 5 },
    authToken: "eyy35t4m5vtk489k7vtk5ivk8ct74",
    url
  },
  {
    result: undefined,
    actualResult: undefined,
    status: 'waiting', // DONE, WAITING, RUNNING
    message: 'User could not be found.',
    logLevel: 'ERROR',
    applicationName: 'BingoBangoBongo',
    processName: 'java.exe',
    processId: 9385,
    dateTime: new Date(2020, 4, 20),
    extra: { userId: 5, endpoint: '/users/5' },
    authToken: "eyy35t4m5vtk489k7vtk5ivk8ct74",
    url
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
        [theme.breakpoints.down('sm')] : {
          flexDirection: 'column'
        },
        justifyContent: 'center',
      },
      item: {
        [theme.breakpoints.up('md')]: {
          width: '40%',
          minHeight: '500px',
        },
        border: '1px solid black',
        padding: '1em',
      },
    },
    MuiTypography: {
      h1: {
        fontSize: '2em',
      },
    },
    MuiSvgIcon: {
      root: {
        fontSize: '1em'
      }
    },
  },
});

export default function () {
  const [testRunning, setTestRunning] = useState(false);
  const [tests, setTests] = useState(sampleTests);

  const performTest = async (params) => {
    startTest(params.index);

    try {
      const result = await fetch(params.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': '0xABC',
        },
        body: JSON.stringify(params), // TODO Only send relevant test info
      });

      completeTest(params.index, result.status, result);
    } catch (exception) {
      completeTest(params.index, 'ERR', exception);
    }
  };

  const renderTest = (test) => {
    const [isOpen,setIsOpen] = useState(false);
    const {
      status,
      result,
      resultObj,
      index,
      message,
      logLevel,
      applicationName,
      authToken,
      processName,
      processId,
      dateTime,
      url,
      extra
    } = test;

    const renderStatus = () => {
      switch (status) {
        case 'done':
          return result === 200 ? <><DoneIcon /> [{result}]</> : <><ClearIcon /> [{result}]</>;
        case 'waiting':
          if (testRunning) {
            return 'Waiting to run...';
          }
          break;
        default:
          if (testRunning) {
            return <CircularProgress size={'1em'} />;
          }
          return undefined;
      }
    };

    return (
      <div  style={{border: '1px solid black', padding: '0.5em', borderRadius: '0.5em', width: '100%', cursor: isOpen ? 'default' : 'pointer', marginTop: '1em'}} onClick={!isOpen ? () => setIsOpen(true) : undefined}>
        <div style={{ display: 'flex'}}>
          <div style={{ width: '50%', }}>
            <div>Test {index + 1}</div>
          </div>
          <div style={{width: '50%'}}>
             <div style={{float:'right'}}>{renderStatus()} <span style={{cursor: 'pointer'}}>{isOpen ? <ArrowUpIcon onClick={() => setIsOpen(false)} /> : <ArrowDownIcon onClick={() => setIsOpen(true)} />}</span></div>
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'column'}}>
          {isOpen ? (
            <>
              <div style={{borderBottom: '2px solid grey', marginBottom: '1em', marginTop: '1em', width: '100%'}} />

              <div style={{display: 'flex'}}>

              <div style={{ width: '60%', }}>
                <div>Details</div>
                <div>message: {message}</div>
                <div>dateTime: {dateTime.toString()}</div>
                <div>applicationName: {applicationName}</div>
                <div>processName: {processName}</div>
                <div>processId: {processId}</div>
                <div>logLevel: {logLevel}</div>
                <div>extra: {JSON.stringify(extra)}</div>
                <div>authToken: {authToken}</div>
                <div>url: {url}</div>
              </div>
              <div style={{width: '40%'}}>
                <div>Results</div>
                {status === 'done' ? (
                  <>
                    <div>{isNaN(result) ? (
                      <div>
                        {resultObj.toString()}
                      </div>
                    ) : (
                      <div>
                        <div>status: {resultObj.status}</div>
                        <div>statusText: {resultObj.statusText}</div>
                        <div>headers: {JSON.stringify(resultObj.headers)}</div>
                      </div>
                    )}</div>
                  </>
                ) : 'No results to display'}
              </div>

              </div>

            </>
          ) : undefined}
        </div>
      </div>
    );
  };

  const completeTest = (testIndex, result, resultObj) => {
    setTests(
      tests.map((item, index) => {
        if (index === testIndex) {
          item.result = result;
          item.status = 'done';
          item.resultObj = resultObj;
        }
        return item;
      }),
    );
  };

  const resetTests = async () => {
    setTests(
      tests.map((item) => {
        item.result = null;
        item.status = 'waiting';
        return item;
      }),
    );
  };

  const startTest = (testIndex) => {
    setTests(
      tests.map((item, index) => {
        if (index === testIndex) {
          item.status = 'running';
        }

        return item;
      }),
    );
  };

  const performAllTests = async () => {
    await resetTests();
    setTestRunning(true);
    for (const index in tests) {
      await performTest({...tests[index], index: parseInt(index)});
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
              <Typography variant="h1">
                RUN SET OF REQUESTS
              </Typography>
              <div style={{borderTop: '3px solid grey', marginTop: '1em', marginBottom: '1em'}}></div>
              <Button
                disabled={testRunning}
                onClick={performAllTests}
              >
                Go
              </Button>
              <br />
              {tests && tests.length > 0 ? (
                <>
                  {tests.map((test, index) => (
                    <div key={index}>{renderTest({...test, index})}</div>
                  ))}
                </>
              ) : (
                'No tests available'
              )}
            </Grid>
            <Grid item>
              <Typography variant="h1">RUN CUSTOM REQUEST</Typography>
              <div style={{borderTop: '3px solid grey', marginTop: '1em', marginBottom: '1em'}}></div>
              <Button>
                Go
              </Button>
              <br />
              <label htmlFor="message">Message</label>
              <input type="text" id="message" /><br />

              <label htmlFor="debugLevel">Debug Level</label>
              <input type="text" id="debugLevel" /><br />

              <label htmlFor="url">URL</label>
              <input type="text" id="url" defaultValue={url} />
            </Grid>
          </Grid>
        </ThemeProvider>
      </ThemeProvider>
    </div>
  );
}
