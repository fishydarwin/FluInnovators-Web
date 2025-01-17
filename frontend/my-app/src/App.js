
import React, { useState } from "react";
import "./App.css";

function App() {
    const [vaccineResponse, setVaccineResponse] = useState(null);
    const [vaccineError, setVaccineError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState(''); 

    const makeVaccineRequest = async (id, requestBody) => {
        setLoading(true);
        setStatus('started');
        try {
            const response = await fetch(`http://localhost:8080/vaccine-response/add?patientId=${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.status} ${response.statusText}`);
            }
            const newVaccineResponse = await response.json();
            let newId = newVaccineResponse.id;

            const response2 = await fetch(`http://localhost:8080/vaccine-response/compute/${newId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody), 
            });

            if (!response2.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response2.json();
            setVaccineResponse(data);
            if (data.complete) {
                setStatus('done');
            } else {
                setStatus('in-progress');
                pollForResult(newId); 
            }
            setVaccineError(null);
        } catch (err) {
            setVaccineError(err.message);
            setVaccineResponse(null);
        } finally {
            setLoading(false);
        }
    };

    const pollForResult = (id) => {
        const interval = setInterval(async () => {
            try {
                const resultResponse = await fetch(`http://localhost:8080/vaccine-response/result/${id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (!resultResponse.ok) {
                    throw new Error(`Error fetching result: ${resultResponse.status} ${resultResponse.statusText}`);
                }

                const resultData = await resultResponse.json();
                setVaccineResponse(resultData);

                if (resultData.complete) {
                    setStatus("done");
                    clearInterval(interval); 
                }
            } catch (err) {
                console.error("Error during polling:", err.message);
            }
        }, 3000); 
    };

    return (
        <div className="app">
            <div className="container">
                <img
                    src="/fi_logo_colors.png"
                    alt="Our Product"
                    className="product-image"
                    style={{ width: "350px", height: "auto" }}
                />

                <div className="chart-section">
                    <div className="chart">
                        <div className="chart-header">
                            <div className="green-check">✔</div>
                        </div>
                        <div className="chart-content">
                            <div className="chart-bars">
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "30%" }}></div>
                                    <span></span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "40%" }}></div>
                                    <span></span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "50%" }}></div>
                                    <span></span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "60%" }}></div>
                                    <span></span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "70%" }}></div>
                                    <span></span>
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </div>

                <div className="text-section">
                    <h2>How It Works</h2>
                    <p>
                        This vaccine risk prediction app is designed to evaluate a patient's
                        health risk after receiving a specific vaccine. It leverages advanced AI models trained
                        on a database, which contains extensive data on blood sample markers,
                        genetic traits, and patient details like age and ethnicity. By analyzing this data,
                        the app predicts whether a vaccine poses a high or low risk to a patient.
                    </p>
                    <p>
                        The app sends the patient's information to an AI model for analysis,
                        associating it with a unique ID. If the AI has completed the analysis, it retrieves the result (high or low risk)
                        from the database.
                    </p>
                </div>

                <div className="ai-analysis">
                    <h2>AI Powered Analysis</h2>
                    <p>Start a new analysis for a patient if anything seems off. Enter the ID of the patient. </p>
                    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                        <input
                            type="number"
                            placeholder="Enter ID"
                            style={{ padding: "10px", fontSize: "16px", flex: "1" }}
                            onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                    const input = e.target;
                                    makeVaccineRequest(input.value, {});
                                }
                            }}
                        />
                        <button
                            className="start-analysis"
                            onClick={() => {
                                const input = document.querySelector('.ai-analysis input');
                                const requestBody = { "params": [
                                    {"d_geo_mean": document.getElementById("input1").value},
                                    {"geo_mean": document.getElementById("input2").value},
                                    {"CD85j_pos_CD4_pos_T_cells": document.getElementById("input3").value},
                                    {"CD161_pos_CD45RA_pos_Tregs": document.getElementById("input4").value},
                                    {"L50_IFNB": document.getElementById("input5").value}]
                                };
                                makeVaccineRequest(input.value, requestBody);
                            }}
                        >
                            Start Analysis
                        </button>

                    </div>
                    <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginTop: "10px" }}>
                        <input type="text" placeholder="Difference of geometric means" id="input1" style={{ padding: "10px", fontSize: "16px" }} />
                        <input type="text" placeholder="Geometric mean" id="input2" style={{ padding: "10px", fontSize: "16px" }} />
                        <input type="text" placeholder="CD85j+CD4+ T cells" id="input3" style={{ padding: "10px", fontSize: "16px" }} />
                        <input type="text" placeholder="CD161+CD45RA+ Tregs" id="input4" style={{ padding: "10px", fontSize: "16px" }} />
                        <input type="text" placeholder="L50_IFNB" id="input5" style={{ padding: "10px", fontSize: "16px" }} />
                    </div>
                    <div className="analysis-progress">
                        <div className={`status started ${status === 'started' ? 'scaled' : ''}`}>Analysis Started</div>
                        <div className={`status in-progress ${status === 'in-progress' ? 'scaled' : ''}`}>Analysis In Progress</div>
                        <div className={`status done ${status === 'done' ? 'scaled' : ''}`}>Analysis Done</div>
                    </div>
                    <h2>Vaccine Response</h2>
                    <div className="analysis-progress">
                        {loading && <p>Loading...</p>}
                        {vaccineError && <p style={{ color: "black" }}>Error: Either server is down or id does not exist.</p>}
                        {vaccineResponse && (
                            <div className="vaccine-response">
                                
                                {vaccineResponse.complete ? (
                                    <><p style={{ color: "red" }} >The AI model has successfully completed its analysis.</p><p style={{ color: "red" }}>
                                        {vaccineResponse.atRisk ?
                                            "The model predicts that the patient has a high likelihood of experiencing complications or adverse effects from the vaccine." :
                                            "The model predicts that the patient has a low likelihood of experiencing complications or adverse effects from the vaccine."}
                                    </p></>
                                ) : (
                                    <p>The analysis is not complete yet.</p>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
