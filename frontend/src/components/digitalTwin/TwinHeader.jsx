export default function TwinHeader({ exists }) {

    return (

        <div className="dt-header">

            <div className="dt-avatar">

                <img
                src="/robot.png"
                alt="AI"
                className="dt-avatar-img"
                />

            </div>

            <div>

                <h2 className="dt-name">

                    {exists ? "Your Digital Twin" : "Create Digital Twin"}

                </h2>

                <p className="dt-desc">

                    Your AI companion profile.

                </p>

            </div>

        </div>

    );

}