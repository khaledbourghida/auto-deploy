class Navigator:
    def __init__(self, page):
        self.page = page
        self.shell = None
        self.stack = []

    def set_root(self, shell):
        self.shell = shell
        self.page.controls.clear()
        self.page.add(shell)

    def push(self, page_view):
        self.stack.append(page_view)
        self._render()
        
    def push_home(self):
        from ui.pages.home_page import HomePage
        self.shell.show_sidebar()
        self.push(HomePage(self))
        
    def push_fullscreen(self, page_view):
        self.stack.append(page_view)
        self.shell.hide_sidebar()
        self._render()
        
    def pop_fullscreen(self):
        self.shell.show_sidebar()
        if len(self.stack) > 1:
            self.stack.pop()
        self._render()

    def pop(self):
        if len(self.stack) > 1:
            self.stack.pop()

        # if len(self.stack) >= 1:
        #     self.shell.show_sidebar()

        self._render()

    def replace(self, page_view):
        if self.stack:
            self.stack.pop()
        self.stack.append(page_view)
        self._render()

    def _render(self):
        current = self.stack[-1]
        self.shell.set_content(current)
        self.page.update()
