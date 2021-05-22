from tkinter import Label, Button, Frame
from textwrap import dedent

try:
    from .frame import ScrolledFrame
except ImportError:
    from pathlib import Path
    from subprocess import run
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit


class Example(ScrolledFrame):
    lbl: Label
    hLbls: list[Label]
    vLbls: list[Label]
    curCol: int
    curRow: int
    rdBtn: Button
    rHzBtn: Button
    rVtBtn: Button

    def __init__(self):
        ScrolledFrame.__init__(self)
        self.grid(column=0,
                  columnspan=2,
                  row=1,
                  rowspan=2,
                  sticky='nsew')
        self.option_add('*font', 'Ebrima 12')

        self.container.master.columnconfigure(0, weight=1)
        self.container.master.rowconfigure(1, weight=1)

        self.lbl = Label(master=self,
                         text='Start',
                         justify='left',
                         relief='ridge')
        self.lbl.grid(sticky='nsew')
        self.hLbls = list()
        self.vLbls = list()
        self.curCol = 1
        self.curRow = 1

        rLbl = Label(master=self,
                     text='Horizontal1')
        rLbl.grid(column=self.curCol,
                  row=0)

        bLbl = Label(master=self,
                     text='Vertical1')
        bLbl.grid(column=0,
                  row=self.curRow)

        self.rdBtn = Button(text="View readme",
                            command=self.addReadme)
        self.rdBtn.grid(column=0,
                        row=0)

        hzFrm = Frame(bd=1,
                      relief='ridge')
        hzFrm.grid(column=2,
                   row=1)
        hzLbl = Label(master=hzFrm,
                      text="Right Labels:")
        hzLbl.grid(column=0,
                   columnspan=2,
                   row=0)
        aHzBtn = Button(master=hzFrm,
                        text="Add",
                        command=self.addHorz)
        aHzBtn.grid(column=0,
                    row=1)
        self.rHzBtn = Button(master=hzFrm,
                             text="Remove",
                             command=self.remHorz,
                             state='disabled')
        self.rHzBtn.grid(column=1,
                         row=1)

        vtFrm = Frame(bd=1,
                      relief='ridge')
        vtFrm.grid(column=0,
                   row=3)
        vtLbl = Label(master=vtFrm,
                      text="Bottom Labels:")
        vtLbl.grid(column=0,
                   columnspan=2,
                   row=0)
        aVtBtn = Button(master=vtFrm,
                        text="Add",
                        command=self.addVert)
        aVtBtn.grid(column=0,
                    row=1)
        self.rVtBtn = Button(master=vtFrm,
                             text="Remove",
                             command=self.remVert,
                             state='disabled')
        self.rVtBtn.grid(column=1,
                         row=1)

        self.master.mainloop()

    def addReadme(self):
        self.rdBtn.config(text="Hide readme",
                          command=self.remReadme)
        self.lbl.config(text=(f'{ScrolledFrame.__doc__}\n'
                              f'{dedent(ScrolledFrame.__init__.__doc__)}'))
        self.redraw()

    def remReadme(self):
        self.rdBtn.config(text="Show readme",
                          command=self.addReadme)
        self.lbl.config(text='Start')
        self.redraw()

    def addHorz(self) -> None:
        self.curCol += 1
        txt = f'Horizontal{self.curCol}'
        rLbl = Label(master=self,
                     text=txt)
        rLbl.grid(column=self.curCol,
                  row=0)
        self.hLbls.append(rLbl)
        self.redraw()
        self.rHzBtn.config(state='normal')

    def remHorz(self) -> None:
        if self.hLbls:
            self.hLbls.pop().destroy()
            self.curCol -= 1
            self.redraw()
            if not self.hLbls:
                self.rHzBtn.config(state='disabled')

    def addVert(self) -> None:
        self.curRow += 1
        txt = f'Vertical{self.curRow}'
        bLbl = Label(master=self,
                     text=txt)
        bLbl.grid(column=0,
                  row=self.curRow)
        self.vLbls.append(bLbl)
        self.redraw()
        self.rVtBtn.config(state='normal')

    def remVert(self) -> None:
        if self.vLbls:
            self.vLbls.pop().destroy()
            self.curRow -= 1
            self.redraw()
            if not self.vLbls:
                self.rVtBtn.config(state='disabled')


if __name__ == "__main__":
    Example()
