import {FC} from 'react'
import { Button, Form, Input } from 'antd';
import { Link } from 'react-router-dom'

import { DataProps } from '../utils/types'

interface AuthProps {
    titleText?: string
    isPassword?: boolean
    buttonText?: string
    linkText?: string
    linkPath?: string
    onSubmit:(values: DataProps) => void
    loading?: boolean
}

const Auth:FC<AuthProps> = ({
    titleText = "Sign In", 
    isPassword = true,
    buttonText = "Login",
    linkText = "New User?",
    linkPath = '/check-user',
    onSubmit,
    loading = false,
}) => {

    return (
        <div className='login'>
            <div className="inner">
                <div className="header">
                    <h3>{titleText}</h3>
                    <h2>Inventory</h2>
                </div>

                <Form layout="vertical" onFinish={onSubmit}>
                    <Form.Item 
                        label="Email"
                        name="email"
                        rules={[{ required: true, message: 'Please input your email' }]}
                    >
                        <Input placeholder="Your Email" type="email" />
                    </Form.Item>
                    { 
                        isPassword && 
                        <Form.Item 
                            label="Password"
                            name="password"
                            rules={[{ required: true, message: 'Please input your password' }]}
                        >
                            <Input placeholder="Your Password" type="password" />
                        </Form.Item>
                    }
                    <Form.Item >
                        <Button htmlType='submit' type="primary" block loading={loading}>{buttonText}</Button>
                    </Form.Item>
                    <Link to={linkPath}>{linkText}</Link>
                </Form>
            </div>
        </div>
    )
}

export default Auth

