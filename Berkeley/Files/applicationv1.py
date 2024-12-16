import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tables_params import *
from tables_data import *
from validators import *

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Airport Database")
        self.root.configure(bg='#07917f')
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.curr_columns = []
        self.curr_height = 0
        self.cancelaction = '' # d - delete, e - edit, i - insert
        self.cancelparam = ''
        self.canceltable = ''
        self.cancelid = ''
        self.curr_tabname = ''
        self.curr_ids = []
        self.curref = 0
        self.curr_foreigns = []
        self.curr_rawtable = []
        self.packeting = 0
        self.text_field_p = None
        self.tf = 0
        self.unqerr = 0
        self.valerr = 0

        style = ttk.Style()
        style.map("Treeview",
                  background=[('selected', '#76c7c0')],
                  foreground=[('selected', 'black')])
        
        self.button_frame = tk.Frame(self.root, bg='#07917f')
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.dropdown = ttk.Combobox(self.button_frame, values=['Flights', 'Airlines', 'Airplanes', 'Destinations', 'Passengers', 'Flights-Destinations', 'Flights-Passengers'], width=10)
        self.dropdown.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.dropdown.bind("<<ComboboxSelected>>", lambda event: self.on_table_change(0))
        self.dropdown.set('Flights')

        # Create 5 vertically stacked buttons
        button1 = tk.Button(self.button_frame, text="Select Table", width=25, height=3, command=self.on_table_change)
        button1.pack(pady=5, anchor="n")
        button2 = tk.Button(self.button_frame, text="Create", width=25, height=3, command=self.add_row)
        button2.pack(pady=5, anchor="n")
        button3 = tk.Button(self.button_frame, text="Update", width=25, height=3, command=self.edit_row)
        button3.pack(pady=5, anchor="n")
        button4 = tk.Button(self.button_frame, text="Delete", width=25, height=3, command=self.delete_row)
        button4.pack(pady=5, anchor="n")
        button5 = tk.Button(self.button_frame, text="Select File", width=25, height=3, command=self.load_json_file)
        button5.pack(pady=5, anchor="n")

        self.checkbox_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(self.button_frame, text="Cascade", variable=self.checkbox_var)
        self.checkbox.pack(pady=10)

        # Create Text widgets
        self.text_field_3 = tk.Text(self.button_frame, width=10, height=3)  # Set width and height
        self.text_field_3.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Frame for the table with scrollbars
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=0, column=1, padx=10, pady=(10, 0))
        
        self.scr_frame = tk.Frame(self.root)
        self.scr_frame.grid(row=0, column=1, padx=0, pady=(525, 0))
        
        # Create a canvas to hold the table
        self.canvas = tk.Canvas(self.table_frame, width=606, height=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a canvas to hold the table
        self.scr_canvas = tk.Canvas(self.scr_frame, width=622, height=0)
        self.scr_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(self.scr_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure the canvas to use the scrollbars
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # Create a frame inside the canvas to hold the Treeviews
        self.table_content = tk.Frame(self.canvas)

        # Add the frame to the canvas
        self.canvas.create_window((0, 0), window=self.table_content, anchor='nw')

        self.root.bind('<Tab>', lambda event: self.on_table_change())
        self.root.bind('<Control-d>', lambda event: self.delete_row())
        self.root.bind('<Control-z>', lambda event: self.cancel())
        self.root.bind('<Control-e>', lambda event: self.edit_row())
        self.root.bind('<Control-n>', lambda event: self.add_row())
        self.root.bind('<Control-p>', lambda event: self.toggle_packet_mode())
        self.root.bind('<Control-r>', lambda event: self.run_packet())

        self.text_field_3.config(state=tk.DISABLED)


        self.tree = ttk.Treeview(self.table_content, height = 0, columns=("", ""), show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.on_table_change(None)
    
    def toggle_packet_mode(self):
        if self.packeting == 0:
            self.packeting = 1
        else:
            self.packeting = 0
            self.text_field_p.destroy()
            self.tf = 0
        self.on_table_change(0)

    def load_json_file(self):
        if not self.packeting:
            return
        # Open a file selection dialog to select a JSON file
        file_path = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")])
        
        if file_path:  # Check if a file was selected
            try:
                with open(file_path, 'r') as file:
                    # Load the JSON data
                    data = json.load(file)
                    # Clear the text area before inserting new content
                    self.text_field_p.delete(1.0, tk.END)
                    # Display the JSON contents in the text area
                    self.text_field_p.insert(tk.END, json.dumps(data, indent=4))  # Pretty print JSON
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON file:\n{e}")

    def run_packet(self):
        json_string = self.text_field_p.get(1.0, tk.END)
        err = process_json_data(self.curr_tabname, json_string, self.curr_ids)
        if err:
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "ERROR")
            self.text_field_3.config(state=tk.DISABLED)
        else:
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "SUCCESS")
            self.text_field_3.config(state=tk.DISABLED)

    def show_dialog(self, current_values):
        dialog = tk.Toplevel(self.root)
        dialog.title("Input Values")
        dialog.configure(bg="#76c7c0")
        result = []
        entries = []
        tabdata = getTableParams(self.dropdown.get())
        # print(current_values)
        for index, column_name in enumerate(self.curr_columns):
            label = ttk.Label(dialog, text=column_name + ":")
            label.grid(row=index, column=0, padx=5, pady=5)
            # Check if the current column should be a dropdown
            if index < tabdata[-1] and tabdata[index + 1][3] == 1:
                # Create a combobox for dropdown
                inids, invals = get_records(tabdata[index + 1][4][0])
                fortabdata = getTableParams(tabdata[index + 1][4][0])
                find = 0
                for j in range(fortabdata[-1]):
                    if fortabdata[j + 1][0] == tabdata[index + 1][4][1]:
                        find = j
                listvals = extract_elements(invals, find)
                entry = ttk.Combobox(dialog, values=listvals, state='readonly')
                entry.grid(row=index, column=1, padx=5, pady=5)
                entry.set(current_values[index] if index < len(current_values) else "")
            else:
                # Create entry for text input
                entry = ttk.Entry(dialog)
                entry.grid(row=index, column=1, padx=5, pady=5)
                entry.insert(0, current_values[index] if index < len(current_values) else "")
            entries.append(entry)
        def save():
            result.extend(entry.get() for entry in entries)
            dialog.destroy()
        dialog.bind("<Control-s>", lambda event: save())
        save_button = ttk.Button(dialog, text="Save", command=save)
        save_button.grid(row=len(self.curr_columns), columnspan=2, pady=10)
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        print(result)
        z = 0
        for el in result:
            if z < tabdata[-1] and tabdata[z + 1][3] == 1:
                inids, invals = get_records(tabdata[z + 1][4][0])
                fortabdata = getTableParams(tabdata[z + 1][4][0])
                find = 0
                for j in range(fortabdata[-1]):
                    if fortabdata[j + 1][0] == tabdata[z + 1][4][1]:
                        find = j
                listvals = extract_elements(invals, find)
                b = 0
                for v in listvals:
                    if v == el:
                        result[z] = int(inids[b])
                    b += 1
            z += 1
        print(result)
        for r in range (tabdata[-1]):
            if not tabdata[r + 1][6] == '':
                res = validate(result[r], tabdata[r + 1][6])
                if not res:
                    self.valerr = 1
                    print(result[r])
        for r in range (tabdata[-1]):
            if tabdata[r + 1][7] == 1:
                oids, orecs = get_records(tabdata[0])
                lst = extract_elements(orecs, r)
                for l in lst:
                    if l == result[r] and not l == current_values[r]:
                        self.unqerr = 1
        return tuple(result) if result else None

    def add_row(self):
        new_values = self.show_dialog(("", ""))
        if self.valerr == 1:
            self.valerr = 0
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "VALIDATION ERROR")
            self.text_field_3.config(state=tk.DISABLED)
            return
        if self.unqerr == 1:
            self.unqerr = 0
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "UNIQUE VIOLATION")
            self.text_field_3.config(state=tk.DISABLED)
            return
        if new_values:
            self.curr_height += 1
            fdata = unite_arrays(self.curr_columns, new_values)
            nid = add_new_record(self.curr_tabname, fdata)
            self.cancelaction = 'd'
            self.cancelid = nid
            self.canceltable = self.curr_tabname
            self.on_table_change(0)
            
    def edit_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Choose a record")
            return
        item = selected_item[0]
        current_values = self.tree.item(item, 'values')
        new_values = self.show_dialog(current_values)
        if self.valerr == 1:
            self.valerr = 0
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "VALIDATION ERROR")
            self.text_field_3.config(state=tk.DISABLED)
            return
        if self.unqerr == 1:
            self.unqerr = 0
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "UNIQUE VIOLATION")
            self.text_field_3.config(state=tk.DISABLED)
            return
        if new_values:
            order = int(item[1:]) - 1
            fdata = unite_arrays(self.curr_columns, new_values)
            print(fdata)
            edit_record(self.curr_tabname, fdata, self.curr_ids[order])
            self.cancelaction = 'e'
            self.cancelparam = unite_arrays(self.curr_columns, self.curr_rawtable[order])
            self.cancelid = self.curr_ids[order]
            self.canceltable = self.curr_tabname
            self.on_table_change(0)

    def delete_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Choose a record")
            return
        item = selected_item[0]
        order = int(item[1:]) - 1
        cascading = self.checkbox_var.get()
        tabdata = getTableParams(self.curr_tabname)
        if cascading == 1 and tabdata[-2] == 1:
            selfname = tabdata[0]
            if selfname == 'airlines':
                subdata = getTableParams('Flights')
                subids, subrecs = get_records('flights')
                j = 0
                k = 1
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delete_record('flights', subids[j])
                        subdata1 = getTableParams('Flights-Destinations')
                        subids1, subrecs1 = get_records('flightsdestinations')
                        subdata2 = getTableParams('Flights-Passengers')
                        subids2, subrecs2 = get_records('flightspassengers')
                        j1 = 0
                        k1 = 0
                        j2 = 0
                        k2 = 0
                        for ent in subrecs1:
                            if str(ent[k1]) == str(subids[j]):
                                delete_record('flightsdestinations', subids1[j1])
                            j1 += 1
                        for ent in subrecs2:
                            if str(ent[k2]) == str(subids[j]):
                                delete_record('flightspassengers', subids2[j2])
                            j2 += 1
                    j += 1
            if selfname == 'airplanes':
                subdata = getTableParams('Flights')
                subids, subrecs = get_records('flights')
                j = 0
                k = 2
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delete_record('flights', subids[j])
                        subdata1 = getTableParams('Flights-Destinations')
                        subids1, subrecs1 = get_records('flightsdestinations')
                        subdata2 = getTableParams('Flights-Passengers')
                        subids2, subrecs2 = get_records('flightspassengers')
                        j1 = 0
                        k1 = 0
                        j2 = 0
                        k2 = 0
                        for ent in subrecs1:
                            if str(ent[k1]) == str(subids[j]):
                                delete_record('flightsdestinations', subids1[j1])
                            j1 += 1
                        for ent in subrecs2:
                            if str(ent[k2]) == str(subids[j]):
                                delete_record('flightspassengers', subids2[j2])
                            j2 += 1
                    j += 1
            if selfname == 'destinations':
                subdata = getTableParams('Flights-Destinations')
                subids, subrecs = get_records('flightsdestinations')
                j = 0
                k = 1
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delete_record('flightsdestinations', subids[j])
                    j += 1
            if selfname == 'passengers':
                subdata = getTableParams('Flights-Passengers')
                subids, subrecs = get_records('flightspassengers')
                j = 0
                k = 1
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delete_record('flightspassengers', subids[j])
                    j += 1
            if selfname =='flights':
                subdata1 = getTableParams('Flights-Destinations')
                subids1, subrecs1 = get_records('flightsdestinations')
                subdata2 = getTableParams('Flights-Passengers')
                subids2, subrecs2 = get_records('flightspassengers')
                j1 = 0
                k1 = 0
                j2 = 0
                k2 = 0
                for ent in subrecs1:
                    if str(ent[k1]) == str(self.curr_ids[order]):
                        delete_record('flightsdestinations', subids1[j1])
                    j1 += 1
                for ent in subrecs2:
                    if str(ent[k2]) == str(self.curr_ids[order]):
                        delete_record('flightspassengers', subids2[j2])
                    j2 += 1
        delerr = 0
        if cascading == 0 and tabdata[-2] == 1:
            selfname = tabdata[0]
            if selfname == 'airlines':
                subdata = getTableParams('Flights')
                subids, subrecs = get_records('flights')
                j = 0
                k = 1
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delerr = 1
                    j += 1
            if selfname == 'airplanes':
                subdata = getTableParams('Flights')
                subids, subrecs = get_records('flights')
                j = 0
                k = 2
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delerr = 1
                    j += 1
            if selfname == 'destinations':
                subdata = getTableParams('Flights-Destinations')
                subids, subrecs = get_records('flightsdestinations')
                j = 0
                k = 1
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delerr = 1
                    j += 1
            if selfname == 'passengers':
                subdata = getTableParams('Flights-Passengers')
                subids, subrecs = get_records('flightspassengers')
                j = 0
                k = 1
                for ent in subrecs:
                    if str(ent[k]) == str(self.curr_ids[order]):
                        delerr = 1
                    j += 1
            if selfname =='flights':
                subdata1 = getTableParams('Flights-Destinations')
                subids1, subrecs1 = get_records('flightsdestinations')
                subdata2 = getTableParams('Flights-Passengers')
                subids2, subrecs2 = get_records('flightspassengers')
                j1 = 0
                k1 = 0
                j2 = 0
                k2 = 0
                for ent in subrecs1:
                    if str(ent[k1]) == str(self.curr_ids[order]):
                        delerr = 1
                    j1 += 1
                for ent in subrecs2:
                    if str(ent[k2]) == str(self.curr_ids[order]):
                        delerr = 1
                    j2 += 1
        if delerr == 1:
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "CANNOT DELETE")
            self.text_field_3.config(state=tk.DISABLED)
            return
        for item in selected_item:
            current_values = self.tree.item(item, 'values')
            order = int(item[1:]) - 1
            self.curr_height -= 1
            delete_record(self.curr_tabname, self.curr_ids[order])
            self.cancelaction = 'i'
            self.cancelparam = unite_arrays(self.curr_columns, self.curr_rawtable[order])
            self.canceltable = self.curr_tabname
            self.cancelid = self.curr_ids[order]
            self.on_table_change(0)

    def on_closing(self):
        try:
            print("Closing")
        except Exception:
            pass
        root.destroy() 

    def on_table_change(self, tabtoggle = 1):
        if tabtoggle == 1:
            old_value = self.dropdown.get()
            if old_value == 'Flights':
                self.dropdown.set('Airlines')
            elif old_value == 'Airlines':
                self.dropdown.set('Airplanes') 
            elif old_value == 'Airplanes':
                self.dropdown.set('Destinations') 
            elif old_value == 'Destinations':
                self.dropdown.set('Passengers') 
            elif old_value == 'Passengers':
                self.dropdown.set('Flights-Destinations') 
            elif old_value == 'Flights-Destinations':
                self.dropdown.set('Flights-Passengers') 
            elif old_value == 'Flights-Passengers':
                self.dropdown.set('Flights') 
            else:
                self.dropdown.set('Flights')
        new_value = self.dropdown.get()
        print(f"Selected table: {new_value}")
        tabdata = getTableParams(new_value)
        tablen = tabdata[-1]
        tabname = tabdata[0]
        self.curref = tabdata[-2]
        self.curr_tabname = tabname
        tabrecslen = get_len_mod_name(tabname)
        tabids, tabrecs = get_records(tabname)
        self.curr_height = tabrecslen
        self.curr_ids = tabids
        newcols = []
        for i in range (tablen):
            newcols.append(tabdata[i + 1][0])
        self.curr_columns = newcols
        self.tree.destroy()
        if self.packeting == 1 and not self.tf:
            self.text_field_p = tk.Text(self.table_content, height=25, width=70)
            self.text_field_p.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.table_content.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.tf = 1
            return
        if self.packeting:
            return
        self.tree = ttk.Treeview(self.table_content, height=tabrecslen, columns=self.curr_columns, show="headings")
        for column in self.curr_columns:
            self.tree.heading(column, text=column)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        listvals = []
        x = 0
        self.curr_rawtable = []
        for rec in tabrecs:
            self.curr_rawtable.append(rec)
        # tabrecs = sorted(tabrecs, key=lambda x: x[0])
        for rec in tabrecs:
            # print(rec)
            y = 0
            for col in rec:
                if y < tabdata[-1] and tabdata[y + 1][3] == 1:
                    inids, invals = get_records(tabdata[y + 1][4][0])
                    fortabdata = getTableParams(tabdata[y + 1][4][0])
                    find = 0
                    for j in range(fortabdata[-1]):
                        if fortabdata[j + 1][0] == tabdata[y + 1][4][1]:
                            # print(fortabdata[j + 1][0], tabdata[y + 1][4][1])
                            find = j
                    listvals = extract_elements(invals, find)
                    temp_list = list(rec)
                    a = 0
                    for el in inids:
                        # print('...')
                        # print(el, col)
                        # print('...')
                        if str(el) == str(col):
                            # print(el, col)
                            x = a
                        a += 1
                    # print(inids)
                    # print(temp_list, y, listvals, x)
                    # print('--------------------')
                    temp_list[y] = listvals[x]
                    rec = tuple(temp_list)
                y += 1
            self.tree.insert("", "end", values=rec)
        self.table_content.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def cancel(self):
        if self.cancelaction == 'd':
            delete_record(self.canceltable, self.cancelid)
            self.cancelaction = ''
            self.on_table_change(0)
        elif self.cancelaction == 'e':
            edit_record(self.canceltable, self.cancelparam, self.cancelid)
            self.cancelaction = ''
            self.on_table_change(0)
        elif self.cancelaction == 'i':
            add_new_record(self.canceltable, self.cancelparam, self.cancelid)
            self.cancelaction = ''
            self.on_table_change(0)
        else:
            self.text_field_3.config(state=tk.NORMAL)
            self.text_field_3.delete(1.0, tk.END)
            self.text_field_3.insert(tk.END, "NOTHING TO CANCEL")
            self.text_field_3.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
