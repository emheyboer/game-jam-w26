from screen import Screen

class MapScreen(Screen):
    def draw(self) -> None:
        """
        Renders the screen
        """
        for x in range(0, 18):
            for y in range(0, 11):
                sprite = self.sprites[f"map_{x:02d}_{y:02d}"]
                sprite.draw(self.screen, (x * 16, y * 16), (16, 16))
    
    def on_event(self, event):
        """
        Responds to an individual pygame event. On screen change, returns the new screen
        """
        return self