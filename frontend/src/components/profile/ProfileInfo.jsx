import { useAuth } from "../../context/AuthContext";

export default function ProfileInfo() {

    const { user } = useAuth();

    const fields = [
        ["Username", user?.username],
        ["Email", user?.email],
        ["User ID", user?.id],
        ["Status", user?.is_active ? "Active" : "Inactive"],
    ];

    return (
        <div
            style={{
                background: "white",
                borderRadius: 16,
                padding: 30,
                boxShadow: "var(--shadow)",
            }}
        >
            <h2
                style={{
                    marginBottom: 25,
                }}
            >
                Account Information
            </h2>

            {fields.map(([label, value]) => (
                <div
                    key={label}
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        padding: "16px 0",
                        borderBottom: "1px solid #eee",
                    }}
                >
                    <strong>{label}</strong>

                    <span>{value}</span>
                </div>
            ))}
        </div>
    );
}