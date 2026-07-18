import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App";
import "./styles/theme.css";
import "./styles/global.css";
import "./styles/common.css";
import "./styles/layout.css";

import { AuthProvider } from "./context/AuthContext";

createRoot(
    document.getElementById("root")
).render(

    <StrictMode>

        <AuthProvider>

            <App />

        </AuthProvider>

    </StrictMode>

);