import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import csv

# Create the main window
root = tk.Tk()
root.title("Stereotaxic Coordinate Calculator")
root.geometry("1200x800")  # Adjusted initial size

# Function to save data
def save_data():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write experiment details
                writer.writerow(['Experiment Details'])
                writer.writerow(['Model', model_var.get()])
                writer.writerow(['Experiment ID', experiment_id_entry.get()])
                writer.writerow(['Animal ID', animal_id_entry.get()])
                writer.writerow(['Lead/Team', lead_team_entry.get()])
                writer.writerow(['Animal Weight', animal_weight_entry.get()])
                writer.writerow(['Animal Age', animal_age_entry.get()])
                writer.writerow([])
                # Write region of interest
                writer.writerow(['Region of Interest'])
                writer.writerow(['', 'Min Range', 'Max Range'])
                writer.writerow(['AP', roi_ap_entry_min.get(), roi_ap_entry_max.get()])
                writer.writerow(['ML', roi_ml_entry_min.get(), roi_ml_entry_max.get()])
                writer.writerow(['DV', roi_dv_entry_min.get(), roi_dv_entry_max.get()])
                writer.writerow([])
                # Write reference inputs
                writer.writerow(['Reference Input'])
                writer.writerow(['Bregma AP', bregma_ap_entry.get()])
                writer.writerow(['Bregma ML', bregma_ml_entry.get()])
                writer.writerow(['Bregma DV', bregma_dv_entry.get()])
                writer.writerow(['Lambda AP', lambda_ap_entry.get()])
                writer.writerow(['Lambda ML', lambda_ml_entry.get()])
                writer.writerow(['Lambda DV', lambda_dv_entry.get()])
                writer.writerow([])
                # Write drilling inputs
                writer.writerow(['Drilling'])
                writer.writerow(['', 'L-Hemisphere', 'R-Hemisphere'])
                writer.writerow(['AP', drilling_ap_entry_left.get(), drilling_ap_entry_right.get()])
                writer.writerow(['ML', drilling_ml_entry_left.get(), drilling_ml_entry_right.get()])
                writer.writerow(['Diameter', drilling_diameter_entry_left.get(), drilling_diameter_entry_right.get()])
                writer.writerow([])
                # Write electrode placements
                writer.writerow(['Electrode Placements'])
                writer.writerow(['Position', 'AP', 'ML', 'DV', 'Rating', 'Comment'])
                for idx, entry in enumerate(entry_rows, start=1):
                    ap_entry, ml_entry, dv_entry, rating_vars, rating_checkbuttons, comment_entry, delete_button, total_ap_label, total_ml_label, total_dv_label, _, position_label = entry
                    # Find the selected rating
                    rating = None
                    for i, var in enumerate(rating_vars):
                        if var.get() == 1:
                            rating = i
                            break
                    rating = rating if rating is not None else ''
                    writer.writerow([
                        idx,
                        ap_entry.get(),
                        ml_entry.get(),
                        dv_entry.get(),
                        rating,
                        comment_entry.get()
                    ])
            messagebox.showinfo("Save Successful", f"Data saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving:\n{e}")

# Function to load data
def load_data():
    filename = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                idx = 0
                # Clear existing entries
                clear_entries()
                while idx < len(data):
                    row = data[idx]
                    if row and row[0] == 'Experiment Details':
                        idx += 1
                        while idx < len(data) and data[idx] and data[idx][0] != '':
                            if len(data[idx]) >= 2:
                                if data[idx][0] == 'Model':
                                    model_var.set(data[idx][1])
                                elif data[idx][0] == 'Experiment ID':
                                    experiment_id_entry.delete(0, tk.END)
                                    experiment_id_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Animal ID':
                                    animal_id_entry.delete(0, tk.END)
                                    animal_id_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Lead/Team':
                                    lead_team_entry.delete(0, tk.END)
                                    lead_team_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Animal Weight':
                                    animal_weight_entry.delete(0, tk.END)
                                    animal_weight_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Animal Age':
                                    animal_age_entry.delete(0, tk.END)
                                    animal_age_entry.insert(0, data[idx][1])
                            idx += 1
                    elif row and row[0] == 'Region of Interest':
                        idx += 1  # Skip header
                        idx += 1  # Skip subheader
                        while idx < len(data) and data[idx] and data[idx][0] != '':
                            if len(data[idx]) >= 3:
                                if data[idx][0] == 'AP':
                                    roi_ap_entry_min.delete(0, tk.END)
                                    roi_ap_entry_min.insert(0, data[idx][1])
                                    roi_ap_entry_max.delete(0, tk.END)
                                    roi_ap_entry_max.insert(0, data[idx][2])
                                elif data[idx][0] == 'ML':
                                    roi_ml_entry_min.delete(0, tk.END)
                                    roi_ml_entry_min.insert(0, data[idx][1])
                                    roi_ml_entry_max.delete(0, tk.END)
                                    roi_ml_entry_max.insert(0, data[idx][2])
                                elif data[idx][0] == 'DV':
                                    roi_dv_entry_min.delete(0, tk.END)
                                    roi_dv_entry_min.insert(0, data[idx][1])
                                    roi_dv_entry_max.delete(0, tk.END)
                                    roi_dv_entry_max.insert(0, data[idx][2])
                            idx += 1
                    elif row and row[0] == 'Reference Input':
                        idx += 1
                        while idx < len(data) and data[idx] and data[idx][0] != '':
                            if len(data[idx]) >= 2:
                                if data[idx][0] == 'Bregma AP':
                                    bregma_ap_entry.delete(0, tk.END)
                                    bregma_ap_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Bregma ML':
                                    bregma_ml_entry.delete(0, tk.END)
                                    bregma_ml_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Bregma DV':
                                    bregma_dv_entry.delete(0, tk.END)
                                    bregma_dv_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Lambda AP':
                                    lambda_ap_entry.delete(0, tk.END)
                                    lambda_ap_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Lambda ML':
                                    lambda_ml_entry.delete(0, tk.END)
                                    lambda_ml_entry.insert(0, data[idx][1])
                                elif data[idx][0] == 'Lambda DV':
                                    lambda_dv_entry.delete(0, tk.END)
                                    lambda_dv_entry.insert(0, data[idx][1])
                            idx += 1
                    elif row and row[0] == 'Drilling':
                        idx += 1  # Skip header
                        idx += 1  # Skip subheader
                        while idx < len(data) and data[idx] and data[idx][0] != '':
                            if len(data[idx]) >= 3:
                                if data[idx][0] == 'AP':
                                    drilling_ap_entry_left.delete(0, tk.END)
                                    drilling_ap_entry_left.insert(0, data[idx][1])
                                    drilling_ap_entry_right.delete(0, tk.END)
                                    drilling_ap_entry_right.insert(0, data[idx][2])
                                elif data[idx][0] == 'ML':
                                    drilling_ml_entry_left.delete(0, tk.END)
                                    drilling_ml_entry_left.insert(0, data[idx][1])
                                    drilling_ml_entry_right.delete(0, tk.END)
                                    drilling_ml_entry_right.insert(0, data[idx][2])
                                elif data[idx][0] == 'Diameter':
                                    drilling_diameter_entry_left.delete(0, tk.END)
                                    drilling_diameter_entry_left.insert(0, data[idx][1])
                                    drilling_diameter_entry_right.delete(0, tk.END)
                                    drilling_diameter_entry_right.insert(0, data[idx][2])
                            idx += 1
                    elif row and row[0] == 'Electrode Placements':
                        idx += 1  # Skip header row
                        idx += 1
                        while idx < len(data) and data[idx] and data[idx][0] != '':
                            if len(data[idx]) >= 6:
                                add_entry()
                                last_entry = entry_rows[-1]
                                last_entry[0].delete(0, tk.END)
                                last_entry[0].insert(0, data[idx][1])
                                last_entry[1].delete(0, tk.END)
                                last_entry[1].insert(0, data[idx][2])
                                last_entry[2].delete(0, tk.END)
                                last_entry[2].insert(0, data[idx][3])
                                rating = data[idx][4]
                                # Set the appropriate checkbox
                                for i, var in enumerate(last_entry[3]):
                                    if str(i) == rating:
                                        var.set(1)
                                    else:
                                        var.set(0)
                                last_entry[5].delete(0, tk.END)
                                last_entry[5].insert(0, data[idx][5])  # Comment
                            idx += 1
                    else:
                        idx += 1
                # After loading all data, update overlays
                overlay_coordinates()
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading:\n{e}")

