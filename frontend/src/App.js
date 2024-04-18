import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingPage } from "./pages/landing";
import { Menu } from "./components/Menu";
import { Footer } from "./components/Footer";

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Menu />
                <div className="AppContainer">
                    <div className="AppPage">
                        <Routes>
                            <Route path="" element={<LandingPage />} />
                        </Routes>
                    </div>
                </div>
                <Footer />
            </BrowserRouter>
        </div>
    );
}

export default App;
