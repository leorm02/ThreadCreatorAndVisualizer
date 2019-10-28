import urwid
import threading
import time
import random
import time 

threads = list()
tempi = list()
values = []

class GraphView(urwid.WidgetWrap):

    palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('line',         'black',      'light gray', 'standout'),
        ('bg background','light gray', 'black'),
        ('bg 1',         'black',      'dark blue', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 2 smooth',  'dark cyan',  'black'),
        ('button normal','light gray', 'dark blue', 'standout'),
        ('button select','white',      'dark green'),
        ('line',         'black',      'light gray', 'standout'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
        ('pg smooth',     'dark magenta','black')
        ]   #palette tema 

    def __init__(self, x):
        urwid.WidgetWrap.__init__(self, self.main_window())

    def update_graph(self): 
        max_value = max(values)
        l = []
        for n in range(len(values)):
            
            if n & 1:
                l.append([0,values[n]])
            else:
                l.append([values[n],0])
        self.graph.set_data(l,max_value)

    def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

    def exit_program(self, w):
        raise urwid.ExitMainLoop()

    def graph_controls(self):
        testo = ""
        for i in range(len(values)):
            testo += "Thread_"+str(i) +": " + str(values[i]/float(1000)) + "s \n"
        # setup mode radio buttons
        self.mode_buttons = []
        l = [urwid.Text(testo,align="center"),
            urwid.Divider(),
            self.button("Quit", self.exit_program ),
            ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w

    def main_window(self):

        self.graph = urwid.BarGraph(['bg background','bg 1','bg 2'], satt={(1,0): 'bg 1 smooth', (2,0): 'bg 2 smooth'})
        self.graph_wrap = urwid.WidgetWrap( self.graph )
        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        c = self.graph_controls()
        w = urwid.Columns([('weight',2,self.graph_wrap),
            ('fixed',1,vline), c],
            dividechars=1, focus_column=2) 
        w = urwid.AttrWrap(w,'body')
        w = urwid.LineBox(w)
        w = urwid.AttrWrap(w,'line')
        return w

class GraphController:

    def __init__(self):
        self.view = GraphView(self)
        # update the view
        self.view.update_graph()

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()
 
class myThread (threading.Thread):
    def __init__(self, threadID, name,counter):

        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        tempo = -(int(round(time.time() * 1000)))
        print("Starting " + self.name)
        print_time(self.name, self.counter,  5)
        print("exiting " + self.name)
        tempo = tempo + int(round(time.time() * 1000))
        values.insert(self.threadID, tempo)

def print_time(threadName, delay, counter):
    while counter:        
        time.sleep(random.randint(1, delay))
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

class MyTerminal(urwid.WidgetWrap):

    def __init__(self):

        self.screen_text = urwid.Text("Inserisci numero thread da creare poi premi enter per far iniziare il programma")
        self.prompt_text = urwid.Edit('Numero Thread: ', '')
        self._w = urwid.Frame(header=urwid.Pile([urwid.Text('Crea Thread'),
                             urwid.Divider()]),
                             body=urwid.ListBox([self.screen_text]),
                             footer=self.prompt_text,
                             focus_part='footer')

    def keypress(self, size, key):    
        if key == 'enter':
            createThread(int(self.prompt_text.edit_text))
            raise urwid.ExitMainLoop()
        super(MyTerminal, self).keypress(size, key)

def createThread(nThread):
    for i in range(nThread):
        delay = 5 
        threadName = "Thread-"+str(i)

        newThread = myThread(i, threadName, delay)

        threads.append(newThread)#appending new thread
        newThread.start()#starting new thread
    
    for thread in threads:
        thread.join()

def main():

    my_term = MyTerminal()

    urwid.MainLoop(my_term).run()    

    print ("Exiting Main Thread")

    GraphController().main()

if '__main__'==__name__:
    main()



