import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingPage } from "./pages/landing";
import { Menu } from "./components/Menu";
import { Footer } from "./components/Footer";
import { AboutUs } from "./pages/aboutUs";
import { login } from "./api";
import { useState } from "react";
import { useCookies } from "react-cookie"
import Modal from 'react-modal';
import axios from "axios"

const API_URL = "http://localhost:8080"

function App() {

    const [cookies, setCookie] = useCookies(['user', 'token'])
    const [successLogin, setSuccessLogin] = useState(true);
    const [successRegister, setSuccessRegister] = useState(true);
    const [authError, setAuthError] = useState('');
    function login(user, password) {
        axios.post(`${API_URL}/login`, { user, password })
            .then((data) => {
                const expires = new Date(data.data.expire)
                console.log(expires)
                setCookie('token', data.data.token, { path: "/", expires });
                setCookie('user', user, { path: "/", expires });
                setSuccessLogin(true);
                closeAuth();
            })
            .catch((e) => {
                setAuthError(e.response.data)
                setSuccessLogin(false)
            })
    }

    function register(user, password) {
        axios.post(`${API_URL}/register`, { user, password })
            .then((data) => {
                closeAuth();
                setSuccessRegister(true)
            })
            .catch((e) => {
                setAuthError(e.response.data)
                setSuccessRegister(false)
            })
    }

    const [authModalOpen, setAuthModalOpen] = useState(false);
    const [isRegisterModal, setIsRegisterModal] = useState(false);

    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');

    Modal.setAppElement('#root');

    function openAuth() {
        setAuthModalOpen(true);
    }

    function closeAuth() {
        setAuthModalOpen(false);
        setIsRegisterModal(false);
    }

    return (
        <div className="App" >
            <BrowserRouter>
                <Menu openAuthCallback={openAuth} />
                <Modal
                    isOpen={authModalOpen}
                    onRequestClose={closeAuth}
                    className="AuthModal"
                    overlayClassName="OverlayAuthModal"
                    bodyOpenClassName="AuthModalOpen"
                >
                    {!isRegisterModal ?
                        <>
                            <h2>ВХОД</h2>
                            {!successLogin && <span style={{ color: "red" }}>Неправильный логин или пароль.<br />{authError}</span>}
                            <div className="AuthInputContainer">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 2C11.0111 2 10.0444 2.29324 9.22215 2.84265C8.3999 3.39206 7.75904 4.17295 7.3806 5.08658C7.00216 6.00021 6.90315 7.00555 7.09607 7.97545C7.289 8.94536 7.7652 9.83627 8.46447 10.5355C9.16373 11.2348 10.0546 11.711 11.0245 11.9039C11.9945 12.0969 12.9998 11.9978 13.9134 11.6194C14.827 11.241 15.6079 10.6001 16.1573 9.77785C16.7068 8.95561 17 7.98891 17 7C17 5.67392 16.4732 4.40215 15.5355 3.46447C14.5979 2.52678 13.3261 2 12 2ZM12 10C11.4067 10 10.8266 9.82405 10.3333 9.49441C9.83994 9.16476 9.45542 8.69623 9.22836 8.14805C9.0013 7.59987 8.94189 6.99667 9.05764 6.41473C9.1734 5.83279 9.45912 5.29824 9.87868 4.87868C10.2982 4.45912 10.8328 4.1734 11.4147 4.05764C11.9967 3.94189 12.5999 4.0013 13.1481 4.22836C13.6962 4.45542 14.1648 4.83994 14.4944 5.33329C14.8241 5.82664 15 6.40666 15 7C15 7.79565 14.6839 8.55871 14.1213 9.12132C13.5587 9.68393 12.7956 10 12 10ZM21 21V20C21 18.1435 20.2625 16.363 18.9497 15.0503C17.637 13.7375 15.8565 13 14 13H10C8.14348 13 6.36301 13.7375 5.05025 15.0503C3.7375 16.363 3 18.1435 3 20V21H5V20C5 18.6739 5.52678 17.4021 6.46447 16.4645C7.40215 15.5268 8.67392 15 10 15H14C15.3261 15 16.5979 15.5268 17.5355 16.4645C18.4732 17.4021 19 18.6739 19 20V21H21Z" fill="white" />
                                </svg>
                                <input placeholder="ВВЕДИТЕ ЛОГИН" className="AuthInput" onChange={(e) => setUser(e.target.value)} />
                            </div>

                            <div className="AuthInputContainer">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <g clip-path="url(#clip0_11_154)">
                                        <path d="M12 2C9.243 2 7 4.243 7 7V10H6C4.897 10 4 10.897 4 12V20C4 21.103 4.897 22 6 22H18C19.103 22 20 21.103 20 20V12C20 10.897 19.103 10 18 10H17V7C17 4.243 14.757 2 12 2ZM18 12L18.002 20H6V12H18ZM9 10V7C9 5.346 10.346 4 12 4C13.654 4 15 5.346 15 7V10H9Z" fill="white" />
                                        <path d="M4 -3C3.01109 -3 2.04439 -2.70676 1.22215 -2.15735C0.399903 -1.60794 -0.24096 -0.827048 -0.619398 0.0865827C-0.997836 1.00021 -1.09685 2.00555 -0.903926 2.97545C-0.711 3.94536 -0.234797 4.83627 0.464466 5.53553C1.16373 6.2348 2.05464 6.711 3.02455 6.90393C3.99445 7.09685 4.99979 6.99784 5.91342 6.6194C6.82705 6.24096 7.60794 5.6001 8.15735 4.77785C8.70676 3.95561 9 2.98891 9 2C9 0.673918 8.47322 -0.597852 7.53553 -1.53553C6.59785 -2.47322 5.32608 -3 4 -3ZM4 5C3.40666 5 2.82664 4.82405 2.33329 4.49441C1.83994 4.16476 1.45542 3.69623 1.22836 3.14805C1.0013 2.59987 0.941888 1.99667 1.05764 1.41473C1.1734 0.832786 1.45912 0.298237 1.87868 -0.12132C2.29824 -0.540878 2.83279 -0.8266 3.41473 -0.942356C3.99667 -1.05811 4.59987 -0.998701 5.14805 -0.771638C5.69623 -0.544575 6.16476 -0.160058 6.49441 0.333289C6.82405 0.826637 7 1.40666 7 2C7 2.79565 6.68393 3.55871 6.12132 4.12132C5.55871 4.68393 4.79565 5 4 5ZM13 16V15C13 13.1435 12.2625 11.363 10.9497 10.0503C9.63699 8.7375 7.85652 8 6 8H2C0.143485 8 -1.63699 8.7375 -2.94975 10.0503C-4.2625 11.363 -5 13.1435 -5 15V16H-3V15C-3 13.6739 -2.47322 12.4021 -1.53553 11.4645C-0.597852 10.5268 0.673918 10 2 10H6C7.32608 10 8.59785 10.5268 9.53553 11.4645C10.4732 12.4021 11 13.6739 11 15V16H13Z" fill="black" />
                                    </g>
                                    <defs>
                                        <clipPath id="clip0_11_154">
                                            <rect width="24" height="24" fill="white" />
                                        </clipPath>
                                    </defs>
                                </svg>
                                <input placeholder="ВВЕДИТЕ ПАРОЛЬ" className="AuthInput" type="password" onChange={(e) => setPassword(e.target.value)} />
                            </div>
                            <span className="AuthToRegister" onClick={() => setIsRegisterModal(true)}>У меня еще нет аккаунта</span>
                            <button className="AuthButton" onClick={() => login(user, password)}>
                                ВОЙТИ
                            </button>
                        </> : <>
                            <h2>РЕГИСТРАЦИЯ</h2>
                            {!successRegister && <span style={{ color: "red" }}>Не удалось зарегистрироваться<br />{authError}</span>}
                            <div className="AuthInputContainer">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 2C11.0111 2 10.0444 2.29324 9.22215 2.84265C8.3999 3.39206 7.75904 4.17295 7.3806 5.08658C7.00216 6.00021 6.90315 7.00555 7.09607 7.97545C7.289 8.94536 7.7652 9.83627 8.46447 10.5355C9.16373 11.2348 10.0546 11.711 11.0245 11.9039C11.9945 12.0969 12.9998 11.9978 13.9134 11.6194C14.827 11.241 15.6079 10.6001 16.1573 9.77785C16.7068 8.95561 17 7.98891 17 7C17 5.67392 16.4732 4.40215 15.5355 3.46447C14.5979 2.52678 13.3261 2 12 2ZM12 10C11.4067 10 10.8266 9.82405 10.3333 9.49441C9.83994 9.16476 9.45542 8.69623 9.22836 8.14805C9.0013 7.59987 8.94189 6.99667 9.05764 6.41473C9.1734 5.83279 9.45912 5.29824 9.87868 4.87868C10.2982 4.45912 10.8328 4.1734 11.4147 4.05764C11.9967 3.94189 12.5999 4.0013 13.1481 4.22836C13.6962 4.45542 14.1648 4.83994 14.4944 5.33329C14.8241 5.82664 15 6.40666 15 7C15 7.79565 14.6839 8.55871 14.1213 9.12132C13.5587 9.68393 12.7956 10 12 10ZM21 21V20C21 18.1435 20.2625 16.363 18.9497 15.0503C17.637 13.7375 15.8565 13 14 13H10C8.14348 13 6.36301 13.7375 5.05025 15.0503C3.7375 16.363 3 18.1435 3 20V21H5V20C5 18.6739 5.52678 17.4021 6.46447 16.4645C7.40215 15.5268 8.67392 15 10 15H14C15.3261 15 16.5979 15.5268 17.5355 16.4645C18.4732 17.4021 19 18.6739 19 20V21H21Z" fill="white" />
                                </svg>
                                <input placeholder="ВВЕДИТЕ ЛОГИН" className="AuthInput" onChange={(e) => setUser(e.target.value)} />
                            </div>

                            <div className="AuthInputContainer">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <g clip-path="url(#clip0_11_154)">
                                        <path d="M12 2C9.243 2 7 4.243 7 7V10H6C4.897 10 4 10.897 4 12V20C4 21.103 4.897 22 6 22H18C19.103 22 20 21.103 20 20V12C20 10.897 19.103 10 18 10H17V7C17 4.243 14.757 2 12 2ZM18 12L18.002 20H6V12H18ZM9 10V7C9 5.346 10.346 4 12 4C13.654 4 15 5.346 15 7V10H9Z" fill="white" />
                                        <path d="M4 -3C3.01109 -3 2.04439 -2.70676 1.22215 -2.15735C0.399903 -1.60794 -0.24096 -0.827048 -0.619398 0.0865827C-0.997836 1.00021 -1.09685 2.00555 -0.903926 2.97545C-0.711 3.94536 -0.234797 4.83627 0.464466 5.53553C1.16373 6.2348 2.05464 6.711 3.02455 6.90393C3.99445 7.09685 4.99979 6.99784 5.91342 6.6194C6.82705 6.24096 7.60794 5.6001 8.15735 4.77785C8.70676 3.95561 9 2.98891 9 2C9 0.673918 8.47322 -0.597852 7.53553 -1.53553C6.59785 -2.47322 5.32608 -3 4 -3ZM4 5C3.40666 5 2.82664 4.82405 2.33329 4.49441C1.83994 4.16476 1.45542 3.69623 1.22836 3.14805C1.0013 2.59987 0.941888 1.99667 1.05764 1.41473C1.1734 0.832786 1.45912 0.298237 1.87868 -0.12132C2.29824 -0.540878 2.83279 -0.8266 3.41473 -0.942356C3.99667 -1.05811 4.59987 -0.998701 5.14805 -0.771638C5.69623 -0.544575 6.16476 -0.160058 6.49441 0.333289C6.82405 0.826637 7 1.40666 7 2C7 2.79565 6.68393 3.55871 6.12132 4.12132C5.55871 4.68393 4.79565 5 4 5ZM13 16V15C13 13.1435 12.2625 11.363 10.9497 10.0503C9.63699 8.7375 7.85652 8 6 8H2C0.143485 8 -1.63699 8.7375 -2.94975 10.0503C-4.2625 11.363 -5 13.1435 -5 15V16H-3V15C-3 13.6739 -2.47322 12.4021 -1.53553 11.4645C-0.597852 10.5268 0.673918 10 2 10H6C7.32608 10 8.59785 10.5268 9.53553 11.4645C10.4732 12.4021 11 13.6739 11 15V16H13Z" fill="black" />
                                    </g>
                                    <defs>
                                        <clipPath id="clip0_11_154">
                                            <rect width="24" height="24" fill="white" />
                                        </clipPath>
                                    </defs>
                                </svg>
                                <input placeholder="ВВЕДИТЕ ПАРОЛЬ" className="AuthInput" type="password" onChange={(e) => setPassword(e.target.value)} />
                            </div>
                            {password !== password2 && <span style={{ color: "red" }}>Пароли не совпадают</span>}
                            <div className="AuthInputContainer">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <g clip-path="url(#clip0_11_154)">
                                        <path d="M12 2C9.243 2 7 4.243 7 7V10H6C4.897 10 4 10.897 4 12V20C4 21.103 4.897 22 6 22H18C19.103 22 20 21.103 20 20V12C20 10.897 19.103 10 18 10H17V7C17 4.243 14.757 2 12 2ZM18 12L18.002 20H6V12H18ZM9 10V7C9 5.346 10.346 4 12 4C13.654 4 15 5.346 15 7V10H9Z" fill="white" />
                                        <path d="M4 -3C3.01109 -3 2.04439 -2.70676 1.22215 -2.15735C0.399903 -1.60794 -0.24096 -0.827048 -0.619398 0.0865827C-0.997836 1.00021 -1.09685 2.00555 -0.903926 2.97545C-0.711 3.94536 -0.234797 4.83627 0.464466 5.53553C1.16373 6.2348 2.05464 6.711 3.02455 6.90393C3.99445 7.09685 4.99979 6.99784 5.91342 6.6194C6.82705 6.24096 7.60794 5.6001 8.15735 4.77785C8.70676 3.95561 9 2.98891 9 2C9 0.673918 8.47322 -0.597852 7.53553 -1.53553C6.59785 -2.47322 5.32608 -3 4 -3ZM4 5C3.40666 5 2.82664 4.82405 2.33329 4.49441C1.83994 4.16476 1.45542 3.69623 1.22836 3.14805C1.0013 2.59987 0.941888 1.99667 1.05764 1.41473C1.1734 0.832786 1.45912 0.298237 1.87868 -0.12132C2.29824 -0.540878 2.83279 -0.8266 3.41473 -0.942356C3.99667 -1.05811 4.59987 -0.998701 5.14805 -0.771638C5.69623 -0.544575 6.16476 -0.160058 6.49441 0.333289C6.82405 0.826637 7 1.40666 7 2C7 2.79565 6.68393 3.55871 6.12132 4.12132C5.55871 4.68393 4.79565 5 4 5ZM13 16V15C13 13.1435 12.2625 11.363 10.9497 10.0503C9.63699 8.7375 7.85652 8 6 8H2C0.143485 8 -1.63699 8.7375 -2.94975 10.0503C-4.2625 11.363 -5 13.1435 -5 15V16H-3V15C-3 13.6739 -2.47322 12.4021 -1.53553 11.4645C-0.597852 10.5268 0.673918 10 2 10H6C7.32608 10 8.59785 10.5268 9.53553 11.4645C10.4732 12.4021 11 13.6739 11 15V16H13Z" fill="black" />
                                    </g>
                                    <defs>
                                        <clipPath id="clip0_11_154">
                                            <rect width="24" height="24" fill="white" />
                                        </clipPath>
                                    </defs>
                                </svg>
                                <input placeholder="ПОДТВЕРДИТЕ ПАРОЛЬ" className="AuthInput" type="password" onChange={(e) => setPassword2(e.target.value)} />
                            </div>
                            <button disabled={password !== password2} className="AuthButton" onClick={() => register(user, password)}>
                                ПРОДОЛЖИТЬ
                            </button>
                        </>}
                </Modal>
                <div className="AppContainer">
                    <div className="AppPage">
                        <Routes>
                            <Route path="" element={<LandingPage />} />
                            <Route path="/about" element={<AboutUs />} />

                        </Routes>
                    </div>
                </div>
                <Footer />
            </BrowserRouter>
        </div>
    );
}

export default App;
