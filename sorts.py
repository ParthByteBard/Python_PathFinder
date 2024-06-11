import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pygame.mixer
pygame.mixer.init()
sound1=pygame.mixer.Sound("sort-sound.mp3")
sound2=pygame.mixer.Sound("sound2.wav")
search=pygame.mixer.Sound("search_sound.wav")
bonus=pygame.mixer.Sound("bonus_alert.wav")


default_volume=0.3
sound1.set_volume(default_volume)


""" Helper function to swap elements i and j of list A. """
def swap(A, i, j):
    if i != j:
        A[i], A[j] = A[j], A[i]


"""In-place bubble sort."""
def bubblesort(A):
    if len(A) == 1:
        return
    swapped = True
    
    for i in range(len(A) - 1):
       
        if not swapped:
            break
        swapped = False
        for j in range(len(A) - 1 - i):
            sound1.play()
            if A[j] > A[j + 1]:
                swap(A, j, j + 1)
                swapped = True
            yield A
    sound1.stop()
    bonus.play()    
           


"""In-place insertion sort."""
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

"""Merge sort."""
def mergesort(A, start, end):
    if end <= start:
        return
    
    mid = start + ((end - start + 1) // 2) - 1
    
    yield from mergesort(A, start, mid)
    yield from mergesort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A
    sound1.stop()
   


"""Helper function for merge sort."""
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




"""In-place quicksort."""
def quicksort(A, start, end):

    if start >= end:
        return
    
    pivot = A[end]
    pivotIdx = start

    for i in range(start, end):
        
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            sound1.play()
            pivotIdx += 1
        yield A
    swap(A, end, pivotIdx)
    yield A

    yield from quicksort(A, start, pivotIdx - 1)
    yield from quicksort(A, pivotIdx + 1, end)
    sound1.stop()
    
    


"""In-place selection sort."""
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




if __name__ == "__main__":
    # Get user input to determine range of integers (1 to N) and desired sorting method (algorithm).
    N = int(input("Enter number of integers: "))
    method_msg = "\n\nSelect the sorting algorithm\nb:bubble sort\ns:selection sort\nm:merge sort\nq:quick sort\ni:insertion sort\n"
    method = input(method_msg)

    # Build and randomly shuffle list of integers.
    A = [x + 1 for x in range(N)]
    random.seed(time.time())
    random.shuffle(A)

    # Get appropriate generator to supply to matplotlib FuncAnimation method.
    # At every stage of the sorting algorithm, the generator yields the current state of the list.
    # This state represents how the list looks after each iteration or operation of the sorting algorithm.
    #The FuncAnimation function from matplotlib.animation then uses these yielded states to update the animation. Each yielded state corresponds to a frame in the animation, allowing the visualization to dynamically show how the list evolves throughout the sorting process.
    #The yielded states are used by FuncAnimation to update the animation, effectively showcasing the progression of the sorting algorithm visually.
    
    if method == "b":
        title = "Bubble sort"
        generator = bubblesort(A)
    elif method == "i":
        title = "Insertion sort"
        generator = insertionsort(A)
    elif method == "m":
        title = "Merge sort"
        generator = mergesort(A, 0, N - 1)
        bonus.play()
    elif method == "q":
        title = "Quicksort"
        generator = quicksort(A, 0, N - 1)
    else:
        title = "Selection sort"
        generator = selectionsort(A)

    

    # Initialize figure and axis.
    fig, ax = plt.subplots()
    ax.set_title(title)

    # Initialize a bar plot. Note that matplotlib.pyplot.bar() returns a
    # list of rectangles (with each bar in the bar plot corresponding
    # to one rectangle), which we store in bar_rects.
    bar_rects = ax.bar(range(len(A)), A, align="edge")

    # Set axis limits. Set y axis upper limit high enough that the tops of
    # the bars won't overlap with the text label.
    ax.set_xlim(0, N)
    ax.set_ylim(0, int(1.07 * N))

    # Place a text label in the upper-left corner of the plot to display
    # number of operations performed by the sorting algorithm (each "yield"
    # is treated as 1 operation).
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    # Define function update_fig() for use with matplotlib.pyplot.FuncAnimation().
    # To track the number of operations, i.e., iterations through which the
    # animation has gone, define a variable "iteration". This variable will
    # be passed to update_fig() to update the text label, and will also be
    # incremented in update_fig(). For this increment to be reflected outside
    # the function, we make "iteration" a list of 1 element, since lists (and
    # other mutable objects) are passed by reference (but an integer would be
    # passed by value).
    # NOTE: Alternatively, iteration could be re-declared within update_fig()
    # with the "global" keyword (or "nonlocal" keyword).
    iteration = [0]
    def update_fig(A, rects, iteration):
        for rect, val in zip(rects, A):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text("# of operations: {}".format(iteration[0]))

    anim = animation.FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, iteration), frames=generator, interval=0,
        repeat=False)
    bonus.play()
    plt.show()

