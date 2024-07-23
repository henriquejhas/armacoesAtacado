(function(win,doc){
    'use script';
    if(doc.querySelector('#formCard')){
        let formCard = doc.querySelector("#formCard");
        formCard.addEventListener('submit', (e) =>{
            e.preventDefault();
            const card = PagSeguro.encryptCard({
              publicKey: doc.querySelector("#publicKey").value,
              holder: doc.querySelector("#cardHolder").value,
              number: doc.querySelector("#cardNumber").value.replace(/\s/g, ""),
              expMonth: doc.querySelector("#cardMonth").value,
              expYear: doc.querySelector("#cardYear").value,
              securityCode: doc.querySelector("#cardCVV").value
            });

            const encrypted = card.encryptedCard;
            const hasErrors = card.hasErrors;
            const errors = card.errors;
            if(!hasErrors){
                $("#loading").css("display", "flex")
                doc.querySelector("#encriptedCard").value = encrypted;
                formCard.submit();
            }

            console.log("encrypted: " + encrypted);
            console.log("hasErros: " + hasErrors);

            console.log(errors[0]['code']);

            if(errors[0]['code'] == 'INVALID_NUMBER'){
                mensagemR("Número do cartão inválido");
            }else if(errors[0]['code'] == 'INVALID_HOLDER'){
                mensagemR("Nome do titular inválido");
            }else if(errors[0]['code'] == 'INVALID_EXPIRATION_MONTH'){
                mensagemR("Mês de validade inválido");
            }else if(errors[0]['code'] == 'INVALID_EXPIRATION_YEAR'){
                mensagemR("Ano de validade inválido");
            }else if(errors[0]['code'] == 'INVALID_SECURITY_CODE'){
                mensagemR("código de segurança CVV inválido");
            }
        })
    }

    var sitekey = $("#sitekey").text()

    grecaptcha.ready(function() {
      grecaptcha.execute(sitekey, {action: 'submit'}).then(function(token) {
          // Add your logic to submit to your backend server here.
          $("#formCard").append('<input type="hidden" name="sitetoken" value="' + token + '">');
      });
    });


})(window, document);