require.config({
    baseUrl: '/static/js/seqpeek_view',

    paths: {
        d3: 'vendor/d3.min',
        domReady: 'vendor/domReady',
        jquery: 'vendor/jquery-1.11.1.min',
        underscore: 'vendor/underscore',
        vq: 'vendor/vq.min'
    },

    shim: { }
});


require([
    'domReady',
    './view',
    'vq'

], function(
    domReady,
    SeqPeekViewFactory,
    vq
) {
    domReady(function() {
        if (typeof __data_bundle == "undefined" || __data_bundle === "undefined") {
            console.log("SeqPeek plot data bundle is undefined");
            return;
        }

        var target_table = $(document).find("#seqpeek-table")[0];
        var tableView = SeqPeekViewFactory.create(target_table, __data_bundle);
        tableView.render();
    });
});
