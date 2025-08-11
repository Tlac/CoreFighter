import {Link, useNavigate} from "react-router-dom";
import {useAuth} from "@/app/AuthContext";

export default function Navbar() {
    const {isAuthenticated, logout} = useAuth();
    const navigate = useNavigate();

    return (
        <nav className="bg-white shadow sticky top-0 z-50">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex h-14 items-center justify-between">
                    <Link to="/" className="text-xl font-bold text-indigo-600">CoreFighter</Link>

                    <div className="hidden md:flex space-x-4">
                        <Link className="hover:text-indigo-800" to="/">Home</Link>
                        {isAuthenticated && (
                            <Link className="hover:text-indigo-800" to="/profile">Profile</Link>
                        )}
                        {isAuthenticated ? (
                            <button
                                className="hover:text-red-600"
                                onClick={() => {
                                    logout();
                                    navigate("/", {replace: true});
                                }}
                            >
                                Logout
                            </button>
                        ) : (
                            <Link className="hover:text-indigo-800" to="/login">Login</Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}
