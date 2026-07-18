import { useState } from "react";

export default function CreateMemoryModal({
    open,
    onClose,
    onCreate,
}) {
    const [form, setForm] = useState({
        title: "",
        content: "",
        category: "Personal",
        importance: 3,
        is_favorite: false,
    });

    if (!open) return null;

    function handleChange(e) {
        const { name, value, type, checked } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]:
                type === "checkbox"
                    ? checked
                    : value,
        }));
    }

    async function handleSubmit(e) {
        e.preventDefault();

        await onCreate({
            ...form,
            importance: Number(form.importance),
        });

        setForm({
            title: "",
            content: "",
            category: "Personal",
            importance: 3,
            is_favorite: false,
        });
    }

    return (
        <div
            style={{
                position: "fixed",
                inset: 0,
                background: "rgba(0,0,0,.45)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                zIndex: 999,
            }}
        >
            <div
                style={{
                    width: 500,
                    background: "#fff",
                    borderRadius: 12,
                    padding: 25,
                }}
            >
                <h2>Create Memory</h2>

                <form onSubmit={handleSubmit}>

                    <label>Title</label>

                    <input
                        name="title"
                        value={form.title}
                        onChange={handleChange}
                        required
                        style={{
                            width: "100%",
                            marginBottom: 15,
                        }}
                    />

                    <label>Content</label>

                    <textarea
                        name="content"
                        value={form.content}
                        onChange={handleChange}
                        rows={5}
                        required
                        style={{
                            width: "100%",
                            marginBottom: 15,
                        }}
                    />

                    <label>Category</label>

                    <select
                        name="category"
                        value={form.category}
                        onChange={handleChange}
                        style={{
                            width: "100%",
                            marginBottom: 15,
                        }}
                    >
                        <option>Personal</option>
                        <option>Work</option>
                        <option>Learning</option>
                        <option>Project</option>
                        <option>Health</option>
                    </select>

                    <label>Importance</label>

                    <input
                        type="range"
                        min="1"
                        max="5"
                        name="importance"
                        value={form.importance}
                        onChange={handleChange}
                        style={{
                            width: "100%",
                        }}
                    />

                    <p>
                        Importance: {form.importance}
                    </p>

                    <label
                        style={{
                            display: "flex",
                            gap: 10,
                            marginBottom: 20,
                        }}
                    >
                        <input
                            type="checkbox"
                            name="is_favorite"
                            checked={form.is_favorite}
                            onChange={handleChange}
                        />

                        Favorite
                    </label>

                    <div
                        style={{
                            display: "flex",
                            justifyContent: "flex-end",
                            gap: 10,
                        }}
                    >
                        <button
                            type="button"
                            onClick={onClose}
                        >
                            Cancel
                        </button>

                        <button type="submit">
                            Save Memory
                        </button>
                    </div>

                </form>

            </div>
        </div>
    );
}