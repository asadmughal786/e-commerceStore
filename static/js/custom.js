// const MonthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

// $("#reviewForm").submit(function(e){
//     e.preventDefault()

//     let dt = new Date();
//     let time = dt.getDay() + ", " + MonthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

//     $.ajax({
//         data: $(this).serialize(),
//         method: $(this).attr("method"),
//         url: $(this).attr("action"),
//         dataType: "json",

//         success: function(response){
//             console.log('comment saved to the db');
            


//             if(response.bool == true){
//                 $("#reviewResponse").html('Review Added Successfully')
//                 $(".hide-review-form").hide()

//                 let _html = '<li>'

//                     _html+= '<div class="review-heading">'

//                     _html+= '<h5 class="name">'+ response.context.user +'</h5>'
//                     _html+= '<p class="date">'+ time +'</p>'

//                     _html+= '<div class="review-rating">'
//                     _html+= '<i class="fa fa-star"></i>'
                    
//                     for (let index = 1; index < response.context.rating ; index++) {
//                         _html+= '<i class="fa fa-star"></i>'
                        
//                     }
//                     _html+= '</div>'
                    


//                     _html+= '</div>'

//                     _html+= '<div class="review-body">'
//                     _html+= '<p>'+ response.context.review+ '</p>'
//                     _html+= '</div>'
//                     _html+= '</li>'
//                     $(".review-body").prepend(_html)
//             }
            
//         }


//     })

// })

const MonthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

$("#reviewForm").submit(function (e) {
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDate() + " " + MonthNames[dt.getMonth()] + ", " + dt.getFullYear();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",

        success: function (response) {
            console.log('comment saved to the db');

            if (response.bool == true) {
                $("#reviewResponse").html('Review Added Successfully');
                $(".hide-review-form").hide();

                let _html = '<li>';
                _html += '<div class="review-heading">';
                _html += '<h5 class="name">' + response.context.user + '</h5>';
                _html += '<p class="date">' + time + '</p>';
                _html += '<div class="review-rating">';
                _html += '<i class="fa fa-star"></i>';

                for (let index = 1; index < response.context.rating; index++) {
                    _html += '<i class="fa fa-star"></i>';
                }
                _html += '</div>';
                _html += '</div>';
                _html += '<div class="review-body">';
                _html += '<p>' + response.context.review + '</p>';
                _html += '</div>';
                _html += '</li>';

                // Append the new review to the reviews list
                $("#reviews ul.reviews").prepend(_html);
            }
        }
    });
});



// Add to cart funtionality


$("#add-to-cart-btn").on("click",function(){
    let quantity = $("#product-quantity").val()
    let product_title = $(".products-title").val()
    let product_id = $(".products-id").val()
    let product_price = $("#product-price-val").text()  
    let product_color = $(".product-color").val()
    let this_val = $(this)

    console.log("Quantity:",quantity);
    console.log("Title:",product_title);
    console.log("Product id:",product_id);
    console.log("Product Price:",product_price);
    console.log("Product Color:",product_color);
    console.log("Product Current Elemet:",this_val);
    
    $.ajax({
        url:'/add-to-cart',
        data: {
            'id': product_id,
            'title':product_title,
            'price': product_price,
            'qty': quantity,
            'color': product_color,
        },
        dataType:'json',
        beforeSend: function(){
            console.log("Adding Product to cart");
        },
        success: function(response){
            this_val.html('item added to cart')
            console.log("Added Product to cart!");
            $(".cart-items-count").text(response.totalCartItems)
        }
    })
})

