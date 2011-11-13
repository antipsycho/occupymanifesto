(function($) {

  $(document).ready(function() {

    var Manager = new AjaxSolr.Manager();
    Manager.addWidget(new AjaxSolr.ArborWidget({
        'id': 'graph',
        'target': '#viewport'
    }));

    Manager.init();
    Manager.store.addByValue('q', '*:*');

    var params = {
      facet: true,
      'facet.field': [ 'path' ],
      'facet.limit': 5,
      'facet.mincount': 1
    };
    for (var name in params) {
      Manager.store.addByValue(name, params[name]);
    }

    Manager.doRequest();
  })
})(this.jQuery)
