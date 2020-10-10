import React, { useEffect, useState } from 'react';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

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
      test results...
      <br />
      {results ? (
        <>
          {results.map(result => <div>{result}</div>)}
        </>
      ) : 'no results'}
    </div>
  );
}
