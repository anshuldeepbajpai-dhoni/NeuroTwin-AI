export default function PageContainer({ children }) {
    return (
        <main
            style={{
                flex: 1,
                padding: "30px",
                overflowY: "auto",
            }}
        >
            {children}
        </main>
    );
}