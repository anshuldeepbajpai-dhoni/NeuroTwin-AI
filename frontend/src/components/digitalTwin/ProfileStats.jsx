import StatCard from "../common/StatCard";

export default function ProfileStats(){

    return(

        <div
            style={{
                display:"grid",
                gridTemplateColumns:"repeat(3,1fr)",
                gap:"20px",
                marginBottom:"30px",
            }}
        >

            <StatCard

                icon="📝"

                value="5"

                label="Profile Fields"

            />

            <StatCard

                icon="🎯"

                value="100%"

                label="Completed"

            />

            <StatCard

                icon="🤖"

                value="Available"

                label="AI Status"

            />

        </div>

    );

}