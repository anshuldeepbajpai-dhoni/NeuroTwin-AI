import ProfileCard from "../../components/profile/ProfileCard";
import ProfileInfo from "../../components/profile/ProfileInfo";
import EditProfileForm from "../../components/profile/EditProfileForm";
import AvatarUpload from "../../components/profile/AvatarUpload";


export default function Profile() {

    return (

        <div
            className="profile-grid"
            style={{
                display: "grid",
                gridTemplateColumns: "350px 1fr",
                gap: 30,
            }}
        >

            <ProfileCard />

            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: 30,
                }}
            >
                <ProfileCard />

                <ProfileInfo />

                <EditProfileForm />

                <AvatarUpload />

            </div>

        </div>

    );

}