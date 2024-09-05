from urllib import response


class WhoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            print(user.first_name) 
        else:
            print("Unknown user")  
        
        response = self.get_response(request) 
        
        return response  
       
       
# class popupForRegister:
#  def __init__(self,get_response):
#     self.get_response=get_response
    
#  def __call__(self,request):
#   user=request.user
#   if user.is_authenticated:
#    response['X_Show_Popup']='true'
#   else:
#    response['X-Show-Popup'] = 'false'
   
#   return response
