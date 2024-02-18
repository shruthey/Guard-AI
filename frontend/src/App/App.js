import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ButtonForm from "../ButtonForm/ButtonForm";
import InputPage from "../InputPage/InputPage";
import "./App.scss";

function App() {
  return (
    <Router>
      <header className="App-header">
        <h1 className="vertical-text">Shield Pro</h1>
      </header>
      <Routes>
        <Route path="/" element={<ButtonForm />} />
        <Route path="/input" element={<InputPage />} />
        <Route path="/input-page" element={<InputPage />} />
        <Route path="/button" element={<ButtonForm />} />
      </Routes>
    </Router>
  );
}

export default App;
