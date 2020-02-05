var alayaToDo = (function ($, window) {
  return {
    getRequestSettings: function (url, method) {
      return {
        "url": url,
        "method": method
      }
    },
    errorHelper: function (error) {
      var _alert = $("#alert-todo-list");
      $('#myModal').modal('hide');

      _alert.removeClass("alert-success");
      _alert.addClass("alert-danger");
      _alert.find("span.feedback").text(error);
      _alert.fadeIn()
      setTimeout(function () {
        _alert.fadeOut()
      }, 2000);
    },
    doneHelper: function (response) {
      var _alert = $("#alert-todo-list");
      $('#myModal').modal('hide');

      _alert.removeClass("alert-danger");
      _alert.addClass("alert-success");
      _alert.find("span.feedback").text(response);
      _alert.fadeIn()
      setTimeout(function () {
        _alert.fadeOut()
      }, 2000);
    },
    completeToDo: function (event, url) {
      var _this = this;
      var _btn = $(event.target).is('span') 
        ? $(event.target).parent()
        : $(event.target);
      $
        .ajax(this.getRequestSettings(url, "PUT"))
        .done(function (response) {
          _btn.remove();
          _this.doneHelper(response);
        })
        .fail(_this.errorHelper)
    },
    deleteToDo: function (event, url) {
      var _modal = $('#myModal');
      var _this = this;
      var _tr = $(event.target).is('button') 
        ? $(event.target).parent().parent() 
        : $(event.target).parent().parent().parent();

      _modal.modal('show');
        _modal
          .on('shown.bs.modal', function (e) {
            $('#btn-ok')
              .off('click')
              .on('click', function (e) {
                $
                  .ajax(_this.getRequestSettings(url, "DELETE"))
                  .done(function (response) {
                    _tr.remove();
                    _this.doneHelper(response);
                  })
                  .fail(_this.errorHelper)
              });
          })
          .on('hidden.bs.modal', function (e) {
          });
    },
    showJSON: function (event, url) {
      var _modal = $('#jsonModal');
      var _this = this;

      $
        .ajax(_this.getRequestSettings(url, "GET"))
        .done(function (response) {
          _modal.find(".modal-body #pretty").append("<pre>" + JSON.stringify(response, null, 2) + "</pre>")
          _modal.find(".modal-body #raw").append(JSON.stringify(response))

          _modal.modal('show');
          _modal
            .on('shown.bs.modal', function (e) {
              $('#btn-ok')
                .off('click')
                .on('click', function (e) {
                  _modal.modal('hide');
                });
            })
            .on('hidden.bs.modal', function (e) {
              _modal.find(".modal-body #pretty").empty()
              _modal.find(".modal-body #raw").empty()
            });
        })
        .fail(_this.errorHelper)
    }
  }
})(jQuery, window);

$( document ).ready(function() {
  var _alert = $("#alert-flash")
  if (_alert.length > 0) {
    setTimeout(function () {
      _alert.fadeOut();
    }, 2000)
  }
});