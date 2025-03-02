/**
 *	Gets the ancestor element of the passed element which matches selector
 *
 * @param {element} element - reference element
 * @param {string} selector - selector for parent to match
 * @return {element} - parent element
 */
HTMLElement.prototype.getParentElement = function (selector)
{
    var tempParent = this;

    while (!tempParent.matches(selector))
    {
        tempParent = tempParent.parentElement;
    }

    if (tempParent)
    {
        return tempParent;
    }
    return false;
};


/**
 * Makes a request to the server and queries the database according to one of the registered commands
 *
 * @param {*} command the name of the function to be called on the server in resources/py/request_commands.py
 * @param {*} object the data to send in the request
 
 */
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
/**
 * Grabs the data from a form element and serializes it into a JSON object
 *
 * @param {*} form the element to grab the data from
 * @return {*} 
 */
function serializeForm(form)
{
    return Array.from(new FormData(form).entries())
        .reduce((data, [key, value]) => ({ ...data, [key]: value }), {});
}
/**
 * gets the url parameters and returns them as an object
 *
 * @return {JSON} 
 */
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
/**
 * removes a parameter from the url
 *
 * @param {*} key the key of the parameter to remove
 */
function removeUrlParam(key)
{
    const url = new URL(window.location.href);
    url.searchParams.delete(key);  //remove parameter by key

    // update URL in the browser 
    window.history.replaceState({}, '', url);
}
