import {Link, useNavigate} from "react-router-dom";

export default function NotFound() {
    const navigate = useNavigate();
    const hasSession = Boolean(localStorage.getItem("accessToken"));

    return (
        <main className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
            <div className="w-full max-w-lg text-center">
                <div
                    className="mx-auto mb-6 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-100">
                    <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        aria-hidden="true"
                        className="h-8 w-8 text-indigo-600"
                    >
                        <path d="M12 3l9 6-9 6-9-6 9-6z" fill="currentColor" opacity=".15"/>
                        <path
                            d="M21 9v6l-9 6-9-6V9m18 0l-9 6m9-6L12 3M12 15L3 9"
                            stroke="currentColor"
                            strokeWidth="1.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                </div>

                <p className="text-sm uppercase tracking-wider text-indigo-600">404</p>
                <h1 className="mt-2 text-3xl font-bold text-slate-900">Page not found</h1>
                <p className="mt-2 text-slate-600">
                    Sorry, we couldn’t find the page you’re looking for. It might have been moved,
                    renamed, or never existed.
                </p>

                <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
                    <button
                        onClick={() => navigate(-1)}
                        className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                    >
                        Go back
                    </button>
                    <Link
                        to="/"
                        className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
                    >
                        Go home
                    </Link>
                    {hasSession && (
                        <Link
                            to="/profile"
                            className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-black"
                        >
                            My profile
                        </Link>
                    )}
                </div>

                <div className="mt-4 text-sm text-slate-500">
                    If you typed the address, double-check the URL. Otherwise, use the links above.
                </div>
            </div>
        </main>
    );
}
