// add to cart
$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
       
        // fetch the data
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        data = {
            food_id: food_id
        }
        // sending data through ajax
        $.ajax({
            type:'GET',
            url:url,
            data: data,
            success: function(res){
                if(res.status == 'login_required'){
                    swal(res.message, "", "info").then(()=>{
                        window.location = '/accounts/login-user'
                    })
                }
                console.log(res);
                cc = res.cart_counter['cart_count'];
                item_quantity = res['item_quantity'];
                $('#cart_counter').html(cc);
                $('#qty-'+ food_id).html(item_quantity);
                
            }
        })
    })

    // quantity of the food item
    $('.item_qty').each(function(){
        var id = $(this).attr('id');
        var quantity = $(this).attr('data-qty');

       $("#"+id).html(quantity);
    })
})

// decrease cart
$(document).ready(function(){
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        data = {
            food_id:food_id
        }
        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success:function(res){
                console.log(res);
                if(res.status == 'login_required'){
                    swal(res.message, "", "info").then(()=>{
                        window.location = '/accounts/login-user'
                    })
                }
                cc = res.cart_counter['cart_count'];
                item_quantity = res['item_quantity']
                $('#cart_counter').html(cc);
                $('#qty-'+food_id).html(item_quantity);
            }
        })
    })
})