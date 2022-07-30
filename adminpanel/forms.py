from django import forms
from store.models import Product
from category.models import Category


# class AddProductForm(forms.ModelForm):
#     class Meta:
#         model=Product
#         fields = '__all__'

# class AddProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [ 'product_name', 'slug', 'description', 'price', 'image', 'stock', 'is_available', 'category']

#         def __init__ (self,args,*kwargs):
#             super(AddProductForm,self).__init__(args,*kwargs)
        

#             self.fields['category'].widget.attrs['class'] = 'form-control'

#             self.fields['product_name'].widget.attrs['placeholder'] = 'product name'
#             self.fields['product_name'].widget.attrs['class'] = 'form-control'
#             self.fields['product_name'].widget.attrs['type'] = 'text'

#             self.fields['stock'].widget.attrs['placeholder'] = 'available stock'
#             self.fields['stock'].widget.attrs['class'] = 'form-control'
#             self.fields['stock'].widget.attrs['type'] = 'text'
            
#             self.fields['is_available'].widget.attrs['class'] = 'form-check-input'
#             self.fields['is_available'].widget.attrs['type'] = 'checkbox '

#             self.fields['price'].widget.attrs['placeholder'] = 'price'
#             self.fields['price'].widget.attrs['class'] = 'form-control'
#             self.fields['price'].widget.attrs['type'] = 'text'

#             self.fields['description'].widget.attrs['placeholder'] = 'product description'
#             self.fields['description'].widget.attrs['class'] = 'form-control'
#             self.fields['description'].widget.attrs['type'] = 'text'
#             self.fields['description'].widget.attrs['rows'] = '3'

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','description','price','image','is_available','stock','category']

    def _init_(self,args,*kwargs):
        super(AddProductForm,self)._init_(args,*kwargs)

        self.fields['product_name'].widget.attrs['placeholder']='Enter Product name'
        self.fields['product_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['product_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Product discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3

        self.fields['price'].widget.attrs['placeholder']='Enter Product Price'
        self.fields['price'].widget.attrs['class']='form-control form-control-user'
        self.fields['price'].widget.attrs['type']='text'

        self.fields['stock'].widget.attrs['placeholder']='Enter Product Stock'
        self.fields['stock'].widget.attrs['class']='form-control form-control-user'
        self.fields['stock'].widget.attrs['type']='text'


        self.fields['category'].widget.attrs['class']='form-control form-control-user'


        self.fields['image'].widget.attrs['placeholder']='Add images'
        self.fields['image'].widget.attrs['class']='form-control'
        self.fields['image'].widget.attrs['type']='file'

class EditCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'slug', 'description', 'is_available', 'cat_images']

