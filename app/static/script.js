function handleSubmit() {
    // Find all checked checkboxes
    const checkboxes = document.querySelectorAll('.checkbox:checked');
    // Loop through each checked checkbox and log its value
    let docsJSON = {
        "files":[]
    }
    checkboxes.forEach(checkbox => {
        docsJSON.files.push(checkbox.value)
    });
    console.log(docsJSON);
    send_json_to_endpoint('/multiple-docs-query', docsJSON)
    // Do whatever else you need to do with the checked checkboxes here...
}

function send_json_to_endpoint(endpoint, json_variable){
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_variable)
    })
    .then(function(response) {
        console.log(response);
        window.location.href = '/query_form';
    })
    .catch(function(error) {
        console.error(error);
    });
}