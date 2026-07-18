import { useAuth } from "../../context/AuthContext";

export default function Navbar(){

const {user,logout}=useAuth();

return(

<header
style={{
height:70,
background:"white",
padding:"0 30px",
display:"flex",
justifyContent:"space-between",
alignItems:"center",
boxShadow:"var(--shadow)",
zIndex:100,
}}
>

<div>

<h2>

NeuroTwin AI

</h2>

</div>

<div
style={{
display:"flex",
alignItems:"center",
gap:20,
}}
>

<div
style={{
textAlign:"right",
}}
>

<strong>

{user?.username}

</strong>

<br/>

<small>

{user?.email}

</small>

</div>

<div
style={{
width:45,
height:45,
borderRadius:"50%",
background:"var(--primary)",
color:"white",
display:"flex",
justifyContent:"center",
alignItems:"center",
fontWeight:"bold",
}}
>

{user?.username?.charAt(0)}

</div>

<div
    style={{
        width: 12,
        height: 12,
        borderRadius: "50%",
        background: "#10b981",
    }}
/>

<button
style={{
background:"var(--danger)",
padding:"10px 18px",
color:"white",
}}
onClick={logout}
>

Logout

</button>

</div>

</header>

);

}