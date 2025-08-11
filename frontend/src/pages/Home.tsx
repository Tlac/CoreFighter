import {Link} from "react-router-dom";
import {useAuth} from "@/app/AuthContext";

export default function Home() {
    const {isAuthenticated} = useAuth();

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold">Welcome to CoreFighter</h1>
            <div className="mt-4 flex flex-wrap gap-3">
                {!isAuthenticated ? (
                    <Link className="underline text-indigo-600 hover:text-indigo-800" to="/login">
                        Login
                    </Link>
                ) : (
                    <>
                        <Link className="underline text-indigo-600 hover:text-indigo-800" to="/profile">
                            My Decks
                        </Link>
                        <Link className="underline text-indigo-600 hover:text-indigo-800" to="/logout">
                            Logout
                        </Link>
                    </>
                )}
            </div>
        </div>
    );
}
