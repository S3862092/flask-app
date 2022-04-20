//variables 

const cartBtn = document.querySelector('.cart-btn');
const closeCartBtn = document.querySelector('.close-cart');
const clearCartBtn = document.querySelector('.clear-cart');
const cartDOM = document.querySelector('.cart');
const cartOverlay = document.querySelector('.close-overlay');
const cartItems = document.querySelector('.close-items');
const cartTotal = document.querySelector('.close-total');
const cartContent = document.querySelector('.close-content');
const productsDOM = document.querySelector('.products-center');

// cart 
let cart = [];

// Responsible for getting the products
class Products{
    async getProducts(){
        try{
            let result = await fetch('static/js/cakes.json');
            let data = await result.json();
            let products = data.items;
            products = products.map(item => {
                const {title,price} = item.fields
                const {id} = item.sys
                const image = item.fields.image.fields.file.url;
                return {title,price,id,image}
            })
            return products
        }catch (error){
            console.log(error);
        }    
    }
}

function changePage(id){
    console.log(id);
    location.href = "/orderNow";
    
}

// display products, Responsible for getting all of the items that are being returned by the product
class UI{
    displayProducts(products){
        let result = '';
        products.forEach(product => {
            result += `
            <!-- single product -->
            <article class = "product">
                <div class = "img-container">
                    <img src = ${product.image} alt = "product" class = "product-img">
                    <button class = "bag-btn" data-id = ${product.id}" onClick = "changePage(${product.id})">
                        <i class = "fas fa-shopping-cart"></i>
                        Order Now
                    </button>
                </div>
                <h3>${product.title}</h3>
                <h4>$${product.price}</h4>
            </article>
            <!--end single product -->
            
            `;
        });
        productsDOM.innerHTML = result; 
    }
    
}

// Local storage
class Storage{
    static saveProducts(products){
        localStorage.setItem("products", JSON.stringify(products));
    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    const ui = new UI();
    const products = new Products();

    //get all products
    products.getProducts().then(products => {
        ui.displayProducts(products);
        Storage.saveProducts(products);
    })
});