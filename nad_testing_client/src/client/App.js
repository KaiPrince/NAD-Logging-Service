import React, { useEffect, useState } from 'react';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export default function () {
  const [results, setResults] = useState(null);

  const performTest = async (params) => {
    console.log(`running test ${params}`);

    // await sleep(3000)
    if (params === 'realbaderror') throw new Error()

    try {
      const result = await fetch('http://localhost:5000/log', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: 'message',
          logLevel: '1',
          applicationId: '0x01',
          authToken: 'asdfsagtgrtg',
          dateTime: new Date('2020-01-01'),
        })
      });

      return params;
    } catch (exception) {
      return `error during ${params}`;
    }
  };

  const performAllTests = () => {
    Promise.all([
      'test1',
      'test2',
      // 'realbaderror'
    ].map(performTest))
      .then((results) => {
        setResults(results);
        console.log(results);
      })
      .catch((err) => {
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