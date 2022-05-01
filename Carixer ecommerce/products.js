

$(document).ready(function(e){
    vasanth.products.forEach((i)=>loadproducts1(i));
});

function loadproducts1(data){
 var pro = '<a style="text-decoration:none; color:#000;" href="productdetail.html" class=\"card border-light text-center me-3 list_card\" id='+data.id+'><img src='+data.image+' class=\"card-img-top img\"><div class=\"card-body\"><h6 class=\"card-title blue fw-bold\">'+data.title+'</h6><p class=\"card-text blue fw-bold\">₹ '+data.price+'</p><p><span class=\"fa fa-star checked\"></span><span class=\"fa fa-star checked\"></span><span class=\"fa fa-star checked\"></span><span class=\"fa fa-star\"></span><span class=\"fa fa-star\"></span><span class=\"fw-normal\"> '+data.rating.count+' reviews</span></p></div></a>'

 $("#listproducts").append(pro);
}

$(document).ready(function(){
 $("#fourview").on("click", function(){
     $(".list_card").css("max-width","26rem");
     console.log("gdhj")
 })
 $("#threeview").on("click", function(){
     $(".list_card").css("max-width","18rem");
 })
})

$(document).ready(function (e) {
    jsonObject.productslike.forEach((i) => loadproducts2(i));
  });

  function loadproducts2(data) {
    var pro =
      '<li class="card border-light text-center me-3 like_card" id=' +
      data.id +
      "><img src=" +
      data.image +
      ' class="card-img-top img"><div class="card-body"><h6 class="card-title blue fw-bold">' +
      data.title +
      '</h6><p class="card-text blue fw-bold">₹ ' +
      data.price +
      '</p><p><span class="fa fa-star checked"></span><span class="fa fa-star checked"></span><span class="fa fa-star checked"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fw-normal"> ' +
      data.rating.count +
      " reviews</span></p></div></li>";

    $("#likeproducts").append(pro);
  }

  $(document).ready(function () {
    $("#fourview").on("click", function () {
      $(".list_card").css("max-width", "26rem");
    });
    $("#threeview").on("click", function () {
      $(".list_card").css("max-width", "18rem");
    });
  });

  $(document).ready(function () {
    var quantitiy = 0;
    $(".quantity-right-plus").click(function (e) {
      // Stop acting like a button
      e.preventDefault();
      // Get the field name
      var quantity = parseInt($("#quantity").val());

      // If is not undefined

      $("#quantity").val(quantity + 1);

      // Increment
    });

    $(".quantity-left-minus").click(function (e) {
      // Stop acting like a button
      e.preventDefault();
      // Get the field name
      var quantity = parseInt($("#quantity").val());

      // If is not undefined

      // Increment
      if (quantity > 0) {
        $("#quantity").val(quantity - 1);
      }
    });
  });

  var elmId = "";
  $(document).ready(function(){
    $(".list_card").click(function(){
        elmId = $(this).attr("id");
        alert(elmId);
        if("vasanth.products.id:contains(elmId)"){
            vasanth.products.filter((elmId)=>{
                console.log(elmId)
            });
        }
        

  });
});