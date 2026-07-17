import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);
        setError("");

        try {
            await login({
                username: formData.email,
                password: formData.password,
            });

            navigate("/");
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                    "Invalid email or password."
            );
        } finally {
            setLoading(false);
        }
    };
    
    console.log("API URL:", import.meta.env.VITE_API_BASE_URL);

    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "100vh",
                background: "#f4f6f9",
            }}
        >
            <div
                style={{
                    width: "400px",
                    background: "#fff",
                    padding: "40px",
                    borderRadius: "12px",
                    boxShadow: "0 8px 20px rgba(0,0,0,0.1)",
                }}
            >
                <h1
                    style={{
                        textAlign: "center",
                        marginBottom: "30px",
                    }}
                >
                    NeuroTwin AI
                </h1>

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: "20px" }}>
                        <label>Email</label>

                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Enter your email"
                            required
                            style={{
                                width: "100%",
                                padding: "12px",
                                marginTop: "8px",
                            }}
                        />
                    </div>

                    <div style={{ marginBottom: "20px" }}>
                        <label>Password</label>

                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Enter your password"
                            required
                            style={{
                                width: "100%",
                                padding: "12px",
                                marginTop: "8px",
                            }}
                        />
                    </div>

                    {error && (
                        <p
                            style={{
                                color: "red",
                                marginBottom: "15px",
                            }}
                        >
                            {error}
                        </p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: "100%",
                            padding: "12px",
                            background: "#2563eb",
                            color: "#fff",
                            border: "none",
                            borderRadius: "6px",
                            cursor: "pointer",
                        }}
                    >
                        {loading ? "Signing In..." : "Login"}
                    </button>
                </form>

                <p
                    style={{
                        textAlign: "center",
                        marginTop: "20px",
                    }}
                >
                    Don't have an account?{" "}
                    <Link to="/register">Register</Link>
                </p>
            </div>
        </div>
    );
}