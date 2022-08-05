function bin(){
$('#captcha-btn').on('click',function (event){
    var $this=$(this);
   var email =$("input[name='email']").val();
   if (!email){
       alert('请先输入邮箱！');
       return;
   }
   //通过js发送请求：ajax
    $.ajax({
        url:'/user/captcha',
        method:'POST',
        data:{'email':email},
        success:function (res){
            var code =res['code'];
            if(code==200){
                $this.off('click');
                var countDown=60;
                var timer = setInterval(function (){
                     countDown-=1;
                    if (countDown>0){
                        $this.text(countDown+'秒后重新发送');
                    }else{
                        $this.text('获取验证码');
                        bin();
                        //如果不需要倒计时，要清除倒计时，否则会一直执行
                        clearInterval(timer);
                    }
                },1000);
                alert('验证码发送成功');
            }else{
                alert(res['message']);
            }
        }
    })
});
}
$(function (){
    bin();
});