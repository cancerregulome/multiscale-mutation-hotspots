require.config({
    baseUrl: '/static/js/seqpeek_view',

    paths: {
        d3: 'vendor/d3.min',
        domReady: 'vendor/domReady',
        jquery: 'vendor/jquery-1.11.1.min',
        "jquery-ac": 'vendor/jquery-ui-autocomplete.min',
        underscore: 'vendor/underscore',
        vq: 'vendor/vq.min'
    },

    shim: { }
});


require([
    'domReady',
    './view',
    'jquery',
    'jquery-ac',
    'vq'
], function(
    domReady,
    SeqPeekViewFactory,
    __jquery,
    __jquery_ac,
    __vq
) {
    domReady(function() {
        var GENE_LIST = __static_data.gene_list;

        $('#genes').autocomplete({
            source: GENE_LIST,
            minLength: 3,
            delay: 500
        });

        $('#gene-tumor-form').on("submit", function() {
            var form = this;
            var gene = $('#genes').val().toUpperCase();

            // Check that at least one tumor type is selected.
            // .val return null if nothing is selected
            var tumor_types = $('#tumor_type_select').val() | [];
            if (tumor_types.length < 1) {
                return false;
            }

            // Check that the gene is valid
            if (GENE_LIST.lastIndexOf(gene) == -1) {
                return false;
            }

            $(form).append('<input name="gene" value="' + gene + '" type="hidden" class="plot-attr" />');
            return true;
        });

        if (typeof __data_bundle == "undefined" || __data_bundle === "undefined") {
            console.log("SeqPeek plot data bundle is undefined");
            return;
        }

        var target_table = $(document).find("#seqpeek-table")[0];
        var tableView = SeqPeekViewFactory.create(target_table, __data_bundle);
        tableView.render();
    });
});
