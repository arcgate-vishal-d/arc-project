//  Image Preview
$('input').click(function () {
  var id = $(this).attr('id');
  $('#' + id).change(function () {
      const file = this.files[0];
      if (file) {
          let reader = new FileReader();
          reader.onload = function (event) {
              pre_id = id.slice(11,)
              $("#" + pre_id).attr("src", event.target.result);
          };
          reader.readAsDataURL(file);
      }
  });
});

//  Image Validations
window.Parsley.addValidator("maxFileSize", {
  validateString: function (_value, maxSize, parsleyInstance) {
    var files = parsleyInstance.$element[0].files;
    return files.length != 1 || files[0].size <= maxSize * 1000;
  },
  requirementType: "integer",
  messages: {
    en: "This file should not be larger than %s Kb",
  },
});

// custom image validations
window.ParsleyValidator.addValidator(
  "fileextension",
  function (value, requirement) {
    allowed_extensions = requirement.split(",");
    var fileExtension = value.split(".").pop();
    for (i = 0; i < allowed_extensions.length; i++) {
      if (fileExtension == allowed_extensions[i]) {
        return true;
      }
    }
    return false;
  },
  32
).addMessage("en", "fileextension", "The extension must be jpg, jpeg, png");
