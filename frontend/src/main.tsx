import React from "react";
import ReactDOM from "react-dom/client";
import App from "./app/App";
import "./index.css";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {AuthProvider} from "@/app/AuthContext";

const qc = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <QueryClientProvider client={qc}>
            <AuthProvider>
                <App/>
            </AuthProvider>
        </QueryClientProvider>
    </React.StrictMode>
);
