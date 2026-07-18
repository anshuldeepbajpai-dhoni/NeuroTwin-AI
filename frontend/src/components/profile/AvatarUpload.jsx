import { useRef, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import authService from "../../services/authService";

export default function AvatarUpload() {

    const { user, refreshUser } = useAuth();

    const inputRef = useRef(null);

    const [loading, setLoading] = useState(false);

    const handleUpload = async (e) => {

        const file = e.target.files[0];

        if (!file) return;

        setLoading(true);

        try {

            await authService.uploadAvatar(file);

            await refreshUser();

        } catch (error) {

            console.error(error);

            alert("Unable to upload avatar.");

        }

        setLoading(false);

    };

    const handleDelete = async () => {

        setLoading(true);

        try {

            await authService.deleteAvatar();

            await refreshUser();

        } catch (error) {

            console.error(error);

            alert("Unable to delete avatar.");

        }

        setLoading(false);

    };

    return (

        <div
            style={{
                background: "white",
                padding: 25,
                borderRadius: 16,
                boxShadow: "var(--shadow)",
                marginTop: 20,
                textAlign: "center",
            }}
        >

            <img
                src={
                    user?.avatar_url ||
                    "https://via.placeholder.com/120"
                }
                alt="Avatar"
                style={{
                    width: 120,
                    height: 120,
                    borderRadius: "50%",
                    objectFit: "cover",
                }}
            />

            <br /><br />

            <input
                ref={inputRef}
                type="file"
                accept="image/*"
                hidden
                onChange={handleUpload}
            />

            <button
                onClick={() => inputRef.current.click()}
                disabled={loading}
                style={buttonStyle}
            >
                Upload Avatar
            </button>

            <button
                onClick={handleDelete}
                disabled={loading}
                style={{
                    ...buttonStyle,
                    background: "#dc3545",
                    marginLeft: 10,
                }}
            >
                Delete
            </button>

        </div>

    );

}

const buttonStyle = {

    padding: "10px 20px",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    background: "var(--primary)",
    color: "white",

};