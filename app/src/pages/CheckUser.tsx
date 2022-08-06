import { FC, useState } from 'react'
import axios from 'axios'
import { notification } from 'antd'

import Auth from '../components/Auth';
import { DataProps, CustomAxiosError } from '../utils/types';
import { LoginUrl } from '../utils/network';


const CheckUser:FC = () => {

    const [loading, setLoading] = useState(false)

    const onSubmit = async (values: DataProps) => {
        setLoading(true)
        const response = await axios.post(LoginUrl, {...values, is_new_user:true}).catch(
            (e: CustomAxiosError) => {
                notification.error({
                    message: 'User Check Error',
                    description: e.response?.data.error,
                })
            }
        )
        if(response) {
            console.log("Check Completed")
        }
        setLoading(false)
    }

    return <Auth 
        titleText='Verify Yourself!'
        buttonText='Submit'
        linkText='Go Back'
        isPassword={false}
        linkPath='/login'
        onSubmit={onSubmit}
    />
}

export default CheckUser
