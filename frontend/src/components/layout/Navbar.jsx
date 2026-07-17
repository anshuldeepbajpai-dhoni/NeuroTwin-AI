import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
    const navigate = useNavigate();

    const {
        user,
        logout,
    } = useAuth();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <header
            style={{
                height: "70px",
                background: "#1E293B",
                color: "#FFFFFF",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "0 30px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            }}
        >
            {/* Left Section */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                }}
            >
                <h2
                    style={{
                        margin: 0,
                        fontSize: "24px",
                        fontWeight: "700",
                    }}
                >
                    🧠 NeuroTwin AI
                </h2>
            </div>

            {/* Right Section */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "15px",
                }}
            >
                <span
                    style={{
                        fontSize: "15px",
                    }}
                >
                    Welcome,
                    <strong>
                        {" "}
                        {user?.username || user?.email || "User"}
                    </strong>
                </span>

                <button
                    onClick={handleLogout}
                    style={{
                        background: "#EF4444",
                        color: "#FFFFFF",
                        border: "none",
                        padding: "10px 18px",
                        borderRadius: "6px",
                        cursor: "pointer",
                        fontWeight: "600",
                    }}
                >
                    Logout
                </button>
            </div>
        </header>
    );
}