# Function to create a new experiment
def new_experiment():
    result = messagebox.askyesnocancel("New Experiment", "Do you want to save the current experiment before starting a new one?")
    if result is True:
        save_data()
        reset_program()
    elif result is False:
        reset_program()
    else:
        # Cancelled, do nothing
        pass

def reset_program():
    # Clear all entries and reset variables
    clear_entries()
    # Reset experiment details
    experiment_id_entry.delete(0, tk.END)
    animal_id_entry.delete(0, tk.END)
    lead_team_entry.delete(0, tk.END)
    animal_weight_entry.delete(0, tk.END)
    animal_age_entry.delete(0, tk.END)
    # Reset ROI entries
    roi_ap_entry_min.delete(0, tk.END)
    roi_ap_entry_max.delete(0, tk.END)
    roi_ml_entry_min.delete(0, tk.END)
    roi_ml_entry_max.delete(0, tk.END)
    roi_dv_entry_min.delete(0, tk.END)
    roi_dv_entry_max.delete(0, tk.END)
    # Reset reference inputs
    bregma_ap_entry.delete(0, tk.END)
    bregma_ap_entry.insert(0, "0.0")
    bregma_ml_entry.delete(0, tk.END)
    bregma_ml_entry.insert(0, "0.0")
    bregma_dv_entry.delete(0, tk.END)
    bregma_dv_entry.insert(0, "0.0")
    lambda_ap_entry.delete(0, tk.END)
    lambda_ap_entry.insert(0, "0.0")
    lambda_ml_entry.delete(0, tk.END)
    lambda_ml_entry.insert(0, "0.0")
    lambda_dv_entry.delete(0, tk.END)
    lambda_dv_entry.insert(0, "0.0")
    # Reset drilling inputs
    drilling_ap_entry_left.delete(0, tk.END)
    drilling_ml_entry_left.delete(0, tk.END)
    drilling_diameter_entry_left.delete(0, tk.END)
    drilling_ap_entry_right.delete(0, tk.END)
    drilling_ml_entry_right.delete(0, tk.END)
    drilling_diameter_entry_right.delete(0, tk.END)
    # Reset model
    model_var.set("Rat")
    # Reset overlays
    overlay_coordinates()

