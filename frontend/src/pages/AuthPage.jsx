import React, { useState } from 'react'
import "./AuthPage.css"
import { useAuth } from '../context/AuthContext';
import { useLocation, useNavigate } from 'react-router-dom';

const AuthPage = () => {
    const {login, signup} = useAuth();

    const navigate = useNavigate();
    const location = useLocation();

    const from = location.state?.from?.pathname || "/dashboard";

    const [loading, setLoading] = useState(false);
    const [apiError, setApiError] = useState("");
    const [successMessage, setSuccessMessage] = useState("")

    const [isLogin, setIsLogin] = useState(false);
    const [authForm, setAuthForm] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
    })
    const [passwordError, setPasswordError] = useState("")

    const handleChange = (e) => {
        setAuthForm((prevForm) => ({
            ...prevForm,
            [e.target.name]: e.target.value
        }));

        if (passwordError) setPasswordError("")
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        setPasswordError("");
        setApiError("");
        setSuccessMessage("");

        if (!isLogin && authForm.password !== authForm.confirmPassword) {
            setPasswordError("Passwords do not match!")
            return;
        }
        try {
            setLoading(true);

            if (isLogin) {
                await login({
                    username: authForm.username,
                    password: authForm.password
                })
                navigate(from, {replace:true})
            }
            else {
                await signup({
                    username: authForm.username,
                    email: authForm.email,
                    password: authForm.password
                })
                setSuccessMessage("Account created successfully! Now you can log in")
                setIsLogin(true);
                
                setAuthForm((prevForm) => ({
                    ...prevForm,
                    email: "",
                    confirmPassword: ""
                }));
            }
        }
        catch (error) {
            const message = error.response?.data?.message || error.response?.data?.detail || "Try again, something went wrong!"
            console.error(error);
            setApiError(message);
        }
        setLoading(false)
    }

    return (
        <>
            <div className="auth-page">
                <div className="auth-brand">
                    <div className="brand-logo">CG</div>
                    <h1>CodeGraph<span>AI</span></h1>

                    <div className="brand-content">
                        <p className="eyebrow">UNDERSTAND YOUR CODEBASE</p>
                        <h2>
                            Your code has a story.
                            <br />
                            <span>Let's explore it.</span>
                        </h2>
                        <p className="brand-description">
                            Explore code relationships, understand dependencies, and get intelligent answers about your codebase with AI.
                        </p>

                        <div className="feature-list">
                            <p>✦ Intelligent code analysis</p>
                            <p>✦ Interactive dependency graphs</p>
                            <p>✦ AI-powered code understanding</p>
                        </div>
                    </div>

                    <p className="brand-footer">
                        Built for developers who think beyond code.
                    </p>
                </div>

                <div className="auth-form-section">
                    <div className="auth-card">
                        <div className="mobile-brand">
                            <div className="brand-logo">CG</div>
                            <h2>CodeGraph<span>AI</span></h2>
                        </div>

                        <div className="auth-heading">
                            <h2>{isLogin ? "Welcome back" : "Create your account"}</h2>
                            <p>
                                {isLogin
                                    ? "Sign in to continue exploring your code."
                                    : "Start understanding your codebase with AI."}
                            </p>
                        </div>
                        {apiError && (
                            <p className="error-message">{apiError}</p>
                        )}

                        {successMessage && isLogin && (
                            <p className="success-message">{successMessage}</p>
                        )}
                        <form onSubmit={handleSubmit}>
                            <div className='form-group'>
                                <label>Username</label>
                                <input name="username" type="text" value={authForm.username} onChange={handleChange} required />
                            </div>

                            {!isLogin &&
                                <div className="form-group">
                                    <label>Email address</label>
                                    <input type="email" name="email" value={authForm.email} onChange={handleChange} required />
                                </div>
                            }
                            <div className="form-group">
                                <label>Password</label>
                                <input type="password" name="password" value={authForm.password} onChange={handleChange} required minLength={8} />
                            </div>
                            {!isLogin && (
                                <>
                                    <div className="form-group">
                                        <label>Confirm password</label>
                                        <input name="confirmPassword" type="password" value={authForm.confirmPassword} onChange={handleChange} required minLength={8} />
                                    </div>
                                    {passwordError && (
                                        <p className='error-message'>{passwordError}</p>
                                    )}
                                </>
                            )}
                            <button className="submit-btn" type="submit" disabled={loading}>
                                {loading
                                    ? "Please wait..."
                                    : isLogin
                                        ? "Sign In"
                                        : "Create Account"}
                                {!loading && <span>→</span>}
                            </button>
                        </form>
                        <p className="auth-switch">
                            {isLogin ? "Don't have an account?" : "Already have an account?"}
                            <button
                                type="button"
                                onClick={() => setIsLogin(!isLogin)}
                            >
                                {isLogin ? "Sign up" : "Login"}
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </>
    )
}

export default AuthPage