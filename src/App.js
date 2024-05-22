import './App.css';
import Home from './components/Home';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


console.log("Hi")
function App() {
  return (
    <div className='container'>
      <Router>
        <Routes>
          <Route exact path="/home" element={<Home />}></Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
