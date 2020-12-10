$(function() {
    $("#expire_date").datepicker({
      defaultDate: "10/22/2020"
    });
});

window.onload = function(){
    $.ajax({ 	
        type : 'GET',
        url : '/all_shoes_1'
        })
      .done(function(res) {
        console.log(res.length)
        setCookie('shoes', res.length + 1 , 1)

    });
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
      
       
    });
  }

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
                    
                },
                type: 'POST',
                url: '/create-add-product'
            }).done(function(){
                window.location.href = 'http://localhost:5000/manager-product'
                $('#imge-submit').click()

            })
            
        }
        
        
    }