# Function to overlay coordinates and update AP Distance
def overlay_coordinates():
    try:
        # Get Bregma and Lambda physical coordinates in mm
        bregma_ap = float(bregma_ap_entry.get())
        bregma_ml = float(bregma_ml_entry.get())
        bregma_dv = float(bregma_dv_entry.get())  # Ensure bregma_dv is obtained

        lambda_ap = float(lambda_ap_entry.get())
        lambda_ml = float(lambda_ml_entry.get())
        lambda_dv = float(lambda_dv_entry.get())

        # Compute delta_AP_mm (AP Distance)
        delta_AP_mm = lambda_ap - bregma_ap

        # Update AP Distance label
        ap_distance_label.config(text=f"{delta_AP_mm:.2f} mm")

        if delta_AP_mm == 0:
            messagebox.showerror("Invalid Input", "Bregma and Lambda AP values cannot be the same.")
            return

        # Fixed Bregma and Lambda positions on images (in pixels)
        # Since we removed the left image, we only need to set up for the right canvas

        # Right image coordinates
        right_x_b = 950
        right_y_b = 690
        right_x_l = 1760
        right_y_l = 690

        # Compute scaling factors based on the fixed positions and user inputs
        # For the canvas, AP maps to X-axis, ML maps to Y-axis

        # Right canvas scaling factor
        delta_pixels_right = right_x_l - right_x_b  # pixels
        scale_right = delta_pixels_right / delta_AP_mm  # pixels per mm

        # Store Bregma pixel coordinates and scaling factor in the canvas
        # Right canvas
        right_canvas.x_b = right_x_b
        right_canvas.y_b = right_y_b
        right_canvas.scale = scale_right
        right_canvas.bregma_ap = bregma_ap
        right_canvas.bregma_ml = bregma_ml
        right_canvas.bregma_dv = bregma_dv  # Assign bregma_dv

        right_canvas.coords_data = {
            'bregma_pixel': (right_x_b, right_y_b),
            'lambda_pixel': (right_x_l, right_y_l)
        }

        # Redraw overlays
        redraw_overlays()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

# Variables to track ROI overlay states
roi_l_overlay_active = False
roi_r_overlay_active = False

def toggle_l_roi_overlay():
    global roi_l_overlay_active
    roi_l_overlay_active = not roi_l_overlay_active
    redraw_overlays()

def toggle_r_roi_overlay():
    global roi_r_overlay_active
    roi_r_overlay_active = not roi_r_overlay_active
    redraw_overlays()

# Variables to track Drilling overlay states
drilling_l_overlay_active = True
drilling_r_overlay_active = True

def toggle_l_drilling_overlay():
    global drilling_l_overlay_active
    drilling_l_overlay_active = not drilling_l_overlay_active
    redraw_overlays()

def toggle_r_drilling_overlay():
    global drilling_r_overlay_active
    drilling_r_overlay_active = not drilling_r_overlay_active
    redraw_overlays()

# Variable to track Grid overlay state
grid_overlay_active = False

def toggle_grid_overlay():
    global grid_overlay_active
    grid_overlay_active = not grid_overlay_active
    redraw_overlays()

