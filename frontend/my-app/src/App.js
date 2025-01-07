
import React from "react";
import "./App.css";

function App() {
    return (
        <div className="app">
            <div className="container">
                <h1>Our Product</h1>

                <div className="chart-section">
                    <div className="chart">
                        <div className="chart-header">
                            <div className="green-check">✔</div>
                        </div>
                        <div className="chart-content">
                            <div className="chart-bars">
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "30%" }}></div>
                                    <span>15</span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "40%" }}></div>
                                    <span>17</span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "50%" }}></div>
                                    <span>21</span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "60%" }}></div>
                                    <span>30</span>
                                </div>
                                <div className="bar">
                                    <div className="bar-value" style={{ height: "70%" }}></div>
                                    <span>42</span>
                                </div>
                            </div>
                            <div className="values-labels">
                                <div className="value-item">
                                    <p>Actual values</p>
                                    <span>---</span>
                                </div>
                                <div className="value-item">
                                    <p>Optimal values</p>
                                    <span>---</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="text-section">
                    <h2>Lorem Ipsum</h2>
                    <p>
                        Lorem Ipsum is simply dummy text of the printing and typesetting
                        industry. Lorem Ipsum has been the industry's standard dummy text
                        ever since the 1500s, when an unknown printer took a galley of type
                        and scrambled it to make a type specimen book. It has survived not
                        only five centuries, but also the leap into electronic typesetting,
                        remaining essentially unchanged. It was popularised in the 1960s
                        with the release of Letraset sheets containing Lorem Ipsum
                        passages, and more recently with desktop publishing software like
                        Aldus PageMaker including versions of Lorem Ipsum.
                    </p>
                    <p className="description">Any necessary description</p>
                </div>

                <div className="ai-analysis">
                    <h2>AI Powered Analysis</h2>
                    <p>Start a new analysis for this patient if anything seems off.</p>
                    <button className="start-analysis">Start Analysis</button>
                    <div className="analysis-progress">
                        <div className="status started">Analysis Started</div>
                        <div className="status in-progress">Analysis In Progress</div>
                        <div className="status done">Analysis Done</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
