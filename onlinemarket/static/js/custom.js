let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: {'country': ['us']},
        })
    autocomplete.addListener('place_changed', onPlaceChanged);    
}


function onPlaceChanged() {
    const place = autocomplete.getPlace();
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = 'Start typing...';
    } else {
        console.log(place);
        
    }
    const geocoder = new google.maps.Geocoder()
    const address = document.getElementById('id_address').value
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            const latitude = results[0].geometry.location.lat();
            const longitude = results[0].geometry.location.lng();
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);
        }
    });

    const components = place.address_components;
    let zip_code = '';
    for (let i = 0; i < components.length; i++) {
        for (let j = 0; j < components[i].types.length; j++) {
            if (components[i].types[j] == 'locality') {
                $('#id_city').val(components[i].long_name);
            }
            if (components[i].types[j] == 'administrative_area_level_1') {
                $('#id_state').val(components[i].long_name);
            }
            if (components[i].types[j] == 'country') {
                $('#id_country').val(components[i].long_name);
            }
            if (components[i].types[j] == 'postal_code') {
                zip_code = components[i].long_name;
            }
        }
    }
    $('#id_zip_code').val(zip_code);
}

$(document).ready(function(){
    
    $('.add_to_cart').on('click', function(e) {
        e.preventDefault();
        const url = $(this).attr('data-url');
        const product_id = $(this).attr('data-id');
        
        $.ajax({
            type: 'GET',
            url: url,
            data: {
                id: product_id,
            },
            success: function(response) {
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/accounts/login'
                    })

                } else if (response.status == 'failed') {
                    swal(response.message, '', 'warning')
                } else {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    $('#quantity-'+product_id).html(response.cart_product_qty);

                    if (window.location.pathname == '/cart/') {
                        const {subtotal, tax, grand_total} = response.amounts;
                        updateAmounts(subtotal, tax, grand_total)
                    }
                }
            }

        })
    })

    // PUt the cart item quantity in product of vendor_detail
    $('.item_qty').each(function() {
        const item_product_id = $(this).attr('id');
        const quantity = $(this).attr('data-qty');
        $('#'+item_product_id).html(quantity);
    })

    $('.decrease_cart').on('click', function(e) {
        e.preventDefault();
        const url = $(this).attr('data-url')
        const item_id = $(this).attr('id')
        const product_id = $(this).attr('data-id')
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info')

                } else if (response.status == 'failed') {
                    swal(response.message, '', 'warning')
                } else {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    $('#quantity-'+product_id).html(response.cart_product_qty)
                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.cart_product_qty, item_id)
                        checkCartEmpty()
                        const {subtotal, tax, grand_total} = response.amounts;
                        updateAmounts(subtotal, tax, grand_total)
                    }
                    
                }
                
                
            }
        })
    })

    $('.remove_cart').on('click', function(e) {
        e.preventDefault();
      
        const url = $(this).attr('data-url')
        const item_id = $(this).attr('data-id')
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info')
                } else if (response.status == 'failed') {
                    swal(response.message, '', 'warning')
                } else {
                    $('#cart_counter').html(response.cart_counter.cart_count)
                    swal('Delete the cart item', '', 'info')
                    if (window.location.pathname == '/cart/') {
                        removeCartItem(0, item_id)
                        checkCartEmpty()
                        const {subtotal, tax, grand_total} = response.amounts;
                        updateAmounts(subtotal, tax, grand_total)
                    }
                }
            }
        })
    })

    function removeCartItem(cart_item_qty, item_id) {
        if (window.location.pathname == '/cart/') {
            if (cart_item_qty <= 0) {
                document.getElementById('cart-item-'+item_id).remove()
            }
        }
        
    }

    function checkCartEmpty() {
        const cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById('empty-cart').style.display = 'block';
            // document.getElementById('cart-counter').style.display = 'none';
        }

    }

    function updateAmounts(subtotal, tax, grand_total) {
        $('#subtotal').html(subtotal);
        $('#tax').html(tax);
        $('#grand_total').html(grand_total);
    }

