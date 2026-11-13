import { createContext, useContext, useState, useEffect } from "react";
import * as authService from "../services/authService";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await api.get("/auth/me");
                setUser(response.data)
            }
            catch(error) {
                setUser(null);
            }
            finally {
                setIsLoading(false)
            }
        };
        checkAuth();
    }, [])

    const login = async (credentials) => {
        const data = await authService.login(credentials);
        setUser(data.username)
        return data;
    }

    const signup = async (userdata) => {
        return await authService.signup(userdata);
    }

    const logout = async () => {
        await authService.logout();
        setUser(null);
    }

    return (
        <AuthContext.Provider value = {{user, isLoading, login, signup, logout}}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => {
    const context = useContext(AuthContext);
    return context;
}