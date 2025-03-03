function handleInput(element, mappingKey)
{
    const convertToNumberIfPossible = (value) => isNaN(Number(value)) ? value : Number(value);

    const inputValue = convertToNumberIfPossible(element.value);
    const codeblock = document.querySelector('codeblock');
    const inputValueElement = document.querySelector('.input-value');
    if (!inputValueElement)
    {
        codeblock.innerHTML = codeblock.innerHTML.replace("?", "<div class = 'input-value'>" + inputValue + "</div>");
    }
    else
    {
        inputValueElement.innerHTML = inputValue;
    }

    runDynamicQuery(inputValue, mappingKey)
        .then(r => document.getElementById('dynamic_query_result').innerHTML = r.html)
        // .then(r => console.log(r))
        .catch(e => document.getElementById('dynamic_query_result').innerHTML = 'No results.');
}

async function runDynamicQuery(input, mappingKey)
{
    return await dbRequest('dynamic_query',
        {
            mapping_key: mappingKey,
            input
        }
    );
}