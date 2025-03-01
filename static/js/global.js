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

function getUrlParams()
{
    const urlParams = new URLSearchParams(window.location.search);
    const paramsObject = {};

    urlParams.forEach((value, key) =>
    {
        paramsObject[key] = value;
    });

    return paramsObject;
}

function removeUrlParam(key)
{
    const url = new URL(window.location.href);
    url.searchParams.delete(key);  //remove parameter by key

    // update URL in the browser 
    window.history.replaceState({}, '', url);
}
