"use strict";
var DaterangePicker = DaterangePicker || {};
$(function() {
    DaterangePicker = {
        init: function() {
            $(".input-daterangepicker").daterangepicker(), $("#daterangepicker-1").daterangepicker({}, function(t, e, a) {
                $("#daterangepicker-1 .form-control").val(t.format("YYYY-MM-DD") + " / " + e.format("YYYY-MM-DD"))
            }), $("#daterangepicker-1_modal").daterangepicker({}, function(t, e, a) {
                $("#daterangepicker-1 .form-control").val(t.format("YYYY-MM-DD") + " / " + e.format("YYYY-MM-DD"))
            }), $("#daterangepicker-2").daterangepicker({}, function(t, e, a) {
                $("#daterangepicker-2 .form-control").val(t.format("YYYY-MM-DD") + " / " + e.format("YYYY-MM-DD"))
            }), $("#daterangepicker-3").daterangepicker({
                timePicker: !0,
                startDate: moment().startOf("hour"),
                endDate: moment().startOf("hour").add(32, "hour"),
                locale: {
                    format: "M/DD hh:mm A"
                }
            }), $("#daterangepicker-3_modal").daterangepicker({
                timePicker: !0,
                startDate: moment().startOf("hour"),
                endDate: moment().startOf("hour").add(32, "hour"),
                locale: {
                    format: "M/DD hh:mm A"
                }
            }), $("#daterangepicker-4").daterangepicker({
                singleDatePicker: !0,
                showDropdowns: !0,
                minDate: moment("2012-01-01"),
                maxDate: moment().endOf("year")
            }, function(t, e, a) {
                var r = moment().diff(t, "years");
                alert("You are " + r + " years old!")
            });
            var t = moment().subtract(29, "days"),
                e = moment();

            function a(t, e) {
                $("#daterangepicker-5 span").html(t.format("MMMM D, YYYY") + " - " + e.format("MMMM D, YYYY"))
            }

            function r(t, e) {
                $("#daterangepicker-5_modal span").html(t.format("MMMM D, YYYY") + " - " + e.format("MMMM D, YYYY"))
            }
            $("#daterangepicker-5").daterangepicker({
                startDate: t,
                endDate: e,
                ranges: {
                    Today: [moment(), moment()],
                    Tomorrow: [moment().add(1, "days"), moment().add(1, "days")],
                    "Next 7 Days": [moment(), moment().add(6, "days")],
                    "Next 30 Days": [moment(), moment().add(29, "days")],
                    "This Month": [moment().startOf("month"), moment().endOf("month")],
                    "Next Month": [moment().add(1, "month").startOf("month"), moment().add(1, "month").endOf("month")]
                }
            }, a), a(t, e), $("#daterangepicker-5_modal").daterangepicker({
                startDate: t,
                endDate: e,
                ranges: {
                    Today: [moment(), moment()],
                    Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
                    "Last 7 Days": [moment().subtract(6, "days"), moment()],
                    "Last 30 Days": [moment().subtract(29, "days"), moment()],
                    "This Month": [moment().startOf("month"), moment().endOf("month")],
                    "Last Month": [moment().subtract(1, "month").startOf("month"), moment().subtract(1, "month").endOf("month")]
                }
            }, r), r(t, e)
        }
    }, $(document).ready(DaterangePicker.init)
});