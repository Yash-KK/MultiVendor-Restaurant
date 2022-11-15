// GOOGLE APIS
let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        // console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address':address}, function(results, status){
        // console.log('results=>',results);
        // console.log('status=>',status);
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('id_address').val(address);

        }
    });

    // loop through the address components and assign them to form field
    console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
                
            // get the country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name)
            }

            // get the state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name)
            }

            // get the city
            if(place.address_components[i].types[j] == "locality"){
                $('#id_city').val(place.address_components[i].long_name)
            }

            // get pincode            
             if(place.address_components[i].types[j] == "postal_code"){
                $('#id_pincode').val(place.address_components[i].long_name)
            } else{
                $("#id_pincode").val('');
            }
            

        }
    }
}




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
               
                $('#total').html(res.cart_amount['total'])
                
            }
        })
    })

    // quantity of the food item
    // looping  through the cart items and displaying the relevant quantity on the food item
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

                    // updating the total, sub_total, tax  
                    $('#subtotal').html(res.cart_amount['sub_total'])
                    
                    $('total').html(res.cart_amount['total'])
                    
                }
                
                // displaying 'No Cart items'
                if(cc ===0){ 
                    console.log("Entered this one")
                    $('#empty-cart').show()
                    $('#to-hide').hide()
                    
                    // if cart count after deleting is 0. Set the total, tax, subtotal to 0
                    $("#subtotal").html(0);
                    
                    $('#total').html(0);
                }
               
            }
        })
    })

    // ADD OPENING HOUR'S
    $('.add_hours').click(function(e){
        e.preventDefault();
        let condition;

        let day = document.getElementById('id_day').value
        let from_hour = document.getElementById('id_from_hour').value
        let to_hour = document.getElementById('id_to_hour').value
        let is_closed = document.getElementById('id_is_closed').checked;
        let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
        let url = document.getElementById('add_hour_url').value;
       
        // alert("Added Hours")
        if(is_closed){
            condition = "day==''"            
        } else{
            condition = "day == '' || from_hour =='' || to_hour == ''"
        }
        
        if(eval(condition)){
            // fill out the entries
            swal("Fill out Entries", "", "info");   
            $("#opening_hours").trigger("reset");                      
        } else{
            // send data to frontend
            $.ajax({
                type:"POST",
                url:url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token
                },
                success: function(res){
                    if(res.success){
                        if(res.is_closed){
                            let html = '<tr id="hour-'+ res.id +'" ><td> <b> '+ res.day +' </b> </td>   <td> Closed </td>   <td> <a href="#"  class="remove_add_hours" data_url="/vendor/remove-opening-hours/'+ res.id +'/" >Remove</a> </td> </tr>'
                            $('.opening_hours').append(html);
                        } else{
                            let html = '<tr id="hour-'+ res.id +'" ><td> <b> '+ res.day +' </b> </td>   <td> '+ res.from_hour +' - '+ res.to_hour +'  </td>   <td> <a href="#" class="remove_add_hours" data_url="/vendor/remove-opening-hours/'+ res.id +'/" >Remove</a> </td> </tr>'
                            $('.opening_hours').append(html);
                        }

                        $('.opening_hours').trigger("reset");
                        $("#opening_hours").trigger("reset");
                        console.log(res);                       
                    } else if (res.failure){
                       
                        swal(res.failure, '', 'warning');
                       
                        $("#opening_hours").trigger("reset");
                    }
                   
                    
                } 

            })

        }
    });

     // REMOVE ADD HOURS  
    
    $(document).on('click', '.remove_add_hours', function(e){
        e.preventDefault();
        let url = $(this).attr('data_url');       
        console.log(url);

        $.ajax({
            'type':'GET',
            'url': url,
            'success': function(res){
                if(res.success){
                    // delete the <tr> id
                    $('#hour-'+ res.hour_id).remove();
                }
            }
        })
    })

    // close document ready
})

