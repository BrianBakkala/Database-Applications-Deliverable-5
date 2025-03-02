const NEWROW_PARAM = "newrow";



async function submitCreate(table)
{
    await dbRequest('create',
        {
            data: serializeForm(document.querySelector('form')),
            table
        });

    window.location.href = window.location.href.split("?") + "?" + NEWROW_PARAM + "=true";
}

function onloadHandler()
{
    const urlParams = getUrlParams();
    if (urlParams[NEWROW_PARAM])
    {
        newRowHandler();
    }
}
/**
 * handles the UX for a new row being added to the table
 *
 */
function newRowHandler()
{
    //scroll to bottom
    window.scrollTo(0, document.body.scrollHeight);
    window.removeUrlParam(NEWROW_PARAM);

    //highlight new row
    const row = document.querySelector('tbody tr:nth-last-of-type(2)');
    row.classList.add('highlight');
}

/**
 * handles the UX for the edit button being clicked for a certain row
 *
 * @param {*} clickedButton the clicked button
 */
function toggleEditMode(clickedButton)
{
    const parentForm = clickedButton.getParentElement('form');
    parentForm.toggleAttribute('edit-mode');
}
/**
 * handles the UX for the delete button being clicked for a certain row
 *
 * @param {*} clickedButton the clicked button
 */
function toggleDeleteMode(clickedButton)
{
    const parentForm = clickedButton.getParentElement('form');
    parentForm.toggleAttribute('delete-mode');
}