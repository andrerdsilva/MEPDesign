# -*- coding: utf-8 -*-
""" Open about information in default browser.  """

__context__ = 'zero-doc'

__title__ = 'About'
__author__ = 'André Rodrigues da Silva'

import webbrowser


url = 'https://github.com/andrerdsilva'

# Open URL in a new tab, if a browser window is already open.
webbrowser.open_new_tab(url)

# Open URL in new window, raising the window if possible.
#webbrowser.open_new(url)