let cart_footer = document.getElementsByClassName('cart__footer')[0]
let quantity = document.getElementsByClassName('product-form__quantity')[0]
if(cart_footer){
    cart_footer.innerHTML += 'Duoc giam gia ne'
}

if(quantity){
    let content = '<div id="app-bundle-id"/>'
    quantity.outerHTML += content
}

let script = document.createElement('script');
        script.type = 'text/javascript';
        script.id = 'nestscale-nestdesk-script'
        script.src = 'https://odoo.website/shopify/static/js/bundle.js';
        document.head.appendChild(script);