# Function to redraw overlays
def redraw_overlays():
    canvas_widget = right_canvas
    if not hasattr(canvas_widget, 'coords_data'):
        return

    x_b = canvas_widget.x_b
    y_b = canvas_widget.y_b
    scale = canvas_widget.scale

    # Get the display size of the image
    display_width = getattr(canvas_widget, 'display_image_width', canvas_widget.winfo_width())
    display_height = getattr(canvas_widget, 'display_image_height', canvas_widget.winfo_height())

    # Calculate scaling factors for image resizing
    original_image_width = right_original_image.width
    original_image_height = right_original_image.height

    scale_x = display_width / original_image_width
    scale_y = display_height / original_image_height

    # Offsets due to image centering
    offset_x = getattr(canvas_widget, 'offset_x', 0)
    offset_y = getattr(canvas_widget, 'offset_y', 0)

    # Adjusted positions for Bregma and Lambda
    x_b_adj = x_b * scale_x + offset_x
    y_b_adj = y_b * scale_y + offset_y

    x_l = canvas_widget.coords_data['lambda_pixel'][0]
    y_l = canvas_widget.coords_data['lambda_pixel'][1]
    x_l_adj = x_l * scale_x + offset_x
    y_l_adj = y_l * scale_y + offset_y

    # Clear previous overlays
    canvas_widget.delete('overlay')

    # Draw Bregma
    canvas_widget.create_oval(
        x_b_adj - 5, y_b_adj - 5,
        x_b_adj + 5, y_b_adj + 5,
        fill='red', tags='overlay'
    )
    canvas_widget.create_text(x_b_adj + 10, y_b_adj + 10, text='Bregma', fill='red', tags='overlay')

    # Draw Lambda
    canvas_widget.create_oval(
        x_l_adj - 5, y_l_adj - 5,
        x_l_adj + 5, y_l_adj + 5,
        fill='blue', tags='overlay'
    )
    canvas_widget.create_text(x_l_adj + 10, y_l_adj + 10, text='Lambda', fill='blue', tags='overlay')

    # Draw grid if active
    if grid_overlay_active:
        draw_grid(canvas_widget, x_b, y_b, scale, scale_x, scale_y, offset_x, offset_y)

    # Use red color for both hemispheres
    fill_color = (255, 0, 0, int(255 * 0.2))  # 20% opacity red

    # Draw the drilling region for Left Hemisphere
    if drilling_l_overlay_active:
        try:
            drill_ap_left = float(drilling_ap_entry_left.get())
            drill_ml_left = float(drilling_ml_entry_left.get())
            drill_diameter_left = float(drilling_diameter_entry_left.get())

            # Compute differences from Bregma
            delta_ap_left = drill_ap_left - canvas_widget.bregma_ap
            delta_ml_left = drill_ml_left - canvas_widget.bregma_ml

            # Convert differences to pixels
            pixel_dx_left = delta_ap_left * scale
            pixel_dy_left = -delta_ml_left * scale  # Negative because Y increases downward

            # Adjusted pixel positions
            pixel_x_left = x_b + pixel_dx_left
            pixel_y_left = y_b + pixel_dy_left

            # Adjusted for image resizing and centering
            pixel_x_adj_left = pixel_x_left * scale_x + offset_x
            pixel_y_adj_left = pixel_y_left * scale_y + offset_y

            # Diameter in pixels
            diameter_pixels_left = drill_diameter_left * scale * scale_x

            # Draw semi-transparent circle for Left Hemisphere
            circle_image_left = Image.new('RGBA', (int(diameter_pixels_left), int(diameter_pixels_left)), (0, 0, 0, 0))
            draw_left = ImageDraw.Draw(circle_image_left)
            draw_left.ellipse((0, 0, diameter_pixels_left, diameter_pixels_left), fill=fill_color)
            circle_photo_image_left = ImageTk.PhotoImage(circle_image_left)
            canvas_widget.create_image(
                pixel_x_adj_left - diameter_pixels_left / 2,
                pixel_y_adj_left - diameter_pixels_left / 2,
                image=circle_photo_image_left,
                anchor='nw',
                tags='overlay'
            )
            # Keep a reference to prevent garbage collection
            canvas_widget.circle_image_left = circle_photo_image_left

        except ValueError:
            pass  # Ignore if inputs are invalid

    # Draw the drilling region for Right Hemisphere
    if drilling_r_overlay_active:
        try:
            drill_ap_right = float(drilling_ap_entry_right.get())
            drill_ml_right = float(drilling_ml_entry_right.get())
            drill_diameter_right = float(drilling_diameter_entry_right.get())

            # Compute differences from Bregma
            delta_ap_right = drill_ap_right - canvas_widget.bregma_ap
            delta_ml_right = drill_ml_right - canvas_widget.bregma_ml

            # Convert differences to pixels
            pixel_dx_right = delta_ap_right * scale
            pixel_dy_right = -delta_ml_right * scale  # Negative because Y increases downward

            # Adjusted pixel positions
            pixel_x_right = x_b + pixel_dx_right
            pixel_y_right = y_b + pixel_dy_right

            # Adjusted for image resizing and centering
            pixel_x_adj_right = pixel_x_right * scale_x + offset_x
            pixel_y_adj_right = pixel_y_right * scale_y + offset_y

            # Diameter in pixels
            diameter_pixels_right = drill_diameter_right * scale * scale_x

            # Draw semi-transparent circle for Right Hemisphere
            circle_image_right = Image.new('RGBA', (int(diameter_pixels_right), int(diameter_pixels_right)), (0, 0, 0, 0))
            draw_right = ImageDraw.Draw(circle_image_right)
            draw_right.ellipse((0, 0, diameter_pixels_right, diameter_pixels_right), fill=fill_color)
            circle_photo_image_right = ImageTk.PhotoImage(circle_image_right)
            canvas_widget.create_image(
                pixel_x_adj_right - diameter_pixels_right / 2,
                pixel_y_adj_right - diameter_pixels_right / 2,
                image=circle_photo_image_right,
                anchor='nw',
                tags='overlay'
            )
            # Keep a reference to prevent garbage collection
            canvas_widget.circle_image_right = circle_photo_image_right

        except ValueError:
            pass  # Ignore if inputs are invalid

    # Draw electrode placement points
    for i, entry in enumerate(entry_rows):
        ap_entry, ml_entry, dv_entry, rating_vars, rating_checkbuttons, comment_entry, delete_button, total_ap_label, total_ml_label, total_dv_label, overlay_id, position_label = entry
        try:
            # Get additive values
            delta_ap_input = float(ap_entry.get())
            delta_ml_input = float(ml_entry.get())
            delta_dv_input = float(dv_entry.get())

            # Compute total values
            total_ap = canvas_widget.bregma_ap + delta_ap_input
            total_ml = canvas_widget.bregma_ml + delta_ml_input
            total_dv = canvas_widget.bregma_dv + delta_dv_input  # Using bregma_dv

            # Update total value labels
            total_ap_label.config(text=f"{total_ap:.2f}")
            total_ml_label.config(text=f"{total_ml:.2f}")
            total_dv_label.config(text=f"{total_dv:.2f}")

            # Find the selected rating
            rating = None
            for idx, var in enumerate(rating_vars):
                if var.get() == 1:
                    rating = idx
                    break

            if rating is None:
                rating = 0  # Default to 0 if none selected

            # Compute differences from Bregma
            delta_ap = total_ap - canvas_widget.bregma_ap
            delta_ml = total_ml - canvas_widget.bregma_ml

            # Convert differences to pixels
            pixel_dx = delta_ap * scale
            pixel_dy = -delta_ml * scale  # Negative because Y increases downward

            # Adjusted pixel positions
            pixel_x = x_b + pixel_dx
            pixel_y = y_b + pixel_dy

            # Adjusted for image resizing and centering
            pixel_x_adj = pixel_x * scale_x + offset_x
            pixel_y_adj = pixel_y * scale_y + offset_y

            # Determine color based on rating
            color_map = {
                0: 'black',
                1: '#face3c',
                2: '#2c4ef5',
                3: '#75f222',
            }
            color = color_map.get(rating, 'black')

            # Draw point and save the overlay ID
            point_id = canvas_widget.create_oval(
                pixel_x_adj - 3, pixel_y_adj - 3,
                pixel_x_adj + 3, pixel_y_adj + 3,
                fill=color, tags='overlay'
            )
            entry[10] = point_id  # Update overlay_id in entry_rows

        except ValueError:
            continue  # Skip entries with invalid data