// Add opening hour
    $('.add_hour').on('click', function(e) {
        e.preventDefault();
        let day = document.getElementById('id_day').value 
        let from_time = document.getElementById('id_from_time').value
        let to_time = document.getElementById('id_to_time').value
        let is_closed = document.getElementById('id_is_closed').checked 
        let url = document.getElementById('add_hour_url').value 
        let csrf_token = $('input[name=csrfmiddlewaretoken]').val()

        if (is_closed) {
            condition = "day != ''"
            is_closed = 'True'
        } else {
            condition = "day != '' && from_time != '' && to_time != ''"
            is_closed = 'False'
        }

        if (eval(condition)) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_time': from_time,
                    'to_time': to_time,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token,
                },
                success: update_view_add_opening_hour,
                
            });
        } else {
            swal('Please fill all fields', '', 'info')
        }
    })

    update_view_add_opening_hour = function(response) {
        if (response.status == 'success') {
            if (response.is_closed == 'Closed') {
                html = '<tr id="hour-'+response.id+'"><td style="border: none;"><b>'+response.day+'</b></td><td style="border: none;">Closed</td><td style="border: none;"><a href="#" class="remove_hour" data-url="/vendor/opening_hours/delete/'+response.id+'">Remove</a></td></tr>';
            } else {
                html = '<tr id="hour-'+response.id+'"><td style="border: none;"><b>'+response.day+'</b></td><td style="border: none;">'+response.from_hour+' - '+response.to_hour+'</td><td style="border: none;"><a href="#" class="remove_hour" data-url="/vendor/opening_hours/delete/'+response.id+'">Remove</a></td></tr>';
            }

            $('.opening_hours').append(html);
            document.getElementById('opening_hours').reset()
        } else {
            swal(response.message, '', 'error')
        }
    }

    $(document).on('click', '.remove_hour', function(e) {
        e.preventDefault();
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                if (response.status == 'success') {
                    document.getElementById('hour-'+response.id).remove()
                } else {
                    swal(response.message, '', 'error')
                }
            }
        })
    })
    
    $('#flash_select').on('click', function(e) {
        e.preventDefault();
        const url = $(this).attr('data-url');
        const flash_sale_id = $(this).attr('data-id');
        let flash_select = document.getElementById('flash_select');
        let flash_checkout = document.getElementById('flash_checkout');
        $.ajax({
            type: 'GET',
            url: url,
            data: {
                flash_sale_id: flash_sale_id,
            },
            success: (response) => {
                console.log(response)
                if (response.status == 'error') {
                    swal(response.message, '', 'warning')
                } else {
                    
                    flash_select.classList.remove('btn-primary');
                    flash_select.classList.add('btn-secondary');
                    flash_checkout.classList.remove('d-none');
                    swal(response.message, '', 'success');
                }
            }
        })
    })

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie('csrftoken')

    $(document).on('submit', '.add-review', function(e) {
        e.preventDefault();
        const stars = document.querySelectorAll('input[type=radio]');
        let rating = 1;
        for (let star of stars) {
            if (star.checked) {
                rating = star.getAttribute('value');
                break;
            }
        }
        const comment = document.querySelector('#comment');
        const url = $(this).attr('data-url');
        const product_id = $(this).attr('data-id');
        if (comment.value != '') {
            $.ajax({
                type: 'POST',
                url,
                data: {
                    rating,
                    comment: comment.value,
                    'csrfmiddlewaretoken': csrfToken,
                    'product_id': product_id
                },
                success: updateReviewsAfterCreation,
                error: handleError
            })
        }
    })

    function handleError(error) {
        console.log(error);
    }

    function updateReviewsAfterCreation(response) {
        console.log(response)
        if (response.status == 'success') {
            const { id, rating, comment, username } = response;
            const url = '/market/delete_reivew/' + id;
            html = `<div class="card mt-3" id="review-${id}"><div class="card-body"><div><p class="starability-result" data-rating="${rating}"></p><span><b>${username}</b> - ${comment}</span></div><div class="d-inline delete-review" data-url="${url}"><a href="${url}"><button class="btn btn-danger">Delete</button></a></div></div></div>`;
    
            $('.review-list').append(html);
            const commentEle = document.getElementById('comment');
            commentEle.value = '';
        } else {
            handleError(response.message);
        }
    }

    $(document).on('click', '.delete-review', function(e) {
        e.preventDefault();
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                console.log(response)
                if (response.status == 'success') {
                    const element = document.getElementById('review-'+response.id);
                    element.remove();
                } else {
                    swal(response.message, '', 'error');
                }
            }
        })
    })
})