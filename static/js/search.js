

$(document).ready(function(){
    $.ajaxSetup({ cache: false });
    $('#search_input').keyup(function(){
     $('#result').html('');
     $('#state').val('');
     var searchField = $('#search_input').val();
     console.log(searchField)
     if (searchField == ""){
         $('#result').append('')
     }
     else{
        $.ajax({
            data: {
                search : searchField
            },
            type : 'POST',
            url : '/search'
            }).done(function(data){
                data.forEach( element => {
                     $('#result').append(`<li style="text-align:left; font-size: 18px" >
                     <img src="${element.list_image[0]}" height="50" width="50" class="img-thumbnail" />
                    <a style = "color: white"href="http://localhost:5000/shop/${element.name}-${element.id}">
                     ${element.name}
                    </a>`);
                   }); 
            })
     }
    
    });
    
    $('#result').on('click', 'li', function() {
     var click_text = $(this).text();
     $('#search_input').val($.trim(click_text[0]));
     $("#result").html('');
    //  console.log(click_text)
    //  window.location.href = "http://localhost:5000/shop/"
    });
   });