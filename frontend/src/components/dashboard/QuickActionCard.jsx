export default function QuickActionCard({
    title,
    description,
    onClick,
}) {
    return (
        <div
            onClick={onClick}
            style={{
                background: "white",
                borderRadius: "16px",
                padding: "25px",
                cursor: "pointer",
                boxShadow: "var(--shadow)",
                transition: ".25s",
            }}
        >
            <h3>{title}</h3>

            <p
                style={{
                    marginTop: 10,
                    color: "#6b7280",
                }}
            >
                {description}
            </p>
        </div>
    );
}