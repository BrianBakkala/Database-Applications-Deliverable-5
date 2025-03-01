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


function toggleCreateMode()
{
    const form = document.querySelector('form');
    form.reset();

    //show appropriate buttons
    document.querySelector('#add-row-template').toggleAttribute('hidden');
    [...document.querySelectorAll('.button-group button')].forEach(x => x.toggleAttribute('hidden'));

    //focus on first input
    document.querySelector('#add-row-template input').focus();
    console.log(document.querySelector('#add-row-template input'));

    //scroll to bottom
    window.scrollTo(0, document.body.scrollHeight);
}

function onloadHandler()
{
    const urlParams = getUrlParams();
    if (urlParams[NEWROW_PARAM])
    {
        newRowHandler();
    }
}

function newRowHandler()
{
    //scroll to bottom
    window.scrollTo(0, document.body.scrollHeight);
    window.removeUrlParam(NEWROW_PARAM);

    //highlight new row
    const row = document.querySelector('tbody tr:nth-last-of-type(2)');
    row.classList.add('highlight');
}