from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.template import loader
from django.db import IntegrityError
import datetime
import pytz
from django.core.exceptions import ValidationError

from .models import TodoList
from .models import TodoItem

# Create your views here.

#->before template
# def index(request):
#     todolists = TodoList.objects.all()
#     list_items=TodoItem.objects.all()

#     output=', '.join(item.title for item in list_items) 
#     return HttpResponse(output)

# after template
def index(request):
    """url:todo/ , Home page displays links to all lists"""

    todolists = TodoList.objects.all()
    todoitems = TodoItem.objects.all()
    # template = loader.get_template('todo/index.html')
    context = {
        'todolists': todolists,
        'todoitems': todoitems,
    }
    # return HttpResponse(template.render(context,request)) #this or->
    return render(request, 'todo/index.html',context)

def view(request):
    """displays all lists and items in todo app"""

    todolists = TodoList.objects.all()
    todoitems = TodoItem.objects.all()
    # template = loader.get_template('todo/index.html')
    context = {
        'todolists': todolists,
        'todoitems': todoitems,
    }

    # return HttpResponse(template.render(context,request)) #this or->
    return render(request, 'todo/view.html',context)

def createlist(request):
    """creates list"""

    if request.method == "GET":
        return render(request, 'todo/createlist.html')

    name = request.POST.get("name")
    if(name == ""):
        return HttpResponse("Error: Name cannot be blank")
    try:
        TodoList.objects.create(list_name=name)
        lists = TodoList.objects.all()
        context = {
            'todolists': lists,
        }
        return redirect("/todo/")
    except IntegrityError:
        return HttpResponse("Error: list name already exists")

def detail(request,list_id):
    """each list in detail -- updation and deletion"""

    if request.method == "GET":
        try:
            todolist=TodoList.objects.get(id=list_id)
        except:
            raise Http404("This List Does not exist")
        items_list=TodoItem.objects.filter(todo_list=todolist)
        context={
            'todolist':todolist,
            'items_list':items_list
        }
        return render(request, 'todo/detail.html',context)   
    
    if 'update' in request.POST:
        todolist_name = request.POST.get("name")
        if(todolist_name == ""):
            return HttpResponse("Error: Name cannot be blank")
        try:
            t=TodoList.objects.get(id=list_id)
            items_list=TodoItem.objects.filter(todo_list=t)

            todolist=request.POST.get("name")
            TodoList.objects.filter(id=list_id).update(list_name=todolist_name)
            todolists = TodoList.objects.all()
        except IntegrityError:
            return HttpResponse("Error: list name already exists")

    elif 'delete' in request.POST:
        try:
            t=TodoList.objects.get(id=list_id)
            t.delete()
        except:
            return Http404("This list does not exist")
        
    todolists = TodoList.objects.all()
    items = TodoItem.objects.all()
    context = {
        'todolists': todolists,
        'todoitems': items,
    }
    return redirect("/todo/")

def createitem(request,list_id=None):
    """creates item"""

    if request.method == "GET":
        lists = TodoList.objects.all()
        context = {
        'todolists': lists,
        'listid':list_id
        }
        return render(request, 'todo/createitem.html',context)

    todoitem=request.POST.get("item")
    if(todoitem==""):
        return HttpResponse("Error: List name cannot be blank")

    try: 
        todo_list = request.POST.get("todolist")
        try:
            t=TodoList.objects.get(id=todo_list)
        except:
            raise Http404("List id not found")

        todo_list=int(todo_list)
        check=bool(request.POST.get("check",False))
        time=request.POST.get("time")
        date=request.POST.get("date")
        if(time!=''):
            duetime=datetime.datetime.strptime(time,'%H:%M').time()
        else:
            duetime=datetime.datetime.now().strftime('%H:%M')
            duetime=datetime.datetime.strptime(duetime,'%H:%M').time()

        if(date!=''):
            duedate=datetime.datetime.strptime(date,'%Y-%m-%d').date()
        else:
            duedate=datetime.datetime.now().strftime('%Y-%m-%d')
            duedate=datetime.datetime.strptime(duedate,'%Y-%m-%d').date()

        due_date=datetime.datetime.combine(duedate,duetime)

        TodoItem.objects.create(title=todoitem,checked=check,due_date=due_date,todo_list=t)

        for obj in TodoItem.objects.filter(title=todoitem):
            print(obj.due_date)

        t=TodoList.objects.get(id=todo_list)
        items_list=TodoItem.objects.filter(todo_list=todo_list)
        context = {
            'todolist': t,
            'items_list':items_list,
        }
        return redirect("/todo/"+str(todo_list))
    except IntegrityError:
        return HttpResponse("Error: item name already exists under the selected list")

def item(request,list_id,item_id):
    """shows each item in detail -- updation and deletion"""
    
    if request.method == "GET":
        try:
            todolist = TodoList.objects.get(id=list_id)
        except:
            raise Http404("This List Does not exist")
        try:
            todoitem=TodoItem.objects.get(id=item_id)
        except:
            raise Http404("This Item Does not exist")
        lists = TodoList.objects.all()
        context = {
        'todolist': todolist,
        'todoitem': todoitem,
        'todolists':lists,
        }
        return render(request, 'todo/item.html',context)
    
    if 'update' in request.POST:
        try:
            todo_list = int(request.POST.get("todolist"))
            try:
                t=TodoList.objects.get(id=todo_list)
            except:
                return Http404("List does not exist")
            items_list=TodoItem.objects.filter(todo_list=todo_list)

            obj=TodoItem.objects.get(id=item_id)
            todoitem=request.POST.get("item")
            if(todoitem==""):
                return HttpResponse("Error: List name cannot be blank")
            
            todochecked=bool(request.POST.get("check",False))
            time=request.POST.get("time")
            date=request.POST.get("date")
            if(time!=''):
                duetime=datetime.datetime.strptime(time,'%H:%M').time()
            else:
                time=obj.due_date.strftime('%H:%M')
                duetime=datetime.datetime.strptime(time,'%H:%M').time()
            if(date!=''):
                duedate=datetime.datetime.strptime(date,'%Y-%m-%d').date()
            else:
                date=obj.due_date.strftime('%Y-%m-%d')
                duedate=datetime.datetime.strptime(date,'%Y-%m-%d').date()
            due_date=datetime.datetime.combine(duedate,duetime)

            TodoItem.objects.filter(id=item_id).update(title=todoitem,checked=todochecked,due_date=due_date,todo_list=t)
        except IntegrityError:
            return HttpResponse("Error: item name already exists under the selected list")
        

    elif 'delete' in request.POST:
        todoitem=TodoItem.objects.get(id=item_id)
        todoitem.delete()

        todo_list = int(request.POST.get("todolist"))
        try:
            t=TodoList.objects.get(id=todo_list)
            items_list=TodoItem.objects.filter(todo_list=todo_list)
        except:
            return HttpResponse("List name not given")
        
    context = {
        'todolist': t,
        'items_list':items_list,
    }
    return redirect("/todo/"+str(list_id))