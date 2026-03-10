import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import threading

class CropApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Wycinarka')
        self.root.geometry('1000x500')

        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.mouse_clicked)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)
        self.canvas.bind("<B1-Motion>", self.making_rectangle)

        self.image=None
        self.current_image=None

        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.button_open_cam = tk.Button(button_frame, text='Open Camera',command=self.get_image)
        self.button_open_cam.pack()
        self.button_king = tk.Button(button_frame, text='Krol',command=lambda:self.define_type("krol"))
        self.button_king.pack(side='left')
        self.button_queen = tk.Button(button_frame, text='Krolowa', command=lambda:self.define_type("krolowa"))
        self.button_queen.pack(side='left')
        self.button_rook = tk.Button(button_frame, text='Wieza', command=lambda:self.define_type("wieza"))
        self.button_rook.pack(side='left')
        self.button_bishop = tk.Button(button_frame, text='Goniec', command=lambda:self.define_type("goniec"))
        self.button_bishop.pack(side='left')
        self.button_knight = tk.Button(button_frame, text='Skoczek', command=lambda:self.define_type("skoczek"))
        self.button_knight.pack(side='left')
        self.button_pawn = tk.Button(button_frame, text='Pionek', command=lambda:self.define_type("pionek"))
        self.button_pawn.pack(side='left')


        self.camera = cv2.VideoCapture(0)


        self.rectangle_id=None
        self.croped_image=None
        self.root.mainloop()


    def get_image(self):
        def thread_function(): #making thread to ensure that camera
            # and crop app will be working at the same time
            while True:
                result, frame = self.camera.read()
                if result is False:
                    print('frame is not captured')
                cv2.imshow('Space: take photo, ESC - Escape', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                   cv2.destroyWindow('Space: take photo, ESC - Escape')
                   return
                if key == 32:  # Space
                    self.current_image = frame.copy()
                    self.root.after(0, self.display_image_from_camera)
        threading.Thread(target=thread_function, daemon=True).start()  #
    def display_image_from_camera(self):
        pil_img= Image.fromarray(cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB))
        self.image = ImageTk.PhotoImage(pil_img)
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
    def mouse_clicked(self, event):
        self.rectangle_start_x=event.x
        self.rectangle_start_y=event.y
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)
        self.rectangle_id = self.canvas.create_rectangle(
            self.rectangle_start_x,self.rectangle_start_y,
            self.rectangle_start_x,self.rectangle_start_y,
            outline='green',width=3)

    def mouse_release(self, event):
        x_up,y_up,x_down,y_down=self.canvas.coords(self.rectangle_id)
        height, width = self.current_image.shape[:2]
        scaled_x = width / self.canvas.winfo_width()
        scaled_y = height /self.canvas.winfo_height()
        self.croped_image= self.current_image[int(y_up):int(y_down),int(x_up):int(x_down)]
    def making_rectangle(self, event):
        self.canvas.coords(self.rectangle_id,
                           self.rectangle_start_x,self.rectangle_start_y,
                           event.x,event.y)

    def define_type(self,name):
        if self.croped_image is None:
            print('No image')
            return
        os.makedirs(f"pionki/{name}", exist_ok=True)
        counter = len([i for i in os.listdir(f"pionki/{name}") if i.endswith('.png')])
        filename = f'pionki/{name}/{name}{counter + 1}.png'
        cv2.imwrite(filename, self.croped_image)
        print(f"zapisano plik {filename}")
app = CropApp()
