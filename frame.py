from tkinter import Frame, Canvas, Scrollbar, Grid, Pack, Place, Widget, Event
from re import search as re_search
from typing import (Union as U,
                    Optional as O,
                    Callable as C)


class ScrolledFrame(Frame):
    """This widget behaves like a tkFrame widget with scrollbars.

The scrollbars can be on any 2 edges of the widget, and can automatically
disappear when not needed. Configuration options are passed to the
<class> widget, along with most method calls; however, geometry methods
are redirected to the <container> widget.

Attributes
----------
container : tkFrame
    The outermost widget. Contains the <scroll_canvas>, <scrollbar_v>, and
    <scrollbar_h> widgets

scroll_canvas : tkCanvas
    The Canvas widget that allows scrolling. Contains the <class> widget

scrollbar_v : tkScrollbar
    The vertical Scrollbar widget

scrollbar_h : tkScrollbar
    The horizontal Scrollbar widget

<class> : tkFrame
    The Frame widget that will hold all child widgets

dohide : bool
    Whether to hide the scrollbars when not needed

doupdate : bool
    Whether to automatically redraw the widget whenever it's resized

scrollspeed : int
    The number of lines to scroll by. 0 disables mousewheel scrolling

Methods
-------
redraw() -> None
    Updates the widget's scroll-area and (un)hide the scrollbars

Any <tkFrame> methods
"""
    __padding: tuple[int, int, int, int]
    __BG: str
    __CURSOR: str
    dohide: bool
    doupdate: bool
    scrollspeed: int
    scrollbar_h: O[Scrollbar]
    scrollbar_v: O[Scrollbar]
    __showVScroll: bool
    __showHScroll: bool
    __allChildren: set[Widget]
    __sfc: str
    __sbX: str
    __sbY: str
    __mainWinId: int

    def __init__(self, master: O[Widget] = None, scrollbars: str = 'SE', dohide: bool = True,
                 padding: U[int, tuple[int], list[int]] = (3, 0, 0, 3), doupdate: bool = True,
                 scrollspeed: int = 2, **kwargs):
        """\
        Parameters
        ----------
        master : tkWidget, optional (default is tkTk)
            The parent widget

        scrollbars : str, optional (default is "SE")
            Where to put the scrollbars

        padding : int | sequence[int] where len=(2 or 4), optional (default is (3, 0, 0, 3))
            Padding around the scroll_canvas widget

        dohide : bool, optional (default is True)
            Whether to hide the scrollbars when not needed

        doupdate : bool, optional (default is True)
            Whether to automatically redraw the widget whenever it's resized

        scrollspeed : int, optional (default is 2)
            The number of lines to scroll by. 0 disables mousewheel scrolling

        **kwargs : keyword arguments, optional
            Any additional tkFrame parameters
        """
        self.__validateVars(padding, scrollbars)
        # set var defaults if not specified
        kwargs.update(bd=kwargs.pop('borderwidth', kwargs.pop('bd', 2)),
                      relief=kwargs.pop('relief', 'ridge'),
                      width=kwargs.pop('width', 300),
                      height=kwargs.pop('height', 200))
        # set initial values
        self.__BG = (kwargs.get('background') or
                     kwargs.get('bg', 'SystemButtonFace'))
        self.__CURSOR = kwargs.get('cursor', '')
        self.dohide = dohide
        self.doupdate = doupdate
        self.scrollspeed = scrollspeed
        self.scrollbar_h = None
        self.scrollbar_v = None
        self.__showVScroll = False
        self.__showHScroll = False
        self.__allChildren = set()
        # create widget
        self.__createContainer(master, kwargs)
        self.__sfc = f'{self.container.winfo_id()}_children'
        self.__createScrollFrame()
        self.redraw()
        if doupdate:
            self.container.bind(sequence='<Configure>',
                                func=self.redraw)
        # Pass geometry methods to container
        def meths(cls): return vars(cls).keys()
        all_frame_methods = meths(Frame)
        all_geo_methods = meths(Pack) | meths(Grid) | meths(Place)
        geo_methods = all_geo_methods.difference(all_frame_methods)
        for method in geo_methods:
            if not re_search(r'^_|config|slaves|propagate|location', method):
                setattr(self, method, getattr(self.container, method))

    def __validateVars(self, pad: U[int, list, tuple], sbars: str) -> None:
        # validate padding
        errmsg_pad = ("the <padding> parameter must be either an integer "
                      "(pad_ALL) or a sequence of 2 (pad_NS, pad_EW) or 4 "
                      "(pad_N, pad_E, pad_S, pad_W) integers")
        if not isinstance(pad, (int, list, tuple)):
            raise TypeError(errmsg_pad)
        elif isinstance(pad, int):
            self.__padding = tuple([pad] * 4)
        else:
            if len(pad) not in [2, 4] or False in [isinstance(n, int) for n in pad]:
                raise ValueError(errmsg_pad)
            else:
                self.__padding = tuple(pad if len(pad) == 4 else (pad * 2))
        # validate scrollbars
        errmsg_sbar = ('the <scrollbars> parameter must be a combination of '
                       'up to 2 non-opposing strings from the following: '
                       '("N"="T"=North | "S"="B"=South), ("E"="R"=East | "W"="L"=West)')
        if not isinstance(sbars, str):
            raise TypeError(errmsg_sbar)
        sbs = sbars.upper()
        repl = sbs.maketrans('TBRL', 'NSEW')
        s = sbs.translate(repl)
        if re_search(r'^[NS](?:$|[EW]$)|^[EW](?:$|[NS]$)', s):
            self.__sbX = ''.join(set('NS') & set(s))
            self.__sbY = ''.join(set('EW') & set(s))
        else:
            raise ValueError(errmsg_sbar)

    def __createContainer(self, master: Widget, kwargs: dict) -> None:
        # create the container that holds everything
        self.container = Frame(master=master,
                               **kwargs)
        self.container.grid_propagate(0)
        self.container.rowconfigure(1 if self.__sbX == 'N' else 0,
                                    weight=1)
        self.container.columnconfigure(1 if self.__sbY == 'W' else 0,
                                       weight=1)

    def __createScrollFrame(self) -> None:
        pad_n, pad_e, pad_s, pad_w = self.__padding
        # create the canvas that holds the scrolled window
        self.scroll_canvas = Canvas(master=self.container,
                                    highlightthickness=0,
                                    bg=self.__BG,
                                    cursor=self.__CURSOR)
        self.scroll_canvas.grid(column=(1 if self.__sbY == 'W' else 0),
                                row=(1 if self.__sbX == 'N' else 0),
                                sticky='nsew',
                                padx=(pad_w, pad_e),
                                pady=(pad_n, pad_s))
        # create the scrolled window
        Frame.__init__(self,
                       master=self.scroll_canvas,
                       background=self.__BG,
                       cursor=self.__CURSOR)
        # create scrollbars
        if self.__sbY:
            self.scrollbar_v = Scrollbar(master=self.container,
                                         orient='vertical',
                                         command=self.scroll_canvas.yview)
            self.scrollbar_v.grid(column=(0 if self.__sbY == 'W' else 1),
                                  row=(1 if self.__sbX == 'N' else 0),
                                  sticky='ns')
            self.scroll_canvas.configure(yscrollcommand=self.scrollbar_v.set)
            self.__showVScroll = True
        if self.__sbX:
            self.scrollbar_h = Scrollbar(master=self.container,
                                         orient='horizontal',
                                         command=self.scroll_canvas.xview)
            self.scrollbar_h.grid(column=(1 if self.__sbY == 'W' else 0),
                                  row=(0 if self.__sbX == 'N' else 1),
                                  sticky='ew')
            self.scroll_canvas.configure(xscrollcommand=self.scrollbar_h.set)
            self.__showHScroll = True
        # create the window
        self.__mainWinId = self.scroll_canvas.create_window(0, 0,
                                                            anchor='nw',
                                                            window=self)

    def __bindScroll(self, func: C) -> None:
        def scrollView(e: Event):
            val = (self.scrollspeed * (-1 if e.delta > 0 else 1))
            func(val, 'units')
        self.bind_class(className=self.__sfc,
                        sequence='<MouseWheel>',
                        func=scrollView)

    def __updateScrolling(self, sbars: str) -> None:
        if self.scrollbar_v and 'v' in sbars:
            # there is a vert scrollbar and it needs to be updated
            if self.__showVScroll:
                # the vScroll is needed
                self.scrollbar_v.grid()
                if self.scrollspeed:
                    # bind scroll to the vScroll
                    self.__bindScroll(self.scroll_canvas.yview_scroll)
            else:
                # the vScroll isn't needed
                self.scroll_canvas.yview_moveto(0)
                if self.dohide:
                    # hide the vScroll
                    self.scrollbar_v.grid_remove()
                if self.scrollspeed and self.__showHScroll and 'h' not in sbars:
                    # there is a horz scrollbar and it won't be updated otherwise
                    self.__bindScroll(self.scroll_canvas.xview_scroll)
        if self.scrollbar_h and 'h' in sbars:
            # there is a horz scrollbar and it needs to be updated
            if self.__showHScroll:
                # the hScroll is needed
                self.scrollbar_h.grid()
                if self.scrollspeed and not self.__showVScroll:
                    # there isn't a vert scrollbar, so bind the hScroll
                    self.__bindScroll(self.scroll_canvas.xview_scroll)
            else:
                # the hScroll isn't needed
                self.scroll_canvas.xview_moveto(0)
                if self.dohide:
                    self.scrollbar_h.grid_remove()
        if self.scrollspeed and not self.__showVScroll and not self.__showHScroll:
            # neither scrollbar is needed
            self.unbind_class(className=self.__sfc,
                              sequence='<MouseWheel>')

    def __retag(self) -> None:
        # recurse through all children of widget and add the custom class tag
        c = [self.container]
        for w in c:
            c.extend(w.winfo_children())
        curChildren = set(c)
        newWidgets = curChildren.difference(self.__allChildren)
        for w in newWidgets:
            w.bindtags((self.__sfc,) + w.bindtags())
        self.__allChildren = curChildren

    def redraw(self, _=None) -> None:
        self.__retag()
        self.update_idletasks()
        reqWd = self.winfo_reqwidth()
        scrCnvWd = self.scroll_canvas.winfo_width()
        reqHt = self.winfo_reqheight()
        scrCnvHt = self.scroll_canvas.winfo_height()
        rebind = str()
        # check if the window is wider than the container
        iswide = scrCnvWd < reqWd
        # update horz scroll if it exists and is in the wrong state
        if self.scrollbar_h and ((iswide and not self.__showHScroll) or (not iswide and self.__showHScroll)):
            self.__showHScroll = not self.__showHScroll
            rebind += 'h'
        # check if the window is taller than the container
        istall = scrCnvHt < reqHt
        # update vert scroll if it exists and is in the wrong state
        if self.scrollbar_v and ((istall and not self.__showVScroll) or (not istall and self.__showVScroll)):
            self.__showVScroll = not self.__showVScroll
            rebind += 'v'
        # update the scrollbars if necessary
        if rebind:
            self.__updateScrolling(rebind)
        # update the window with the new sizes
        self.scroll_canvas.configure(scrollregion=(0, 0, reqWd, reqHt))
        self.scroll_canvas.itemconfigure(tagOrId=self.__mainWinId,
                                         width=max(reqWd, scrCnvWd),
                                         height=max(reqHt, scrCnvHt))
        self.update_idletasks()

    def configure(self, **kwargs) -> None:
        # intercept configure commands
        kw = dict()
        bg = kwargs.get('background', kwargs.get('bg'))
        if bg:
            # get requested background
            kw['bg'] = self.__BG = bg
        cur = kwargs.get('cursor')
        if cur:
            # get requested cursor
            kw['cursor'] = self.__CURSOR = cur
        if kw:
            # update config for sub-widgets
            self.container.configure(**kw)
            self.scroll_canvas.configure(**kw)
        # update config for main widget
        Frame.configure(self, **kwargs)

    config = configure

    def destroy(self) -> None:
        Frame.destroy(self)
        self.container.destroy()


if __name__ == '__main__':
    from pathlib import Path
    from subprocess import run
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
