// $('body').on('click', '#nav-button', function(){
//     console.log("button cliked");
//     let state = $(this).parents('nav').find('.navbar-collapse').hasClass('show');
//     console.log("state=",state);
//     if(state==false){
//         var body = document.querySelector("body");
//         body.classList.remove("body");
//         body.classList.add("body-collapse");
//     }
//     if(state==true){
//         var body = document.querySelector("body");
//         body.classList.remove("body-collapse");
//         body.classList.add("body");
//     }

// });


// $('body').on('click', '.nav-link', function(){
//     console.log('nav-link-clicked');
//     $(this).parents('nav').find('.navbar-collapse').removeClass('show');
//     $(this).parents('.body-collapse').removeClass("body-collapse");
// });
// let qrUrl = 'https://staging.medicause.in/get-app';

    console.log('helllo')
    let qrUrl = 'https://staging.medicause.in/get-app';
    let qrcodeContainer = document.getElementById("qr-code-block");
    qrcodeContainer.innerHTML = "";
    new QRCode(qrcodeContainer, {
        text: qrUrl,
        width: 300,
        height: 300,
    });
    document.body.appendChild(qrcodeContainer);
    console.log('byeeeeeeeee')


$('#qr-download-btn').click(function(){
    html2canvas(document.getElementById('qr-code-block'),		{
        allowTaint: true,
        useCORS: true
    }).then(function (canvas) {
        console.log(canvas);
        console.log(canvas.toDataURL());
        var a = document.createElement('a');
        a.href = canvas.toDataURL();
        a.download = 'medicause_app_qr.png';
        a.click();
    });
});       

$('#contact-form').submit(function(e){
    e.preventDefault()
    debugger;
    var data = $('#contact-form').serializeArray();
    jQuery.ajax({
        type: "POST",
        // url: `https://staging.medicause.in/api/v1/get-in-touch`,
        url: `https://staging.medicause.in/api/v1/get-in-touch`,
        dataType: "JSON",
        data: data,
        success: function (response) {
            console.log(response);
            alert('Thanks for submitting your enquiry');
            location.reload();
        },
        error: function (error) {
            console.log(error);
        },
    });
});
