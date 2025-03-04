const HIGHLIGHT_ROW_PARAM = "highlight_row";


/////////////////////////
//////////CRUD OPERATIONS
/**
 * Sends a create request
 *
 * @param {*} table
 */
async function submitCreate(table)
{
    await dbRequest('create',
        {
            table,
            data: serializeForm(document.querySelector('form:has(#add-row-template)')),
        },
        () => { window.location.href = window.location.href.split("?")[0].split(",")[0] + "?" + HIGHLIGHT_ROW_PARAM + "=last"; });
}

/**
 * Sends a delete request
 *
 * @param {*} table
 * @param {*} recordId
 */
async function submitDelete(table, recordId)
{
    await dbRequest('delete',
        {
            record_id: recordId,
            table
        },
        () => window.location.reload());

}
/**
 * Sends an update request
 *
 * @param {*} clickedButton
 * @param {*} table
 * @param {*} recordId
 * @return {*} 
 */
async function submitUpdate(clickedButton, table, recordId)
{

    if (recordId == "0")
    {
        const form = document.querySelector('form:has(#add-row-template)');
        if (form.checkValidity())
        {
            submitCreate(table);
        }
        else
        {
            form.reportValidity(); // Shows validation messages
        }

        return;
    }

    await dbRequest('update',
        {
            record_id: recordId,
            table,
            data: serializeForm(clickedButton.getParentElement('form')),
        },
        () => { window.location.href = window.location.href.split("?") + "?" + HIGHLIGHT_ROW_PARAM + "=" + recordId; }
    );
}
/**
 * Fires when the page loads
 *
 */
function onloadHandler()
{
    const urlParams = getUrlParams();
    if (urlParams[HIGHLIGHT_ROW_PARAM])
    {
        highlightRow(urlParams[HIGHLIGHT_ROW_PARAM]);
    }
}
/**
 * handles the UX for a new row being added to the table
 *
 */
function highlightRow(rowId)
{
    //scroll to bottom
    let cell;
    if (rowId === 'last')
    {
        const rows = [...document.querySelectorAll('.custom-table-tbody .custom-table-tr:not(#add-row-template)')];
        cell = rows[rows.length - 1].querySelector('.custom-table-td:not(.crud-ops-button-group)');
        window.scrollTo(0, document.body.scrollHeight);
    }
    else
    {
        cell = document.querySelector('#form_row_' + rowId + " .custom-table-tr .custom-table-td:not(.crud-ops-button-group)");
    }
    console.log("highlighting row", rowId);
    console.log(cell);
    window.removeUrlParam(HIGHLIGHT_ROW_PARAM);

    //highlight new row
    cell.classList.add('highlight');
}

/**
 * handles the UX for the edit button being clicked for a certain row
 *
 */
function toggleCreateMode()
{
    const form = document.querySelector('form:has(#add-row-template)');
    form.reset();

    //show appropriate buttons
    document.querySelector('#add-row-template').toggleAttribute('hidden');
    document.querySelector('.button-group').toggleAttribute('hidden');
    document.querySelector('#add-row-template .crud-ops-button-group').toggleAttribute('invisible');

    //focus on first input
    document.querySelector('#add-row-template input').focus();

    //scroll to bottom
    window.scrollTo(0, document.body.scrollHeight);
}

/**
 * handles the UX for the edit button being clicked for a certain row
 *
 * @param {*} clickedButton the clicked button
 */
function toggleEditMode(clickedButton)
{
    const form = clickedButton.getParentElement('form');
    if (form.querySelector('#add-row-template'))
    {
        toggleCreateMode();
        return;
    }

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