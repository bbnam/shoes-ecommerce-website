var name =''
		var price = ''
		var image = ''
		window.onload = function() {
			// console.log(window.location.href)
			
			url = window.location.href + "?format=json"
			$.ajax({
					type : 'GET',
					url : url,
					success: function(res) {
						let html = ''
							for (var i =1 ; i < res[0].list_image.length; i++){
								html += `<div class="carousel-item">
								<img class="d-block w-100" src=${res[0].list_image[i]} alt="">
							</div>`
							}
							$("#image-show").append(html);
							$("#first-image").html(`<img class="d-block w-100" src=${res[0].list_image[0]} alt="First slide">`);	
							$("#shoes-name").html(res[0].name);
							$("#shoes-price").html(res[0].price);
							$("#home").html(`<p>${res[0].description}</p>`)
							name = res[0].name
							price = res[0].price
							image= res[0].list_image[0]
											}
										})

							event.preventDefault();

			}


		// target size
		var size = 0	
		var name_size_target = ''
		$('input.visually-hidden').click(function() {  
			name_size_target = $(this).attr('value')
			$.ajax({
						data : {
							size : window.location.href.substring(window.location.href.length - 1, window.location.href.length),
							name : $(this).attr('value')
						}, 	
							type : 'POST',
							url : '/size'
							})
						.done(function(data) {
							size = data
							
							if (data == '' || data[0].amount == 0){
								$('#have-shoes').hide()
								$('#no-shoes').show()
							}
							else{
								$('#have-shoes').html(data[0].amount + " sản phẩm có sẵn" )
								$('#no-shoes').hide()
								$('#have-shoes').show()
							}

						})
	});
							
	function add () {
		var result = document.getElementById('sst'); 
		var sst = result.value; 
		if (size == ''){
			result.value = 0
		}
		else{
		if( !isNaN( sst ) && sst <size[0].amount) 
			result.value++;
		if(result.value > size[0].amount){
			result.value = size[0].amount
		}
		return false;
		}
		
	
	}
	function sub () {
		var result = document.getElementById('sst'); 
		var sst = result.value; 
		if (size == ''){
			result.value = 0
		}
		else{
			if( !isNaN( sst ) && sst > 0) 
				result.value--;
			if(result.value > size[0].amount){
				result.value = size[0].amount
			}
			return false;
		}
		
	}
	var dict = []
	function addtoCart () {
		console.log(size)
		if (document.getElementById('sst').value == 0 || document.getElementById('sst').value > size[0].amount){
			Swal.fire({
			icon: 'error',
			title: 'Lỗi',
			text: 'Số lượng hàng hóa không hợp lệ',
			})
			localStorage.removeItem("cart")
		}
		else{
			Swal.fire(
			'Thành Công!!',
			'Thêm vào giỏ hàng thành công',
			'success'
			)

			dict.push({
				key: name + ' - ' + name_size_target + ' - '+ image+ ' - '+ size[0].amount + ' - '+ price + ' - ' + size[0].id,
				value: document.getElementById('sst').value

			})

			let dict_1 = {
				key: name + ' - ' + name_size_target + ' - '+ image+ ' - '+ size[0].amount + ' - '+ price + ' - ' + size[0].id,
				value: document.getElementById('sst').value
			}
			if (JSON.parse(localStorage.getItem("cart")) == null)
			{
				localStorage.setItem("cart", JSON.stringify(dict))
			}
			else{
				let a = JSON.parse(localStorage.getItem("cart"))
				a[(a.length).toString()] = dict_1
				localStorage.setItem("cart", JSON.stringify(a))
				
				input = JSON.parse(localStorage.getItem("cart"))
				var newObj = {};
                for(i in input){
                var item = input[i];
                    if(newObj[item.key] === undefined){
                        newObj[item.key] = 0;
                    }
                    newObj[item.key] += parseInt(item.value);
                }

                var result = [];
                
                for(i in newObj){
                    result.push({'key':i,'value':newObj[i]});
                }
				localStorage.setItem("cart", JSON.stringify(result))
				console.log(result)

			}

		}
    }
    
    $(document).ready(function() {
        $("#rating input:radio").click(function() {
  
            $("input[type='radio'][name='rating']:checked").val();
            
  
        });
  
      
  
  }
)