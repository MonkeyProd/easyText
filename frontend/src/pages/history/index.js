import React from 'react'
import styles from "./style.module.css";
import {useQuery} from "@tanstack/react-query"
import axios from "axios";
import { useCookies } from "react-cookie"
import { Link } from 'react-router-dom';

const API_URL = "http://localhost:8080"

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

export const History = () => {
    const [cookies, setCookie] = useCookies(['user', 'token'])
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
            {isSuccess && <table className={styles.HistoryTable}>
                <thead>
                    <td>ID</td>
                    <td>Ссылка</td>
                    <td>Язык</td>
                    <td>Результат</td>
                    <td>Успех</td>
                    {/* <td>requester</td> */}
                    <td>Время</td>
                </thead>
                <tbody>
                    {
                        data.map((elem,i)=>{
                            return <tr>
                            <td>{elem.id_}</td>
                            <td className={styles.HistoryLinkCol}><Link className={styles.HistoryLink} to={elem.url}>{elem.url}</Link></td>
                            <td>{elem.language}</td>
                            <td colSpan={elem.success? 1: 2}>{elem.success === 1 ?
                            <button onClick={()=>download('res.txt',elem.result)}><u>Скачать результат</u></button>
                            :"❌"}</td>
                            {elem.success ? <td>✅</td>: <></>}
                            {/* <td>{elem.requester}</td> */}
                            <td>{elem.timestamp}</td>
                            </tr>
                        })
                    }
                </tbody>
            </table>
            }
        </div>
    )
}
