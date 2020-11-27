// load single-product

var shoes_show = 1

window.onload = function() {
			$.ajax({
					type : 'GET',
					url : '/all_shoes',
					success: function(res) {
						len_shoes = res.length
						localStorage.setItem('allshoes', JSON.stringify(res));
						res = res.slice(0,shoes_show)
						let html = '';
						res.forEach(element => {
							let htmlSegment = `<div class="col-lg-4 col-md-6">
								<div class="single-product">
									<a href="/shop/${element.name}">
										<img class="img-fluid" src="${element.list_image[0]}" alt="" "> 
									<div id='name' class="product-details" style="text-align: center" >
										<h6 class>${element.name}</h6>
										<div class="price d-flex justify-content-center">
											<h6>$${element.price}</h6>
											<h6 class="l-through">${element.price}</h6>
										</div>
									</div>
									<a>
								</div>
							</div>
						`

						html += htmlSegment
						});
						$("#single-product").append(html);
						show_vewmore(shoes_show, JSON.parse(localStorage.getItem("allshoes")).length)

						}
						
					})
event.preventDefault();	

			$.ajax({
				type : 'GET',
				url : '/categories',
				success: function(res) {
					// res = res.slice(0,1)
					let cateSegment = `<ul class="main-categories">
					<li class="main-nav-list"><a data-toggle="collapse" href="" onclick=showcategory(); aria-expanded="false" aria-controls="fruitsVegetable" id="0" name="All"><span
								 class="lnr lnr-arrow-right"></span>All</a>
						</li>
					`
					res.forEach(element => {
						len = element.length
						cateSegment += `
						<li class="main-nav-list"><a data-toggle="collapse" href="" onclick=showcategory(); aria-expanded="false" aria-controls="fruitsVegetable" name=${element.name} id=${element.id}><span
								 class="lnr lnr-arrow-right"></span>${element.name}</a>
						</li>

					`
					
					
					});
					cateSegment += `
					</ul>
					`
					$("#category-form").append(cateSegment);
					}
				})
			event.preventDefault();
			
			

}

// sort and show


function show_vewmore(value, len_shoes){
	console.log(value)
	if(parseInt(value) < parseInt(len_shoes)){
		$('#more').show()
	}
	else{
		$('#more').hide()
	}
	
}

function more(){
	
	res = JSON.parse(localStorage.getItem("allshoes"))

	show_shoes(res.slice(shoes_show, shoes_show+1),1)

	shoes_show = shoes_show + 1
	show_vewmore(shoes_show, JSON.parse(localStorage.getItem("allshoes")).length)
}

function show_shoes(data, append){
				let html = '';
				data.forEach(element => {
				let htmlSegment = `<div class="col-lg-4 col-md-6">
					<div class="single-product">
						<a href="/shop/${element.name}">
							<img class="img-fluid" src="${element.list_image[0]}" alt="" "> 
							<div id='name' class="product-details " style="text-align: center">
								<h6 class>${element.name}</h6>
								<div class="price d-flex justify-content-center" >
								<h6>$${element.price}</h6>
								<h6 class="l-through">${element.price}</h6>
							</div>
						</div>
						<a>
					</div>
				</div>
			`
			
			html += htmlSegment
			});
			if (append == 0){
				$("#single-product").html(html);
			}
			else{
				$("#single-product").append(html);
			}
			
			// document.getElementById('single-product'). = html
}

// function 

$(document).ready(function(){
    $(".list li").on("click", function(){
        var dataId = $(this).attr("data-value");
		// alert("The data-id of clicked item is: " + dataId);
		// console.log(typeof(dataId))
		var res = JSON.parse(localStorage.getItem("allshoes"))
		if (dataId == 0){
			show_shoes(JSON.parse(localStorage.getItem("allshoes")).slice(0,1),0)
			shoes_show = 1
			show_vewmore(shoes_show, JSON.parse(localStorage.getItem("allshoes")).length)

		}
		if (dataId == 1){
			res.sort(function(a,b){
				return parseFloat(b.price) - parseFloat(a.price);
			})
			localStorage.setItem('allshoes', JSON.stringify(res));

			show_shoes(res.slice(0,1),0)
			shoes_show = 1
			show_vewmore(shoes_show, JSON.parse(localStorage.getItem("allshoes")).length)

		}
		if(dataId == 2){
			res.sort(function(a,b){
				return parseFloat(a.price) - parseFloat(b.price);
			})
			localStorage.setItem('allshoes', JSON.stringify(res));			
			show_shoes(res.slice(0,1),0)
			shoes_show = 1
			show_vewmore(shoes_show, JSON.parse(localStorage.getItem("allshoes")).length)


		}
		event.preventDefault();
		
	});
	



});

function showcategory(){

	console.log(event.target.id)
	var name_category = event.target.name
	if (event.target.id == 0){
		$.ajax({
			type : 'GET',
			url : '/all_shoes',
			success: function(res) {
				
				let html = `<p style="font-size: 20px; padding-bottom: 10px;" >
					${name_category}
				</p>`
				// console.log(event.target.name)
				$('#name-category').html(html)
				localStorage.setItem('allshoes', JSON.stringify(res));
				
				show_shoes(res.slice(0,1),0)
				shoes_show = 1
				show_vewmore(shoes_show, JSON.parse(localStorage.getItem("allshoes")).length)

				}
			})
	}
	$.ajax({
		type : 'POST',
		data: {
			id : event.target.id,
		},
		url : '/category',
		success: function(res) {
			show_shoes(res,0)
			let html = `<p style="font-size: 20px; padding-bottom: 10px;" >
			${name_category}
		</p>`
		// console.log(event.target.name)
		$('#name-category').html(html)
		localStorage.setItem('allshoes', JSON.stringify(res));
		
		show_shoes(res.slice(0,1),0)
		shoes_show = 1
		show_vewmore(shoes_show, JSON.parse(localStorage.getItem("allshoes")).length)


		}
		})
}

