import {useState} from "react";
import {login} from "@/api/auth";
import {setTokens} from "@/api/client";
import {useNavigate} from "react-router-dom";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState<string | null>(null);
    const nav = useNavigate();

    async function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        setErr(null);
        setLoading(true);
        try {
            const {access, refresh} = await login(username, password);
            setTokens(access, refresh);
            nav("/profile");
        } catch (e: any) {
            setErr(e.message.detail || "Login failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen bg-slate-100 flex items-center justify-center p-6">
            <form onSubmit={onSubmit} className="w-full max-w-sm bg-white rounded-xl p-6 shadow">
                <h1 className="text-xl font-semibold mb-4">Sign in</h1>

                <label className="block text-sm font-medium mb-1">Username</label>
                <input
                    className="w-full border rounded px-3 py-2 mb-3"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    autoComplete="username"
                />

                <label className="block text-sm font-medium mb-1">setPassword</label>
                <input
                    className="w-full border rounded px-3 py-2 mb-3"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="current-password"
                />

                {err && <p className="text-sm text-red-600 mb-3">{err}</p>}

                <button
                    disabled={loading}
                    className="w-full bg-indigo-600 text-white rounded py-2 font-medium disabled:opacity-60"
                >
                    {loading ? "Signing in..." : "Login"}
                </button>
            </form>
        </div>
    );
}
