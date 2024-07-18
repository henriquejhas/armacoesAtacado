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
                doc.querySelector("#encriptedCard").value = encrypted;
                formCard.submit();
            }

            console.log("encrypted: " + encrypted);
            console.log("hasErros: " + hasErrors);
            console.log(errors);
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