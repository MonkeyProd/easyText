import React from "react";
import styles from "./style.module.css";
import { useCookies } from "react-cookie";
import { Link } from "react-router-dom";
import Cookies from "universal-cookie";

export const Menu = (props) => {
    const [cookies, asd] = useCookies();
    const cookies_storage = new Cookies();
    function logout() {
        cookies_storage.remove("token");
        cookies_storage.remove("user");
        window.location.reload();
    }
    return (
        <div className={styles.Menu}>
            <div className={styles.Label}>
                <Link className={styles.Label} to="/">
                    <svg
                        width="42"
                        height="42"
                        viewBox="0 0 42 42"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M15.75 27.65H19.25V34.5625H22.75V10.3688H26.25V34.5625H29.75V10.3688H35V6.91251H15.75C9.95925 6.91251 5.25 11.5629 5.25 17.2813C5.25 22.9996 9.95925 27.65 15.75 27.65ZM15.75 10.3688H19.25V24.1938H15.75C11.8895 24.1938 8.75 21.0935 8.75 17.2813C8.75 13.469 11.8895 10.3688 15.75 10.3688Z"
                            fill="white"
                        />
                    </svg>
                    <span className={styles.LabelText}>easyText</span>
                </Link>
            </div>
            <div className={styles.RightCorner}>
               
                <Link to="/about" className={styles.AboutUsLink}>
                    О нас
                </Link>
                {!cookies["user"] ? (
                    <>
                        {cookies["user"]}

                        <button
                            className={styles.LoginButton}
                            onClick={() => props.openAuthCallback()}
                        >
                            ВОЙТИ
                            <svg
                                width="24"
                                height="25"
                                viewBox="0 0 24 25"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M12 2.89999C11.0111 2.89999 10.0444 3.18957 9.22215 3.73211C8.3999 4.27465 7.75904 5.04578 7.3806 5.94799C7.00216 6.8502 6.90315 7.84297 7.09607 8.80075C7.289 9.75853 7.7652 10.6383 8.46447 11.3288C9.16373 12.0194 10.0546 12.4896 11.0245 12.6801C11.9945 12.8706 12.9998 12.7729 13.9134 12.3991C14.827 12.0254 15.6079 11.3926 16.1573 10.5806C16.7068 9.76865 17 8.81404 17 7.83749C17 6.52799 16.4732 5.27211 15.5355 4.34615C14.5979 3.42019 13.3261 2.89999 12 2.89999ZM12 10.8C11.4067 10.8 10.8266 10.6262 10.3333 10.3007C9.83994 9.9752 9.45542 9.51252 9.22836 8.97119C9.0013 8.42987 8.94189 7.83421 9.05764 7.25954C9.1734 6.68487 9.45912 6.157 9.87868 5.74269C10.2982 5.32838 10.8328 5.04623 11.4147 4.93192C11.9967 4.81761 12.5999 4.87628 13.1481 5.1005C13.6962 5.32473 14.1648 5.70444 14.4944 6.19162C14.8241 6.6788 15 7.25157 15 7.83749C15 8.6232 14.6839 9.37672 14.1213 9.9323C13.5587 10.4879 12.7956 10.8 12 10.8ZM21 21.6625V20.675C21 18.8417 20.2625 17.0835 18.9497 15.7871C17.637 14.4908 15.8565 13.7625 14 13.7625H10C8.14348 13.7625 6.36301 14.4908 5.05025 15.7871C3.7375 17.0835 3 18.8417 3 20.675V21.6625H5V20.675C5 19.3655 5.52678 18.1096 6.46447 17.1837C7.40215 16.2577 8.67392 15.7375 10 15.7375H14C15.3261 15.7375 16.5979 16.2577 17.5355 17.1837C18.4732 18.1096 19 19.3655 19 20.675V21.6625H21Z"
                                    fill="#2A302E"
                                />
                            </svg>
                        </button>
                    </>
                ) : (
                    <>
                     <Link to="/" className={styles.AboutUsLink}>
                    Попробовать easyText
                    </Link>
                        <Link to="/history" className={styles.AboutUsLink}>
                            История
                        </Link>
                        Пользователь: {cookies["user"]}
                        <span
                            className={styles.LogoutButton}
                            onClick={() => logout()}
                        >
                            Выйти
                        </span>
                    </>
                )}
            </div>
        </div>
    );
};
