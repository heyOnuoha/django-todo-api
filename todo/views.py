from django.http.response import HttpResponse
from django.core import serializers
from .models import TodoItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils import  timezone
import json

@csrf_exempt # Tells Django to not worry about cross-site request forgery
# add todo item to our model
def add_todo(request):
    
    if request.method == 'POST': # make sure the request is a POST request

        # First we will read the todo data from the request.body object
        
        body = ''
        
        try:
        
            body = json.loads(request.body.decode('utf-8')) # parse json body from string to python dictionary
            
        except json.JSONDecodeError:
            
            return JsonResponse({
                'status': False,
                'message': 'JSON body was not supplied' # tell developer to set the content type to application/json and pass and empty json
            })
        
        title = body.get('title')
        description = body.get('description')
        
        # next, check if the title is empty or null
        
        if title is None or title == '':
            
            # return false message if field `title` is empty or null
            
            return JsonResponse({
                'status': False,
                'message': 'Field `title` is required' 
            })
            
        # next, check if the description is empty or null
            
        if description is None or description == '':
            
            # return false message if field `description` is empty or null
            
           description = '' # set description to an empty string

        todo = TodoItem(title=title, description=description) # Initialize a new Todo Item
        todo.save() # save todo item

        #return true message after saving the todo item

        return JsonResponse({
            'status': True,
            'message': f'Todo Item: {title}  has been created'
        })

            
    # return false message if any other method is used

    return JsonResponse({
        'status': False,
        'message': 'ONLY POST METHOD ALLOWED'
    })

@csrf_exempt # Tells Django to not worry about cross-site request forgery  
# a view to fetch all todo items
def get_todos(request):
    
    if request.method == 'GET': # make sure the request is a GET request
        
        todos = TodoItem.objects.values() # query all todo items in our TodoItem model, we use the .values() because Queryset is not serializable
        todos_list = list(todos) # list converts query sets to python readable list

        return JsonResponse({
            'status': True,
            'payload': todos_list # return a field `payload` containing an array of todo items
        }, safe=False) # 
        
    # return false message if any other method is used

    return JsonResponse({
        'status': False,
        'message': 'ONLY GET METHOD ALLOWED'
    })

@csrf_exempt # Tells Django to not worry about cross-site request forgery   
# get single todo item
def get_todo_by_id(request, id): # id of todo item (read from route)
    
    if request.method == 'GET': # make sure the request is a GET request
        
        todo_item = TodoItem.objects.filter(pk=id)
        todo_item_exist = todo_item.exists()
        
        if not todo_item_exist:
            
            return JsonResponse({
                'status': False, # we return false to tell the frontend that something went wrong
                'message': 'Todo item does not exists' # return a field `payload` containing an array of todo items
            })
            
        return JsonResponse({
            'status': True,
            'payload': model_to_dict(todo_item.first()) # fetch the first and only item in the queryset
        })

    # return false message if any other method is used
    return JsonResponse({
        'status': False,
        'message': 'ONLY GET METHOD ALLOWED'
    })

@csrf_exempt # Tells Django to not worry about cross-site request forgery    
# update single todo item
def update_todo(request, id): # id of todo item (read from route)
    
    if request.method == 'PUT': # make sure the request is a PUT request
        
        # First we will read the todo data from the request.body object
        
        body = json.loads(request.body.decode('utf-8')) # parse json body from string to python dictionary
        
        title = body.get('title')
        description = body.get('description')
        
        # next, check if the title is empty or null
        
        if title is None or title == '':
            
            # return false message if field `title` is empty or null
            
            return JsonResponse({
                'status': False,
                'message': 'Field `title` is required' 
            })
            
        # next, check if the description is empty or null
            
        if description is None or description == '':
            
            # return false message if field `description` is empty or null
            
            description = '' # set description to an empty string
        
        todo_item = TodoItem.objects.filter(pk=id)
        todo_item_exist = todo_item.exists()
        
        if not todo_item_exist:
            
            return JsonResponse({
                'status': False, # we return false to tell the frontend that something went wrong
                'message': 'Todo item does not exists' # return a field `payload` containing an array of todo items
            })
            
        todo_item.update(title=title, description=description) # query to update the title and description field
        
        return JsonResponse({
            'status': True,
            'payload': model_to_dict(todo_item.first()) # fetch the first and only item in the queryset
        })
        

    # return false message if any other method is used
    return JsonResponse({
        'status': False,
        'message': 'ONLY PUT METHOD ALLOWED'
    })

@csrf_exempt # Tells Django to not worry about cross-site request forgery    
# complete single todo item
def complete_todo(request, id): # id of todo item (read from route)
    
    if request.method == 'PUT': # make sure the request is a GET request
        
        todo_item = TodoItem.objects.filter(pk=id)
        todo_item_exist = todo_item.exists()
        
        if not todo_item_exist:
            
            return JsonResponse({
                'status': False, # we return false to tell the frontend that something went wrong
                'message': 'Todo item does not exists' # return a field `payload` containing an array of todo items
            })
            
        todo_item.update(is_completed=True, completed_at=timezone.now()) # query to update the field is_completed to True
        
        return JsonResponse({
            'status': True,
            'message': 'Todo completed'
        })

    # return false message if any other method is used
    return JsonResponse({
        'status': False,
        'message': 'ONLY PUT METHOD ALLOWED'
    })
   
@csrf_exempt # Tells Django to not worry about cross-site request forgery 
# delete single todo item
def delete_todo(request, id): # id of todo item (read from route)
    
    if request.method == 'DELETE': # make sure the request is a DELETE request
        
        todo_item = TodoItem.objects.filter(pk=id)
        todo_item_exist = todo_item.exists()
        
        if not todo_item_exist:
            
            return JsonResponse({
                'status': False, # we return false to tell the frontend that something went wrong
                'message': 'Todo item does not exists' # return a field `payload` containing an array of todo items
            })
            
        todo_item.delete()
            
        return JsonResponse({
            'status': True,
            'message': 'Todo deleted'
        })
        

    # return false message if any other method is used
    return JsonResponse({
        'status': False,
        'message': 'ONLY DELETE METHOD ALLOWED'
    })