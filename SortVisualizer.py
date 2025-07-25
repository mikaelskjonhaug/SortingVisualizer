import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = 40, 40, 40

    GRADIENTS = [
		WHITE,
        WHITE,
        WHITE
	]

    FONT = pygame.font.SysFont('helvetica', 15) # This font seems p sweet ngl no cap
    LARGE_FONT = pygame.font.SysFont('helvetica', 15)

    SIDE_PAD = 100 
    TOP_PAD = 60

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)
        
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        #self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.block_height = ((self.height - self.TOP_PAD) / (self.max_value - self.min_value)) # possible bug, might need math.floor [1:03:19]
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, sorting_algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    controls = draw_info.FONT.render(f"{sorting_algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.WHITE)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 5))

    sorting = draw_info.FONT.render("[R] reset [SPACE] sort [A] asc. [D] desc. [B] bbl srt [S] select srt [I] insrt srt", 1, draw_info.WHITE)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 25))

    draw_list(draw_info)

    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.block_height

        color = draw_info.WHITE 

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

def generate_random_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    
    return lst

def generate_range_list(start_val, end_val):
    lst = list(range(start_val, end_val + 1))
    random.shuffle(lst)
    return lst


def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    
    return lst

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        smallest = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[smallest] and ascending:
                smallest = j
                draw_list(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, True)
            elif lst[j] > lst[smallest] and not ascending:
                smallest = j
                draw_list(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, True)
        lst[i], lst[smallest] = lst[smallest], lst[i]
        yield True

    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        j = i
        while lst[j-1] > lst[j] and j > 0:
            lst[j], lst[j-1] = lst[j-1], lst[j]
            j -= 1
        draw_list(draw_info, {j: draw_info.RED, j-1: draw_info.GREEN}, True)
        yield True
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 30
    min_val = 1
    max_val = 100
    #lst = generate_random_list(n, min_val, max_val) # generates a list of n random values ranging from min_val to max_val

    lst = generate_range_list(1, 100)

    draw_info = DrawInformation(800, 600, lst)

    sorting = False

    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None


    while run:
        clock.tick(100) #n = events per second

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False    
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        for event in pygame.event.get(): #enables 'X'ing out'
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r: # New list
                lst = generate_random_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_b:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_i:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_s:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

            elif event.key == pygame.K_SPACE and sorting == False: # Start Sort
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting: # Ascending 
                ascending = True

            elif event.key == pygame.K_d and not sorting: # Descending
                ascending = False

    pygame.quit()

if __name__ == "__main__": # runs main
    main()
