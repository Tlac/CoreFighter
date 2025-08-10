import {Link} from "react-router-dom";

export default function Home() {
    const hasSession = Boolean(localStorage.getItem("accessToken"));

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold">Welcome to CoreFighter</h1>
            <div className="mt-4 flex flex-wrap gap-3">
                {!hasSession ? (
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
