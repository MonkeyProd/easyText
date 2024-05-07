import React, { useState, useRef, useEffect } from 'react'
import {useQuery} from "@tanstack/react-query"
import axios from "axios";
import styles from "./style.module.css";
import button_styles from "./button.module.css";
import DropdownList from "react-widgets/DropdownList";
import {FidgetSpinner} from "react-loader-spinner"
import {ExplosiveButton} from "./button"
import TextareaAutosize from 'react-textarea-autosize';

const API_URL = "http://localhost:8080"

export const Chat = () => {
    const [url, setUrl] = useState('https://github.com/TanStack/query/issues/5371')
    const [language, setLanguage] = useState('eng')
    const {isLoading, isFetching, isPaused, isSuccess, isError, error, data, refetch} = useQuery({
        queryKey: ['chat'],
        queryFn: () => axios.post(`${API_URL}/parse`, {url, language}, { withCredentials: true }).then((data)=>data.data),
        enabled: false
    });
    const button_ref = useRef(null)
    useEffect(() => {
      let mybutton = new ExplosiveButton(button_ref.current)
    }, [button_ref])
    
    const parse = ()=>{
        refetch()
    }
    return (
        <div className={styles.ChatContainer}>
  
            <div className="AuthInputContainer" style={{gap: "9px", backgroundColor: "#00000061"}}>
            <svg className={styles.Icon} xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 122.88 122.88"><title>hyperlink</title><path fill="#fff" d="M60.54,34.07A7.65,7.65,0,0,1,49.72,23.25l13-12.95a35.38,35.38,0,0,1,49.91,0l.07.08a35.37,35.37,0,0,1-.07,49.83l-13,12.95A7.65,7.65,0,0,1,88.81,62.34l13-13a20.08,20.08,0,0,0,0-28.23l-.11-.11a20.08,20.08,0,0,0-28.2.07l-12.95,13Zm14,3.16A7.65,7.65,0,0,1,85.31,48.05L48.05,85.31A7.65,7.65,0,0,1,37.23,74.5L74.5,37.23ZM62.1,89.05A7.65,7.65,0,0,1,72.91,99.87l-12.7,12.71a35.37,35.37,0,0,1-49.76.14l-.28-.27a35.38,35.38,0,0,1,.13-49.78L23,50A7.65,7.65,0,1,1,33.83,60.78L21.12,73.49a20.09,20.09,0,0,0,0,28.25l0,0a20.07,20.07,0,0,0,28.27,0L62.1,89.05Z"/></svg>
                <input placeholder="ВВЕДИТЕ ССЫЛКУ" className="AuthInput"  style={{width: "100%", backgroundColor: "transparent"}} onChange={(e)=>{setUrl(e.target.value)}} />
                <DropdownList
                    placeholder='Яzык'
                    onChange={(data) => {setLanguage(data)}}
                    data={["rus", "eng", "rus+eng"]}
                />
           
            <button ref={button_ref} onClick={()=>parse()}>Отправить</button>
   
            </div>

            <div className={styles.ResultContainer}>
                {!data && !isSuccess && !isFetching && !isError && <h3 className={styles.Info}> Здесь будет результат</h3>}
                {isSuccess && data && !isFetching && <TextareaAutosize className={styles.DataContainer}>{!isFetching && data}</TextareaAutosize >}
                {isFetching && <FidgetSpinner
                visible={true}
                height="80"
                width="80"
                backgroundColor={'white'}
                ariaLabel="fidget-spinner-loading"
                wrapperStyle={{}}
                wrapperClass="fidget-spinner-wrapper"
                />}
                {isError && <h1>Ошибка</h1>}
            </div>
        </div>
    )
}
