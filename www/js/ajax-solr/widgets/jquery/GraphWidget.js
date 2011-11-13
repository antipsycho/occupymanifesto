(function($) {

AjaxSolr.GraphWidget = AjaxSolr.AbstractWidget.extend({

    graph: null,
    layouter: null,
    renderer: null,

    init: function() {

        var width = $('#' + this.target).width();
        var height = $('#' + this.target).height();

        this.graph = new Graph();
        this.layouter = new Graph.Layout.Spring(this.graph);
        this.renderer = new Graph.Renderer.Raphael(this.target, this.graph, width, height);
    },

    redraw: function() {
        this.layouter.layout();
        this.renderer.draw();
    },

    afterRequest: function () {

        $('#' + self.target).empty();

        // First pass - add all documents as nodes
        for (var i = 0, l = this.manager.response.response.docs.length; i < l; i++) {
            var doc = this.manager.response.response.docs[i];
            var title = doc.title;

            if (title.length > 24) {
                title = title.substring(0, 23) + '...';
            }

            this.graph.addNode(doc.id, {label: title});
        }

        // Second pass - draw directed edges between nodes
        for (var i = 0, l = this.manager.response.response.docs.length; i < l; i++) {
            var doc = this.manager.response.response.docs[i];
            if (!doc.parent) continue;
            this.graph.addEdge(doc.id, doc.parent, {directed: true});
        }

        // Render the diagram
        this.redraw();
    }
});

})(this.jQuery)
