function zip() {
  var args = [].slice.call(arguments);
  var shortest = args.length==0 ? [] : args.reduce(function(a,b){
      return a.length<b.length ? a : b
  });

  return shortest.map(function(_,i){
      return args.map(function(array){return array[i]})
  });
}


function submitData() {
    var data = {
      'agent_1': $('#agent-1').find('input[name="input1"]').val(),
      'agent_2': $('#agent-2').find('input[name="input2"]').val()
    };
    
    $.ajax({
      url: '/process',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
        console.log(response)
        alert('Task is added!');
        $('b#agent-1-utility').text(response.utility_a1);
        $('b#agent-2-utility').text(response.utility_a2);
        var zipped = zip(response.a1offers, response.a2offers);
        
        let template = ``;
        let final_template = ``;
        for (let i = 0; i < zipped.length; i++){
          if (i < zipped.length -1){
            element = `
              <div class="col-md-12 mx-1">
                <div class="row">
                    <div class="col-md-1">
                      <label><b>${i+1}</b></label>
                    </div>
                    <div class="col-md-2">
                        <label for="input2"><b>Buyer <b class="text-light bg-dark"></b> Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-danger">${zipped[i][0]}</b>
                    </div>
                    <div class="col-md-3">
                        <label for="input2"><b>Seller <b class="text-light bg-dark"></b> Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-danger">${zipped[i][1]}</b>
                    </div>
                </div>
            </div>`
            template = template.concat(element)
          } else {
            final_element = `
              <div class="col-md-12 mx-1">
                <div class="row">
                    <div class="col-md-3">
                        <label for="input2"><b>Buyer <b class="text-light bg-dark">final</b> Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-success">${zipped[i][0]}</b>
                    </div>
                    <div class="col-md-3">
                        <label for="input2"><b>Seller <b class="text-light bg-dark">final</b> Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-success">${zipped[i][1]}</b>
                    </div>
                </div>
            </div>`
            final_template = final_template.concat(final_element)
          }
        }

        var html_template = new DOMParser().parseFromString(template, 'text/html');
        var rejectedDiv = document.getElementById("rejected");
        while(html_template.body.firstChild) {
          rejectedDiv.appendChild(html_template.body.firstChild);
        }

        var html_template_final = new DOMParser().parseFromString(final_template, 'text/html');
        var acceptedDiv = document.getElementById("accepted");
        while(html_template_final.body.firstChild) {
          acceptedDiv.appendChild(html_template_final.body.firstChild);
        }
        
        // Update result
        $('b#winner').text(response.winner);
        $('b#result').text(response.result);
      },
      error: function(error) {
        alert('Error sending data');
      }
    });
  }


function submitDataNewNegotiator(){
  var data = {
    'n_steps': $('#agent-1').find('input[name="input1"]').val()
  };
  
  $.ajax({
    url: '/process_new',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function(response) {
      console.log(response)
      template = `
      <img src="/static/images/${response.image}" alt="Result">
      `
      var html_template = new DOMParser().parseFromString(template, 'text/html');
      var main = document.getElementById("main");
      if (main) {
        // Replace the image
        main.replaceWith(html_template.body.firstChild);
      } else {
        while(html_template.body.firstChild) {
          main.appendChild(html_template.body.firstChild);
        }
      }

      // Rejected offers
      for (let row of response.data.slice(0, -1)) {
        var element = `
            <div class="mx-1">
                <div class="row">
                    <div class="col-md-1">
                        <label><b>${response.data.indexOf(row) + 1}</b></label>
                    </div>
                    <div class="col-md-2">
                        <label for="input2"><b>Buyer Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-danger">${row[0]}</b>
                    </div>
                    <div class="col-md-2">
                        <label for="input2"><b>Seller Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-danger">${row[1]}</b>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('rejected').innerHTML += element;
      }

      // Accepted offers
      // var element = `
      //       <div class="col-md-12 mx-1">
      //           <div class="row">
      //               <div class="col-md-3">
      //                   <label for="input2"><b>Buyer final Offer</b></label>
      //               </div>
      //               <div class="col-md-3">
      //                   <b class="text-success">${response.data[response.data.length - 1][0]}</b>
      //               </div>
      //               <div class="col-md-3">
      //                   <label for="input2"><b>Seller final Offer</b></label>
      //               </div>
      //               <div class="col-md-3">
      //                   <b class="text-success">${response.data[response.data.length - 1][1]}</b>
      //               </div>
      //           </div>
      //       </div>
      //   `;
      // document.getElementById('accepted').innerHTML += element;

      // The Winner
      var element = `
          <div class="row py-3 my-3">
              <div class="col-md-2"></div>
              <div class="col-md-8 border border-success rounded my-3">
                  <h4 style="color: #0c915e;" >        Winner : <b class="text-dark" id="winner">
                      ${response.winner || '___'}
                  </b></h4>
                  <h4 style="color: #0c915e;" >Accepted Offer : <b class="text-dark" id="result">
                      ${response.result || '___'}
                  </b></h4>
                  <h4 style="color: #0c915e;" >Steps : <b class="text-dark" id="result">
                      ${response.steps || '___'}
                  </b></h4>
                  <hr>
                  <div class="col-md-12 mx-1">
                    <div class="row">
                        <div class="col-md-3">
                            <label for="input2"><b>Buyer final Offer</b></label>
                        </div>
                        <div class="col-md-3">
                            <b class="text-success">${response.data[response.data.length - 1][0]}</b>
                        </div>
                        <div class="col-md-3">
                            <label for="input2"><b>Seller final Offer</b></label>
                        </div>
                        <div class="col-md-3">
                            <b class="text-success">${response.data[response.data.length - 1][1]}</b>
                        </div>
                    </div>
                  </div>
              </div>
          </div>
      `;
      document.getElementById('winner').innerHTML += element;

    },
    error: function(error) {
      alert('Error sending data');
    }
  });
}