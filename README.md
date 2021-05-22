# [Scrolled Frame](https://github.com/Cryden13/Python/tree/main/scrolledframe)

This widget behaves like a tkFrame widget with scrollbars.

The scrollbars can be on any 2 edges of the widget, and can automatically
disappear when not needed. Configuration options are passed to the
`class` widget, along with most method calls; however, geometry methods
are redirected to the `container` widget.

## Usage

`ScrolledFrame`( [master, scrollbars, padding, dohide, doupdate, scrollspeed, **kwargs] )

## Parameters

1. ### `master` _(optional)_

    **tkWidget** _(default=tkTk)_  
    The parent widget

2. ### `scrollbars` _(optional)_

   **String** _(default="SE")_  
   Where to put the scrollbars

3. ### `padding` _(optional)_

   **Integer OR sequence of integers** _(default=(3,0,0,3))_  
   Padding around the scroll_canvas widge

4. ### `dohide` _(optional)_

   **Boolean** _(default=True)_  
   Whether to hide the scrollbars when not needed

5. ### `doupdate` _(optional)_

   **Boolean** _(default=True)_  
   Whether to automatically redraw the widget whenever it's resized

6. ### `scrollspeed` _(optional)_

   **Integer** _(default=2)_  
   The number of lines to scroll by. 0 disables mousewheel scrolling

7. ### `**kwargs` _(optional)_

    **Dictionary** _(default=None)_  
    Any additional tkFrame parameters

## Attributes

- ### `container` **: tkFrame**

    The outermost widget. Contains the `scroll_canvas`, `scrollbar_v`, and
    `scrollbar_h` widgets

- ### `scroll_canvas` **: tkCanvas**

    The Canvas widget that allows scrolling. Contains the `class` widget

- ### `scrollbar_v` **: tkScrollbar**

    The vertical Scrollbar widget

- ### `scrollbar_h` **: tkScrollbar**

    The horizontal Scrollbar widget

- ### `<class>` **: tkFrame**

    The Frame widget that will hold all child widgets

- ### `dohide` **: bool**

    Whether to hide the scrollbars when not needed

- ### `doupdate` **: bool**

    Whether to automatically redraw the widget whenever it's resized

- ### `scrollspeed` **: int**

    The number of lines to scroll by. 0 disables mousewheel scrolling

## Methods

- ### `redraw() -> None`

    Updates the widget's scroll-area and (un)hide the scrollbars

- ### Any `tkFrame` methods

## Changelog

<table>
    <tbody>
        <tr>
            <th align="center">Version</th>
            <th align="left">Changes</th>
        </tr>
        <tr>
            <td align="center">1.0</td>
            <td>Initial release</td>
        </tr>
        <tr>
            <td align="center">1.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>added option to move scrollbars</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed incorrect method redirect</li>
                        <li>fixed description</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">1.2</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>added ability to toggle hiding</li>
                        <li>added padding option</li>
                        <li>added validation</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed bg and cursor options</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.0</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>changed main class to inner frame</li>
                        <li>added auto updating and the option to toggle said auto updating</li>
                        <li>added access to data members</li>
                        <li>added mousewheel binding</li>
                        <li>added redraw function</li>
                        <li>consolidated redundant functions</li>
                        <li>removed unnecessary tk.frame</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed validation</li>
                        <li>fixed faulty tagging</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>added scrollspeed argument</li>
                        <li>cleaned up code</li>
                        <li>added a bunch of comments</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed lag when updating list</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.2</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>added typing hints</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed redraw error</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.3</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>added more notation</li>
                        <li>made errors more verbose</li>
                        <li>made more attributes available</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>stopped excessive redraws</li>
                        <li>fixed 'destroy' method</li>
                    </ul>
                </dl>
            </td>
        </tr>
    </tbody>
</table>
