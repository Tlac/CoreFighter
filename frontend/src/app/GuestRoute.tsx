import {Navigate, Outlet} from "react-router-dom";

export default function GuestRoute() {
    const token = localStorage.getItem("accessToken");
    return token ? <Navigate to="/profile" replace/> : <Outlet/>;
}
