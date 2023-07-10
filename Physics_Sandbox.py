import random
import sys
import pygame
import pymunk
import pymunk.pygame_util
from pygame.color import THECOLORS
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

size = (800, 400)


class CreateBody(object):

    def __init__(self, pos, type, xVel, yVel):
        self.body = pymunk.Body(1, 100, body_type=type)
        self.body.position = pos
        self.body.velocity = (xVel, yVel)

    def update(self):
        # Update the position of the pymunk body based on its velocity
        self.body.position += self.body.velocity
        # Check if the box is out of bounds and reverse the velocity if it is
        if self.body.position.x <= 0 or self.body.position.x >= size[0]:
            self.body.velocity = (-self.body.velocity.x, self.body.velocity.y)
        if self.body.position.y <= 0 or self.body.position.y >= size[1]:
            self.body.velocity = (self.body.velocity.x, -self.body.velocity.y)


class CreateCircle(CreateBody):

    def __init__(self, pos, type, xVel, yVel, rad):
        super().__init__(pos, type, xVel, yVel)
        self.shape = pymunk.Circle(self.body, rad)
        self.shape.color = THECOLORS["red"]


class CreateBox(CreateBody):

    def __init__(self, pos, type, xVel, yVel, rad):
        super().__init__(pos, type, xVel, yVel)
        self.shape = pymunk.Poly.create_box(self.body, (rad, rad))
        self.shape.color = THECOLORS["orange"]


class CreateTriangle(CreateBody):

    def __init__(self, pos, type, xVel, yVel, rad):
        super().__init__(pos, type, xVel, yVel)
        self.shape = pymunk.Poly(self.body, [(rad * 1.5, rad), (rad, rad * 4), (rad * 2, rad * 2)])
        self.shape.color = THECOLORS["blue"]


class Game():

    def __init__(self, rad, typeshape, difficulty_level):
        self.rad = rad
        self.typeshape = typeshape
        self.difficulty_level = difficulty_level
        self.is_collision_detected = False

    def generate_random_objects(self, space):
        ran = random.randint(1, 3)
        # 'Beginner','Intermediate','Advanced'
        ran_x = random.randint(50, 750)
        ran_y = random.randint(20, 350)

        if self.difficulty_level == 'Beginner':
            vel_x = random.randint(3000, 5000)
            vel_y = random.randint(-800, -600)
            rad = random.randint(20, 25)
        elif self.difficulty_level == 'Intermediate':
            vel_x = random.randint(1000, 9000)
            vel_y = random.randint(-1000, -500)
            rad = random.randint(30, 45)
        elif self.difficulty_level == 'Advanced':
            vel_x = random.randint(-9000, -5000)
            vel_y = random.randint(-600, -500)
            rad = random.randint(40, 60)

        if ran == 1:
            temp = CreateCircle((ran_x, ran_y), pymunk.Body.DYNAMIC, vel_x, vel_y, rad)
        elif ran == 2:
            temp = CreateBox((ran_x, ran_y), pymunk.Body.DYNAMIC, vel_x, vel_y, rad)
        elif ran == 3:
            temp = CreateTriangle((ran_x, ran_y), pymunk.Body.DYNAMIC, vel_x, vel_y, rad)

        temp.shape.elasticity = 0.5
        temp.shape.friction = 0.1
        temp.shape.mass = 1
        temp.shape.collision_type = 1
        space.add(temp.body, temp.shape)
        return ran

    def run(self):

        pygame.init()  # initiate pygame
        screen = pygame.display.set_mode(size)  # creating the display surface object
        pygame.display.set_caption("Physics sandbox")
        clock = pygame.time.Clock()
        shapes = []  # creating list in which we will store the position of the shapes instantiated
        space = pymunk.Space()
        space.gravity = (-5000, 8000)
        score = 0

        def collision(arbiter, space, data):  # Handle the collision here
            # print("Collision detected")
            self.is_collision_detected = True
            return False

        left_wall = pymunk.Segment(space.static_body, (0, 0), (0, size[1]), 5)
        right_wall = pymunk.Segment(space.static_body, (size[0], 0), (size[0], size[1]), 5)
        top_wall = pymunk.Segment(space.static_body, (0, 0), (size[0], 0), 5)
        bottom_wall = pymunk.Segment(space.static_body, (0, size[1]), (size[0], size[1]), 5)

        handler = space.add_collision_handler(2, 1)
        handler.begin = collision

        if self.difficulty_level == 'Advanced':
            left_wall.elasticity = 2.5
            right_wall.elasticity = 2.5
            top_wall.elasticity = 2.5
            bottom_wall.elasticity = 2.5
        else:
            left_wall.elasticity = 2
            right_wall.elasticity = 2.1
            top_wall.elasticity = 1.9
            bottom_wall.elasticity = 2.4

        space.add(left_wall, right_wall, top_wall, bottom_wall)
        ticks_to_next_ball = 100
        font = pygame.font.Font(None, 20)

        # Game loop
        while True:  # while True:
            screen.fill((255, 255, 255))  # background color
            ticks_to_next_ball -= 1

            # Check if 10 seconds have elapsed
            if ticks_to_next_ball == 0:
                number_generated = self.generate_random_objects(space)
                if number_generated == 1:  # Circle
                    score += 3
                if number_generated == 2:  # Box
                    score += 5
                if number_generated == 3:  # Triangle
                    score += 7
                ticks_to_next_ball = 100

            screen.blit(font.render(str(score), True, (0, 0, 0)), (15, 15))

            # Example of list comprehension.
            event_list = pygame.event.get()
            event_list = [(pygame.display.quit, pygame.quit(), sys.exit(0)) for event in event_list if
                          event.type == pygame.QUIT]
            # We could do it just like next
            # for event in pygame.event.get():
            # if event.type == pygame.QUIT:  # input to close the game
            #   pygame.quit()
            #   sys.exit(0)

            if self.typeshape == 'Circle':
                player = CreateCircle(pygame.mouse.get_pos(), pymunk.Body.DYNAMIC, 1, 1, self.rad)
            if self.typeshape == 'Square':
                player = CreateBox(pygame.mouse.get_pos(), pymunk.Body.DYNAMIC, 1, 1, self.rad)
            if self.typeshape == 'Triangle':
                player = CreateTriangle(pygame.mouse.get_pos(), pymunk.Body.DYNAMIC, 1, 1, self.rad)

            player.shape.color = THECOLORS['green']
            player.shape.collision_type = 2
            player.shape.elasticity = 2.5
            space.add(player.body, player.shape)

            if self.is_collision_detected:
                Window().draw_window_over(score)
                break

            space.step(1 / 1000.0)  # it is the loop to update the simulation
            space.debug_draw(pymunk.pygame_util.DrawOptions(screen))
            space.remove(player.body, player.shape)
            pygame.display.flip()
            shapes = [obj.update() for obj in shapes]  # List comprehension.
            clock.tick(60)


