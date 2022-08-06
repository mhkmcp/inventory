import { FC, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { notification } from 'antd'

import Auth from '../components/Auth';
import { DataProps, CustomAxiosError } from '../utils/types'
import { LoginUrl } from '../utils/network'
import { tokenName } from '../utils/data'


interface LoginDataProps {
    data: {
        access: string
    }
}


const Login: FC = () => {
    
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const onSubmit = async (values: DataProps) => {
        setLoading(true)
        const response: LoginDataProps = await axios.post(LoginUrl, values).catch(
            (e: CustomAxiosError) => {
                notification.error({
                    message: 'Login Error',
                    description: e.response?.data.error,
                })
            }
        ) as LoginDataProps
        if(response) {
            localStorage.setItem(tokenName, response.data.access)
            navigate('/')
        }
        setLoading(false)
    }

    return <Auth onSubmit={onSubmit} loading={loading} />
}

export default Login
