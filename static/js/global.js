async function dbRequest(command, object)
{
    return await fetch('/request/' + command, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(object),
    });
}

function serializeForm(form)
{
    return Array.from(new FormData(form).entries())
        .reduce((data, [key, value]) => ({ ...data, [key]: value }), {});
}