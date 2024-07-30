
//'use strict';


var stripe = Stripe('pk_test_51POs4ZP6qrjtDGURB7JPMJggiqmo27TOcemrSC7ErQuqCzkxEUFMfj53KBIVgT8S2f5rqgZILxzK80WePvbwnMvp00hDMUW6fE');

var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
  base: {
    color: "#000",
    lineHeight: '2.4',
    fontSize: '16px'
  }
};


var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function (event) {
  var displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-info');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-info');
  }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
  ev.preventDefault();

  var firstName = document.getElementById("firstName").value;
  var lastName = document.getElementById("lastName").value;
  var custAdd = document.getElementById("custAddress").value;
  var zipCode = document.getElementById("zipCode").value;


  $.ajax({
    type: "POST",
    url: 'http://localhost:8000/orders/add/',
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
    },
    success: function (json) {
      console.log(json.success)
      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address: {
              line1: custAdd
            },
            name: firstName + lastName
          },
        }
      }).then(function (result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });

    },
    error: function (xhr, errmsg, err) { },
  });



});