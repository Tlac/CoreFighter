import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";

import GuestRoute from "@/app/GuestRoute";
import ProtectedRoute from "@/app/ProtectedRoute";
import Home from "@/pages/Home";
import Login from "@/pages/Login";
import Logout from "@/pages/Logout";
import Profile from "@/pages/Profile";
import NotFound from "@/pages/NotFound";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home/>}/>

                <Route element={<GuestRoute/>}>
                    <Route path="/login" element={<Login/>}/>
                </Route>

                <Route element={<ProtectedRoute/>}>
                    <Route path="/profile" element={<Profile/>}/>
                    <Route path="/logout" element={<Logout/>}/>
                </Route>

                <Route path="*" element={<NotFound/>}/>
            </Routes>
        </BrowserRouter>
    );
}
