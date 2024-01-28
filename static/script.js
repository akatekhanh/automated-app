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
        return true;
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
                        <label for="input2"><b>Agent 1 <b class="text-light bg-dark"></b> Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-danger">${zipped[i][0]}</b>
                    </div>
                    <div class="col-md-3">
                        <label for="input2"><b>Agent 2 <b class="text-light bg-dark"></b> Offer</b></label>
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
                        <label for="input2"><b>Agent 1 <b class="text-light bg-dark">final</b> Offer</b></label>
                    </div>
                    <div class="col-md-3">
                        <b class="text-success">${zipped[i][0]}</b>
                    </div>
                    <div class="col-md-3">
                        <label for="input2"><b>Agent 2 <b class="text-light bg-dark">final</b> Offer</b></label>
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