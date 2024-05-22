import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import axios from 'axios';

const MultiSelectDropdown = () => {
  const [options, setOptions] = useState([]);
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [predictions, setPredictions] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/symptoms')
      .then(response => {
        const symptomOptions = response.data.map(symptom => ({
          value: symptom,
          label: symptom.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
        }));
        setOptions(symptomOptions);
      })
      .catch(error => {
        console.error('There was an error fetching the symptoms!', error);
      });
  }, []);

  const handleChange = (selected) => {
    setSelectedOptions(selected);
  };

  const handlePredict = () => {
    const selectedValues = selectedOptions.map(option => option.value);
    axios.post('http://localhost:5000/predict', {
      selectedSymptoms: selectedValues
    })
    .then(response => {
      setPredictions(response.data);
    })
    .catch(error => {
      console.error('There was an error!', error);
    });
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Select Your Symptoms</h2>
      <Select
        isMulti
        value={selectedOptions}
        onChange={handleChange}
        options={options}
      />
      <button className='btn btn-primary' style={{ marginTop: '20px' }} onClick={handlePredict}>Predict</button>
      {predictions && (
        <div>
          <h3>Predictions:</h3>
          <p><strong>Random Forest:</strong> {predictions.rf_model_prediction}</p>
          <p><strong>Naive Bayes:</strong> {predictions.naive_bayes_prediction}</p>
          <p><strong>SVM:</strong> {predictions.svm_model_prediction}</p>
          <p><strong>Final Prediction:</strong> {predictions.final_prediction}</p>
        </div>
      )}
    </div>
  );
};

export default MultiSelectDropdown;
