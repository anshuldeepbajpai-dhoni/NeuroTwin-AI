import { NavLink } from "react-router-dom";

export default function Sidebar() {

    return (

        <aside className="sidebar">

            <h2>🤖 NeuroTwin</h2>

            <NavLink to="/dashboard">Dashboard</NavLink>

            <NavLink to="/digital-twin">Digital Twin</NavLink>

            <NavLink to="/memory">Memory</NavLink>

            <NavLink to="/chat">AI Chat</NavLink>

            <NavLink to="/profile">Profile</NavLink>

        </aside>

    );

}