import ping3
from datetime import datetime
from tkinter import Tk, Label, mainloop, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

root = Tk()
root.title("Internet Latency")

latency_label = Label(root, text="Latency: N/A")
latency_label.pack()

# create the figure and axes for the line graph
fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Latency (ms)")

# create the line graph using FigureCanvasTkAgg
line_graph = FigureCanvasTkAgg(fig, master=root)
line_graph.get_tk_widget().pack()

# create lists to store the x and y values for the line graph
x_values = []
y_values = []

# create a DataFrame to store the internet latency data
data = {"time": [], "latency": []}
df = pd.DataFrame(data)


def update_latency():
    # get the current time
    x = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # get the internet latency
    y = ping3.ping("google.com")
    # append the x and y values to the lists
    x_values.append(x)
    y_values.append(y)
    # update the line graph
    ax.clear()
    ax.plot(x_values, y_values)
    line_graph.draw()
    # update the latency label
    latency_label.config(text="Latency: " + str(y) + " ms")
    # append the new data to the DataFrame
    global df
    df = df.append({"time": x, "latency": y}, ignore_index=True)
    # schedule the function to be called again in 1 second
    root.after(1000, update_latency)


def save_to_excel():
    # save the DataFrame to an excel file
    df.to_excel("internet_latency.xlsx")
    print("Data saved to internet_latency.xlsx")


# create a button to save the data to an excel file
save_button = Button(root, text="Save to Excel", command=save_to_excel)
save_button.pack()

update_latency()
root.mainloop()
