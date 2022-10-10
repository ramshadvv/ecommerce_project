

                                                           if (document.querySelector('input[name="payment"]')) {
                                                                document.querySelectorAll('input[name="payment"]').forEach((elem) => {
                                                                elem.addEventListener("change", function(event) {
                                                                    var item = event.target.value;
                                                                    console.log(item);
                                                                    var action = this.dataset.action
                                                                    console.log(action)
                                                                    placeOrder(item,action)
                                                                });
                                                                });
                                                            }

                                                            function placeOrder(item,action){
                                                                console.log('user in logged in ,sending data....')
                                                                var url = '/place_order/'
                                                                fetch(url,{
                                                                  method:'POST',
                                                                  headers:{'content-Type':'application/json',
                                                                  'X-CSRFToken':csrftoken,
                                                                },
                                                                body:JSON.stringify({'action':action,'payment':item})
                                                              
                                                                })
                                                                .then((response)=>{
                                                                  return response.json()
                                                                })
                                                                .then((data)=>{
                                                                  console.log('data:',data)
                                                                 // location.reload()
                                                                  
                                                                })
                                                              }
                                                   


// ////////////////////////////////////////////////////////////////////////////

                                                            //   <script type = 'text/javascript'>

                                                              var blah  = document.getElementsByName('blah')
                                                              function validation(){
                                                  
                                                                  if(validateName()==true && validateSecondName()==true && validateEmail()==true && validateNumber()==true){
                                                                      
                                                                      var form =    $('#form-id').serialize() 
                                                                      console.log(form)
                                                                      $("#form-id").ajaxSubmit({url: 'checking_address', type: 'post'})
                                                  
                                                                  }
                                                                  
                                                                  else{
                                                                      alert("Please fill the fields")
                                                                  
                                                                  }
                                                                  }
                                                                  function validateNumber(){
                                                                      var number= $('#billing-phone').val();
                                                                      var NumberPattern= /^\d{10}$/
                                                                      if(number==""){
                                                                      $('#enter-number').html("Enter Phone number");
                                                                          return false
                                                                      }else if(number.match(NumberPattern)){
                                                                      $('#enter-number').html("");
                                                                          return true
                                                                      }else{
                                                                      $('#enter-number').html("Enter valid the Phone number");
                                                                          return false
                                                                      }
                                                                  }
                                                                  
                                                                  function validateEmail(){
                                                                  var email = $('#billing-email').val();
                                                                  var patternemail = /^[^]+@[^]+\.[a-z]{2,3}$/
                                                                  if(email==""){
                                                                      $('#enter-email').html("Enter the Email");
                                                                          return false
                                                                      }else if(email.match(patternemail)){
                                                                      $('#enter-email').html("");
                                                                          return true
                                                                      }else{
                                                                      $('#enter-email').html("Enter the valid Email");
                                                                          return false
                                                                      }
                                                                  }
                                                                  
                                                                  function validateName(){
                                                                  var name= $('#billing-fname').val();
                                                                  var patternName=/^[A-Za-z]+$/;
                                                                  
                                                                  if(name==""){
                                                                      $('#enter-name').html("Enter first name");
                                                                          return false
                                                                      }else if(name.match(patternName)){
                                                                      $('#enter-name').html("");
                                                                          return true
                                                                      }else{
                                                                      $('#enter-name').html("Enter Correct Name");
                                                                          return false
                                                                      }
                                                                  }
                                                                  
                                                                  function validateSecondName(){
                                                                  var secondName= $('#billing-lname').val();
                                                                  var pattern=/^[A-Za-z]+$/
                                                                  if(secondName==""){
                                                                      $('#enter-lastname').html("Enter the last name");
                                                                          return false
                                                                      }else if(secondName.match(pattern)){
                                                                      $('#enter-lastname').html("");
                                                                          return true
                                                                      }else{
                                                                      $('#enter-lastname').html("Enter last name");
                                                                          return false
                                                                      }
                                                                  }
                                                              
                                                                  function validateHousename(){
                                                                      var secondName= $('#billing-house-name').val();
                                                                      var pattern=/^[A-Za-z]+$/
                                                                      if(secondName==""){
                                                                          $('#enter-housename').html("Enter your house name or Building name");
                                                                              return false
                                                                          }else if(secondName.match(pattern)){
                                                                          $('#enter-housename').html("");
                                                                              return true
                                                                          }else{
                                                                          $('#enter-housename').html("Enter your house name or Building name");
                                                                              return false
                                                                          }
                                                                      }
                                                  
                                                  
                                                                  function validateStreetName(){
                                                                      var secondName= $('#billing-street').val();
                                                                      var pattern=/^[A-Za-z]+$/
                                                                          if(secondName==""){
                                                                              $('#enter-street-name').html("Enter your street name or  area");
                                                                                  return false
                                                                              }else if(secondName.match(pattern)){
                                                                              $('#enter-streetname').html("");
                                                                                  return true
                                                                              }else{
                                                                              $('#enter-streetname').html("Enter your street name or  area");
                                                                                  return false
                                                                              }
                                                                          }
                                                                  function validateState(){
                                                                          var secondName= $('#billing-state').val();
                                                                          var pattern=/^[A-Za-z]+$/
                                                                              if(secondName==""){
                                                                                  $('#enter-state').html("Enter your state");
                                                                                      return false
                                                                                   }else if(secondName.match(pattern)){
                                                                                  $('#enter-state').html("");
                                                                                      return true
                                                                                  }else{
                                                                                   $('#enter-state').html("Enter your state");
                                                                                      return false
                                                                                      }
                                                                                  }
                                                                          
                                                                  function validateTown(){
                                                                          var secondName= $('#billing-town-city').val();
                                                                          var pattern=/^[A-Za-z]+$/
                                                                               if(secondName==""){
                                                                                          $('#enter-town').html("Enter your town or city ");
                                                                                              return false
                                                                                          }else if(secondName.match(pattern)){
                                                                                          $('#enter-town').html("");
                                                                                              return true
                                                                                          }else{
                                                                                          $('#enter-town').html("Enter your town or city");
                                                                                              return false
                                                                                          }
                                                              
                                                                                      }
                                                                      function validateCountry(){
                                                                          var secondName= $('#billing-country').val();
                                                                              var pattern=/^[A-Za-z]+$/
                                                                                  if(secondName==""){
                                                                                          $('#enter-country').html("Enter your country");
                                                                                              return false
                                                                                           }else if(secondName.match(pattern)){
                                                                                          $('#enter-country').html("");
                                                                                                  return true
                                                                                               }else{
                                                                                          $('#enter-country').html("Enter your country");
                                                                                                  return false
                                                                                               }
                                                                              
                                                                                              }                              
                                                  
                                                                      function validatePostcode(){
                                                                          var number= $('#billing-zip').val();
                                                                          var NumberPattern= /^\d{6}$/
                                                                                  if(number==""){
                                                                                      $('#enter-postcode').html("Enter postcode");
                                                                                          return false
                                                                                  }else if(number.match(NumberPattern)){
                                                                                       $('#enter-postcode').html("");
                                                                                          return true
                                                                                  }else{
                                                                                      $('#enter-postcode').html("Enter valid the postcode");
                                                                                          return false
                                                                                              }
                                                                                          }
                                                     
                                                  
                                                              
                                                  
              ///////////////////////////////////////