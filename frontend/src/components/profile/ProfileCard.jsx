import { useAuth } from "../../context/AuthContext";

export default function ProfileCard() {
    const { user } = useAuth();

    return (
        <div
            style={{
                background: "white",
                borderRadius: 16,
                padding: 30,
                boxShadow: "var(--shadow)",
                textAlign: "center",
            }}
        >
            <div
                style={{
                    width: 110,
                    height: 110,
                    borderRadius: "50%",
                    background: "var(--primary)",
                    color: "white",
                    fontSize: 42,
                    fontWeight: "bold",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    margin: "0 auto 20px",
                }}
            >
                {user?.username?.charAt(0)?.toUpperCase()}
            </div>

            <h2>{user?.username}</h2>

            <p style={{ color: "#6b7280" }}>
                {user?.email}
            </p>

            <span
                style={{
                    display: "inline-block",
                    marginTop: 15,
                    background: "#dcfce7",
                    color: "#166534",
                    padding: "6px 14px",
                    borderRadius: 20,
                }}
            >
                {user?.is_active ? "Active User" : "Inactive"}
            </span>
        </div>
    );
}