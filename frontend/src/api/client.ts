let accessToken = localStorage.getItem("accessToken") || "";
let refreshToken = localStorage.getItem("refreshToken") || "";

export function setTokens(access: string, refresh?: string) {
    accessToken = access;
    localStorage.setItem("accessToken", access);
    if (refresh) {
        refreshToken = refresh;
        localStorage.setItem("refreshToken", refresh);
    }
}

async function tryRefresh(): Promise<boolean> {
    if (!refreshToken) return false;
    const res = await fetch("/api/auth/token/refresh/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({refresh: refreshToken}),
    });
    if (!res.ok) return false;
    const data = await res.json();
    setTokens(data.access);
    return true;
}

/** Generic API function: attaches token, retries once after refresh */
export async function api<T>(url: string, options: RequestInit = {}): Promise<T> {
    const doFetch = () =>
        fetch(url, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(accessToken ? {Authorization: `Bearer ${accessToken}`} : {}),
                ...(options.headers || {}),
            },
        });

    let res = await doFetch();

    if (res.status === 401 && (await tryRefresh())) {
        res = await doFetch();
    }

    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || res.statusText);
    }
    return res.json();
}
