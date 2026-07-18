export default function EmptyState({

    title,

    description,

    button,

}) {

    return (

        <div className="empty-state">

            <h2>

                {title}

            </h2>

            <p>

                {description}

            </p>

            {button}

        </div>

    );

}