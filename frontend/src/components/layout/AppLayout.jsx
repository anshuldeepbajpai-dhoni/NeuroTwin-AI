import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function AppLayout({ children }) {

    return (

        <div className="app-layout">

            <Sidebar />

            <div className="app-main">

                <Topbar />

                <div className="app-content">

                    {children}

                </div>

            </div>

        </div>

    );

}