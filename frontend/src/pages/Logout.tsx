import {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {useAuth} from "@/app/AuthContext";

export default function Logout() {
    const {logout} = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        logout();
        navigate("/", {replace: true});
    }, [logout, navigate]);

    return null;
}
