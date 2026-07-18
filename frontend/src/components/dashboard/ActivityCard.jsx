export default function ActivityCard({
    title,
    time,
}) {
    return (
        <div
            style={{
                padding: "18px",
                borderBottom: "1px solid #eee",
            }}
        >
            <strong>{title}</strong>

            <br />

            <small
                style={{
                    color: "#888",
                }}
            >
                {time}
            </small>
        </div>
    );
}