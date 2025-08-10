export type TokenPair = { access: string; refresh: string };

export async function login(username: string, password: string): Promise<TokenPair> {
    const res = await fetch("/api/auth/token/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password}),
    });
    if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || "Invalid credentials");
    }
    return res.json();
}

export async function refresh(refreshToken: string): Promise<{ access: string }> {
    const res = await fetch("/api/auth/token/refresh/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({refresh: refreshToken}),
    });
    if (!res.ok) throw new Error("Refresh failed");
    return res.json();
}
