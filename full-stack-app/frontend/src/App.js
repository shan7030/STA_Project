import { useState, useEffect } from 'react';
import Select from 'react-select';
import './App.css';


function App() {

  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [results, setResults] = useState([]);
  const [results2, setResults2] = useState([]);


  const customStyles = {
    control: (provided) => ({
      ...provided,
      width: 700, // Adjust the width as needed
      fontSize: '14px',
    }),
    singleValue: (provided) => ({
      ...provided,
      color: 'black', // Set text color to black
      fontSize: '14px',
    }),
    option: (provided) => ({
      ...provided,
      color: 'black', // Set options text color to black
      fontSize: '14px',
    }),
  };


  useEffect(() => {
    // Fetch data from API
    fetch('https://sta220-backend.onrender.com/all-courses/')
      .then(response => response.json())
      .then(data => {
        // Data received, set options
        const optionsValues = [];

        for (let i = 0; i < data.length; i++) {
          optionsValues.push({
            value: data[i]['course_id'],
            label: data[i]['course_title']
          })
        }

        setOptions(optionsValues);

      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []); // Run once on component mount


  const handleButtonClick = () => {
    // Handle button click action here
    console.log('Button clicked', selectedOption);

    if (selectedOption) {
      // Access the selected option value
      const courseTitle = selectedOption.label;
      console.log('Selected course title:', courseTitle);

      // Call the endpoint with the selected course title
      fetch(`https://sta220-backend.onrender.com/results/?course_title=${encodeURIComponent(courseTitle)}&id=${1}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          // Handle the response data here
          console.log('API response:', data);
          setResults(data);
        })
        .catch(error => {
          setResults([]);
          console.error('Error fetching data:', error);
        });

      
    } else {
      setResults([]);
      console.log('No option selected');
    }

  };

  const handleOptionChange = (selectedOption) => {
    setSelectedOption(selectedOption);
  };


  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={{ flex: '1', height: '10%' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', width: '100%' }}>
          <h2>Course Recommender</h2>
        </div>
      </div>

      <div style={{ flex: '1', height: '10%' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 'inherit', width: '100%' }}>

          <Select options={options} styles={customStyles} onChange={handleOptionChange} />
          <button className="App-button" onClick={handleButtonClick}>Recommend Courses</button>
        </div>
      </div>

      <div style={{ flex: '1', height: '80%' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 'inherit', width: '100%' }}>
          {results.map((result, index) => (
            <a key={index} href={result.course_url} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className='card-link'>
                {result.course_title} {/* Assuming 'name' is a field in the result */}
              </div>
            </a>
          ))}
        </div>
      </div>

      <div style={{  height: '200px' }}> </div>

    </div>
  );
}

export default App;
