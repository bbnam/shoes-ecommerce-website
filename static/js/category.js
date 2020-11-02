// load single-product
window.onload = function() {
			$.ajax({
					type : 'GET',
					url : '/all_shoes',
					success: function(res) {
						res = res.slice(0,1)
						let html = '';
						res.forEach(element => {
							let htmlSegment = `<div class="col-lg-4 col-md-6">
								<div class="single-product">
									<img class="img-fluid" src="${element.picture}" alt="">
									<div id='name' class="product-details">
										<h6>${element.name}</h6>
										<div class="price">
											<h6>${element.price}</h6>
											<h6 class="l-through">${element.price}</h6>
										</div>
										<div class="prd-bottom">
											<a href="" class="social-info">
												<span class="ti-bag"></span>
												<p class="hover-text">add to bag</p>
											</a>
											<a href="" class="social-info">
												<span class="lnr lnr-heart"></span>
												<p class="hover-text">Wishlist</p>
											</a>
											<a href="" class="social-info">
												<span class="lnr lnr-sync"></span>
												<p class="hover-text">compare</p>
											</a>
											<a href="" class="social-info">
												<span class="lnr lnr-move"></span>
												<p class="hover-text">view more</p>
											</a>
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
// show option
function selectFun() {
    var selectBox = document.getElementById("show-select");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;
	// alert(selectedValue);
	$.ajax({
		type : 'GET',
		url : '/all_shoes',
		success: function(res) {
			res = res.slice(0,selectedValue)
			let html = '';
			res.forEach(element => {
				let htmlSegment = `<div class="col-lg-4 col-md-6">
					<div class="single-product">
						<img class="img-fluid" src="${element.picture}" alt="">
						<div id='name' class="product-details">
							<h6>${element.name}</h6>
							<div class="price">
								<h6>${element.price}</h6>
								<h6 class="l-through">${element.price}</h6>
							</div>
							<div class="prd-bottom">
								<a href="" class="social-info">
									<span class="ti-bag"></span>
									<p class="hover-text">add to bag</p>
								</a>
								<a href="" class="social-info">
									<span class="lnr lnr-heart"></span>
									<p class="hover-text">Wishlist</p>
								</a>
								<a href="" class="social-info">
									<span class="lnr lnr-sync"></span>
									<p class="hover-text">compare</p>
								</a>
								<a href="" class="social-info">
									<span class="lnr lnr-move"></span>
									<p class="hover-text">view more</p>
								</a>
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
		})
	event.preventDefault();
	
	
}
