function handleInput(element, mappingKey)
{
    const convertToNumberIfPossible = (value) => isNaN(Number(value)) ? value : Number(value);

    runDynamicQuery(convertToNumberIfPossible(element.value), mappingKey)
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
        , (response) =>
        {
            const codeblock = document.querySelector('codeblock');
            const inputValueText = document.querySelector('.input-value');
            if (!inputValueText)
            {
                codeblock.innerHTML = codeblock.innerHTML.replace("?", "<div class = 'input-value'>" + input + "</div>");
            }
            else
            {
                inputValueText.innerHTML = input;
            }

            return response;

        });
}