class Window():

    def __init__(self):
        self.window = Tk()  # Creating the window with tkinter
        self.window.title("Physics")
        self.window.geometry('480x350')
        self.window.resizable(False, False)
        self.window.config(background="#213141")
        self.frame = Frame(self.window, width=80, highlightbackground='black', highlightthicknes=3)
        self.frame.grid(row=1, column=1, padx=60, pady=40, ipadx=70, ipady=80)

    def draw(self):
        # Welcome Text
        text = Label(self.frame, text="Welcome to our Physical Sandbox")
        text.place(x=10, y=50)
        text.pack()

        image = Image.open("background.jpg")
        photo = ImageTk.PhotoImage(image.resize((210, 210), Image.Resampling.LANCZOS))

        label = Label(self.frame, image=photo, bg='green')
        label.image = photo
        label.pack()

        radtext = Label(self.frame, text="Select the measure:")
        radtext.place(x=30, y=60)
        rad = IntVar()

        # We tried to get the data in a textbox, but it was better to do it in a scale
        # value to control de type inputs directly.
        rad_value = Scale(self.frame, from_=20, to=60, variable=rad, orient=HORIZONTAL)
        rad_value.set(30)
        rad_value.pack()
        rad_value.place(x=200, y=60)

        # The user will choose the shape from a combobox.
        shapetext = Label(self.frame, text="Select the shape:")
        shapetext.pack()
        shapetext.place(x=30, y=120)
        n = tk.StringVar()

        # Adding combobox drop down list
        shapechoosen = ttk.Combobox(self.frame, width=10, textvariable=n)
        shapechoosen['values'] = ('Circle', 'Triangle', 'Square')
        shapechoosen.place(x=200, y=120)
        shapechoosen.current(0)

        # The user will choose a level from a combobox.
        level = Label(self.frame, text='Choose level :')
        level.pack()
        level.place(x=30, y=180)
        n1 = tk.StringVar()
        
        # Adding combobox drop down list
        levelChoosen = ttk.Combobox(self.frame, width=10, textvariable=n1)
        levelChoosen['values'] = ('Beginner', 'Intermediate', 'Advanced')
        levelChoosen.place(x=200, y=180)
        levelChoosen.current(0)

        # Send shape, radio size and level to Game
        SendShape = Button(self.frame, text='Play', activebackground='green',
                           command=lambda: Window.play(self, rad_value.get(), shapechoosen.get(), levelChoosen.get()))
        SendShape.pack()
        SendShape.place(x=160, y=240)

        # Rules button
        rule = Button(self.frame, text='Rule', activebackground='green', command=lambda: Window.rule(self))
        rule.pack()
        rule.place(x=70, y=240)
        
        # Close button
        quit = Button(self.frame, text='Close', activebackground='green', command=lambda: self.window.destroy())
        quit.pack()
        quit.place(x=250, y=240)

        self.window.mainloop()

    def rule(self):
        rule_window = tk.Toplevel()  # We create the window that will show the rules
        rule_window.title("Rule Window")
        rule_window.config(width=600, height=350)
        rule_image = Image.open("rule_image.png")
        rule_photo = ImageTk.PhotoImage(rule_image.resize((490, 210), Image.Resampling.LANCZOS))
        label = Label(rule_window, image=rule_photo, bg='green')
        label.image = rule_photo
        label.pack()
        label.place(x=50, y=40)
        button_close = Button(rule_window, text="Close", command=rule_window.destroy)
        button_close.place(x=260, y=280)

    def play(self, rad, typeshape, level):  # Function to call the game
        self.window.destroy()
        Game(rad, typeshape, level).run()

    def draw_window_over(self, score):  # We create the window that will game over and the score
        game_over = Label(self.frame, text="GAME OVER")
        game_over.place(x=50, y=10)
        game_over = Label(self.frame, text="Your final score is :   " + str(score))
        game_over.place(x=10, y=50)
        play_again = Button(self.frame, text='Play Again', command=lambda: (self.window.destroy(), Window().draw()))
        play_again.pack()
        play_again.place(x=30, y=110)
        close = Button(self.frame, text='Close', command=lambda: self.window.destroy())
        close.pack()
        close.place(x=130, y=110)
        self.window.mainloop()


def main():  # initiate Tkinter window
    Window().draw()


if __name__ == '__main__':
    main()
    print("---------THE GAME HAS ENDED---------")
    print("---------THANKS FOR PLAYING---------")