# Function to draw grid lines
def draw_grid(canvas_widget, x_b, y_b, scale, scale_x, scale_y, offset_x, offset_y):
    try:
        # Define grid range in mm relative to Bregma
        grid_range_ap = (-10, 10)  # From -10 mm to +10 mm
        grid_range_ml = (-10, 10)  # From -10 mm to +10 mm
        grid_interval = 1  # Grid lines every 1 mm

        # Generate AP grid lines
        for ap in range(int(grid_range_ap[0]), int(grid_range_ap[1]) + 1, grid_interval):
            # Convert AP coordinate to pixels
            pixel_dx = ap * scale
            pixel_x = x_b + pixel_dx
            pixel_x_adj = pixel_x * scale_x + offset_x

            # Draw vertical grid line
            canvas_widget.create_line(
                pixel_x_adj, 0,
                pixel_x_adj, canvas_widget.winfo_height(),
                fill='gray', dash=(2, 4), tags='overlay'
            )

            # Add coordinate label (Horizontal Text)
            canvas_widget.create_text(
                pixel_x_adj + 5, y_b * scale_y + offset_y + 15,
                text=f"{ap + canvas_widget.bregma_ap:.1f}",
                fill='gray', font=('Arial', 8), tags='overlay'
            )

        # Generate ML grid lines
        for ml in range(int(grid_range_ml[0]), int(grid_range_ml[1]) + 1, grid_interval):
            # Convert ML coordinate to pixels
            pixel_dy = -ml * scale  # Negative because Y increases downward
            pixel_y = y_b + pixel_dy
            pixel_y_adj = pixel_y * scale_y + offset_y

            # Draw horizontal grid line
            canvas_widget.create_line(
                0, pixel_y_adj,
                canvas_widget.winfo_width(), pixel_y_adj,
                fill='gray', dash=(2, 4), tags='overlay'
            )

            # Add coordinate label
            canvas_widget.create_text(
                x_b * scale_x + offset_x + 25, pixel_y_adj - 5,
                text=f"{ml + canvas_widget.bregma_ml:.1f}",
                fill='gray', font=('Arial', 8), tags='overlay'
            )
    except Exception as e:
        print(f"Error drawing grid: {e}")

# Function to handle input changes and update overlays and AP Distance
def on_input_change(event):
    overlay_coordinates()

# Function to delete an entry
def delete_entry(index):
    # Remove widgets from the interface
    entries = entry_rows[index]
    # entries structure:
    # [ap_entry, ml_entry, dv_entry, rating_vars, rating_checkbuttons, comment_entry,
    #  delete_button, total_ap_label, total_ml_label, total_dv_label,
    #  overlay_id, position_label]

    widgets_to_destroy = [
        entries[0],  # ap_entry
        entries[1],  # ml_entry
        entries[2],  # dv_entry
        entries[5],  # comment_entry
        entries[6],  # delete_button
        entries[7],  # total_ap_label
        entries[8],  # total_ml_label
        entries[9],  # total_dv_label
        entries[11],  # position_label
    ] + entries[4]  # rating checkbuttons

    # Destroy the widgets
    for widget in widgets_to_destroy:
        widget.destroy()

    # Remove the overlay dot
    overlay_id = entries[10]
    if overlay_id is not None:
        right_canvas.delete(overlay_id)

    # Remove the row from the list
    entry_rows.pop(index)

    # Update position labels and adjust grid positions
    for i, entry in enumerate(entry_rows):
        ap_entry, ml_entry, dv_entry, rating_vars, rating_checkbuttons, comment_entry, delete_button, total_ap_label, total_ml_label, total_dv_label, overlay_id, position_label = entry
        position_label.config(text=f"{i + 1}")
        position_label.grid(row=i + 1, column=0, padx=5, pady=5)
        ap_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        total_ap_label.grid(row=i + 1, column=2, padx=5, pady=5)
        ml_entry.grid(row=i + 1, column=3, padx=5, pady=5)
        total_ml_label.grid(row=i + 1, column=4, padx=5, pady=5)
        dv_entry.grid(row=i + 1, column=5, padx=5, pady=5)
        total_dv_label.grid(row=i + 1, column=6, padx=5, pady=5)
        # Place rating checkboxes
        for j, chk in enumerate(rating_checkbuttons):
            chk.grid(row=i + 1, column=7 + j, padx=2, pady=5)
        comment_entry.grid(row=i + 1, column=11, padx=5, pady=5)
        delete_button.grid(row=i + 1, column=12, padx=5, pady=5)
        # Update the delete button command
        idx = i
        delete_button.config(command=lambda idx=idx: delete_entry(idx))
        # Update the rating checkboxes command
        for j, chk in enumerate(rating_checkbuttons):
            chk.config(command=lambda idx=idx, var_idx=j: update_rating(idx, var_idx))

    redraw_overlays()

# Function to add a new entry row
entry_rows = []  # To keep track of entry widgets

def add_entry():
    row = len(entry_rows) + 1  # Start from 1 because of header

    # Position label
    position_label = tk.Label(entry_container, text=f"{row}")
    position_label.grid(row=row, column=0, padx=5, pady=5)

    # AP input and total
    ap_entry = tk.Entry(entry_container, width=8)
    ap_entry.grid(row=row, column=1, padx=5, pady=5)
    total_ap_label = tk.Label(entry_container, text="", fg="grey")
    total_ap_label.grid(row=row, column=2, padx=5, pady=5)

    # ML input and total
    ml_entry = tk.Entry(entry_container, width=8)
    ml_entry.grid(row=row, column=3, padx=5, pady=5)
    total_ml_label = tk.Label(entry_container, text="", fg="grey")
    total_ml_label.grid(row=row, column=4, padx=5, pady=5)

    # DV input and total
    dv_entry = tk.Entry(entry_container, width=8)
    dv_entry.grid(row=row, column=5, padx=5, pady=5)
    total_dv_label = tk.Label(entry_container, text="", fg="grey")
    total_dv_label.grid(row=row, column=6, padx=5, pady=5)

    # Rating variables and checkboxes
    rating_vars = [tk.IntVar() for _ in range(4)]
    rating_checkbuttons = []
    for i, var in enumerate(rating_vars):
        chk = tk.Checkbutton(entry_container, text=str(i), variable=var,
                             command=lambda idx=row-1, var_idx=i: update_rating(idx, var_idx))
        chk.grid(row=row, column=7 + i, padx=2, pady=5)
        rating_checkbuttons.append(chk)

    # Comment entry
    comment_entry = tk.Entry(entry_container, width=15)
    comment_entry.grid(row=row, column=11, padx=5, pady=5)

    # Placeholder for overlay ID
    overlay_id = None

    # Delete button
    delete_button = tk.Button(entry_container, text="Delete", command=lambda idx=row-1: delete_entry(idx))
    delete_button.grid(row=row, column=12, padx=5, pady=5)

    entry_rows.append([
        ap_entry, ml_entry, dv_entry, rating_vars, rating_checkbuttons, comment_entry,
        delete_button, total_ap_label, total_ml_label, total_dv_label, overlay_id,
        position_label
    ])

    # Bind input changes to redraw overlays
    for entry in [ap_entry, ml_entry, dv_entry]:
        entry.bind("<FocusOut>", lambda event: redraw_overlays())
        entry.bind("<Return>", lambda event: redraw_overlays())

    # Redraw overlays to include new point if scaling is available
    if hasattr(right_canvas, 'scale'):
        redraw_overlays()

