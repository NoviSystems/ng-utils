System.import('jquery').then(function ($) {
    n_option_sort = function (a, b) {
        a_int = parseInt(a.value, 10);
        b_int = parseInt(b.value, 10);

        if (a_int > b_int) { return 1; }
        else if (a_int < b_int) { return -1; }
        else { return 0; }
    };

    // setup transfer buttons
    $('[data-transfer-action="select"]').on('click', function () {
        var transfer_id = $(this).data('transfer-id');
        var available_sel = '[data-transfer-bucket="available"][data-transfer-id="'+transfer_id+'"]';
        var selected_sel = '[data-transfer-bucket="selected"][data-transfer-id="'+transfer_id+'"]';

        $(available_sel+' :selected').appendTo(selected_sel);
        $(selected_sel +' option').detach().sort(n_option_sort).appendTo(selected_sel);
    });

    $('[data-transfer-action="deselect"]').on('click', function () {
        var transfer_id = $(this).data('transfer-id');
        var available_sel = '[data-transfer-bucket="available"][data-transfer-id="'+transfer_id+'"]';
        var selected_sel = '[data-transfer-bucket="selected"][data-transfer-id="'+transfer_id+'"]';

        $(selected_sel+' :selected').appendTo(available_sel);
        $(available_sel +' option').detach().sort(n_option_sort).appendTo(available_sel);
    });

    // setup submit
    $('[data-transfer-id]').closest('form').on('submit', function () {
        $('[data-transfer-bucket="selected"] option').prop('selected', 'selected');
    });
});
