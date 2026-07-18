import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import authService from "../../services/authService";

export default function EditProfileForm() {

    const { user, refreshUser } = useAuth();

    const [form, setForm] = useState({
        username: user?.username || "",
        email: user?.email || "",
    });

    const [loading, setLoading] = useState(false);

    const [message, setMessage] = useState("");

    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        setLoading(true);

        setMessage("");

        try {

            await authServiceProfile(form);

            await refreshUser();

            setMessage("Profile updated successfully.");

        } catch (err) {

            setMessage(
                err.response?.data?.detail ||
                "Unable to update profile."
            );

        }

        setLoading(false);

    };

    return (

        <div
            style={{
                background: "white",
                padding: 30,
                borderRadius: 16,
                boxShadow: "var(--shadow)",
            }}
        >

            <h2>Edit Profile</h2>

            <form
                onSubmit={handleSubmit}
                style={{
                    marginTop: 25,
                }}
            >

                <label>Username</label>

                <input
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    style={inputStyle}
                />

                <label>Email</label>

                <input
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    style={inputStyle}
                />

                <button
                    type="submit"
                    disabled={loading}
                    style={buttonStyle}
                >

                    {
                        loading
                            ? "Saving..."
                            : "Save Changes"
                    }

                </button>

                {

                    message && (

                        <p
                            style={{
                                marginTop: 20,
                            }}
                        >

                            {message}

                        </p>

                    )

                }

            </form>

        </div>

    );

}

const inputStyle = {

    width: "100%",
    padding: 12,
    marginTop: 8,
    marginBottom: 20,
    border: "1px solid #ddd",
    borderRadius: 8,

};

const buttonStyle = {

    background: "var(--primary)",
    color: "white",
    padding: "12px 24px",
    borderRadius: 8,

};