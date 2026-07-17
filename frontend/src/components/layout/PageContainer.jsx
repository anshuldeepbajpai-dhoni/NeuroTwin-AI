export default function PageContainer({ children }) {

    return (

        <div
            style={{
                padding: "30px",
                flex: 1
            }}
        >

            {children}

        </div>

    );

}