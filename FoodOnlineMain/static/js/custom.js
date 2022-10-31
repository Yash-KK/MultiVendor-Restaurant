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

                
                // update the total, sub_total, tax 
                $('#subtotal').html(res.cart_amount['sub_total'])
                $('#tax').html(res.cart_amount['tax'])
                $('#total').html(res.cart_amount['total'])
                
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
        id = $(this).attr('id');                          // this id to be used to delete the <li> tag when decreasing the cart items when quantity = 0
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

                
                // update the total, sub_total, tax 
                $('#subtotal').html(res.cart_amount['sub_total'])
                $('#tax').html(res.cart_amount['tax'])
                $('#total').html(res.cart_amount['total'])
                
                // if item quantity == 0: delete the cart item only on the cart page
                if(window.location.pathname =='/cart/'){
                    if(item_quantity ===0){
                        $('#itemId-' + id).remove();
                        console.log('removed!')
                        // display 'No cart items' message after deleting the cart item if cart quantity = 0

                                // displaying 'No Cart items'
                        if(cc ===0){
                            console.log("Entered this one")
                            $('#empty-cart').show()
                            $('#to-hide').hide()
                        }
               
                    }
                }

            }
        })
    })
})



// delete the cart item in the cart page
$(document).ready(function (){
    $('.delete_cart_item').click(function(){
        cart_item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

          
        $.ajax({
            type:'GET',
            url:url,
            data:cart_item_id,
            success: function(res){
                if(res.success){
                    let id = (res.cart_item_id);
                    $('#itemId-'+id).remove();
                    swal("Deleted the Cart Item!", "", "success");

                    cc = res.cart_counter['cart_count'];
                    $('#cart_counter').html(cc);
                }
                
                // displaying 'No Cart items'
                if(cc ===0){
                    console.log("Entered this one")
                    $('#empty-cart').show()
                    $('#to-hide').hide()
                }
               
            }
        })
    })
})