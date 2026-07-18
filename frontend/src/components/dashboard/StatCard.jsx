export default function StatCard({

title,

value,

color,

}){

return(

<div

style={{

background:"var(--card)",

borderRadius:"var(--radius)",

padding:25,

boxShadow:"var(--shadow)",

borderTop:`5px solid ${color}`,

}}

>

<p
style={{
color:"var(--muted)",
marginBottom:12,
}}
>

{title}

</p>

<h2>

{value}

</h2>

</div>

);

}