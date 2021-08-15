from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import loader
import datetime
import pytz

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
    todolists = TodoList.objects.all()
    items = TodoItem.objects.all()
    # template = loader.get_template('todo/index.html')
    context = {
        'todolists': todolists,
        'todoitems': items,
    }

    # return HttpResponse(template.render(context,request)) #this or->
    return render(request, 'todo/index.html',context)

def view(request):
    todolists = TodoList.objects.all()
    items = TodoItem.objects.all()
    # template = loader.get_template('todo/index.html')
    context = {
        'todolists': todolists,
        'todoitems': items,
    }

    # return HttpResponse(template.render(context,request)) #this or->
    return render(request, 'todo/view.html',context)


def detail(request,list_id):
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
    
    # if(request.POST["action"]=="Update"):
    if 'update' in request.POST:
        todolist_name = request.POST["name"]
        t=TodoList.objects.get(id=list_id)
        items_list=TodoItem.objects.filter(todo_list=t)

        todolist=request.POST["name"]
        TodoList.objects.filter(id=list_id).update(list_name=todolist_name)
        todolists = TodoList.objects.all()
        
    elif 'delete' in request.POST:
        t=TodoList.objects.get(id=list_id)
        t.delete()

    todolists = TodoList.objects.all()
    items = TodoItem.objects.all()
    context = {
        'todolists': todolists,
        'todoitems': items,
    }
    return render(request, 'todo/index.html', context)

def createlist(request):
    if request.method == "GET":
        return render(request, 'todo/createlist.html')

    name = request.POST["name"]
    TodoList.objects.create(list_name=name)
    lists = TodoList.objects.all()
    context = {
        'todolists': lists,
    }
    return render(request, 'todo/index.html', context)

def createitem(request):
    if request.method == "GET":
        lists = TodoList.objects.all()
        context = {
        'todolists': lists,
        }
        return render(request, 'todo/createitem.html',context)

    todo_list = int(request.POST["todolist"])
    todoitem=request.POST["item"]
    check=bool(request.POST.get("check",False))
    print(check)
    t=TodoList.objects.get(id=todo_list)
    time=request.POST.get("time")
    date=request.POST.get("date")
    if(time!=''):
        duetime=datetime.datetime.strptime(time,'%H:%M').time()

    if(date!=''):
        duedate=datetime.datetime.strptime(date,'%Y-%m-%d').date()

    if(date=='' and time==''):
        due_date=''
    else:
        due_date=datetime.datetime.combine(duedate,duetime)


    print(due_date)
    if(due_date!=''):
        TodoItem.objects.create(title=todoitem,checked=check,due_date=due_date,todo_list=t)
    else:
        TodoItem.objects.create(title=todoitem,checked=check,todo_list=t)

    for obj in TodoItem.objects.filter(title=todoitem):
        print(obj.due_date)

    t=TodoList.objects.get(id=todo_list)
    items_list=TodoItem.objects.filter(todo_list=todo_list)
    context = {
        'todolist': t,
        'items_list':items_list,
    }
    return render(request, 'todo/detail.html', context)

def item(request,list_id,item_id):
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
        todo_list = int(request.POST["todolist"])
        t=TodoList.objects.get(id=todo_list)
        items_list=TodoItem.objects.filter(todo_list=todo_list)

        obj=TodoItem.objects.get(id=item_id)
        todoitem=request.POST["item"]
        todochecked=bool(request.POST.get("check",False))
        time=request.POST.get("time")
        date=request.POST.get("date")
        print(obj)
        print(obj.due_date)
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
        

    elif 'delete' in request.POST:
        todoitem=TodoItem.objects.get(id=item_id)
        todoitem.delete()

        todo_list = int(request.POST["todolist"])
        t=TodoList.objects.get(id=todo_list)
        items_list=TodoItem.objects.filter(todo_list=todo_list)

    context = {
        'todolist': t,
        'items_list':items_list,
    }
    return render(request, 'todo/detail.html', context)