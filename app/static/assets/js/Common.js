function SavedSuccessfully() {
  $(".alert-success h5").html("Saved successfully.");
  $(".alert-success").show();
  window.setTimeout(function () {
    $(".alert-success").hide();
  }, 3000);
  return false;
}

function DeletedSuccessfully() {
  $(".alert-success h5").html("Deleted successfully.");
  $(".alert-success").show();
  window.setTimeout(function () {
    $(".alert-success").hide();
  }, 3000);
  return false;
}

function ErrorInSaved() {
  $(".alert-danger").show();
  window.setTimeout(function () {
    $(".alert-danger").hide();
  }, 3000);
  return false;
}

function ShowError(Message) {
  $(".alert-danger h5").html(Message);
  $(".alert-danger").show();
  window.setTimeout(function () {
    $(".alert-danger").hide();
  }, 5000);
  return false;
}

function Showinfo(Message) {
  $(".alert-info h5").html(Message);
  $(".alert-info").show();
  window.setTimeout(function () {
    $(".alert-info").hide();
  }, 3000);
  return false;
}

function ShowSuccess(Message) {
  $(".alert-success h5").html(Message);
  $(".alert-success").show();
  window.setTimeout(function () {
    $(".alert-success").hide();
  }, 3000);
  return false;
}

$(".sign_out").click(function () {
  if (confirm("Are you sure you want to sign out?")) {
    var href = $(".sign_out");
    $(".sign_out[href]").attr("href", "/logout");
  } else {
    return false;
  }
});
