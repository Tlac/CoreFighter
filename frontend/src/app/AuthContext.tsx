import {createContext, useContext, useState, ReactNode, useEffect} from "react";
import {setTokens} from "@/api/client";

type AuthContextType = {
    isAuthenticated: boolean;
    login: (access: string, refresh: string) => void;
    logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({children}: { children: ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const access = localStorage.getItem("accessToken");
        if (access) setIsAuthenticated(true);
    }, []);

    const login = (access: string, refresh: string) => {
        setTokens(access, refresh);
        setIsAuthenticated(true); // <— this is what makes the Navbar update instantly
    };

    const logout = () => {
        setTokens("", "");
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{isAuthenticated, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
    return ctx;
}
