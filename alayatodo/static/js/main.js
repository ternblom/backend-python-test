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
      if (error.status === 200) {
        _alert.find("span.feedback").text(error);
      }
      else {
        _alert.find("span.feedback").text($(error.responseText).text());
      }
      _alert.fadeIn()
      setTimeout(function () {
        _alert.fadeOut()
      }, 2000);
    },
    doneHelper: function (response, deletedEl) {
      var _alert = $("#alert-todo-list");
      $('#myModal').modal('hide');

      _alert.removeClass("alert-danger");
      _alert.addClass("alert-success");
      _alert.find("span.feedback").text(response);
      _alert.fadeIn()
      setTimeout(function () {
        _alert.fadeOut()
        if ($("table form").length === 1 || (deletedEl && $("table form").length === 0)) {
          var url = new URLSearchParams(window.location.search);
          var page = url.get('page') ? parseInt(url.get('page')) : 1;
          if ($("table tbody").children().length === 1) {
            window.location = "/todo?page=" + (page > 1 ? page - 1 : 1);
          }

          if (deletedEl && $("table form").length === 0) {
            window.location = "/todo"
          }
        }
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
          _this.doneHelper(response, false);
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
                    _this.doneHelper(response, true);
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
    },
    reloadPage: function (event) {
      var value = $("select option:selected").text()
      var page = 1;
      window.location = "/todo?page=" + page + "&per_page=" + value
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

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          var csrf_token = document.querySelector("meta[name='csrf-token']").getAttribute("content");
          xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
  });
});