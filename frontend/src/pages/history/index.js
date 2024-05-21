import React from 'react'
import styles from "./style.module.css";
import {useQuery} from "@tanstack/react-query"
import axios from "axios";
import { useCookies } from "react-cookie"
import {FidgetSpinner} from "react-loader-spinner"
import { Link } from 'react-router-dom';

const API_URL = "http://localhost:8080"

export const History = () => {
    const [cookies] = useCookies(['user', 'token'])
    if (!cookies['user'] || !cookies['token']){
        window.location.replace('/')
    }
    const {isLoading, isFetching, isPaused, isSuccess, isError, error, data, refetch} = useQuery({
        queryKey: ['history'],
        queryFn: () => axios.post(`${API_URL}/history`,{},{ withCredentials: true }).then((data)=>data.data),
        // enabled: false
    });
    return (
        <div className={styles.AboutContainer}>
            <h1 className={styles.Title}>
            История запросов
            </h1>
            {isFetching && <div><FidgetSpinner
                visible={true}
                height="80"
                width="80"
                backgroundColor={'white'}
                ariaLabel="fidget-spinner-loading"
                wrapperStyle={{}}
                wrapperClass="fidget-spinner-wrapper"
                /> <h3>Загрузка...</h3></div>}
            {(isSuccess && data.length===0) ? "История пуста" : <table className={styles.HistoryTable}>
                <thead>
                    <td>ID</td>
                    <td>Ссылка</td>
                    <td>Язык</td>
                    <td>Результат</td>
                    <td>Успех</td>
                    {/* <td>requester</td> */}
                    <td>Время</td>
                    <td>Скриншот</td>
                </thead>
                <tbody>
                    {
                        data?.map((elem,i)=>{
                            return <tr>
                            <td>{elem.id_}</td>
                            <td className={styles.HistoryLinkCol}><Link className={styles.HistoryLink} to={elem.url}>{elem.url}</Link></td>
                            <td>{elem.language}</td>
                            <td>{
                            elem.text_path?.length>0 ? 
                            <Link className={styles.HistoryLink} to={`${API_URL}/download/${elem.text_path}`} target="_blank"><u>Скачать текст</u></Link> :
                            "Текст недоступен"
                            }</td>
                            <td>{elem.success ? "✅": "❌"}</td>
                            {/* <td>{elem.requester}</td> */}
                            <td>{elem.timestamp}</td>
                            <td>{
                            elem.image_path?.length>0 ? 
                            <Link className={styles.HistoryLink} to={`${API_URL}/download/${elem.image_path}`} target="_blank"><u>Скачать скриншот</u></Link> :
                            "Скриншот недоступен"
                            }</td>
                            </tr>
                        })
                    }
                </tbody>
            </table>
            }
        </div>
    )
}
