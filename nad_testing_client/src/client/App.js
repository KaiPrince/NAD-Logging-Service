import React, { useEffect, useState } from 'react';

import { ThemeProvider, createMuiTheme, Chip } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import DoneIcon from '@material-ui/icons/Done';
import ArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import ArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import ClearIcon from '@material-ui/icons/Clear';
import CssBaseline from '@material-ui/core/CssBaseline';
import Card from '@material-ui/core/Card';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';

const url = 'http://localhost:5000/logger/log';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const sampleTests = [
  {
    result: undefined,
    resultObj: undefined,
    status: 'waiting', // DONE, WAITING, RUNNING
    testData: {
      message: 'The app has crashed unexpectedly.',
      logLevel: 'CRITICAL',
      applicationName: 'BingoBangoBongo',
      processName: 'node.exe',
      processId: 6545,
      dateTime: new Date(2020, 1, 1),
      extra: { userId: 5, endpoint: '/users/5' },
      authToken: "eyy35t4m5vtk489k7vtk5ivk8ct74",
      url
    }
  },
  {
    result: undefined,
    actualResult: undefined,
    status: 'waiting',
    testData: {
      message: 'User authenticated successfully.',
      logLevel: 'INFO',
      applicationName: 'BingoBangoBongo',
      processName: 'node.exe',
      processId: 1337,
      dateTime: new Date(2020, 5, 16),
      extra: { userId: 5 },
      authToken: "eyy35t4m5vtk489k7vtk5ivk8ct74",
      url
    }

  },
  {
    result: undefined,
    actualResult: undefined,
    status: 'waiting',
    testData: {
      message: 'User could not be found.',
      logLevel: 'ERROR',
      applicationName: 'Application 2',
      processName: 'java.exe',
      processId: 9385,
      dateTime: new Date(2020, 4, 20),
      extra: { userId: 5, endpoint: '/users/5' },
      authToken: "eyy35t4m5vtk489k7vtk5ivk8ct74",
      url
    }
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
    MuiCard: {
      root: {
        margin: '0.5em',
        padding: '1.5em'
      }
    },
    MuiGrid: {
      container: {
        flexDirection: 'column',
        [theme.breakpoints.down('xs')]: {
        },
        justifyContent: 'center',
      },
      item: {
        maxWidth: '960px',
        [theme.breakpoints.up('md')]: {
        },
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

const Divider = () => <div style={{ borderTop: '3px solid grey', margin: '1em 0' }}></div>

export default function () {
  const [testsRunning, setTestsRunning] = useState(false);
  const [tests, setTests] = useState(sampleTests);

  const performTest = async (testIndex, testData) => {
    startTest(testIndex);

    try {
      const result = await fetch(testData.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': '0xABC',
        },
        body: JSON.stringify(testData),
      });

      submitTestResult(testIndex, result.status, result);
    } catch (exception) {
      submitTestResult(testIndex, 'ERR', exception);
    }
  };

  const submitTestResult = (testIndex, result, resultObj) => {
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
    setTestsRunning(true);
    for (const index in tests) {
      await performTest(parseInt(index), { ...tests[index].testData });
    }
    setTestsRunning(false);
  };

  const testsCompleted = (tests) => tests.reduce((acc, cur) => {
    return cur.status === 'done' ? acc + 1 : acc;
  }, 0);

  const getTestColor = (result) => {
    if (result) {
      if (isNaN(result)) {
        return '#fff0f0';
      } else {
        return '#f8fff0';
      }
    }
    return '#ffffff';
  }

  const CustomRequest = () => {
    const [message, handleMessage] = useState('The app has crashed unexpectedly.');
    const [logLevel, handleLogLevel] = useState('CRITICAL');
    const [applicationName, handleApplicationName] = useState('BingoBangoBongo');
    const [processName, handleProcessName] = useState('node.exe');
    const [processId, handleProcessId] = useState('6545');
    const [dateTime, handleDateTime] = useState(new Date().toString());
    const [extra, handleExtra] = useState('{ userId: 5, endpoint: \'/users/5\' }');
    const [authToken, handleAuthToken] = useState('eyy35t4m5vtk489k7vtk5ivk8ct74');
    const [url, handleUrl] = useState('http://localhost:5000/logger/log');

    const makeCustomRequest = async () => {
      const result = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': authToken,
        },
        body: JSON.stringify({
          message,
          logLevel,
          applicationName,
          processName,
          processId,
          dateTime,
          extra
        })
      });
  
      console.log(result);
    };

    return (
      <Card style={{ backgroundColor: '#f5f5f5' }}>
        <Typography variant="h1">RUN CUSTOM REQUEST</Typography>
        <Divider />

        <Button
          onClick={makeCustomRequest}
          variant="contained"
        >
          Go
        </Button>

        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-message">message</InputLabel>
          <Input id="select-message" value={message} onChange={(e) => handleMessage(e.target.value)} placeholder="message" />
        </FormControl>

        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-logLevel">logLevel</InputLabel>
          <Input id="select-logLevel" value={logLevel} onChange={(e) => handleLogLevel(e.target.value)} placeholder="logLevel" />
        </FormControl>
        
        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-applicationName">applicationName</InputLabel>
          <Input id="select-applicationName" value={applicationName} onChange={(e) => handleApplicationName(e.target.value)} placeholder="applicationName" />
        </FormControl>
        
        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-processName">processName</InputLabel>
          <Input id="select-processName" value={processName} onChange={(e) => handleProcessName(e.target.value)} placeholder="processName" />
        </FormControl>

        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-processId">processId</InputLabel>
          <Input id="select-processId" value={processId} onChange={(e) => handleProcessId(e.target.value)} placeholder="processId" />
        </FormControl>

        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-dateTime">dateTime</InputLabel>
          <Input id="select-dateTime" value={dateTime} onChange={(e) => handleDateTime(e.target.value)} placeholder="dateTime" />
        </FormControl>

        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-extra">processName</InputLabel>
          <Input id="select-extra" value={extra} onChange={(e) => handleExtra(e.target.value)} placeholder="extra" />
        </FormControl>

        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-authToken">authToken</InputLabel>
          <Input id="select-authToken" value={authToken} onChange={(e) => handleAuthToken(e.target.value)} placeholder="authToken" />
        </FormControl>

        <FormControl style={{ width:'100%', margin: '1em 0' }} >
          <InputLabel id="select-url">url</InputLabel>
          <Input id="select-url" value={url} onChange={(e) => handleUrl(e.target.value)} placeholder="url" />
        </FormControl>
      </Card>
    );
  }

  const TestSuite = () => {
    const requestNumber = testsCompleted(tests);

    const Header = () => {
      return (
        <div style={{ display:'flex', alignItems: 'center' }}>
          <Button
            variant="contained"
            disabled={testsRunning}
            onClick={performAllTests}
          >
            Go
          </Button>
          <div style={{ display: 'flex', justifyContent: 'flex-end', width: '100%' }}>
            <Typography variant="subtitle1">
              {requestNumber}/{tests.length} Requests
            </Typography>
          </div>
        </div>
      );
    };

    return (
      <Card style={{ backgroundColor: '#f5f5f5' }}>
        <Typography variant="h1">
          RUN SET OF REQUESTS
        </Typography>
        <Divider />
        <Header />
  
        {tests && tests.length > 0 ? (
          <>
            {tests.map((test, index) => (
              <Test
                key={JSON.stringify(test.testData)}
                index={index}
                status={test.status}
                result={test.result}
                resultObj={test.resultObj}
                testData={test.testData}
              />
            ))}
          </>
        ) : (
          'No tests available'
        )}
      </Card>
    );
  }

  const Test = ({ index, status, result, resultObj, testData }) => {
    const [panel, setPanel] = useState(0);
    const [isOpen,setIsOpen] = useState(false);
    const {
      message,
      logLevel,
      applicationName,
      authToken,
      processName,
      processId,
      dateTime,
      url,
      extra
    } = testData;

    const testTheme = (theme) => ({
      ...theme,
      overrides: {
        ...theme.overrides,
        MuiCard: {
          root: {
            margin: '1em 0',
            padding: '0'
          }
        }
      },
    });

    const renderStatus = () => {
      switch (status) {
        case 'done':
          return result === 200 ? <><DoneIcon />&nbsp;[{result}]</> : <><ClearIcon />&nbsp;[{result}]</>;
        case 'waiting':
          if (testsRunning) {
            return 'Waiting to run...';
          }
          break;
        default:
          if (testsRunning) {
            return <>&nbsp;<CircularProgress size={'1em'} /></>;
          }
          return undefined;
      }
    };

    return (
      <ThemeProvider theme={testTheme}>
        <Card
          onClick={!isOpen ? () => setIsOpen(true) : undefined}
          style={{ cursor: isOpen? 'default' : 'pointer', backgroundColor: getTestColor(result) }}
        >
          <div style={{padding: '0.5em'}}>
            <div style={{display:'inline-block'}}>
              Test {index + 1}
            </div>
            <div style={{display:'inline-block', float:'right'}}>
              <div style={{display: 'flex', alignItems: 'center', cursor: 'pointer' }} onClick={() => setIsOpen(false)}>
                &nbsp;
                {isOpen ? <ArrowUpIcon /> : <ArrowDownIcon />}
              </div>
            </div>
            <div style={{display:'inline-block', float:'right'}}>
              <div style={{display: 'flex', alignItems: 'center' }}>
                {renderStatus()}
              </div>
            </div>

            {isOpen ? (
              <Grid container direction="column" style={{ marginTop: '1em' }}>
                <Grid item>
                <Typography variant="subtitle2" style={{ marginBottom: '0.5em' }}>Test Results</Typography>
                  {status === 'done' ? (
                    <>
                      <table>
                        <tbody>
                          {isNaN(result) ? (
                            <>
                              <tr>
                                <td>
                                  <Chip label="Error" />
                                </td>
                                <td>
                                  {resultObj.toString()}
                                </td>
                              </tr>
                            </>
                          ) : (
                            <>
                              <tr>
                                <td>
                                  <Chip label="Status Code" />
                                </td>
                                <td>
                                  {resultObj.status}
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <Chip label="Status Text" />
                                </td>
                                <td>
                                  {resultObj.statusText}
                                </td>
                              </tr>
                            </>
                          )}
                        </tbody>
                      </table>
                    </>
                  ) : 'No results to display'}
                </Grid>
                <Grid item>
                  <Typography variant="subtitle2" style={{ marginBottom: '0.5em' }}>Details</Typography>
                  <table>
                    <tbody>
                      <tr>
                        <td>
                          <Chip label="message" />
                        </td>
                        <td>
                          {message}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="dateTime" />
                        </td>
                        <td>
                          {dateTime.toString()}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="applicationName" />
                        </td>
                        <td>
                          {applicationName}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="processName" />
                        </td>
                        <td>
                          {processName}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="processId" />
                        </td>
                        <td>
                          {processId}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="logLevel" />
                        </td>
                        <td>
                          {logLevel}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="extra" />
                        </td>
                        <td>
                          {JSON.stringify(extra)}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="authToken" />
                        </td>
                        <td>
                          {authToken}
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <Chip label="url" />
                        </td>
                        <td>
                          {url}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </Grid>
              </Grid>
            ) : undefined}
          </div>
        </Card>
      </ThemeProvider>
    );
  };

  return (
    <div>
      <ThemeProvider theme={baseTheme}>
        <CssBaseline />
        <ThemeProvider theme={appTheme}>
          <Grid container>
            <Grid item>
              <TestSuite />
            </Grid>
            <Grid item>
              <CustomRequest />
            </Grid>
          </Grid>
        </ThemeProvider>
      </ThemeProvider>
    </div>
  );
}
