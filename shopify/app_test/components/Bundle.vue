<template>
  <div class="bundle">
    <BundleNav/>
    <div class="bundle-content" v-if="url == 'https://odoo.website/apps/shopify/bundle'">
      <div>
        Shop
        <select v-model="current_shop" @change="changeShop()">
          <option v-for="shop in shops">{{ shop.name }}</option>
        </select>
      </div>
      <div>
        Discount rule:
        <select v-model="discount_type">
          <option value="percentage">%</option>
          <option value="fix_amount">Total amount</option>
        </select>
      </div>
      <div>
        Discount value:
        <input type="number" step="0.01" v-model="discount_value">
      </div>

      <div>
        Product
        <Button type="primary" @click="showModal">Open Modal</Button>
        <Modal v-model:visible="visible" width="800px" :title="'Products list of '+current_shop" @ok="handleOk">
          <div class="modal-content">
            <div class="modal-left">
              <div class="modal-top">
                <input type="text">
                <button @click="updateProduct">Update product</button>
              </div>

              <div class="products-list">
                <div class="product-line">
                  <div class="product-check">
                  </div>
                  <div class="product-image">
                    Image
                  </div>
                  <div class="product-title">
                    Title
                  </div>
                  <div class="product-variant">
                    Variant
                  </div>
                  <div class="product-quantity">
                    Quantity
                  </div>
                </div>
                <div class="product-line" v-for="product in products">
                  <div class="product-check">
                    <input type="checkbox" v-model="product.check">
                  </div>
                  <div class="product-image">
                    <img :src="product.image" alt="Ảnh s/p">
                  </div>
                  <div class="product-title">
                    {{ product.title }}
                  </div>
                  <div class="product-variant">
                    <select v-model="product.variant" v-if="product.variants.length>1">
                      <option value="all">All variant</option>
                      <option :value="variant.id" v-for="variant in product.variants">{{ variant.title }}</option>
                    </select>
                  </div>
                  <div class="product-quantity">
                    <input type="number" v-model="product.quantity"/>
                  </div>
                </div>
              </div>
            </div>

            <div class="modal-right">
              <div v-for="product in products">
                <div class="product-line"  v-if="product.check == true">
                  <div class="product-check">
                    <input type="checkbox" v-model="product.check">
                  </div>
                  <div class="product-image">
                    <img :src="product.image" alt="Ảnh s/p">
                  </div>
                  <div class="product-title">
                    {{ product.title }}
                  </div>
                  <div class="product-quantity">
                    x {{product.quantity}}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Modal>

        <div>
          <div v-for="product in products">
              <div class="product-line"  v-if="product.check == true">
                <div class="product-check">
                  <input type="checkbox" v-model="product.check">
                </div>
                <div class="product-image">
                  <img :src="product.image" alt="Ảnh s/p">
                </div>
                <div class="product-title">
                  {{ product.title }}
                </div>
                <div class="product-quantity"> x {{product.quantity}}</div>
              </div>
          </div>
        </div>
      </div>

      <div>
        title
        <input type="text" v-model="title">
      </div>

      <div>
        descripition
        <input type="text" v-model="description">
      </div>

      <div>
        location
        <select v-model="location">
          <option value="before">Before</option>
          <option value="after">After</option>
        </select>
      </div>

      <div>
        Font size
        <input type="number" v-model="font_size">
      </div>

      <div>
        Color
        <input type="color" v-model="color">
      </div>

      <div>
        Add to cart button color
        <input type="color" v-model="button_color">
      </div>

      <button @click="makeBundle">Make bundle</button>
    </div>


    <div class="product-content" v-else-if="url == 'https://odoo.website/apps/shopify/product'">
      <button>Create products</button>
      <div class="products-list">
        <div class="product-line">
          <div class="product-check">
          </div>
          <div class="product-image">
            Image
          </div>
          <div class="product-title">
            Title
          </div>
          <div class="product-variant">
            Variant
          </div>
          <div class="product-quantity">
            Quantity
          </div>
        </div>
        <div class="product-line" v-for="product in products">
          <div class="product-check">
            <input type="checkbox" v-model="product.check">
          </div>
          <div class="product-image">
            <img :src="product.image" alt="Ảnh s/p">
          </div>
          <div class="product-title">
            {{ product.title }}
          </div>
          <div class="product-variant">
            <select v-model="product.variant" v-if="product.variants.length>1">
              <option value="all">All variant</option>
              <option :value="variant.id" v-for="variant in product.variants">{{ variant.title }}</option>
            </select>
          </div>
          <div class="product-quantity">
            <input @change="changeQuantity(product)" type="number" v-model="product.quantity"/>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import {Modal, Button} from "ant-design-vue";
