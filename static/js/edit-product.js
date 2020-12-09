$(function() {
    $("#expire_date").datepicker({
      defaultDate: "10/22/2020"
    });
  });

  window.onload = function(){
    
    $.ajax({
            data : {
                id : JSON.parse(localStorage.getItem("product-item"))
                    }, 	
                type : 'POST',
                url : '/shoes-id'
                })
            .done(function(data) {
     console.log(data)
      
      name = `  <input
                  id="input-name"
                  name="input-name"
                  type="text"
                  value="${data[0].name}"
                  class="form-control validate"
                />`
      $('#name').append(name)
      
      price = `  <input
      id="input-price"
      name="input-price"
      type="number"
      value="${data[0].price}"
      class="form-control validate"
    />`

      $('#price').append(price)


      description = `<textarea                    
                  class="form-control validate tm-small"
                  rows="5"
                  required
                  id = "input-description"
                > ${data[0].description}
                </textarea>`
      $('#description').append(description)
      
    
      localStorage.setItem("shoes", JSON.stringify(data[0].id))
      setCookie('shoes', data[0].id, 1)
        

      let  silde_image = `<div class="carousel-item active">
      <img src ='${data[0].list_image[0].image}' onclick="document.getElementById('fileInput-1').click();" id="img-1" class="d-block w-100" alt="...">
      <div class="carousel-caption d-none d-md-block">
        
      
      </div>
    </div>` 
    var index = 0
    
    for(var i = 2; i < 7; i++){
        for (var j = 1; j < data[0].list_image.length; j++){
            if( i == data[0].list_image[j].index_image){
                silde_image += `<div class="carousel-item">
                    <img src ='${data[0].list_image[j].image}' onclick="document.getElementById('fileInput-${i}').click();" id="img-${i}" class="d-block w-100" alt="...">
                    <div class="carousel-caption d-none d-md-block">
                    </div>
                    </div>` 
                index = 1
            }
            
        }
        
        if (index == 0){
          silde_image += 
            `<div class="carousel-item">
            <img src ='http://placehold.it/180' onclick="document.getElementById('fileInput-${i}').click();" id="img-${i}" class="d-block w-100" alt="...">
            <div class="carousel-caption d-none d-md-block">
              </div>
          </div>`

          
        }
        index = 0
        
        
        
      } 

    //   if (data[0].list_image.length < 6){
    //     for(var i = data[0].list_image.length; i < 6; i++){
    //         silde_image += `<div class="carousel-item">
    //         <img src ='http://placehold.it/180' onclick="document.getElementById('fileInput-${i + 1}').click();" id="img-${i+1}" class="d-block w-100" alt="...">
    //         <div class="carousel-caption d-none d-md-block">
              
    //         </div>
    //       </div>`
    //       } 
    //   }
      $('#slide-image').append(silde_image)

      $.ajax({ 	
          type : 'GET',
          url : '/categories'
          })
        .done(function(res) {
          let html =''
          for (var i = 0; i < res.length; i++){
            html += `<option value=${i + 1} >${res[i].name}</option>`
            
          }
        
          $('#category').append(html)
        
          string = `select option[value='` + data[0].categories_id  +  `']`
          $(string).attr("selected","selected");
      });
  });
  
 



  }
  $( "#size" ).change(function(){
    var selected = $( "#size" ).val()
    console.log(localStorage.getItem("shoes"))
    $.ajax({
                    data:{
                        name: selected,
                        size: JSON.parse(localStorage.getItem("shoes")),
                    },
                    type: 'POST',
                    url: '/size'
                }).done(function(data) {
                  
                  if (data == '') value = 0
                  else{
                    value = data[0].amount
                  }
                    let html = `<label
                                  for="stock"
                                  >Units In Stock
                                </label>
                                  <input
                                  id="input-stock"
                                  name="input-stock"
                                  type="number"
                                  value="${value}"
                                  class="form-control validate"
                                />`
                    ;
                    $('#stock').html(html)
                    

                    
                })

  })
  function readURL(input, id) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $(id)
                    .attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }


    function update(){
        var name_size = $( "#size" ).val()
        var length_size = $('#input-stock').val()
        var product_name = $('#input-name').val()
        var price = $('#input-price').val()
        var description = $('#input-description').val()
        var categories = $('#category').val()
        
        console.log(!Number.isInteger(length_size))
        console.log(name_size == '')
        console.log(!Number.isInteger(price))
        console.log(price == '')
        console.log(categories == "Select category")


        if(name_size =='Select size' 
        || Number.isInteger(length_size) 
        || name_size == '' 
        || Number.isInteger(price)
        || price == ''
        || categories == "Select category"
        ){
            $('#mess').show()
        }
        else{
            $.ajax({
                data:{
                    name_size : name_size,
                    length_size : length_size,
                    product_name : product_name,
                    description : description,
                    categories: categories,
                    price: price,
                    id: JSON.parse(localStorage.getItem("product-item"))
                },
                type: 'POST',
                url: '/update-edit-product'
            }).done(function(){
                window.location.href = 'http://localhost:5000/edit-product'
            })
            $('#imge-submit').click()
        }
        
        
    }