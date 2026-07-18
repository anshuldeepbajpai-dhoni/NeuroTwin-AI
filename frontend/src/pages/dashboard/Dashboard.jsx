import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

import WelcomeCard from "../../components/dashboard/WelcomeCard";
import StatCard from "../../components/dashboard/StatCard";
import QuickActionCard from "../../components/dashboard/QuickActionCard";
import ActivityCard from "../../components/dashboard/ActivityCard";

export default function Dashboard() {

    const navigate = useNavigate();

    const { user } = useAuth();

    return (

        <>

            <WelcomeCard />

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(250px,1fr))",
                    gap: 20,
                    marginBottom: 35,
                }}
            >

                <StatCard
                    title="Username"
                    value={user?.username}
                    color="#2563eb"
                />

                <StatCard
                    title="Email"
                    value={user?.email}
                    color="#10b981"
                />

                <StatCard
                    title="Status"
                    value={
                        user?.is_active
                            ? "Active"
                            : "Inactive"
                    }
                    color="#f59e0b"
                />

                <StatCard
                    title="AI Twin"
                    value="Online"
                    color="#ef4444"
                />

            </div>

            <h2
                style={{
                    marginBottom: 20,
                }}
            >
                Quick Actions
            </h2>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(260px,1fr))",
                    gap: 20,
                }}
            >

                <QuickActionCard
                    title="Profile"
                    description="Manage your account"
                    onClick={() =>
                        navigate("/profile")
                    }
                />

                <QuickActionCard
                    title="Digital Twin"
                    description="Configure your AI twin"
                    onClick={() =>
                        navigate("/digital-twin")
                    }
                />

                <QuickActionCard
                    title="Memory"
                    description="View long-term memory"
                    onClick={() =>
                        navigate("/memory")
                    }
                />

                <QuickActionCard
                    title="AI Chat"
                    description="Talk with your twin"
                    onClick={() =>
                        navigate("/chat")
                    }
                />

            </div>

            <h2
                style={{
                    marginTop: 40,
                    marginBottom: 20,
                }}
            >
                Recent Activity
            </h2>

            <div
                style={{
                    background: "white",
                    borderRadius: 16,
                    boxShadow: "var(--shadow)",
                }}
            >

                <ActivityCard
                    title="Successfully logged in"
                    time="Just now"
                />

                <ActivityCard
                    title="Profile loaded"
                    time="A few seconds ago"
                />

                <ActivityCard
                    title="Dashboard initialized"
                    time="Today"
                />

            </div>

        </>

    );

}