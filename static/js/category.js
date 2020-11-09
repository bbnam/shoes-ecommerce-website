// load single-product
window.onload = function() {
			$.ajax({
					type : 'GET',
					url : '/all_shoes',
					success: function(res) {
						// res = res.slice(0,1)
						let html = '';
						res.forEach(element => {
							let htmlSegment = `<div class="col-lg-4 col-md-6">
								<div class="single-product">
									<a href="#">
										<img class="img-fluid" src="${element.picture}" alt="" "> 
									</a>
									<div id='name' class="product-details ">
										<h6 class>${element.name}</h6>
										<div class="price d-flex justify-content-center">
											<h6>${element.price}</h6>
											<h6 class="l-through">${element.price}</h6>
										</div>
									</div>
								</div>
							</div>
						`
						
						html += htmlSegment
						});
						$("#single-product").append(html);
						}
					})
event.preventDefault();
}


// sort and show

function show_shoes(data){
				let html = '';
				data.forEach(element => {
				let htmlSegment = `<div class="col-lg-4 col-md-6">
					<div class="single-product">
						<img class="img-fluid" src="${element.picture}" alt="">
						<div id='name' class="product-details">
							<h6>${element.name}</h6>
							<div class="price d-flex justify-content-center">
								<h6>${element.price}</h6>
								<h6 class="l-through">${element.price}</h6>
							</div>
						</div>
					</div>
				</div>
			`
			
			html += htmlSegment
			});
			// $("#single-product").load(html);
			document.getElementById('single-product').innerHTML = html
}


$(document).ready(function(){
    $(".list li").on("click", function(){
        var dataId = $(this).attr("data-value");
		// alert("The data-id of clicked item is: " + dataId);
		console.log(typeof(dataId))
		if (dataId == 0){
			$.ajax({
				type : 'GET',
				url : '/all_shoes',
				success: function(res) {
					show_shoes(res)
					}
				})
	
		}
		if (dataId == 1){
			$.ajax({
				type : 'GET',
				url : '/all_shoes',
				success: function(res) {
					res.sort(function(a, b) {
						return parseFloat(b.price) - parseFloat(a.price);
					});
					show_shoes(res)
					}
				})
		}
		if(dataId == 2){
			$.ajax({
				type : 'GET',
				url : '/all_shoes',
				success: function(res) {
					res.sort(function(a, b) {
						return parseFloat(a.price) - parseFloat(b.price);
					});
					show_shoes(res)
					}
				})
		}
		event.preventDefault();
		
    });
});

