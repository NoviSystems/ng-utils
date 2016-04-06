
function nOptionSort(a, b) {
    var aInt = parseInt(a.value, 10);
    var bInt = parseInt(b.value, 10);

    if (aInt > bInt)
        return 1;
    else if (aInt < bInt)
        return -1;
    return 0;
}

System.import('jquery').then(function($) {
    // setup transfer buttons
    $('[data-transfer-action="select"]').on('click', function() {
        var transferId = $(this).data('transfer-id');
        var availableSel = '[data-transfer-bucket="available"][data-transfer-id="' + transferId + '"]';
        var selectedSel = '[data-transfer-bucket="selected"][data-transfer-id="' + transferId + '"]';

        $(availableSel +' :selected').appendTo(selectedSel);
        $(selectedSel +' option').detach().sort(nOptionSort).appendTo(selectedSel);
    });

    $('[data-transfer-action="deselect"]').on('click', function() {
        var transferId = $(this).data('transfer-id');
        var availableSel = '[data-transfer-bucket="available"][data-transfer-id="' + transferId + '"]';
        var selectedSel = '[data-transfer-bucket="selected"][data-transfer-id="' + transferId + '"]';

        $(selectedSel + ' :selected').appendTo(availableSel);
        $(availableSel +' option').detach().sort(nOptionSort).appendTo(availableSel);
    });

    // setup submit
    $('[data-transfer-id]').closest('form').on('submit', function() {
        $('[data-transfer-bucket="selected"] option').prop('selected', 'selected');
    });
});
