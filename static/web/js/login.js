

    // 登录验证
    $(".login_btn").click(function () {

        $.ajax({
            url: "/login/",
            type: "post",
            data: {
                user: $("#user").val(),
                pwd: $("#pwd").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                if (data.user) {
                    if (location.search){
                        location.href = location.search.slice(6)
                    }
                    else {
                         location.href = "/index/"
                    }

                }
                else {
                    $(".error").text(data.error);
                    setTimeout(function(){
                         $(".error").text("");
                    },1000)

                }
            }
        })

    });