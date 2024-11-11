import { useState } from "react";
import axios from "axios";
import "./App.css"; // Import the CSS for styling

function App() {
  const [loadingButton, setLoadingButton] = useState(null); // Track which button is loading
  const [trackingCompleted, setTrackingCompleted] = useState(false); // State to check if tracking is completed
  const [flashMessage, setFlashMessage] = useState(""); // Flash message for the outputs
  const [showDropdown, setShowDropdown] = useState(null); // Track which button's dropdown is shown

  // Adjusted button positions based on the provided image
  const buttonPositions = [
    { id: "dinosaur", label: "Dinosaur Dungeon", style: { top: "2%", left: "72%" } },
    { id: "iceCream", label: "Ice Cream", style: { top: "56.3%", left: "45.3%" } },
    { id: "paintPalette", label: "Paint Palette", style: { top: "47%", left: "77%" } },
    { id: "volcano", label: "Volcano Maze", style: { top: "19%", left: "37%" } },
  ];

  const displayFlashMessage = (message) => {
    setFlashMessage(message);
    setTimeout(() => setFlashMessage(""), 5000); // Automatically clear flash message after 5 seconds
  };

  const handleRunTracking = async (buttonId) => {
    setLoadingButton(buttonId); // Set the loading button
    try {
      const result = await axios.post("http://127.0.0.1:5000/run-tracking", {
        tracking_id: buttonId,
      });
      displayFlashMessage(result.data.message);
      setTrackingCompleted(true); // Set tracking as completed after success
    } catch (error) {
      displayFlashMessage("Error running tracking.");
    } finally {
      setLoadingButton(null); // Reset loading state
      setShowDropdown(null);
    }
  };

  const handlePredictWaitTime = async (buttonId) => {
    setLoadingButton(buttonId); // Set the loading button
    try {
      const result = await axios.get("http://127.0.0.1:5000/predict-wait-time");
      displayFlashMessage(result.data.worst_case_wait_time || result.data.message);
    } catch (e) {
      displayFlashMessage("Error fetching wait time.");
    } finally {
      setLoadingButton(null); // Reset loading state
      setShowDropdown(null);
    }
  };

  const buttons = buttonPositions.map((button) => (
    <div key={button.id} style={button.style} className="map-button-container">
      <button
        className="map-button"
        onClick={() => setShowDropdown(showDropdown === button.id ? null : button.id)}
      >
        {button.label}
      </button>

      {showDropdown === button.id && (
        <div className="dropdown-menu">
          <button
            onClick={() => handleRunTracking(button.id)}
            disabled={loadingButton !== null && loadingButton !== button.id}
            className="dropdown-button"
          >
            {loadingButton === button.id ? <div className="button-spinner"></div> : "Run Tracking"}
          </button>
          <button
            onClick={() => handlePredictWaitTime(button.id)}
            disabled={loadingButton !== null || !trackingCompleted}
            className="dropdown-button"
          >
            {loadingButton === button.id ? <div className="button-spinner"></div> : "Predict Wait Time"}
          </button>
        </div>
      )}
    </div>
  ));

  return (
    <div className="background-container">
      <h1 className="title animate-title">DinoPark Queue Management</h1>
      <div className="button-container">{buttons}</div>

      {/* Flash message for displaying outputs */}
      {flashMessage && (
        <div className="flash-message">
          <span>{flashMessage}</span>
          <button onClick={() => setFlashMessage("")} className="close-button">
            ×
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
