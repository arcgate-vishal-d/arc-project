// Check box validations
function checkBox() {
  var check = $("input[type='checkbox']:checked");
  for (i = 0; i < check.length; i++) {
    checked_id = check[i].getAttribute("id").slice(12);
    $("#subject_questions_" + checked_id).removeAttr("readonly");
    $("#subject_questions_" + checked_id).attr("required", true);
    $("#subject_marks_" + checked_id).removeAttr("readonly");
    $("#subject_marks_" + checked_id).attr("required", true);
    $("#subject_time_" + checked_id).removeAttr("readonly");
    $("#subject_time_" + checked_id).attr("required", true);
    $("#subject_order_" + checked_id).removeAttr("readonly");
    $("#subject_order_" + checked_id).attr("required", true);
  }
  var unchecked = $("input[type='checkbox']:not(:checked)");
  for (i = 0; i < unchecked.length; i++) {
    uncheck_id = unchecked[i].getAttribute("id").slice(12);
    $("#subject_questions_" + uncheck_id).attr("readonly", "readonly");
    $("#subject_questions_" + uncheck_id).removeAttr("required", true);
    $("#subject_marks_" + uncheck_id).attr("readonly", "readonly");
    $("#subject_marks_" + uncheck_id).removeAttr("required", true);
    $("#subject_marks_" + uncheck_id).val(null);
    $("#subject_time_" + uncheck_id).attr("readonly", "readonly");
    $("#subject_time_" + uncheck_id).removeAttr("required", true);
    $("#subject_time_" + uncheck_id).val(null);
    $("#subject_order_" + uncheck_id).attr("readonly", "readonly");
    $("#subject_order_" + uncheck_id).removeAttr("required", true);
  }
  FtotalMarks();
  FtotalTime();
}

// Maintains unique order number.
function orderNumber(ele) {
  var current_id = $(ele).attr("id");
  var currentValue = $(ele).val();
  var checked = $("input[type='checkbox']:checked");
  for (i = 0; i < checked.length; i++) {
    var id = checked[i].getAttribute("id").slice(12);
    var order_value = $("#subject_order_" + id).val();
    order_id = "subject_order_" + id;
    if (order_id !== current_id && order_value === currentValue) {
      if (order_value.trim() !== "" && order_id !== "") {
        alert(
          "This order number is already selected. Please select different number."
        );
        $("#" + current_id).val("");
      }
    }
  }
}

// counter for total marks
function FtotalMarks() {
  totalMarks = parseInt(0);
  $(".totalMarks").each(function (i, obj) {
    if ($(obj).val() !== "") {
      totalMarks += parseInt($(obj).val());
    }
  });
  $("#txtMarks").val(totalMarks);
}

// counter for total time
function FtotalTime() {
  totalTime = parseInt(0);
  $(".totalTime").each(function (i, obj) {
    if ($(obj).val() !== "") {
      totalTime += parseInt($(obj).val());
    }
  });
  $("#txtTime").val(totalTime);
}

// Show questions of selected subject
$('button').click(function () {
    var sub_table = $(this).closest('tr').next('tr').find('div');
    if (sub_table.is(':hidden')){
        $(".dynamic-subjects").hide(600);
    sub_table.show(600);
    }
      
});

// No. of questions with each subject
$('#subject-question-map-form').submit(function (evt) {
    var subjects = $('#subject-question-map-form :input[type=hidden]')

    for(let i=1; i< subjects.length; i++){
        var required_ques = (subjects[i]).getAttribute('question_count')
        var specified_sub = (subjects[i]).getAttribute('id')
        var checkbox_in_subject = $('.sub'+specified_sub+' input[type=checkbox]:checked')
        var error = $('#error'+specified_sub)

        if (required_ques > checkbox_in_subject.length){
            error.html("("+ (required_ques-checkbox_in_subject.length) +" more question needed)")
            error.css({
                "display": "", 
                "color"  : "red"
            });
            evt.preventDefault();
            return false;

        } else{
            error.attr('style','display:none')
        }
    }
});
