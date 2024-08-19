import tkinter as tk
import random


class TankGame:
    def __init__(self, master):
        self.master = master
        master.title("Tank Game")

        # Определяем размеры экрана
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Создаем четыре фрейма для каждой из четырех областей
        self.top_left_frame = tk.Canvas(master, bg="white", width=screen_width // 2, height=screen_height // 2.5,
                                        highlightbackground="black")
        self.top_right_frame = tk.Canvas(master, bg="white", width=screen_width // 2, height=screen_height // 2.5,
                                         highlightbackground="black")
        self.bottom_left_frame = tk.Canvas(master, bg="white", width=screen_width // 2, height=screen_height // 2.5,
                                           highlightbackground="black")
        self.bottom_right_frame = tk.Canvas(master, bg="white", width=screen_width // 2, height=screen_height // 2.5,
                                            highlightbackground="black")

        # Размещаем фреймы на окне
        self.top_left_frame.grid(row=0, column=0)
        self.top_right_frame.grid(row=0, column=1)
        self.bottom_left_frame.grid(row=1, column=0)
        self.bottom_right_frame.grid(row=1, column=1)

        self.draw_areas()  # Создаем области для рисования
        self.create_buttons()  # Создаем кнопки
        self.current_frame = self.bottom_right_frame  # начальная область стрельбы первого игрока
        self.current_player_index = 0  # Индекс текущего игрока

        # Словарь для хранения областей для каждого игрока
        self.frames = {
            0: self.bottom_right_frame,
            1: self.top_right_frame
        }
        # Словарь для хранения привязок обработчиков событий
        self.bindings = {
            0: None,
            1: None
        }

    def draw_areas(self):
        # Создаем прямоугольник для каждой из областей для рисования
        self.top_left_frame.create_rectangle(0, 0, self.top_left_frame.winfo_width(),
                                             self.top_left_frame.winfo_height(), outline="black")
        self.top_right_frame.create_rectangle(0, 0, self.top_right_frame.winfo_width(),
                                              self.top_right_frame.winfo_height(), outline="black")
        self.bottom_left_frame.create_rectangle(0, 0, self.bottom_left_frame.winfo_width(),
                                                self.bottom_left_frame.winfo_height(), outline="black")
        self.bottom_right_frame.create_rectangle(0, 0, self.bottom_right_frame.winfo_width(),
                                                 self.bottom_right_frame.winfo_height(), outline="black")

    def create_buttons(self):
        # Создаем кнопки и размещаем их внизу окна
        start = tk.Button(self.master, text="Старт", command=self.start_game)
        arrange_tanks = tk.Button(self.master, text="Расставить танки", command=self.draw_tanks)
        change_player = tk.Button(self.master, text="Сменить игрока", command=self.change_player)
        ready_to_shoot = tk.Button(self.master, text="Готово", command=self.shoot)

        start.grid(row=2, column=0)
        arrange_tanks.grid(row=2, column=1)
        change_player.grid(row=3, column=0)
        ready_to_shoot.grid(row=3, column=1)

    def start_game(self):
        # Удаляем предыдущие квадраты
        self.top_left_frame.delete("all")
        self.top_right_frame.delete("all")
        self.bottom_left_frame.delete("all")
        self.bottom_right_frame.delete("all")

        # Функция, вызываемая при нажатии кнопки "Старт"
        start_window = tk.Toplevel(self.master)
        start_window.title("Подсказка")

        # Вычисляем координаты для центрирования окна
        x = (start_window.winfo_screenwidth() - start_window.winfo_reqwidth()) // 2
        y = (start_window.winfo_screenheight() - start_window.winfo_reqheight()) // 2
        start_window.geometry("+{}+{}".format(x, y))

        label = tk.Label(start_window, text="Вы начали новую игру.\nРасставьте танки", font=("Arial", 18))
        label.pack(padx=20, pady=20)

    def draw_tanks(self):
        # Определяем область, в которую будем рисовать танки
        if self.current_player_index == 0:
            canvas = self.top_left_frame
        else:
            canvas = self.bottom_left_frame

        # Удаляем предыдущие квадраты
        canvas.delete("all")

        # Функция для рисования танков
        for _ in range(5):
            x = random.randint(0, canvas.winfo_width() - 5)  # Случайные координаты x
            y = random.randint(0, canvas.winfo_height() - 5)  # Случайные координаты y
            canvas.create_rectangle(x, y, x + 10, y + 10, fill="green", outline="black")

    def change_player(self):
        # Изменяем индекс текущего игрока
        self.current_player_index = (self.current_player_index + 1) % 2

        # Удаляем все привязки обработчиков событий
        self.current_frame.unbind("<Button-1>")

        # Скрываем предыдущую рабочую область
        self.current_frame.grid_remove()

        # Обновляем текущую рабочую область
        self.current_frame = self.frames[self.current_player_index]

        # Перепривязываем обработчик клика мыши к новой рабочей области
        self.bindings[self.current_player_index] = self.current_frame.bind("<Button-1>", self.on_click)

        # Отображаем новую рабочую область
        self.current_frame.grid()

    def shoot(self):
        # Проверяем, что выстрел возможен
        if self.shoot_point:
            x, y = self.shoot_point
            # Определяем, в какую рабочую область стрелять в зависимости от текущего игрока
            if self.current_player_index == 0:
                target_canvas = self.bottom_left_frame
            else:
                target_canvas = self.top_left_frame
            # Рисуем выстрел в выбранной области
            target_canvas.create_rectangle(0, y, x, y + 2, fill="red", outline="black")

    def create_point(self, x, y):
        # Определяем, в какой области рисовать точку, в зависимости от текущего игрока
        canvas = self.frames[self.current_player_index]
        canvas.create_rectangle(x, y, x + 2, y + 2, fill="red", outline="black")
        canvas.update()  # Обновляем графический интерфейс

    def create_point_in_left_frame(self, x, y):
        self.top_left_frame.create_rectangle(x, y, x + 2, y + 2, fill="red", outline="black")
        self.top_left_frame.update()  # Обновляем графический интерфейс

    def on_click(self, event):
        # Получаем текущую рабочую область
        current_frame = self.frames[self.current_player_index]

        # Получаем координаты относительно текущей рабочей области
        x = current_frame.canvasx(event.x)
        y = current_frame.canvasy(event.y)

        # Создаем точку только если событие произошло на холсте текущего игрока
        if current_frame == self.current_frame:
            if self.current_player_index == 0:
                self.shoot_point = (x, y)
                self.create_point(x, y)
            elif self.current_player_index == 1:
                self.shoot_point = (x, y)
                self.create_point(x, y)


def main():
    root = tk.Tk()

    # Устанавливаем размеры окна по размерам экрана и позиционируем его в левом верхнем углу
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    app = TankGame(root)

    # Привязываем обработчик кликов мыши к текущей рабочей области в соответствии с текущим игроком
    current_frame = app.frames[app.current_player_index]
    current_frame.bind("<Button-1>", app.on_click)

    root.mainloop()


if __name__ == "__main__":
    main()
