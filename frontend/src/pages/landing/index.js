import React from "react";
import styles from "./style.module.css";

export const LandingPage = () => {
    return <div className={styles.LandingContainer}>
        <div className={styles.AboutUs}>
            <h1>easyText</h1>
            <div className={styles.AboutUsDescription}>
                Инновационное решение в мире искусственного интеллекта — наше уникальное программное обеспечение, спроектированное для распознавания текста с изображений
            </div>
        </div>
        <div className={styles.More}>
            ПОДРОБНЕЕ
            <svg width="26" height="24" viewBox="0 0 26 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.1892 9.293L12.7805 13.586L8.37176 9.293L6.91964 10.707L12.7805 16.414L18.6413 10.707L17.1892 9.293Z" fill="white" />
            </svg>
        </div>
        <div className={styles.OurBenefits}>
            <h1>
                Наши преимущества
            </h1>
            <div className={styles.Row}>
                <div className={styles.Card}>
                    <b>Быстрота и Эффективность</b> Наш ИИ обеспечивает мгновенное распознавание текста, сэкономив ваше время и повысив общую эффективность работы
                </div>
                <div className={styles.Card}>
                    <b>Многосторонний взгляд</b> Способность обрабатывать текст на изображениях различных форматов и качества, обеспечивая высокую точность даже в сложных условиях
                </div>
            </div>
            <div className={styles.Last}>
                <div className={styles.Card}>
                    <b>Безопасность</b> Система предоставляет высокий уровень безопасности при обработке изображений, обеспечивая конфиденциальность ваших данных.
                </div>
            </div>
        </div>
    </div >;
};
