import MainLayout from "../../layouts/MainLayout";
import { useEffect } from "react";
import api from "../../api/api";

export default function Dashboard() {

    useEffect(() => {

        api.get("/health")
            .then((response) => {

                console.log(response.data);

            })
            .catch(console.error);

    }, []);

    return (

        <MainLayout>

            <h1>Dashboard</h1>

        </MainLayout>

    );

}