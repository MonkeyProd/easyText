import React from "react";
import styles from "./style.module.css";

export const Footer = () => {
    return (
        <footer className={styles.Footer}>
            <div className={styles.Left}>
                <div className={styles.InfoLeft}>
                    <div className={styles.InfoTitle}>easyText</div>
                    <div className={styles.InfoBody}>
                        © All Rights Reserved.
                    </div>
                </div>
            </div>
            <div className={styles.Right}>
                <div className={styles.InfoRight}>
                    <div className={styles.InfoTitle}>Связаться с нами</div>
                    <div className={styles.InfoBody}>
                        easytext@gmail.com
                        <br />
                        89853400803
                    </div>
                </div>
                <div className={styles.InfoRight}>
                    <div className={styles.InfoTitle}>Адрес</div>
                    <div className={styles.InfoBody}>
                        г. Москва, ул. Верхняя
                        <br /> Масловка, д. 15
                    </div>
                </div>
            </div>
        </footer>
    );
};
