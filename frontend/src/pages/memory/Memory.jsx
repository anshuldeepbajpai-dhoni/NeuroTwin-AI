import { useEffect, useState } from "react";
import memoryService from "../../services/memoryService";
import CreateMemoryModal from "../../components/memory/CreateMemoryModal";

export default function Memory() {

    const [memories, setMemories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {

        loadMemories();

    }, []);

    async function loadMemories() {

        try {

            setLoading(true);

            const data = await memoryService.getAll();

            console.log("Memory API:", data);

            setMemories(data.items ?? []);

        } catch (err) {

            console.error(err);

            setError("Unable to load memories.");

        } finally {

            setLoading(false);

        }

    }

    async function handleCreate(memory) {

        try {

            await memoryService.create(memory);

            setShowModal(false);

            await loadMemories();

        } catch (err) {

            console.error(err);

            console.log("Response:", err.response);

            console.log("Data:", err.response?.data);

            alert(
                err.response?.data?.detail
                    ? JSON.stringify(err.response.data.detail)
                    : "Unable to create memory."
            );


        }

    }

    if (loading) {

        return <h2>Loading memories...</h2>;

    }

    if (error) {

        return <h2>{error}</h2>;

    }

    return (

        <div>

            <h1>Memory Center</h1>

            <button
                onClick={() => setShowModal(true)}
                style={{
                    marginBottom: 20,
                    padding: "10px 18px",
                    border: "none",
                    borderRadius: 8,
                    cursor: "pointer",
                }}
            >
                + New Memory
            </button>

            <p>Total Memories: {memories.length}</p>

            <div
                style={{
                    marginTop: 25,
                    display: "grid",
                    gap: 20,
                }}
            >

                {
                    memories.length === 0 ? (

                        <p>No memories found.</p>

                    ) : (

                        memories.map((memory) => (

                            <div
                                key={memory.id}
                                style={{
                                    background: "white",
                                    padding: 20,
                                    borderRadius: 12,
                                    boxShadow: "var(--shadow)",
                                }}
                            >

                                <h3>
                                    {memory.title || "Untitled"}
                                </h3>

                                <p>
                                    {memory.content || "No content"}
                                </p>

                                <p>
                                    <strong>Category:</strong> {memory.category}
                                </p>

                                <p>
                                    <strong>Importance:</strong> {memory.importance}
                                </p>

                                <p>
                                    <strong>Favorite:</strong>{" "}
                                    {memory.is_favorite ? "⭐ Yes" : "No"}
                                </p>

                            </div>

                        ))

                    )
                }

            </div>

            <CreateMemoryModal
                open={showModal}
                onClose={() => setShowModal(false)}
                onCreate={handleCreate}
            />

        </div>

    );

}