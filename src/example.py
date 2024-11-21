from src.init import *
from src.landing import *

def graph_data_generator(yData_sets,start_time,end_time,delta, **kwargs):
    
    xData = []
    while start_time <= end_time:
        xData.append(start_time.strftime('%Y-%m-%d %H:%M:%S'))  # or any other format you prefer
        start_time += delta

    # Just for demonstration, I'm populating yData with dummy random values for each hour
    # You can replace it with your actual data or any other logic
    yData = []

        
    for counter in range(yData_sets):
        if kwargs.get('range'):
            yData.append([round(random.uniform(kwargs.get('range')[0], kwargs.get('range')[1]),2) for _ in xData])
        elif kwargs.get('negative'):
            yData.append([random.randint(-500, 500) for _ in xData])
        else:
            yData.append([random.randint(counter*100, (counter+1)*100) for _ in xData])

    if yData_sets == 1:
        yData = yData[0]

    return xData,yData


def embed_graph_data(request,context, **kwargs):

    # Dummy data with datetime strings
    
    # Creating a 48-hour range of datetime data
    end_time = datetime.now()
    if kwargs.get('start_time'):
        start_time = kwargs.get('start_time')
    elif "bar" in request.path:
        start_time = end_time - timedelta(days=14)
    elif "pie" in request.path:
        start_time = end_time - timedelta(days=5)
    else:
        start_time = end_time - timedelta(hours=48)
    
    if "bar" in request.path:
        delta = timedelta(days=1)
    elif "pie" in request.path:
        delta = timedelta(days=1)
    else:
        delta = timedelta(hours=1)

    yData_sets = 3 # How many set of data (just for demo purpose)
    xData,yData = graph_data_generator(yData_sets,start_time,end_time,delta)
    seriesName = []

    for counter in range(yData_sets):
        seriesName.append(f"Series {counter+1}")

    if "pie" in request.path:
        seriesName = [f"Parameter {k}" for k,_ in enumerate(xData)]
    
    negtive_yData = [random.randint(-500, 500) for _ in xData]

    xRange_start = end_time - delta*10
    xRange_end = end_time - delta*6
    context['xRange']= [xRange_start.strftime('%Y-%m-%d %H:%M:%S'),xRange_end.strftime('%Y-%m-%d %H:%M:%S')]
    context['xData']= xData
    context['yData']= yData
    context['negtive_yData']= negtive_yData
    context['seriesName']= seriesName
    return context


@superuser_required
@login_required
def table(request):
    context = initialization(request)
    context['Account'] = Account.objects.all()
    context['table_header'] = ["Parameter A","Parameter B","Parameter C","Parameter D","Parameter E"]
    context['table_data'] = [[random.randint(0, 100) for _ in range(5)] for _ in range(10)] # Dummy data
    return render(request,'example/table.html', context)

@superuser_required
@login_required
def layout(request):
    context = initialization(request)
    return render(request,'example/layout.html', context)

@superuser_required
@login_required
def graph(request):
    context = initialization(request)
    # Dummy data with datetime strings
    context = embed_graph_data(request,context)
    
    print(context['yData'])
    if "bar" in request.path:
        return render(request,'example/bar_graph.html', context)
    elif "pie" in request.path:
        return render(request,'example/pie_graph.html', context)
    else:
        return render(request,'example/line_graph.html', context)

@superuser_required
@login_required
def icon_list(request):
    context = initialization(request)
    
    return render(request,'example/icon_list.html', context)

@superuser_required
@login_required
def button(request):
    context = initialization(request)
    
    return render(request,'example/button.html', context)

@superuser_required
@login_required
def card(request):
    context = initialization(request)

    context = embed_graph_data(request,context)
    
    return render(request,'example/card.html', context)

@superuser_required
@login_required
def inputfile(request):
    context = initialization(request)
    if request.method == "POST":
        print(request.POST)
        # Call "SaveFile" function to convert POST request file (string) to file object
        file_obj = SaveFile(request.POST.get("InputFile")) 
        SavedFile.objects.create(File=file_obj)
    
    return render(request,'example/fileinput.html', context)


@superuser_required
@login_required
def input(request):
    context = initialization(request)
    if request.method == "POST":
        # print(request.POST.get('Editor'))
        # print(request.POST)
        print("\n----------------------------------------------------------")
        context['result'] = {}
        ignore_list = ['csrfmiddlewaretoken']
        not_show_list = ['Editor']
        for key in request.POST:
            if request.POST[key]:
                # Process File where it look something like this 
                # ['{"fileUrls": ["/media/temp/a_a7f8JdC.txt"]}', '{"fileUrls": ["/media/temp/a.txt"]}']
                if key == "File":
                    file_list = request.POST.getlist(key)
                    context['result'][key] = []
                    for file in file_list:
                        file = json.loads(file)
                        context['result'][key].append(file.get("fileUrls")[0])

                # Other than csrf, this function just parse all back for showing
                # Editor not show because it is too large
                elif key not in ignore_list:
                    context['result'][key] = request.POST.getlist(key)
                    if len(context['result'][key]) == 1:
                        context['result'][key] = context['result'][key][0]

                if key in context['result'] and key not in not_show_list:
                    print(key,"=",context['result'][key],":",type(context['result'][key]))
        print("----------------------------------------------------------\n")
    
    return render(request,'example/input.html', context)

def page_creator(request):
    context = initialization(request)
    if request.method == "POST":
        print(request.POST)
        context['parameters'] = []
        context['row_config'] = request.POST.getlist('row_config')
        for key in request.POST:
            if "rowitem" in key:
                content_type = request.POST.getlist(key)
                print(content_type)
                if type(content_type) == list:
                    context['parameters'].append(content_type)
                else:
                    context['parameters'].append([content_type])
        if context['parameters']:
            print(context)
            return render(request,'example/page_creator2.html', context)
    return render(request,'example/page_creator.html', context)



@superuser_required
@login_required
def modal(request):
    context = initialization(request)
    
    return render(request,'example/modal.html', context)

@superuser_required
@login_required
def page(request):
    context = initialization(request)
    
    return render(request,'example/page.html', context)

@superuser_required
@login_required
def animation(request):
    context = initialization(request)
    
    return render(request,'example/animation.html', context)
