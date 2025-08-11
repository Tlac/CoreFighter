import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {useAuth} from "@/app/AuthContext";
import {api} from "@/api/client";

type TokenResponse = { access: string; refresh: string };

export default function Login() {
    const {login, isAuthenticated} = useAuth();
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (isAuthenticated) {
            navigate("/profile", {replace: true});
        }
    }, [isAuthenticated, navigate]);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setSubmitting(true);
        setError(null);

        try {
            const data = await api<TokenResponse>("/api/auth/token/", {
                method: "POST",
                body: JSON.stringify({username, password}),
            });

            login(data.access, data.refresh);

            navigate("/profile", {replace: true});
        } catch (err) {
            setError((err as Error).message || "Login failed.");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <main className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
            <form onSubmit={handleSubmit} className="w-full max-w-sm rounded-2xl bg-white p-6 shadow">
                <h1 className="text-xl font-bold">Sign in</h1>
                <p className="mt-1 text-sm text-slate-600">Use your CoreFighter account.</p>

                <label className="mt-4 block text-sm font-medium text-slate-700">
                    Username
                    <input
                        className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        autoComplete="username"
                        required
                    />
                </label>

                <label className="mt-3 block text-sm font-medium text-slate-700">
                    Password
                    <input
                        type="password"
                        className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        autoComplete="current-password"
                        required
                    />
                </label>

                {error && (
                    <div className="mt-3 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={submitting}
                    className="mt-4 w-full rounded-md bg-indigo-600 px-4 py-2 font-medium text-white hover:bg-indigo-700 disabled:opacity-60"
                >
                    {submitting ? "Signing in…" : "Sign in"}
                </button>
            </form>
        </main>
    );
}
