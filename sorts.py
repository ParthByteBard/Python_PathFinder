import random
import time
import ctypes
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import pygame.mixer
pygame.mixer.init()
# load the sounds into sound variables
sound1 = pygame.mixer.Sound("sort-sound.mp3")
sound2 = pygame.mixer.Sound("sound2.wav")
search = pygame.mixer.Sound("search_sound.wav")
bonus = pygame.mixer.Sound("bonus_alert.wav")
default_volume = 0.8
sound1.set_volume(default_volume)




def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

    
# Helper function to swap elements i and j of list A. 
def swap(A, i, j):
    if i != j:
        A[i], A[j] = A[j], A[i]

# In-place bubble sort.
def bubblesort(A):
    if len(A) == 1:
        return
    swapped = True
    
    for i in range(len(A) - 1):
        if not swapped:
            break
        sound1.play()
        swapped = False
        for j in range(len(A) - 1 - i):
            if A[j] > A[j + 1]:
                swap(A, j, j + 1)
                swapped = True
            yield A
    sound1.stop()
    bonus.play()

# Insertion sort
def insertionsort(A):
    for i in range(1, len(A)):
        sound1.play()
        j = i
        while j > 0 and A[j] < A[j - 1]:
            swap(A, j, j - 1)
            j -= 1
            yield A
    sound1.stop()
    bonus.play()

# Merge Sort
def mergesort(A, start, end):
    if end <= start:
        return
    # the (end - start + 1) calculates the lenght of the array and // means performing intger division
    mid = start + ((end - start + 1) // 2) - 1 
    
    yield from mergesort(A, start, mid)
    yield from mergesort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A
    sound1.stop()

# Merge function which is the backbone of merge sort
def merge(A, start, mid, end):
    merged = []
    leftIdx = start
    rightIdx = mid + 1
    sound1.play()
    while leftIdx <= mid and rightIdx <= end:
        if A[leftIdx] < A[rightIdx]:
            merged.append(A[leftIdx])
            leftIdx += 1
        else:
            merged.append(A[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(A[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(A[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        A[start + i] = sorted_val
        yield A

# quick sort algorithm which includes the part for finding the pivot
def quicksort(A, start, end):
    if start >= end:
        return
    
    pivot = A[end]
    pivotIdx = start
    sound1.play()

    for i in range(start, end):
        
        
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A

    swap(A, end, pivotIdx)
    yield A

    yield from quicksort(A, start, pivotIdx - 1)
    yield from quicksort(A, pivotIdx + 1, end)
    sound1.stop()


# Selection sort algorithm
def selectionsort(A):
    if len(A) == 1:
        return

    for i in range(len(A)):
        # Find minimum unsorted value.
        minVal = A[i]
        minIdx = i
        sound1.play()
        for j in range(i, len(A)):
            if A[j] < minVal:
                minVal = A[j]
                minIdx = j
            yield A
        swap(A, i, minIdx)
        yield A
    sound1.stop()
    bonus.play()

def start_sorting():
    
    selected_method = method_var.get()
    # Check if a valid method is selected
    if selected_method == "None":  
        # If None method is selected display the error message
        messagebox.showerror("Error", "Please enter a valid sorting algorithm.")
        return
    try:
        N = int(num_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for the number of integers.")
        return
    method = method_var.get()

    # Build and randomly shuffle list of integers.

    # range will generate numbers [0,N-1] , adding x+1 means A will contain [1,N]
    A = [x + 1 for x in range(N)]
    # time value in seconds since Jan 1 1970 is treated as seed for random
    # time.time() acts as a seed
    random.seed(time.time())
    # list of integers are shuffled for randomness
    random.shuffle(A)

    # Get appropriate generator for the selected sorting method.
    if method == "Bubble Sort":
        generator = bubblesort(A)
    elif method == "Insertion Sort":
        generator = insertionsort(A)
    elif method == "Merge Sort":
        generator = mergesort(A, 0, N - 1)
    elif method == "Quick Sort":
        generator = quicksort(A, 0, N - 1)
    else:
        generator = selectionsort(A)

    # Start time recording
    start_time = time.time()

    # Initialize figure and axis for animation.
    fig, ax = plt.subplots()
    ax.set_title(method)

    # Initialize a bar plot.
    bar_rects = ax.bar(range(len(A)), A, align="edge")

    ax.set_xlim(0, N)
    ax.set_ylim(0, int(1.07 * N))

    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    iteration = [0]
    sorting_completed = [False]

    def check_sorted(A):
        for i in range(len(A) - 1):
            if A[i] > A[i + 1]:
                return False
        return True

    def update_fig(A, rects, iteration, sorting_completed):
        for rect, val in zip(rects, A):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text("# of operations: {}".format(iteration[0]))

        if check_sorted(A) and not sorting_completed[0]:
            bonus.play()
            sorting_completed[0] = True
            end_time = time.time()
            elapsed_time = end_time - start_time
            time_label.config(text=f"Time taken: {elapsed_time:.6f} seconds")
            for rect in rects:
                rect.set_color('green')
            bonus.play()



    anim = animation.FuncAnimation(fig, func=update_fig,
                                   fargs=(bar_rects, iteration, sorting_completed), frames=generator, interval=50,
                                   repeat=False)
    plt.show()

# Create the main window
root = tk.Tk()
root.title("Sorting Algorithm Visualizer")


# Set the size of the root window and center it
window_width = 400
window_height = 200
center_window(root, window_width, window_height)
# Frame for inputs

input_frame = tk.Frame(root, padx=20, pady=20)
input_frame.pack()

# Number of integers label and entry
num_label = tk.Label(input_frame, text="Number of Integers:")
num_label.grid(row=0, column=0, padx=5, pady=5)
num_entry = tk.Entry(input_frame)
num_entry.grid(row=0, column=1, padx=5, pady=5)

# Sorting method label and dropdown
method_label = tk.Label(input_frame, text="Sorting Method:")
method_label.grid(row=1, column=0, padx=5, pady=5)
method_var = tk.StringVar()
method_var.set("None")
method_dropdown = tk.OptionMenu(input_frame, method_var, "Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Selection Sort")
method_dropdown.grid(row=1, column=1, padx=5, pady=5)
method_dropdown = ttk.Combobox(root, textvariable=method_var, values=tk.OptionMenu, state="readonly")
method_dropdown.bind("<Button-1>", lambda e: method_var.set("None"))
method_dropdown.pack()

# Start button
start_button = tk.Button(root, text="Start Sorting", command=start_sorting)
start_button.pack(pady=10)

# Label to display sorting time
time_label = tk.Label(root, text="")
time_label.pack()

root.mainloop()
