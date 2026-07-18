import { useEffect, useState } from "react";
import digitalTwinService from "../../services/digitalTwinService";
import "../../styles/digitalTwin.css";
import TwinHeader from "./TwinHeader";
import ProfileStats from "./ProfileStats";
import CompletionCard from "./CompletionCard";
import HeroBanner from "./HeroBanner";
import Toast from "../common/Toast";
import PageHeader from "../common/PageHeader";

export default function DigitalTwinForm() {

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [toast, setToast] = useState({
        message: "",
        type: "success",
    });
    const [exists, setExists] = useState(false);

    const [form, setForm] = useState({
        twin_name: "",
        personality: "",
        communication_style: "",
        goals: "",
        interests: "",
    });

    useEffect(() => {
        loadTwin();
    }, []);

    async function loadTwin() {

        try {

            const twin = await digitalTwinService.get();

            setExists(true);

            setForm({
                twin_name: twin.twin_name,
                personality: twin.personality,
                communication_style: twin.communication_style,
                goals: twin.goals,
                interests: twin.interests,
            });

        } catch (err) {

            if (err.response?.status === 404) {

                setExists(false);

            } else {

                console.error(err);

                alert("Unable to load Digital Twin.");

            }

        } finally {

            setLoading(false);

        }

    }

    function handleChange(e) {

        const { name, value } = e.target;

        setForm(prev => ({
            ...prev,
            [name]: value,
        }));

    }

    async function handleSubmit(e) {

        e.preventDefault();

        try {

            setSaving(true);

            if (exists) {

                await digitalTwinService.update(form);

                setToast({
                    message: "Digital Twin updated successfully!",
                    type: "success",
                });

                setTimeout(() => {

                    setToast({
                        message: "",
                        type: "success",
                    });

                },3000);

            } else {

                await digitalTwinService.create(form);

                setToast({
                    message:"Digital Twin created successfully!",
                    type:"success",
                });

                setTimeout(()=>{

                setToast({
                message:"",
                type:"success",
                });

                },3000);

                setExists(true);

            }

        } catch (err) {

            console.error(err);

            setToast({

            message:
            err.response?.data?.detail ||
            "Unable to save Digital Twin.",

            type:"error",

            });

        } finally {

            setSaving(false);

        }

    }

    if (loading) {

        return <h2>Loading Digital Twin...</h2>;

    }

    return (
        <>

        <Toast
            message={toast.message}
            type={toast.type}
        />
        <div className="dt-container">

            <div className="dt-card">

                <PageHeader

                title="🤖 Digital Twin"

                subtitle="Create and manage your AI personality."

                />

                <HeroBanner />

                <TwinHeader exists={exists} />

                <ProfileStats />

                <CompletionCard
                    form={form}
                />

                <form
                    className="dt-form"
                >

                    <div className="dt-group">

                        <label className="dt-label">
                            Twin Name
                        </label>

                        <input
                            className="dt-input"
                            type="text"
                            name="twin_name"
                            value={form.twin_name}
                            onChange={handleChange}
                            required
                        />

                    </div>

                    <div className="dt-group">

                        <label className="dt-label">
                            Communication Style
                        </label>

                        <select
                            className="dt-select"
                            name="communication_style"
                            value={form.communication_style}
                            onChange={handleChange}
                            required
                        >
                            <option value="">Select</option>
                            <option value="Professional">Professional</option>
                            <option value="Friendly">Friendly</option>
                            <option value="Technical">Technical</option>
                            <option value="Casual">Casual</option>
                        </select>

                    </div>


                    <div className="dt-group dt-full">

                        <label className="dt-label">
                            Personality
                        </label>

                        <textarea
                            className="dt-textarea"
                            rows="5"
                            name="personality"
                            value={form.personality}
                            onChange={handleChange}
                            required
                        />

                    </div>

        
                    <div className="dt-group dt-full">

                        <label className="dt-label">
                            Goals
                        </label>

                        <textarea
                            className="dt-textarea"
                            rows="4"
                            name="goals"
                            value={form.goals}
                            onChange={handleChange}
                            required
                        />

                    </div>

                    <div className="dt-group dt-full">

                        <label className="dt-label">
                            Interests
                        </label>

                        <textarea
                            className="dt-textarea"
                            rows="4"
                            name="interests"
                            value={form.interests}
                            onChange={handleChange}
                            required
                        />

                    </div>

                    <button
                        type="submit"
                        disabled={saving}
                        className="dt-save dt-full"
                    >
                        {
                            saving
                                ? "Saving..."
                                : exists
                                    ? "Update Digital Twin"
                                    : "Create Digital Twin"
                        }
                    </button>

                </form>

            </div>

        </div>
    </>    

    );

}