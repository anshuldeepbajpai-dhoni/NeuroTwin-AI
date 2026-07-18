import { useAuth } from "../../context/AuthContext";

export default function WelcomeCard(){

const {user}=useAuth();

return(

<div

style={{

background:

"linear-gradient(135deg,#2563eb,#4338ca)",

padding:35,

borderRadius:20,

color:"white",

marginBottom:30,

boxShadow:"var(--shadow)",

}}

>

<h1>

Welcome,

{user?.username}

👋

</h1>

<p>

Your Digital Twin platform is ready.

</p>

</div>

);

}