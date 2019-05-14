$(".btn").click(function () {
    $.ajax({
        url: "",
        type: "post",
        data: {
            title: $("#title").val(),
            price: $("#price").val(),
            publish_date: $("#publish_date").val(),
            publish: $("#publish").val(),
            author: $("#author").val().toString(),
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
        },
        success: function (data) {
            if (data.error) {
                $(".error").text(data.error);
                setTimeout(function () {
                    $(".error").text("");
                }, 3000)

            }
            else {
                location.href = "/index/"

            }
        }
    })

});