(function($) {

AjaxSolr.GraphWidget = AjaxSolr.AbstractWidget.extend({

    graph: null,
    layouter: null,
    renderer: null,

    init: function() {
        this.graph = new Graph();
        this.layouter = new Graph.Layout.Spring(this.graph);
        this.renderer = new Graph.Renderer.Raphael(this.target, this.graph);
    },

    redraw: function() {
        this.layouter.layout();
        this.renderer.draw();
    },

    afterRequest: function () {
        for (var i = 0, l = this.manager.response.response.docs.length; i < l; i++) {
            var doc = this.manager.response.response.docs[i];
            if (!doc.parent) continue;

            this.graph.addEdge(doc.id, doc.parent, {'directed': true});
        }
        this.redraw();
    }
});

})(this.jQuery)
