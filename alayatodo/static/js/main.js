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