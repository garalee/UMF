
function getResultCount(query){
    $('#lst-ib').value = query
    $('form[name="f"]').submit()

    $('#resultStats').innerHTML