import axios from "axios";
import BundleNav from "./BundleNav.vue";

export default {
  data() {
    return {
      visible: false,
      shops: [],
      current_shop: null,
      discount_type: 'percentage',
      products: [],
      discount_value: 0,
      title:'',
      description:'',
      location:'before',
      color:'#000',
      button_color:'#000',
      font_size:14
    }
  },
  components: {
    BundleNav,
    Modal,
    Button,
  },
  methods: {
    async showModal() {
      this.visible = true
    },
    handleOk(e) {
      this.visible = false;
    },
    async updateProduct() {
      await axios.post('/products/update', {
        jsonrpc: 2.0,
        params: {shop: this.current_shop}
      })
          .then(async (response) => {
            this.products = JSON.parse(response.data.result)
          })
          .catch(e => console.log(e))
      this.visible = true
      for (let product of this.products) {
        product.check = false
        product.quantity = 0
      }
    },
    changeQuantity(product) {
      console.log(1)
      if (product.quantity > 0) {
        product.check = true
      }
    },
    async changeShop(){
      await axios.post('/products/fetch', {
        jsonrpc: 2.0,
        params: {shop: this.current_shop}
      })
          .then(async (response) => {
            this.products = JSON.parse(response.data.result)
          })
          .catch(e => console.log(e))

      for (let product of this.products) {
        product.check = false
        product.quantity = 0
        product.variant = product.variants[0].id
      }
    },
    makeBundle(){
      let products_bundle = []
      for (let product of this.products){
        if(product.check == true){
          if(product.variant == 'all'){
            let variant_id = []
            for(let variant of product.variants){
              variant_id.push(variant.id)
            }
            products_bundle.push({
                variant:variant_id,
                quantity:product.quantity
            })
          }else{
            products_bundle.push({
              variant:[product.variant],
              quantity:product.quantity
            })
          }
        }
      }
      axios.post('/bundle/create', {
        jsonrpc: 2.0,
        params: {
          title:this.title,
          description: this.description,
          shop: this.current_shop,
          discount_type: this.discount_type,
          discount_value: this.discount_value,
          products_bundle: products_bundle,
          location: this.location,
          font_size:this.font_size,
          color:this.color,
          button_color:this.button_color
        }
      })
    }
  }, computed: {
    url() {
      return this.$store.state.url
    }
  },
  async mounted() {
    await axios.post('/shops/info', {
      jsonrpc: 2.0,
      params: {}
    })
    .then(async (response) => {
      this.shops = JSON.parse(response.data.result)
      this.current_shop = this.shops[0].name
    })
    .catch(e => console.log(e))
    await axios.post('/products/fetch', {
        jsonrpc: 2.0,
        params: {shop: this.current_shop}
      })
          .then(async (response) => {
            this.products = JSON.parse(response.data.result)
          })
          .catch(e => console.log(e))
    for (let product of this.products) {
        product.check = false
        product.quantity = 0
        product.variant = product.variants[0].id
      }
  }
}
</script>


<style scoped>
.bundle {
  display: flex;
}

.bundle-content {
  margin: 20px 20%;
}

.modal-content {
  display: flex;
}

.modal-left {
  width: 60%;
}

.modal-right {
  width: 40%;
}

.modal-top {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.product-line {
  display: flex;
  width: 100%;
}

.product-line .product-check {
  width: 10%;
}

.product-line .product-image {
  width: 20%;
}

.product-line .product-image img {
  width: 50px;
  height: 50px;
}

.product-line .product-title {
  width: 20%;
}

.product-line .product-variant {
  width: 25%;
}

.product-line .product-quantity {
  width: 25%;
}

.product-line .product-quantity input {
  width: 100%;
}

.product-content {
  width: 100%;
}
</style>