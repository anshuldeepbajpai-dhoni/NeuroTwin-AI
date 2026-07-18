export default function CompletionCard({ form }) {

    const fields = [
        form.twin_name,
        form.personality,
        form.communication_style,
        form.goals,
        form.interests,
    ];

    const completed = fields.filter(
        value => value && value.trim() !== ""
    ).length;

    const percentage = Math.round(
        (completed / fields.length) * 100
    );

    return (

        <div className="completion-card">

            <div className="completion-top">

                <h3>Digital Twin Completion</h3>

                <span>{percentage}%</span>

            </div>

            <div className="completion-bar">

                <div
                    className="completion-fill"
                    style={{
                        width: `${percentage}%`
                    }}
                />

            </div>

            <p>

                {completed} of {fields.length} sections completed.

            </p>

        </div>

    );

}