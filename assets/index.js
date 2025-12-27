import "./styles/layout.css"
import "./styles/bootstrap.min.css"
import "./styles/animate.min.css"
import "./styles/bolt.css"
import "./styles/custom.css"
// JS
import 'bootstrap'

import 'owl.carousel/dist/assets/owl.carousel.css';
import "owl.carousel"

// Import all of Bootstrap’s CSS
import Alpine from "alpinejs"
import "./js/main"
import "./js/alpineFun.js"
import axios from "axios"

window.axios = axios
window.addEventListener('dragover',e =>{
  e.preventDefault()
})
window.addEventListener('drop',e => {
  e.preventDefault()
},false)


const createProducts = {
    validateForm(formdata){
      const errorrank = [3,3,2]
      formdata.forEach((ele,key) => {
        if(key == "product_name" || key == "product_about" || key == "product_images"){
           if(ele == ""){
             if(!this.error.find(e => e == 'General information')){
              this.error.push('General information')
            }
            return false;
          }else if(ele != undefined || ele != ""){
            errorrank[0] -= 1
            if(errorrank[0] <= 0){
              this.error = this.error.filter(item => item != 'General information')
            }
          }
        }else if(key == "product_price" || key == "product_weight" || key == "product_quantity"){
          if(ele == ""){
            if(!this.error.find(e => e == 'Product and Other')){
              this.error.push('Product and Other')
            }
            return false;
          }else{
            errorrank[1] -= 1
            if(errorrank[1] <= 0){
              this.error = this.error.filter(item => item != 'Product and Other')
            }
          }
        }else if(key == "product_detail" || key == "product_catagory"){ 
          if(ele == ""){
            if(!this.error.find(e => e == 'Catagory')){
              this.error.push('Catagory')
            }
            return false;
          }else if(key == "product_detail" && ele.length == 2){
            if(!this.error.find(e => e == 'Catagory')){
              this.error.push('Catagory')
            }
            return false;
          }
          else{
            errorrank[2] -= 1
            if(errorrank[2] <= 0){
              this.error = this.error.filter(item => item != 'Catagory')
            }
          }        
        }
        if(errorrank[0] == 0 && errorrank[1] == 0 && errorrank[2] == 0){
          return true
        }
      });
    },
     imageCollector(event){
        for(let i of event.target.files){
          if(this.images.length < 5){
            this.images.push({'file':i,'url':URL.createObjectURL(i)})
          }
        }
    },
    removeImage(event,x){
    event.preventDefault()
    var dt = new DataTransfer()
    for (let i of this.$refs.imgfile.files){
        if(x != URL.createObjectURL(i)){
            dt.items.add(i)
        }
    }
    this.$refs.imgfile.files = dt.files
    this.images = this.images.filter(item => item.url != x)
    },
    dragAndDrop(event){
      var test =document.getElementById("create_product_overlay").style.display
      if(test == 'none'){
        document.getElementById("create_product_overlay").style.display = "block"
      }else{
        document.getElementById("create_product_overlay").style.display = 'none'
      }
    },
    DropImage(event){
      for(let i of event.dataTransfer.files){
        if(this.images.length < 5){
          this.images.push({'file':i,'url':URL.createObjectURL(i)})
        }
      }
      document.getElementById("create_product_overlay").style.display = 'none'
    },
    SetUpImages(event){

    },
    dataupdater(id,key,value){
      if(id > this.result.length ){
          if(key=='name'){
              this.result.push({'name':value,'value':''})
          }else{
              this.result.push({'name':'','value':value}) 
          }
          }else{
          const temp = this.result[id - 1]
            if(key=='name'){
              temp.name = value
          }else{
              temp.value = value
          }
      }
    },
    truedataupdater(id,key,value){
      if(id){
          if(key=='name'){
              id.name = value
          }else{
             id.value =value
          }
        }
        console.log(this.items)
    },
    catfinder(event){
      if(event.target.value == ""){
        this.searchedcat = []
        return;
      }
      if(this.selectedcat >= 5){
        return;
      }
      const ul = this.catagories.filter(e => e.fields.name.toLowerCase().includes(event.target.value.toLowerCase()))
      this.searchedcat = ul
    },
    HandleEvent(event,url,token,form){
      event.preventDefault()
      var formdata = new FormData(form)
      const detail = JSON.stringify(this.result)
      if(this.images.lenth != 0){
        formdata.delete("product_images")
        for (let i of this.images){
          formdata.append('product_images',i.file)
        }
      }else if(this.images.lenth == 0){
        formdata.append('product_images',"")
      }
      if(this.selectedcat.length > 0){
        formdata.delete("product_catagory")
        for(let i of this.selectedcat){
          formdata.append('product_catagory',i.pk)
        }
      }else{
        formdata.append('product_catagory',"")
      }
      formdata.append('product_detail',detail)
      const isValid = this.validateForm(formdata)
      if(isValid){
        return;
      }
      this.postsent = true
      axios.post(url,formdata,{headers:{'X-CSRFToken':token}}).then(e => {
        window.location.href = this.home
      }).catch(e => {

      }).finally(e=>{
          this.postsent = false
      })
    }
}
 


window.createProducts = createProducts

window.Alpine = Alpine

Alpine.start()



window.htmx = require('htmx.org')
import Chart from 'chart.js/auto';
window.Chart = Chart;

  
document.addEventListener('DOMContentLoaded', (event) => {
  document.getElementById('bodyContanier').classList.remove('loading-page')
    const popup = document.getElementById('popupmessage');
    if(popup){
      setTimeout(() => {
        popup.classList.add('hiddenaftertime'); 
      }, 3000);
    }
  });
