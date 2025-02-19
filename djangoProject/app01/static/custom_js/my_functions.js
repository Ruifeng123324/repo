function jqry() {
    $.ajax({
        url: '/orm_test/',
        type: 'get',
        data: {
            n1: 123,
            n2: 456
        },
        success: function (res) {
            console.log('send succsess')
        }
    })
}


// jquery 在dom load 完成后给标签绑定方法


$(document).ready(() => {

    $('#bt1').click(function () {
        // $('.item').toggle('slow')        # hide 和show 反复切换
        $('#demo1').append("<div>末尾追加一个div</div>", "<div>第二个参数</div>").prepend("<div>末尾追加一个div</div>");

    });

    $('#bt2').click(
        () => {
            $('#demo1').empty('#id1')
        }
    );

    $('#bt3').click(
        () => {
            $('#demo1').css(
                {
                    'background-color': 'orange',
                    "font-size": "200%"
                }
            ).width('1000px');
            console.log($('#demo1').html())
        }
    );

    $('#jq_test1').click(
        () => {
            $('#test1').load('test.txt')
        }
    );


    $('#jq_test2').click(
        () => {
            $.ajax({
                url: '/orm_test/',
                type: 'get',
                dataType: 'json',
                data: {
                    text: '这是一条jquery ajax request',
                    name: 'aikun',
                    interest: 'black fans'
                },
                success: function (res) {
                    console.log('发送get 请求，收到返回数据： ', res)
                }
            })
        }
    );


    $('#jq_test3').click(
        () => {
            $.ajax({
                url: '/orm_test/',
                type: 'post',
                dataType: 'json',
                data: {
                    n1: 123,
                    n2: 456
                },
                success: function (res) {
                    console.log('发送post 请求，接收到server返回数据a：', res)
                }
            })
        }
    );


    $('#form-sutmit').click(
        () => {
            $.ajax({
                url: '/orm_test/',
                type: 'post',
                dataType: 'json',
                data: $('#form1').serialize(),
                success: function (res) {
                    console.log(res)
                }
            })
        });


    $('#form3sbm').click(
        () => {
            $.ajax({
                url: '/task/',
                type: 'post',
                dataType: 'json',
                data: $('#form2').serialize(),
                success: function (res) {
                    if (res.status) {
                        alert('success')
                    } else {
                        alert('failed')
                    }
                }
            })
        }
    );

    $('#bt-add-modal').click(
        function () {
            edit_uid = undefined
            $('#form-order-add')[0].reset();
            $('#myModal').modal('show')
        }
    );
    var edit_uid;
    $('#order-btn-save').click(
        function () {
            if (edit_uid) {
                console.log('it\'s edit');
                $.ajax({
                    url: '/order_edit/' + '?uid=' + edit_uid,
                    type: 'POST',
                    dataType: 'json',
                    data: $('#form-order-add').serialize(),
                    success: function (res) {
                        console.log(res)
                        if (res.status) {
                            $('#result').text('Submit Success');
                            $('#myModalLabel').text('Create Order');
                            // 清空form
                            $('#form-order-add')[0].reset();
                            // 关闭modal
                            $('#myModalAdd').modal('hide');
                            // 刷新页面
                            location.reload();
                        } else {
                            console.log(res.errors)
                            $.each(res.errors, function (name, error_list) {
                                $('#id_' + name).next().text(error_list[0])
                            })
                        }
                    }
                })
            } else {
                $.ajax({
                    url: '/order_list/',
                    type: 'POST',
                    dataType: 'json',
                    data: $('#form-order-add').serialize(),
                    success: (res) => {
                        if (res.status) {
                            $('#result').text('Submit Success');
                            $('#myModalLabel').text('Create Order');

                            // 清空form
                            $('#form-order-add')[0].reset();
                            alert('tt');
                            // 关闭modal
                            $('#myModalAdd').modal('hide');
                            // 刷新页面
                            location.reload();


                        } else {
                            console.log(res.errors)
                            $.each(res.errors, function (name, error_list) {
                                $('#id_' + name).next().text(error_list[0])
                            })
                        }

                    }
                })
            }
        }
    );

    var del_id
    $('.btn-delete').click(
        function () {
            $('#myModalDel').modal('show');
            var uid = $(this).attr("uid");
            console.log('oid to be del is ', uid);
            del_id = uid

        }
    );
    //点击确认后将全局变量del_id
    $('#confirm-del').click(
        function () {
            $.ajax({
                url: '/order_del/',
                type: 'GET',
                data: {oid: del_id},
                dataType: 'json',
                success: function (res) {
                    if (res.status) {
                        alert('success')
                        $('#myModalDel').modal('hide')
                        location.reload();
                        //重置del_id
                        del_id = 0
                    } else {
                        alert('failed')
                    }
                }
            })
        }
    );


    $('.btn-edit').click(
        function () {
            var current_uid = $(this).attr('uid');
            console.log('current_uid is', current_uid);
            edit_uid = current_uid;

            console.log('edit_uid is', edit_uid);
            $.ajax({
                url: '/order_detail/',
                type: 'GET',
                dataType: 'json',
                data: {uid: current_uid, edit_uid: edit_uid},
                success: function (res) {
                    if (res.status) {
                        // console.log(res.data)
                        //修改对话框标题
                        $.each(res.data, function (name, value) {
                                console.log(name, value)
                                $('#id_' + name).val(value);
                            }
                        );
                        $('#myModalLabel').text('Edit Order');
                        $('#myModalAdd').modal('show');
                    }
                }
            })
        }
    )


});










