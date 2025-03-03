function handleInput(element, mappingKey)
{
    runDynamicQuery(element.value, mappingKey);
}

async function runDynamicQuery(input, mappingKey)
{
    await dbRequest('dynamic_query',
        {
            mapping_key: mappingKey,
            input
        }
        , (response) =>
        {
            document.getElementById('dynamic_query_result').innerHTML = response.html;
        });
}