def update_rating(index, selected_index):
    rating_vars = entry_rows[index][3]
    # Deselect other checkboxes
    for i, var in enumerate(rating_vars):
        if i != selected_index:
            var.set(0)
    # Redraw overlays
    redraw_overlays()

def clear_entries():
    # Clear electrode placements
    for i in range(len(entry_rows) - 1, -1, -1):
        delete_entry(i)

def on_closing():
    result = messagebox.askyesnocancel("Exit", "Do you want to save before exiting?")
    if result is True:
        save_data()
        root.destroy()
    elif result is False:
        if messagebox.askokcancel("Exit", "Are you sure you want to exit without saving?"):
            root.destroy()
    else:
        # Cancelled, do nothing
        pass

root.protocol("WM_DELETE_WINDOW", on_closing)

# Function to resize the image when canvas size changes
def resize_image(event):
    if event is not None:
        # Get the canvas widget
        canvas_widget = event.widget
        width = event.width
        height = event.height
    else:
        # Manually get the canvas and its size
        canvas_widget = right_canvas
        image = right_original_image
        width = canvas_widget.winfo_width()
        height = canvas_widget.winfo_height()
        if width == 1 and height == 1:
            # The canvas hasn't been properly initialized yet
            # Schedule the resize_image function to run after the mainloop starts
            root.after(100, resize_image, None)
            return

    # Resize the image while maintaining aspect ratio
    image = right_original_image
    image_ratio = image.width / image.height
    canvas_ratio = width / height

    if canvas_ratio > image_ratio:
        # Canvas is wider relative to its height than the image
        new_height = height
        new_width = int(height * image_ratio)
    else:
        # Canvas is taller relative to its width than the image
        new_width = width
        new_height = int(width / image_ratio)

    # Calculate offsets to center the image
    offset_x = (width - new_width) // 2
    offset_y = (height - new_height) // 2

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(resized_image)

    # Keep a reference to prevent garbage collection
    canvas_widget.image = photo_image

    # Clear the canvas and display the new image centered
    canvas_widget.delete('overlay')
    canvas_widget.delete('all')
    canvas_widget.create_image(width // 2, height // 2, image=photo_image, anchor='center')

    # Store offsets and display size for overlay calculations
    canvas_widget.offset_x = offset_x
    canvas_widget.offset_y = offset_y
    canvas_widget.display_image_width = new_width
    canvas_widget.display_image_height = new_height

    # Redraw overlays
    redraw_overlays()

# Function to configure the scroll region of the entry canvas
def on_frame_configure(event):
    entry_canvas.configure(scrollregion=entry_canvas.bbox("all"))

# Now proceed with GUI setup and widget creation

# Main frames
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

left_column = tk.Frame(main_frame)
left_column.pack(side='left', fill='both', expand=True)

right_column = tk.Frame(main_frame)
right_column.pack(side='left', fill='both', expand=True)

# Create left top frame to hold left1 and left2
left_top_frame = tk.Frame(left_column)
left_top_frame.pack(side='top', fill='x', expand=False)

# Left1 and Left2 frames
left1_frame = tk.Frame(left_top_frame)
left1_frame.pack(side='left', fill='both', expand=True)

left2_frame = tk.Frame(left_top_frame)
left2_frame.pack(side='left', fill='both', expand=True)

# Load the coordinate map image
right_image_path = "diagram_right.png"
right_original_image = Image.open(right_image_path)

# Right image frame
right_image_frame = tk.Frame(right_column)
right_image_frame.pack(fill='both', expand=True)

# Add title above the right image
right_title = tk.Label(right_image_frame, text="Stereotaxic Coordinate Map", font=("Helvetica", 14, "bold"))
right_title.pack(side='top', pady=5)

# Create Canvas widget for the right image
right_canvas = tk.Canvas(right_image_frame, bg='white')
right_canvas.pack(side='top', fill='both', expand=True)

# Bind resize events to the canvas
right_canvas.bind('<Configure>', resize_image)

# Left1 Frame - File and Experiment Details / Region of Interest
# Save/Load Section (File)
save_load_frame = tk.Frame(left1_frame)
save_load_frame.pack(side='top', fill='x', pady=5)

save_load_title = tk.Label(save_load_frame, text="File", font=("Helvetica", 12, "bold"))
save_load_title.pack(side='top', pady=5)

# Center the buttons
button_frame = tk.Frame(save_load_frame)
button_frame.pack(side='top', pady=5)

new_button = tk.Button(button_frame, text="New", command=new_experiment)
new_button.pack(side='left', padx=5)

save_button = tk.Button(button_frame, text="Save", command=save_data)
save_button.pack(side='left', padx=5)

load_button = tk.Button(button_frame, text="Load", command=load_data)
load_button.pack(side='left', padx=5)

# Experiment Details Section
exp_details_frame = tk.Frame(left1_frame)
exp_details_frame.pack(side='top', fill='x', pady=5)

exp_details_title = tk.Label(exp_details_frame, text="Experiment Details", font=("Helvetica", 12, "bold"))
exp_details_title.grid(row=0, column=0, columnspan=2, pady=5)

# Add "Model" dropdown
tk.Label(exp_details_frame, text="Model:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
model_var = tk.StringVar()
model_dropdown = ttk.Combobox(exp_details_frame, textvariable=model_var, values=["Rat"])
model_dropdown.current(0)  # Set default to "Rat"
model_dropdown.grid(row=1, column=1, padx=5, pady=5)

# Experiment Details Inputs
tk.Label(exp_details_frame, text="Experiment ID:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
experiment_id_entry = tk.Entry(exp_details_frame, width=15)
experiment_id_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(exp_details_frame, text="Animal ID:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
animal_id_entry = tk.Entry(exp_details_frame, width=15)
animal_id_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(exp_details_frame, text="Lead/Team:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
lead_team_entry = tk.Entry(exp_details_frame, width=15)
lead_team_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(exp_details_frame, text="Animal Weight:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
animal_weight_entry = tk.Entry(exp_details_frame, width=15)
animal_weight_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(exp_details_frame, text="Animal Age:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
animal_age_entry = tk.Entry(exp_details_frame, width=15)
animal_age_entry.grid(row=6, column=1, padx=5, pady=5)

# Region of Interest Subsection
roi_frame = tk.Frame(exp_details_frame)
roi_frame.grid(row=7, column=0, columnspan=2, pady=5)

roi_title = tk.Label(roi_frame, text="Region of Interest", font=("Helvetica", 10, "bold"))
roi_title.grid(row=0, column=0, columnspan=3, pady=5)

# Column titles
tk.Label(roi_frame, text="Min Range").grid(row=1, column=1, padx=5, pady=5)
tk.Label(roi_frame, text="Max Range").grid(row=1, column=2, padx=5, pady=5)

# Row labels
tk.Label(roi_frame, text="AP:").grid(row=2, column=0, padx=5, pady=5)
tk.Label(roi_frame, text="ML:").grid(row=3, column=0, padx=5, pady=5)
tk.Label(roi_frame, text="DV:").grid(row=4, column=0, padx=5, pady=5)

# Min Range inputs
roi_ap_entry_min = tk.Entry(roi_frame, width=10)
roi_ap_entry_min.grid(row=2, column=1, padx=5, pady=5)
roi_ml_entry_min = tk.Entry(roi_frame, width=10)
roi_ml_entry_min.grid(row=3, column=1, padx=5, pady=5)
roi_dv_entry_min = tk.Entry(roi_frame, width=10)
roi_dv_entry_min.grid(row=4, column=1, padx=5, pady=5)

# Max Range inputs
roi_ap_entry_max = tk.Entry(roi_frame, width=10)
roi_ap_entry_max.grid(row=2, column=2, padx=5, pady=5)
roi_ml_entry_max = tk.Entry(roi_frame, width=10)
roi_ml_entry_max.grid(row=3, column=2, padx=5, pady=5)
roi_dv_entry_max = tk.Entry(roi_frame, width=10)
roi_dv_entry_max.grid(row=4, column=2, padx=5, pady=5)

# Overlay ROI Buttons (Commented Out)
# overlay_l_roi_button = tk.Button(roi_frame, text="Overlay L-ROI", command=toggle_l_roi_overlay)
# overlay_l_roi_button.grid(row=5, column=0, pady=5)

# overlay_r_roi_button = tk.Button(roi_frame, text="Overlay R-ROI", command=toggle_r_roi_overlay)
# overlay_r_roi_button.grid(row=5, column=2, pady=5)

# Left2 Frame - Reference Input and Drilling
# Reference Input Section
coord_frame = tk.Frame(left2_frame)
coord_frame.pack(side='top', fill='both', expand=True, pady=10)

coord_title = tk.Label(coord_frame, text="Reference Input", font=("Helvetica", 12, "bold"))
coord_title.pack(side='top', pady=5)

# Frame inside coord_frame for inputs
coord_input_frame = tk.Frame(coord_frame)
coord_input_frame.pack(side='top', pady=5)

# Coordinate inputs for Bregma and Lambda in mm
# Rearranged into two columns with row labels

# Row labels
tk.Label(coord_input_frame, text="").grid(row=0, column=0, padx=5)
tk.Label(coord_input_frame, text="AP").grid(row=1, column=0, padx=5, pady=5)
tk.Label(coord_input_frame, text="ML").grid(row=2, column=0, padx=5, pady=5)
tk.Label(coord_input_frame, text="DV").grid(row=3, column=0, padx=5, pady=5)

# Bregma column
tk.Label(coord_input_frame, text="Bregma").grid(row=0, column=1, padx=5, pady=5)
bregma_ap_entry = tk.Entry(coord_input_frame, width=10)
bregma_ap_entry.insert(0, "10.0")  # Default value
bregma_ap_entry.grid(row=1, column=1, padx=5, pady=5)
bregma_ml_entry = tk.Entry(coord_input_frame, width=10)
bregma_ml_entry.insert(0, "3.0")  # Default value
bregma_ml_entry.grid(row=2, column=1, padx=5, pady=5)
bregma_dv_entry = tk.Entry(coord_input_frame, width=10)
bregma_dv_entry.insert(0, "5.0")  # Default value
bregma_dv_entry.grid(row=3, column=1, padx=5, pady=5)

# Lambda column
tk.Label(coord_input_frame, text="Lambda").grid(row=0, column=2, padx=5, pady=5)
lambda_ap_entry = tk.Entry(coord_input_frame, width=10)
lambda_ap_entry.insert(0, "18.5")  # Default value
lambda_ap_entry.grid(row=1, column=2, padx=5, pady=5)
lambda_ml_entry = tk.Entry(coord_input_frame, width=10)
lambda_ml_entry.insert(0, "3.0")  # Default value
lambda_ml_entry.grid(row=2, column=2, padx=5, pady=5)
lambda_dv_entry = tk.Entry(coord_input_frame, width=10)
lambda_dv_entry.insert(0, "7.0")  # Default value
lambda_dv_entry.grid(row=3, column=2, padx=5, pady=5)

# AP Distance display
tk.Label(coord_input_frame, text="AP Distance:").grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='e')
ap_distance_label = tk.Label(coord_input_frame, text="8.5 mm", font=("Helvetica", 12, "bold"))
ap_distance_label.grid(row=4, column=2, padx=5, pady=5, sticky='w')

# Toggle Grid Button
toggle_grid_button = tk.Button(coord_frame, text="Toggle Grid", command=toggle_grid_overlay)
toggle_grid_button.pack(side='top', pady=5)

# Drilling section
drilling_title = tk.Label(coord_frame, text="Drilling", font=("Helvetica", 12, "bold"))
drilling_title.pack(side='top', pady=5)

drilling_frame = tk.Frame(coord_frame)
drilling_frame.pack(side='top', pady=5)

# Column titles
tk.Label(drilling_frame, text="").grid(row=0, column=0, padx=5, pady=5)
tk.Label(drilling_frame, text="L-Hemisphere").grid(row=0, column=1, padx=5, pady=5)
tk.Label(drilling_frame, text="R-Hemisphere").grid(row=0, column=2, padx=5, pady=5)

# Row labels
tk.Label(drilling_frame, text="AP:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(drilling_frame, text="ML:").grid(row=2, column=0, padx=5, pady=5)
tk.Label(drilling_frame, text="Diameter:").grid(row=3, column=0, padx=5, pady=5)

# Left Hemisphere inputs
drilling_ap_entry_left = tk.Entry(drilling_frame, width=10)
drilling_ap_entry_left.grid(row=1, column=1, padx=5, pady=5)
drilling_ml_entry_left = tk.Entry(drilling_frame, width=10)
drilling_ml_entry_left.grid(row=2, column=1, padx=5, pady=5)
drilling_diameter_entry_left = tk.Entry(drilling_frame, width=10)
drilling_diameter_entry_left.grid(row=3, column=1, padx=5, pady=5)

# Right Hemisphere inputs
drilling_ap_entry_right = tk.Entry(drilling_frame, width=10)
drilling_ap_entry_right.grid(row=1, column=2, padx=5, pady=5)
drilling_ml_entry_right = tk.Entry(drilling_frame, width=10)
drilling_ml_entry_right.grid(row=2, column=2, padx=5, pady=5)
drilling_diameter_entry_right = tk.Entry(drilling_frame, width=10)
drilling_diameter_entry_right.grid(row=3, column=2, padx=5, pady=5)

# Overlay Drilling Buttons
overlay_l_drilling_button = tk.Button(drilling_frame, text="Overlay L-Drilling", command=toggle_l_drilling_overlay)
overlay_l_drilling_button.grid(row=4, column=1, pady=5)

overlay_r_drilling_button = tk.Button(drilling_frame, text="Overlay R-Drilling", command=toggle_r_drilling_overlay)
overlay_r_drilling_button.grid(row=4, column=2, pady=5)

# Electrode Placement Section
entry_frame = tk.Frame(left_column)
entry_frame.pack(side='top', fill='both', expand=True, padx=10, pady=10)

entry_title = tk.Label(entry_frame, text="Electrode Placement", font=("Helvetica", 12, "bold"))
entry_title.pack(side='top', pady=5)

# Entry panel (Scrollable frame for entries)
entry_canvas = tk.Canvas(entry_frame)
entry_scrollbar = tk.Scrollbar(entry_frame, orient="vertical", command=entry_canvas.yview)
entry_canvas.configure(yscrollcommand=entry_scrollbar.set)

entry_scrollbar.pack(side="right", fill="y")
entry_canvas.pack(side="left", fill="both", expand=True)

entry_container = tk.Frame(entry_canvas)
entry_canvas.create_window((0, 0), window=entry_container, anchor="nw")

entry_container.bind("<Configure>", on_frame_configure)

# Add column headers
tk.Label(entry_container, text="Position").grid(row=0, column=0, padx=5, pady=5)
tk.Label(entry_container, text="AP Δ").grid(row=0, column=1, padx=5, pady=5)
tk.Label(entry_container, text="AP").grid(row=0, column=2, padx=5, pady=5)
tk.Label(entry_container, text="ML Δ").grid(row=0, column=3, padx=5, pady=5)
tk.Label(entry_container, text="ML").grid(row=0, column=4, padx=5, pady=5)
tk.Label(entry_container, text="DV Δ").grid(row=0, column=5, padx=5, pady=5)
tk.Label(entry_container, text="DV").grid(row=0, column=6, padx=5, pady=5)
tk.Label(entry_container, text="Success Rating").grid(row=0, column=7, columnspan=4, padx=5, pady=5)
tk.Label(entry_container, text="Comment").grid(row=0, column=11, padx=5, pady=5)
tk.Label(entry_container, text="Delete").grid(row=0, column=12, padx=5, pady=5)

# Add initial entry
add_entry()

add_entry_button = tk.Button(entry_frame, text="Add Entry", command=add_entry)
add_entry_button.pack(pady=5)

# Bind input fields to update overlays and AP Distance on change
for entry in [bregma_ap_entry, bregma_ml_entry, bregma_dv_entry,
              lambda_ap_entry, lambda_ml_entry, lambda_dv_entry,
              drilling_ap_entry_left, drilling_ml_entry_left, drilling_diameter_entry_left,
              drilling_ap_entry_right, drilling_ml_entry_right, drilling_diameter_entry_right,
              roi_ap_entry_min, roi_ap_entry_max, roi_ml_entry_min, roi_ml_entry_max]:
    entry.bind("<FocusOut>", on_input_change)
    entry.bind("<Return>", on_input_change)

# Initial overlay of coordinates and AP Distance
overlay_coordinates()

# Run the application
root.mainloop()
