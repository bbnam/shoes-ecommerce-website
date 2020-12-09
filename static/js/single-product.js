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
			if (getCookie('user') != ''){
				$.ajax({
					type : 'POST',
					url : '/get-single-review',
					data:{
						shoes_id: window.location.href.substring(window.location.href.length - 1, window.location.href.length),
						user_id: getCookie('user')
	
					},
					success: function(res) {
						if(res != ''){
							let html = `
							<h4> Your Review </h4>
							<div class="review_item">
												<div class="media">
													<div class="d-flex">
													<img src=${res[0].avatar} style =
												"width: 100px; 
												height: 100px; 
												" alt="">
													</div>
													<div class="media-body">
														<h4>${res[0].name}</h4>
							`
		
							for (var i = 0; i < res[0].rate; i ++){
								html += `<i class="fa fa-star"></i>`
							}
		
							html += `
							</div>
												</div>
												<p>${res[0].comment}
													</p>
											</div>`
								
														
														
													
								
		
		
							$('#your-rate').html(html)
					
							}
						}
						
				})
			}


			login()
			

			this.update_review()


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
	function update_review(){
		$.ajax({
			type : 'POST',
			url : '/get-all-review',
			data:{
				shoes_id: window.location.href.substring(window.location.href.length - 1, window.location.href.length)

			},
			success: function(res) {

				let rate = 0
				var dict_rate = {
					"5": 0,
					"4": 0,
					"3": 0,
					"2": 0,
					"1": 0,
				};

				let html = ''
				res.forEach(element => {
					html += `
					<div class="review_item">
										<div class="media">
											<div class="d-flex">
												<img src="${element.avatar}" style="
													width: 60px; 
													height: 60px; 
													
												"alt="">
											</div>
											<div class="media-body">
												<h4>${element.name}</h4>
					`


					for (var i = 0; i < element.rate; i ++){
						html += `<i class="fa fa-star"></i>`
					}
					rate += element.rate

					dict_rate[element.rate] += 1
					  




					html += `
					</div>
								</div>
									<p>${element.comment}
											</p>
									</div>
					`

				});
				$('#review_list').html(html)
				
				len_res = res.length

				if (len_res == 0){
					avg = 0
				}
				else{
					avg = rate / len_res

				}

				
				$('#average-rate').html(`
					<h5>Overall</h5>
					<h4>${avg}</h4>
					<h6>(${len_res} Reviews)</h6>
				
				`)

				$('#list-star').html(`
						<h3>Based on ${len_res} Reviews</h3>
						<ul class="list" >
							<li><a href="#">${dict_rate['5']} Review <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i
								class="fa fa-star"></i><i class="fa fa-star"></i> </a></li>
					<li><a href="#">${dict_rate['4']} Review <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i
								class="fa fa-star"></i> </a></li>
					<li><a href="#">${dict_rate['3']} Review <i class="fa fa-star"></i><i
								class="fa fa-star"></i><i class="fa fa-star"></i> </a></li>
					<li><a href="#">${dict_rate['2']} Review <i
								class="fa fa-star"></i><i class="fa fa-star"></i> </a></li>
					<li><a href="#"> ${dict_rate['1']} Review <i class="fa fa-star"></i></a></li>
						</ul>

						<div class="container">
							<span id="rateMe4"  class="feedback"></span>
						</div>
					`)
				
		}})

	}	
	
	
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
		
		if (document.getElementById('sst').value == 0 || document.getElementById('sst').value > size[0].amount ){
			Swal.fire({
			icon: 'error',
			title: 'Lỗi',
			text: 'Số lượng hàng hóa không hợp lệ',
			})
			// localStorage.removeItem("cart")
		}
		if (getCookie('user') == ''){
			Swal.fire({
				icon: 'error',
				title: 'Error',
				text: 'You must login',
				})
		}
		else{
			Swal.fire(
			'Thành Công!!',
			'Thêm vào giỏ hàng thành công',
			'success'
			)
			let cart = "cart " + getCookie('user')
			console.log(cart)
			dict.push({
				key: name + ' - ' + name_size_target + ' - '+ image+ ' - '+ size[0].amount + ' - '+ price + ' - ' + size[0].id,
				value: document.getElementById('sst').value

			})

			let dict_1 = {
				key: name + ' - ' + name_size_target + ' - '+ image+ ' - '+ size[0].amount + ' - '+ price + ' - ' + size[0].id,
				value: document.getElementById('sst').value
			}
			if (JSON.parse(localStorage.getItem(cart)) == null)
			{
				localStorage.setItem(cart, JSON.stringify(dict))
			}
			else{
				let a = JSON.parse(localStorage.getItem(cart))
				a[(a.length).toString()] = dict_1
				localStorage.setItem(cart, JSON.stringify(a))
				
				input = JSON.parse(localStorage.getItem(cart))
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
				localStorage.setItem(cart, JSON.stringify(result))
				

			}

		}
    }

function rating(){
		let rate = $("input[type='radio'][name='rating']:checked").val()
		
		if(getCookie('user') != ''){
			$.ajax({
				type : 'POST',
				url : '/add-comment',
				data:{
					rate: rate,
					comment: $('#message').val(),
					shoes_id: window.location.href.substring(window.location.href.length - 1, window.location.href.length),
					user_id: getCookie('user')
	
				},
				success: function(res) {
					console.log(res)
					let html = `
					<h4> Your Review </h4>
					<div class="review_item">
										<div class="media">
											<div class="d-flex">
												<img src="img/product/review-3.png" alt="">
											</div>
											<div class="media-body">
												<h4>${res.user_name}</h4>
					`
	
	
					for (var i = 0; i < rate; i ++){
						html += `<i class="fa fa-star"></i>`
					}
	
					html += `
					</div>
										</div>
										<p>${$('#message').val()}
											</p>
									</div>`
						
												
												
											
						
	
	
					$('#your-rate').html(html)
					update_review()
					}
				})
	
		}
		else{
			Swal.fire({
				icon: 'error',
				title: 'Error',
				text: 'Your must be Login',
				})
				
		}


		



}