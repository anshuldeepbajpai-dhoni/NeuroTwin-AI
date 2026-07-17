import { Link } from "react-router-dom";

export default function Sidebar() {

    return (

        <aside
            style={{
                width: "230px",
                background: "#0F172A",
                color: "white",
                padding: "20px",
                minHeight: "100vh"
            }}
        >

            <h2>Menu</h2>

            <nav
                style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "15px",
                    marginTop: "30px"
                }}
            >

                <Link to="/">Dashboard</Link>

                <Link to="/digital-twin">Digital Twin</Link>

                <Link to="/chat">AI Chat</Link>

                <Link to="/memory">Memory</Link>

                <Link to="/profile">Profile</Link>

            </nav>

        </aside>

    );

}