class Colors:
    dark_grey = [26,31,40]
    green = (57,230,23)
    red = [232,18,18]
    orange = [226,116,17]
    yellow = [237,234,4]
    purple = [166,0,247]
    cyan = [21,204,209]
    blue = [13,64,216]
    light_blue = [173, 216, 230]  # Light blue color for the score rectangle

    @classmethod 
    def get_cell_colors(cls):
        return [
            cls.dark_grey, 
            cls.green, 
            cls.red, 
            cls.orange, 
            cls.yellow, 
            cls.purple, 
            cls.cyan, 
            cls.blue,
            cls.light_blue
        ]