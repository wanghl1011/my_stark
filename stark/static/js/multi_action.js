$(document).ready(function () {
    // $(".multi-btn").on("click",function () {
    //     var action=$(".action-select").val();
    //     var arr=[];
    //     $(".checkbox:checked").each(function () {
    //         var num=parseInt($(this).parent().next().text());
    //         arr.push(num)
    //     });
    //     console.log(arr);
    //     $.ajax({
    //         url:location.href,
    //         type:"post",
    //         data:{
    //             "action":action,
    //             "arr":JSON.stringify(arr)
    //         },
    //         headers:{"X-CSRFToken":$.cookie('csrftoken')},
    //         success:function (data) {
    //             if (data.sta === 1){
    //                 console.log("ojbk");
    //                 location.href=data.url
    //             }
    //         }
    //
    //     })
    // })
    var $checkbox=$(".checkbox");
    $(".total-check").on("click",function () {
        if ($(this).prop("checked")){
            $checkbox.prop("checked",true)
        }else{
            $checkbox.prop("checked",false)
        }
    });
    $checkbox.on("click",function () {
        if (!$(this).prop("checked")){
            $(".total-check").prop("checked",false)
        }
        var num=0;
        $checkbox.each(function () {
            if ($(this).prop("checked")){ num +=1; }
        });
        if (num === $checkbox.length){
            $(".total-check").prop("checked",true)
        }
    })
});
// 把ID字段放到第二位，每次循环选中的多选标签时，就找它的下一个td就是主键，把这个主键
// push到一个数组中，ajax把这个数组传过去