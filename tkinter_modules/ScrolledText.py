from tkinter import *
'''tnx to Mark Lutz'''
class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        # сделать растягиваемым
        self.makewidgets()
        self.settext(text, file)
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        # связать sbar и text
        text.config(yscrollcommand=sbar.set) # сдвиг одного = сдвиг другого
        sbar.pack(side=RIGHT, fill=Y)
        # первым добавлен - посл. обрезан
        text.pack(side=LEFT, expand=YES, fill=BOTH) # Text обрезается первым
        self.text = text
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()
    
    def gettext(self):
        # возвращает строку
        return self.text.get('1.0', END+'-1c') # от начала до конца
if __name__ == '__main__':
    root = Tk()
    if len(sys.argv) > 1:
        st = ScrolledText(file=sys.argv[1])
    #
    else:
        st = ScrolledText(text='Words\ngo here')
    def show(event):
        print(repr(st.gettext()))
    #
    root.bind('<Key-Escape>', show)
    #
    root.mainloop()
