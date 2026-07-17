import Navbar from "../components/layout/Navbar";
import Sidebar from "../components/layout/Sidebar";
import PageContainer from "../components/layout/PageContainer";

export default function MainLayout({ children }) {

    return (

        <>

            <Navbar />

            <div
                style={{
                    display: "flex"
                }}
            >

                <Sidebar />

                <PageContainer>

                    {children}

                </PageContainer>

            </div>

        </>

    );

}