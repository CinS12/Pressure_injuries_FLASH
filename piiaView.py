"""Data representation and user interaction
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

View represents the visualization of the data.
"""

import tkinter as tk
from tkinter import ttk
#pip install pypubsub
import cv2
from PIL import ImageTk, Image
from pubsub import pub
from tkcalendar import DateEntry
from pathlib import Path
from text_CAT import *

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)

class View:
    """
    Class made up of all the functions that directly interact with the user.
    It receives requests and data from Model through the Controller.

    ...

    Methods
    -------
    setup()
        Calls the functions to create and show the main window.
    crear_finestres()
        Calls the functions to create the GUI of the 3 main pages.
    crear_menu()
        Creates and configures the top menu bar widget.
    crear_page_0()
        Creates the frame and main labels of page_0's UI (Main Menu).
    crear_page_1()
        Creates the frame and main labels of page_1's UI (Process images).
    crear_page_2()
        Creates the frame and main labels of page_2's UI (View images).
    inserir_finestres()
        Places the main frames and labels of the 3 pages at the window.
    apretar_boto_1()
        Shows page_1 UI (Process images).
    apretar_boto_2()
        Shows page_2 UI (View images).
    apretar_boto_3()
        Sends a request to check and storage the metadata and processed image.
    botoImg()
        Places the button to process image.
    processar_img()
        Sends a request to the Controller to start image processing.
    carregar_imatge()
        Sends a request to Controller to load an image.
    update_image(img_tk)
        Sends a request to Controller to update the image label.
    ask_mask_confirmation(img_cv2_mask, scale_percent)
        Displays a popup window to ask user confirmation about cropped mask.
    ask_roi_confirmation(img_cv2_mask, img_cv2_roi, tissue, scale_percent)
        Displays a popup window to ask user confirmation about cropped roi
        comparing it with the image mask.
    roi_ok(img_cv2_roi, tissue)
        Closes the popup window and sends a request with the roi and tissue's type.
    segmentacio_ko()
        Closes the cv2 and popup window.
    segmentacio_ok(img_imgtk_mask, img_cv2_mask)
        Closes the popup window and sends a request with the image(mask) and roi.
    segmentation_gui(img_imgtk_mask, img_cv2_mask)
        Creates a GUI for the image segmentation and processing.
    update_perimeter_count()
        Updates the perimeter selection label as selected.
    update_granulation_count(number)
        Update the granulation tissue's label with the number of rois selected.
    update_necrosis_count(number)
        Update the necrosis tissue's label with the number of rois selected.
    update_slough_count(number)
        Update the slough tissue's label with the number of rois selected.
    ask_perimeter()
        Sends a request to the Controller for perimeter's roi selection.
    roi_granulation()
        Sends a request to the Controller for granulation's roi selection.
    roi_necrosis()
        Sends a request to the Controller for necrosis's roi selection.
    roi_slough()
        Sends a request to the Controller for slough's roi selection.
    flash_reduction(img_cv2_mask)
        Sends a request to the Controller for flash reduction.
    crear_dades_p1()
        Creates and places all metadata fields's widgets and button 3 (save data).
    cultiu_si()
        Updates the value of "cultiu" to Yes.
    cultiu_no()
        Updates the value of "cultiu" to No.
    ask_time()
        Places the widgets of contention's time field.
    no_time()
        Hides the widgets of contention's time field.
    entry_popup_tr_ant(title)
        Display a popup for antibiotics treatment's comments.
    entry_popup_tr_top(title)
        Display a popup for topical treatment's comments.
    popup_barthel(title)
        Display a popup for barthel scale's value calculation.
    popup_emina(title)
        Display a popup for emina scale's value calculation.
    p1_tr_top_ok()
        Saves the topical treatment's comments to an attribute and closes popup.
    p1_tr_ant_ok()
        Saves the antibiotics treatment's comments to an attribute and closes popup.
    barthel_getData()
        Saves the barthel sacle answers to an attribute,
        sends a request with this data and closes popup.
    emina_getData()
        Saves the emina sacle answers to an attribute,
        sends a request with this data and closes popup.
    popupmsg(msg)
        Displays a popup window with the message.
        Useful for warnings.
    update_barthel(data)
        Updates barthel's Scale widget with the calculated value.
    update_emina(data)
        Updates emina's Scale widget with the calculated value.
    show_error(data_error)
        Calls the popup function to display the errors found.
    ask_flash_confirmation(img_cv2_mask, img_flash_reduced)
        Displays a popup window to ask user confirmation about the flash reduction result.
    flash_ok(img_cv2_roi)
        Sends a request to Controller with the image's flash reduction result.
        Closes popup window.
    flash_ko()
        Closes popup and all cv2 windows.
    update_flash_label(img_cv2_flash)
        Updates the image's label of GUI processing with the flash reduced one.
    img_processed_accepted()
        Sends the request that image has been processed.
    reset_view()
        Resets image label (after processing process).
    update_data_n_elements(num)
        Updates the label_info of page 2
        with the number of elements found in the storage directory.
    update_list(num)
        Displays all found elements on the list.
        Creates the "double click" event to select an element.
    select_element(event)
        Sends the request with the id of list's selected element.
    crear_elements_p2()
        Creates and places the main frames and labels of page 2 (View images).
    assemble_img_frame()
        Creates and places the label_img of page 2 (View images).
    load_image_i(image_tk)
        Loads the image to the label_img of page 2 (View images).
    load_metadata_i(metadata)
        Loads the metadata to the metadata labels of page 2 (View images).
    """

    def __init__(self, parent):
        self.container = parent
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        return

    def setup(self):
        """
        Calls the functions to create and show the main window.
        """

        self.crear_finestres()
        self.crear_menu()
        self.inserir_finestres()

    def crear_finestres(self):
        """
        Calls the functions to create the GUI of the 3 main pages.
        """

        self.crear_page_0()
        self.crear_page_1()
        self.crear_page_2()


    def crear_menu(self):
        """
        Creates and configures the top menu bar widget.
        """

        self.menubar = tk.Menu(self.container)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Save settings", command=lambda: self.popupmsg("Pàgina en construcció!"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        language_menu = tk.Menu(self.menubar, tearoff=0)
        language_menu.add_command(label="Català", command=lambda: self.popupmsg("Pàgina en construcció!"))
        language_menu.add_command(label="Castellano", command=lambda: self.popupmsg("Página en construcción!"))
        language_menu.add_command(label="English", command=lambda: self.popupmsg("Page is still building!"))
        self.menubar.add_cascade(label="Language", menu=language_menu)
        self.container.config(menu=self.menubar)

    def crear_page_0(self):
        """
        Creates the frame and main labels of page_0's UI (Main Menu).
        """

        self.page_0 = tk.Frame(self.container)
        self.p0_label_0 = ttk.Label(self.page_0, text="Pressure Injuries Image Analysis", font=FONT_BENVINGUDA)
        self.p0_button_1 = ttk.Button(self.page_0, text="Processar imatges", command=self.apretar_boto_1)
        self.p0_button_2 = ttk.Button(self.page_0, text="Visualitzar imatges", command=self.apretar_boto_2)

    def crear_page_1(self):
        """
        Creates the frame and main labels of page_1's UI (Process images).
        """

        self.page_1 = tk.Frame(self.container)
        self.p1_label_1 = ttk.Label(self.page_1, text="Processar imatges", font=FONT_BENVINGUDA)
        self.p1_button_1 = ttk.Button(self.page_1, text="Carrega imatge", command=self.carregar_imatge)
        self.p1_button_2 = ttk.Button(self.page_1, text="Enrere", command=lambda:self.page_0.tkraise())
        self.p1_button_img = ttk.Button(self.page_1, text="Processar imatge", command=lambda:self.processar_img())
        path = Path(__file__).parent / "resources/load_img.png"
        img = ImageTk.PhotoImage(Image.open(path))
        self.p1_img_label = tk.Label(self.page_1, image=img)
        self.p1_img_label.image = img
        self.crear_dades_p1()

    def crear_page_2(self):
        """
        Creates the frame and main labels of page_2's UI (View images).
        """

        self.page_2 = tk.Frame(self.container)
        self.p2_label_2 = ttk.Label(self.page_2, text="Visualitzar imatges", font=FONT_BENVINGUDA)
        self.p2_button_1 = ttk.Button(self.page_2, text="Enrere", command=lambda:self.page_0.tkraise())
        self.crear_elements_p2()

    def inserir_finestres(self):
        """
        Places the main frames and labels of the 3 pages at the window.
        """

        self.page_0.grid(row=0,column=0, sticky="NESW")
        self.p0_label_0.pack(pady=20)
        self.p0_button_1.pack()
        self.p0_button_2.pack()

        self.page_1.grid(row=0,column=0,sticky="NESW")
        self.p1_label_1.grid(row=0, column=2, pady=20, padx=1)
        self.p1_button_1.grid(row=1, column=1, pady=0, padx=20, sticky="SW")
        self.p1_img_label.grid(row=2, column=1, pady=0, padx=20, sticky="N")
        self.p1_data_frame.grid(row=2, column=3, pady=5, padx=1, sticky="n")
        self.p1_button_2.grid(row=2, column=1, pady=20, padx=20, sticky="w")
        self.p1_label_2.grid(row=1, column=1, padx=5, pady=10, sticky="n")
        self.p1_data_camps.grid(row=2, column=1, pady=20, padx=10)
        self.p1_button_3.grid(row=3, column=1, pady=10, padx=10, sticky="e")

        self.page_2.grid(row=0,column=0,sticky="NESW")
        self.p2_label_2.pack(pady=20)
        self.p2_button_1.pack(pady=0)
        self.p2_frame_list.pack(pady=20)
        self.p2_frame_elements.pack(pady=20)
        self.p2_frame_img.grid(row=1, column=1, pady=20, padx=20, sticky="w")
        self.p2_frame_metadata.grid(row=1, column=2, pady=20, padx=20, sticky="w")

        self.page_0.tkraise()

    def apretar_boto_1(self):
        """
        Shows page_1 UI (Process images).
        """

        pub.sendMessage("BUTTON_1_PRESSED")
        self.page_1.tkraise()

    def apretar_boto_2(self):
        """
        Shows page_2 UI (View images).
        """

        pub.sendMessage("BUTTON_2_PRESSED")
        self.page_2.tkraise()

    def apretar_boto_3(self):
        """
        Sends a request to check and storage the metadata and processed image.
        """

        print("view -   Botó 3!")
        data = [self.code_entry, self.age_pers_entry, self.gender_combobox, self.temps_imm_entry,
                self.temps_imm_combobox, self.temps_hosp_entry, self.temps_hosp_combobox, self.temps_inst_entry,
                self.temps_inst_combobox, self.cal_data_entry, self.emina_scale, self.barthel_scale,
                self.contencio, self.temps_conten_entry, self.temps_conten_combobox, self.grade_combobox, self.cultiu,
                self.protein_entry, self.albumina_entry, self.popup_tr_ant, self.popup_tr_top]
        pub.sendMessage("BUTTON_3_PRESSED", data=data)

    def botoImg(self):
        """
        Places the button to process image.
        """

        self.p1_button_img.grid(row=1, column=1, pady=0, padx=20, sticky="SE")

    def processar_img(self):
        """
        Sends a request to the Controller to start image processing.
        """
        pub.sendMessage("ANALYSE_IMAGE")

    def carregar_imatge(self):
        """
        Sends a request to Controller to load an image.
        """

        pub.sendMessage("LOAD_IMAGE")

    def update_image(self, img_tk):
        """
        Sends a request to Controller to update the image label.

        Parameters
        ----------
        image_tk : PIL Image
           image ready to be loaded in a label
        """

        self.p1_img_label.configure(image=img_tk)
        self.p1_img_label.image = img_tk
        return

    def ask_mask_confirmation(self, img_cv2_mask, scale_percent):
        """
        Displays a popup window to ask user confirmation about cropped mask.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image that requires user confirmation
        scale_percent : int
           image resize value (default = 100)
        """

        cv2.destroyAllWindows()
        #Crear la finestra
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 1000
        h = 1100
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Confirmar regió")
        #Definir títol del popup
        title = ttk.Label(self.popup, text="És correcte la regió seleccionada?", font=FONT_TITOL)
        title.configure(anchor="center")
        title.pack(side="top", fill="x", pady=10)
        #Carregar la roi
        im_rgb = cv2.cvtColor(img_cv2_mask, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im_rgb)
        #Escalar la imatge
        width = int(img_cv2_mask.shape[1] * scale_percent / 100)
        height = int(img_cv2_mask.shape[0] * scale_percent / 100)
        dim = (width, height)
        im = im.resize((width, height))
        #resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
        img_imgtk_mask = ImageTk.PhotoImage(image=im)
        self.confirmation_img = tk.Label(self.popup, image=img_imgtk_mask)
        self.confirmation_img.pack(pady=30)
        #Botons GUI
        button1 = ttk.Button(self.popup, text="Sí", command=lambda:self.segmentacio_ok(img_imgtk_mask, img_cv2_mask))
        button2 = ttk.Button(self.popup, text="No", command=self.segmentacio_ko)
        button1.pack()
        button2.pack()
        self.popup.mainloop()

    def ask_roi_confirmation(self, img_cv2_mask, img_cv2_roi, tissue, scale_percent):
        """
        Displays a popup window to ask user confirmation about cropped roi
        comparing it with the image mask.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image before cropping roi
        img_cv2_roi : image cv2
           image that requires user confirmation
        tissue : String
            tissue of the roi
        scale_percent : int
           image resize value (default = 100)
        """

        cv2.destroyAllWindows()
        #Crear la finestra
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 1920
        h = 1080
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Confirmar regió")
        #Definir títol del popup
        title = ttk.Label(self.popup, text="És correcte la regió seleccionada?", font=FONT_TITOL)
        title.configure(anchor="center")
        title.pack(side="top", fill="x", pady=10)
        #Carregar la roi i la imatge
        im_rgb = cv2.cvtColor(img_cv2_mask, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im_rgb)
        roi_rgb = cv2.cvtColor(img_cv2_roi, cv2.COLOR_BGR2RGB)
        roi = Image.fromarray(roi_rgb)
        #Escalar la imatge
        width = int(img_cv2_mask.shape[1] * scale_percent / 100)
        height = int(img_cv2_mask.shape[0] * scale_percent / 100)
        im = im.resize((width, height))
        images_frame = ttk.Frame(self.popup)
        imgtk = ImageTk.PhotoImage(image=im)
        roitk = ImageTk.PhotoImage(image=roi)
        img_label = tk.Label(images_frame, image=imgtk)
        roi_label = tk.Label(images_frame, image=roitk)
        img_label.grid(row=1, column=1, padx=5, pady=5)
        roi_label.grid(row=1, column=2, padx=5, pady=5)
        images_frame.pack(pady=30)
        #Botons GUI
        button1 = ttk.Button(self.popup, text="Sí", command=lambda:self.roi_ok(roi_rgb, tissue))
        button2 = ttk.Button(self.popup, text="No", command=self.segmentacio_ko)
        button1.pack()
        button2.pack()
        self.popup.mainloop()

    def roi_ok(self, img_cv2_roi, tissue):
        """
        Closes the popup window and sends a request with the roi and tissue's type.

        Parameters
        ----------
        img_cv2_roi : image cv2
           roi selected by the user
        tissue : String
            tissue of the roi
        """

        self.popup.destroy()
        pub.sendMessage("ROI_CONFIRMATED", img_cv2_roi=img_cv2_roi, tissue=tissue)

    def segmentacio_ko(self):
        """
        Closes the cv2 and popup window.
        """

        cv2.destroyAllWindows()
        self.popup.destroy()

    def segmentacio_ok(self, img_imgtk_mask, img_cv2_mask):
        """
        Closes the popup window and sends a request with the image(mask) and roi.

        Parameters
        ----------
        img_imgtk_mask : PIL Image
           image before cropping roi
        img_cv2_mask : image cv2
           image that requires user confirmation
        """

        self.popup.destroy()
        pub.sendMessage("PRE_SEGMENTATION_CONFIRMATED", img_imgtk_mask=img_imgtk_mask, img_cv2_mask=img_cv2_mask)

    def segmentation_gui(self, img_imgtk_mask, img_cv2_mask):
        """
        Creates a GUI for the image segmentation and processing.

        Parameters
        ----------
        img_imgtk_mask : PIL Image
           image before cropping roi
        img_cv2_mask : image cv2
           image that requires user confirmation
        """

        # Crear la finestra
        self.popup_img = tk.Toplevel()
        ws = self.popup_img.winfo_screenwidth()
        hs = self.popup_img.winfo_screenheight()
        w = 1000
        h = 1100
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup_img.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup_img.wm_title("Eina de segmentació")
        # Definir títol del popup
        title = ttk.Label(self.popup_img, text="Selecciona el perímetre total i els diferents tipus de teixits de la ferida:", font=FONT_TITOL)
        title.configure(anchor="center")
        #Frame per les dades
        flash_frame = ttk.Frame(self.popup_img, borderwidth=2, relief="groove")
        data_frame = ttk.Frame(self.popup_img)
        accept_frame = ttk.Frame(self.popup_img)
        # Botons GUI
        button_flash = ttk.Button(flash_frame, text="Flash Reduction",command=lambda:self.flash_reduction(img_cv2_mask))
        button_perimeter = ttk.Button(data_frame, text="Perimeter",command=self.ask_perimeter)
        button_granulation = ttk.Button(data_frame, text="Granulation", command=self.roi_granulation)
        button_necrosis = ttk.Button(data_frame, text="Necrosis", command=self.roi_necrosis)
        button_slough = ttk.Button(data_frame, text="Slough", command=self.roi_slough)
        button_accept = ttk.Button(accept_frame, text="Accept", command=self.img_processed_accepted)
        #Labels de la GUI
        self.label_flash = tk.Label(flash_frame, text="Eina en desenvolupament, requereix supervisió.", fg="black", font=FONT_MSG)
        self.label_perimeter = tk.Label(data_frame, text="Selecciona el perímetre total de la ferida", fg="black", font=FONT_MSG)
        self.label_granulation = ttk.Label(data_frame, text="Zones seleccionades: 0", font=FONT_MSG)
        self.label_necrosis = ttk.Label(data_frame, text="Zones seleccionades: 0", font=FONT_MSG)
        self.label_slough = ttk.Label(data_frame, text="Zones seleccionades: 0", font=FONT_MSG)
        # Carregar la roi
        self.img_show = tk.Label(self.popup_img, image=img_imgtk_mask)

        #Col·locar els elements
        button_flash.grid(row=1, column=1, padx=5, pady=5)
        self.label_flash.grid(row=1, column=2, padx=5, pady=5)
        button_perimeter.grid(row=2, column=1, padx=5, pady=5)
        self.label_perimeter.grid(row=2, column=2, padx=5, pady=5)
        button_granulation.grid(row=3, column=1, padx=5, pady=5)
        self.label_granulation.grid(row=3, column=2, padx=5, pady=5)
        button_necrosis.grid(row=4, column=1, padx=5, pady=5)
        self.label_necrosis.grid(row=4, column=2, padx=5, pady=5)
        button_slough.grid(row=5, column=1, padx=5, pady=5)
        self.label_slough.grid(row=5, column=2, padx=5, pady=5)
        button_accept.pack()

        title.pack(pady=10)
        flash_frame.pack(pady=5, padx=5)
        data_frame.pack(pady=5, padx=5)
        self.img_show.pack(pady=10)
        accept_frame.pack(pady=10, padx=10)

        self.popup_img.mainloop()

    def update_perimeter_count(self):
        """
        Updates the perimeter selection label as selected.
        """

        self.label_perimeter["text"] = "Perímetre seleccionat"
        self.label_perimeter["fg"] = "green"

    def update_granulation_count(self, number):
        """
        Update the granulation tissue's label with the number of rois selected.

        Parameters
        ----------
        number : int
           number of granulation rois already selected
        """

        self.label_granulation["text"] = "Zones seleccionades: " + str(number)

    def update_necrosis_count(self, number):
        """
        Update the necrosis tissue's label with the number of rois selected.

        Parameters
        ----------
        number : int
           number of necrosis rois already selected
        """

        self.label_necrosis["text"] = "Zones seleccionades: " + str(number)

    def update_slough_count(self, number):
        """
        Update the slough tissue's label with the number of rois selected.

        Parameters
        ----------
        number : int
           number of slough rois already selected
        """
        self.label_slough["text"] = "Zones seleccionades: " + str(number)

    def ask_perimeter(self):
        """
        Sends a request to the Controller for perimeter's roi selection.

        """
        pub.sendMessage("ASK_PERIMETER")

    def roi_granulation(self):
        """
        Sends a request to the Controller for granulation's roi selection.

        """
        pub.sendMessage("ROI_GRANULATION")

    def roi_necrosis(self):
        """
        Sends a request to the Controller for necrosis's roi selection.

        """
        pub.sendMessage("ROI_NECROSIS")

    def roi_slough(self):
        """
        Sends a request to the Controller for slough's roi selection.

        """

        pub.sendMessage("ROI_SLOUGH")

    def flash_reduction(self, img_cv2_mask):
        """
        Sends a request to the Controller for flash reduction.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected by user to reduce its flash
        """

        pub.sendMessage("FLASH_REDUCTION", img_cv2_mask=img_cv2_mask)

    def crear_dades_p1(self):
        """
        Creates and places all metadata fields's widgets and button 3 (save data).

        """

        self.popup_tr_ant = []
        self.popup_tr_top = []
        self.p1_data_frame = tk.Frame(self.page_1, borderwidth=2, relief="groove")
        self.p1_label_2 = ttk.Label(self.p1_data_frame, text="Recull de dades", font=FONT_BENVINGUDA)

        self.p1_data_camps = ttk.Frame(self.p1_data_frame, borderwidth=2, relief="groove")
        self.p1_data_label = ttk.Label(self.p1_data_camps, text="Omplir els camps següents:", font=FONT_TITOL)
        self.p1_data_label.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        #Codi
        code_label = ttk.Label(self.p1_data_camps, text="Codi", font=FONT_MSG)
        code_label.grid(row=2, column=1, padx=0, pady=10)
        self.code_entry = ttk.Entry(self.p1_data_camps)
        self.code_entry.insert(tk.END, '')
        self.code_entry.grid(row=2, column=2, padx=0, pady=10)
        #Edat
        age_label = ttk.Label(self.p1_data_camps, text="Any naixement", font=FONT_MSG)
        age_label.grid(row=3, column=1, padx=0, pady=10)
        self.age_pers_entry = ttk.Entry(self.p1_data_camps)
        self.age_pers_entry.insert(tk.END, '')
        self.age_pers_entry.grid(row=3, column=2, padx=0, pady=10)
        #Sexe
        gender_pers_label = ttk.Label(self.p1_data_camps, text="Sexe", font=FONT_MSG)
        gender_pers_label.grid(row=4, column=1, padx=5, pady=10)
        self.gender_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=17, justify="left")
        self.gender_combobox["values"] = ["Home", "Dona", "Altre"]
        self.gender_combobox.grid(row=4, column=2, padx=5, pady=10)
        #Temps immobilització
        temps_imm = ttk.Label(self.p1_data_camps, text="Temps d'immobilització", font=FONT_MSG)
        temps_imm.grid(row=6, column=1, padx=0, pady=10)
        self.temps_imm_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_imm_entry.insert(tk.END, '')
        self.temps_imm_entry.grid(row=6, column=2, padx=0, pady=10, sticky="w")
        self.temps_imm_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_imm_combobox["values"] = ["Dies", "Setmanes", "Mesos"]
        self.temps_imm_combobox.current(0)
        self.temps_imm_combobox.grid(row=6, column=2, padx=5, pady=10, sticky="e")
        #Temps hospitalització
        temps_hosp = ttk.Label(self.p1_data_camps, text="Temps hospitalització", font=FONT_MSG)
        temps_hosp.grid(row=7, column=1, padx=0, pady=10)
        self.temps_hosp_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_hosp_entry.insert(tk.END, '')
        self.temps_hosp_entry.grid(row=7, column=2, padx=0, pady=10, sticky="w")
        self.temps_hosp_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_hosp_combobox["values"] = ["Dies", "Setmanes", "Mesos"]
        self.temps_hosp_combobox.current(0)
        self.temps_hosp_combobox.grid(row=7, column=2, padx=5, pady=10, sticky="e")
        # Temps institucionalització
        temps_inst = ttk.Label(self.p1_data_camps, text="Temps institucionalització", font=FONT_MSG)
        temps_inst.grid(row=8, column=1, padx=0, pady=10)
        self.temps_inst_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_inst_entry.insert(tk.END, '')
        self.temps_inst_entry.grid(row=8, column=2, padx=0, pady=10, sticky="w")
        self.temps_inst_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_inst_combobox["values"] = ["Dies", "Setmanes", "Mesos"]
        self.temps_inst_combobox.current(0)
        self.temps_inst_combobox.grid(row=8, column=2, padx=5, pady=10, sticky="e")
        #Data
        date_label = ttk.Label(self.p1_data_camps, text="Data", font=FONT_MSG)
        date_label.grid(row=9, column=1, padx=5, pady=10)
        self.cal_data_entry = DateEntry(self.p1_data_camps, dateformat=3, width=12, background='darkblue',
                        foreground='white', borderwidth=4)
        self.cal_data_entry.grid(row=9, column=2, sticky='nsew')
        # Escala EMINA
        emina_label = ttk.Label(self.p1_data_camps, text="Escala EMINA", font=FONT_MSG)
        emina_label.grid(row=10, column=1, padx=0, pady=10)
        self.emina_scale = tk.Scale(self.p1_data_camps, from_=0, to=15, resolution=1, orient=tk.HORIZONTAL)
        self.emina_scale.grid(row=10, column=2, padx=0, pady=10)
        barthel_button = ttk.Button(self.p1_data_camps, text="Calcular",
                                    command=lambda: self.popup_emina("Escala EMINA"))
        barthel_button.grid(row=10, column=3, pady=10, padx=0)
        #Escala Barthel
        barthel_label = ttk.Label(self.p1_data_camps, text="Escala Barthel", font=FONT_MSG)
        barthel_label.grid(row=11, column=1, padx=0, pady=10)
        self.barthel_scale = tk.Scale(self.p1_data_camps, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL)
        self.barthel_scale.grid(row=11, column=2, padx=0, pady=10)
        barthel_button = ttk.Button(self.p1_data_camps, text="Calcular",
                                    command=lambda: self.popup_barthel("Escala Barthel"))
        barthel_button.grid(row=11, column=3, pady=10, padx=0)
        #Contenció mecànica
        self.contencio=""
        conten_label = ttk.Label(self.p1_data_camps, text="Contenció Mecànica", font=FONT_MSG)
        conten_label.grid(row=12, column=1, padx=0, pady=10)
        self.conten_radiobutton_si = ttk.Radiobutton(self.p1_data_camps, variable="conten", text="Sí", value="si", command=self.ask_time)
        self.conten_radiobutton_no = ttk.Radiobutton(self.p1_data_camps, variable="conten", text="No", value="no", command=self.no_time)
        self.conten_radiobutton_si.grid(row=12, column=2, padx=0, pady=10, sticky="w")
        self.conten_radiobutton_no.grid(row=13, column=2, padx=0, pady=10, sticky="w")
        self.temps_conten_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_conten_entry.insert(tk.END, '')
        self.temps_conten_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_conten_combobox["values"] = ["Dies", "Setmanes", "Mesos"]
        self.temps_conten_combobox.current(0)
        #Grau de la nafra
        grade_label = ttk.Label(self.p1_data_camps, text="Grau de la nafra", font=FONT_MSG)
        grade_label.grid(row=14, column=1, padx=0, pady=10)
        self.grade_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.grade_combobox["values"] = [1, 2, 3, 4]
        self.grade_combobox.grid(row=14, column=2, padx=5, pady=10, sticky="w")
        #Cultiu de l’exsudat
        self.cultiu=""
        cultiu_label = ttk.Label(self.p1_data_camps, text="Cultiu de l'exsudat", font=FONT_MSG)
        cultiu_label.grid(row=15, column=1, padx=0, pady=10)
        self.cultiu_radiobutton_positive = ttk.Radiobutton(self.p1_data_camps, variable="cultiu", text="Positiu", value="positive", command=self.cultiu_si)
        self.cultiu_radiobutton_negative = ttk.Radiobutton(self.p1_data_camps, variable="cultiu", text="Negatiu", value="negative", command=self.cultiu_no)
        self.cultiu_radiobutton_positive.grid(row=15, column=2, padx=0, pady=10, sticky="w")
        self.cultiu_radiobutton_negative.grid(row=15, column=2, padx=0, pady=10, sticky="e")
        #Proteïnes totals
        protein_label = ttk.Label(self.p1_data_camps, text="Proteïnes totals", font=FONT_MSG)
        protein_label.grid(row=16, column=1, padx=0, pady=10)
        self.protein_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.protein_entry.insert(tk.END, '')
        self.protein_entry.grid(row=16, column=2, padx=0, pady=10, sticky="w")
        protein_unit_label = ttk.Label(self.p1_data_camps, text="g/l", font=FONT_MSG)
        protein_unit_label.grid(row=16, column=2, padx=0, pady=10)
        #Albúmina
        albumina_label = ttk.Label(self.p1_data_camps, text="Albúmina", font=FONT_MSG)
        albumina_label.grid(row=17, column=1, padx=0, pady=10)
        self.albumina_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.albumina_entry.insert(tk.END, '')
        self.albumina_entry.grid(row=17, column=2, padx=0, pady=10, sticky="w")
        albumina_unit_label = ttk.Label(self.p1_data_camps, text="g/l", font=FONT_MSG)
        albumina_unit_label.grid(row=17, column=2, padx=0, pady=10)
        #Tractament
        tr_label = ttk.Label(self.p1_data_camps, text="Tractament", font=FONT_MSG)
        tr_label.grid(row=18, column=1, padx=5, pady=10)
        tr_ant_button = ttk.Button(self.p1_data_camps, text="Antibiòtic",
                                     command=lambda: self.entry_popup_tr_ant("Antibiòtic"))
        tr_ant_button.grid(row=18, column=2, pady=10, padx=0, sticky="e")
        tr_top_button = ttk.Button(self.p1_data_camps, text="Tòpic",
                                   command=lambda: self.entry_popup_tr_top(
                                       "Tòpic"))
        tr_top_button.grid(row=18, column=3, pady=10, padx=0)
        #Submit
        self.p1_button_3 = ttk.Button(self.p1_data_frame, text="Guardar", command=self.apretar_boto_3)

    def cultiu_si(self):
        """
        Updates the value of "cultiu" to Yes.
        """

        self.cultiu = "si"

    def cultiu_no(self):
        """
        Updates the value of "cultiu" to Yes.
        """

        self.cultiu = "no"

    def ask_time(self):
        """
        Places the widgets of contention's time field.
        """

        self.temps_conten_entry.grid(row=12, column=2, padx=0, pady=10, sticky="e")
        self.temps_conten_combobox.grid(row=12, column=3, padx=5, pady=10, sticky="w")
        self.contencio = "si"

    def no_time(self):
        """
        Hides the widgets of contention's time field.
        """
        self.temps_conten_entry.grid_forget()
        self.temps_conten_combobox.grid_forget()
        self.contencio = "no"

    def entry_popup_tr_ant(self, title):
        """
        Display a popup for antibiotics treatment's comments.

        Parameters
        ----------
        title : String
           title of the widget
        """

        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 600
        h = 400
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Introduïr text")
        label = ttk.Label(self.popup, text=title, font=FONT_TITOL)
        label.pack(pady=10)
        self.tr_ant_text = tk.Text(self.popup, font=FONT_MSG)
        try:
            self.tr_ant_text.insert(tk.INSERT, self.popup_tr_ant)
        except:
            pass
        self.tr_ant_text.pack(pady=5, padx=10)
        button_ok = ttk.Button(self.popup, text="Desar", command=self.p1_tr_ant_ok)
        button_ok.pack()

    def entry_popup_tr_top(self, title):
        """
        Display a popup for topical treatment's comments.

        Parameters
        ----------
        title : String
           title of the widget
        """

        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 600
        h = 400
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Introduïr text")
        label = ttk.Label(self.popup, text=title, font=FONT_TITOL)
        label.pack(pady=10)
        self.tr_top_text = tk.Text(self.popup, font=FONT_MSG)
        try:
            self.tr_top_text.insert(tk.INSERT, self.popup_tr_top)
        except:
            pass
        self.tr_top_text.pack(pady=5, padx=10)
        button_ok = ttk.Button(self.popup, text="Desar", command=self.p1_tr_top_ok)
        button_ok.pack()

    def popup_barthel(self, title):
        """
        Display a popup for barthel scale's value calculation.

        Parameters
        ----------
        title : String
           title of the widget
        """

        self.popup_sit_nutr = ""
        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 800
        h = 700
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Calcular escala Barthel")

        label = ttk.Label(self.popup, text=title, font=FONT_TITOL)
        label.pack(pady=10)
        text = tk.Text(self.popup, font=FONT_TITOL, relief=tk.GROOVE, width=70, height=3, wrap=tk.WORD)
        text.insert(tk.END, BARTHEL_DESCRIPTION, "desc")
        text.config(state=tk.DISABLED)
        text.tag_configure("desc", justify="center")
        text.config(pady=10, padx=10)
        text.pack(pady=20)
        self.barthel_frame = tk.Frame(self.popup)
        self.barthel_frame.pack(pady=5, padx=10)
        #Descripció
        label_description = ttk.Label(self.barthel_frame, text="Selecciona els paràmetres corresponents:", font=FONT_MSG)
        label_description.grid(row=1, column=2, padx=10, pady=10)
        #Camp menjar
        barthel_menjar = ttk.Label(self.barthel_frame, text="Menjar", font=FONT_MSG)
        barthel_menjar.grid(row=2, column=1, padx=10, pady=10)
        self.menjar_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.menjar_combobox["values"] = ["Independent", "Necessita ajuda", "Dependent"]
        self.menjar_combobox.grid(row=2, column=2, padx=10, pady=10)
        #Camp rentar-se/banyar-se
        barthel_rentar = ttk.Label(self.barthel_frame, text="Rentar-se (banyar-se)", font=FONT_MSG)
        barthel_rentar.grid(row=3, column=1, padx=10, pady=10)
        self.rentar_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.rentar_combobox["values"] = ["Independent", "Dependent"]
        self.rentar_combobox.grid(row=3, column=2, padx=10, pady=10)
        #Camp vestir-se
        barthel_vestir = ttk.Label(self.barthel_frame, text="Vestir-se", font=FONT_MSG)
        barthel_vestir.grid(row=4, column=1, padx=10, pady=10)
        self.vestir_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.vestir_combobox["values"] = ["Independent", "Necessita ajuda", "Dependent"]
        self.vestir_combobox.grid(row=4, column=2, padx=10, pady=10)
        #Camp arreglar-se
        barthel_arreglar = ttk.Label(self.barthel_frame, text="Arreglar-se", font=FONT_MSG)
        barthel_arreglar.grid(row=5, column=1, padx=10, pady=10)
        self.arreglar_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.arreglar_combobox["values"] = ["Independent", "Dependent"]
        self.arreglar_combobox.grid(row=5, column=2, padx=10, pady=10)
        #Camp deposició
        barthel_deposicio = ttk.Label(self.barthel_frame, text="Deposició", font=FONT_MSG)
        barthel_deposicio.grid(row=6, column=1, padx=10, pady=10)
        self.deposicio_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.deposicio_combobox["values"] = ["Continent", "Accident ocasional", "Incontinent"]
        self.deposicio_combobox.grid(row=6, column=2, padx=10, pady=10)
        #Camp micció
        barthel_miccio = ttk.Label(self.barthel_frame, text="Micció", font=FONT_MSG)
        barthel_miccio.grid(row=7, column=1, padx=10, pady=10)
        self.miccio_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.miccio_combobox["values"] = ["Continent", "Accident ocasional", "Incontinent"]
        self.miccio_combobox.grid(row=7, column=2, padx=10, pady=10)
        #Camp anar al lavabo
        barthel_lavabo = ttk.Label(self.barthel_frame, text="Anar al lavabo", font=FONT_MSG)
        barthel_lavabo.grid(row=8, column=1, padx=10, pady=10)
        self.lavabo_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.lavabo_combobox["values"] = ["Independent", "Necessita ajuda", "Dependent"]
        self.lavabo_combobox.grid(row=8, column=2, padx=10, pady=10)
        #Camp traslladar-se (ex: butaca/llit)
        barthel_trasllat = ttk.Label(self.barthel_frame, text="Traslladar-se (ex: buataca/llit)", font=FONT_MSG)
        barthel_trasllat.grid(row=9, column=1, padx=10, pady=10)
        self.trasllat_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.trasllat_combobox["values"] = ["Independent", "Mínima ajuda", "Gran ajuda", "Dependent"]
        self.trasllat_combobox.grid(row=9, column=2, padx=10, pady=10)
        #Camp deambulació
        barthel_deambulacio = ttk.Label(self.barthel_frame, text="Dembulació", font=FONT_MSG)
        barthel_deambulacio.grid(row=10, column=1, padx=10, pady=10)
        self.deambulacio_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.deambulacio_combobox["values"] = ["Independent", "Necessita ajuda", "Independent en cadira de rodes", "Dependent"]
        self.deambulacio_combobox.grid(row=10, column=2, padx=10, pady=10)
        #Camp pujar i baixar escales
        barthel_escales = ttk.Label(self.barthel_frame, text="Pujar i baixar escales", font=FONT_MSG)
        barthel_escales.grid(row=11, column=1, padx=10, pady=10)
        self.escales_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.escales_combobox["values"] = ["Independent", "Necessita ajuda", "Dependent"]
        self.escales_combobox.grid(row=11, column=2, padx=10, pady=10)

        button_ok = ttk.Button(self.popup, text="Desar", command=self.barthel_getData)
        button_ok.pack(pady=20)

    def popup_emina(self, title):
        """
        Display a popup for emina scale's value calculation.

        Parameters
        ----------
        title : String
           title of the widget
        """

        self.popup_sit_nutr = ""
        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 800
        h = 600
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Calcular escala Barthel")

        label = ttk.Label(self.popup, text=title, font=FONT_BENVINGUDA)
        label.pack(pady=10)
        text = tk.Text(self.popup, font=FONT_TITOL, relief=tk.GROOVE, width=70, height=3, wrap=tk.WORD)
        text.insert(tk.END, EMINA_DESCRIPTION, "desc")
        text.config(state=tk.DISABLED)
        text.tag_configure("desc", justify="center")
        text.config(pady=10, padx=10)
        text.pack(pady=30)
        self.emina_frame = tk.Frame(self.popup)
        self.emina_frame.pack(pady=5, padx=10)
        # Descripció
        label_description = ttk.Label(self.emina_frame, text="Selecciona els paràmetres corresponents:",
                                      font=FONT_MSG)
        label_description.grid(row=1, column=2, padx=10, pady=10)
        # Estat mental
        emina_mental = ttk.Label(self.emina_frame, text="Estat mental", font=FONT_MSG)
        emina_mental.grid(row=2, column=1, padx=10, pady=10)
        self.mental_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.mental_combobox["values"] = ["Orientat", "Desorientat, apàtic o passiu", "Letàrgic o hipercinètic", "Comatós, inconscient."]
        self.mental_combobox.grid(row=2, column=2, padx=10, pady=10)
        # Movilitat
        emina_movilitat = ttk.Label(self.emina_frame, text="Movilitat", font=FONT_MSG)
        emina_movilitat.grid(row=3, column=1, padx=10, pady=10)
        self.movilitat_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.movilitat_combobox["values"] = ["Completa", "Lleugerament limitada", "Limitació important", "Immòbil"]
        self.movilitat_combobox.grid(row=3, column=2, padx=10, pady=10)
        # Humitat R/C, Incontinencia
        emina_humitat = ttk.Label(self.emina_frame, text="Humitat R/C, Incontinencia", font=FONT_MSG)
        emina_humitat.grid(row=4, column=1, padx=10, pady=10)
        self.humitat_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.humitat_combobox["values"] = ["No", "Urinària o fecal ocasional", "Urinària o fecal habitual", "Urinària i fecal, ambdues"]
        self.humitat_combobox.grid(row=4, column=2, padx=10, pady=10)
        # Nutrició
        emina_nutricio = ttk.Label(self.emina_frame, text="Nutrició", font=FONT_MSG)
        emina_nutricio.grid(row=5, column=1, padx=10, pady=10)
        self.nutricio_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.nutricio_combobox["values"] = ["Correcta", "Ocasionalment Incompleta", "Incompleta", "No ingereix"]
        self.nutricio_combobox.grid(row=5, column=2, padx=10, pady=10)
        # Activitat
        emina_activitat = ttk.Label(self.emina_frame, text="Activitat", font=FONT_MSG)
        emina_activitat.grid(row=6, column=1, padx=10, pady=10)
        self.activitat_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.activitat_combobox["values"] = ["Deambula", "Deambula amb ajuda", "Sempre requereix ajuda", "No deambula"]
        self.activitat_combobox.grid(row=6, column=2, padx=10, pady=10)

        button_ok = ttk.Button(self.popup, text="Desar", command=self.emina_getData)
        button_ok.pack()

    def p1_tr_top_ok(self):
        """
        Saves the topical treatment's comments to an attribute and closes popup.
        """

        self.popup_tr_top = self.tr_top_text.get(1.0, tk.END)
        self.popup.destroy()
        #print(self.popup_res_mic)

    def p1_tr_ant_ok(self):
        """
        Saves the antibiotics treatment's comments to an attribute and closes popup.
        """

        self.popup_tr_ant = self.tr_ant_text.get(1.0, tk.END)
        self.popup.destroy()
        #print(self.popup_sit_nutr)

    def barthel_getData(self):
        """
        Saves the barthel sacle answers to an attribute,
        sends a request with this data and closes popup.
        """

        data = self
        pub.sendMessage("BARTHEL_DATA_SENT", data=data)
        self.popup.destroy()

    def emina_getData(self):
        """
        Saves the emina sacle answers to an attribute,
        sends a request with this data and closes popup.
        """

        data = self
        pub.sendMessage("EMINA_DATA_SENT", data=data)
        self.popup.destroy()

    def popupmsg(self, msg):
        """
        Displays a popup window with the message.

        Parameters
        ----------
        msg : String
           message that will be displayed to user
        """

        popup = tk.Toplevel()
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        w = 300
        h = 75
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popup.wm_title("Atenció")
        label = ttk.Label(popup, text=msg, font=FONT_MSG)
        label.configure(anchor="center")
        label.pack(side="top", fill="x", pady=10)
        button1 = ttk.Button(popup, text="Ok", command=popup.destroy)
        button1.pack()
        popup.mainloop()

    def update_barthel(self, data):
        """
        Updates barthel's Scale widget with the calculated value.

        Parameters
        ----------
        data : int
            value of the barthel scale
       """

        self.barthel_scale.set(data)

    def update_emina(self, data):
        """
        Updates emina's Scale widget with the calculated value.

        Parameters
        ----------
        data : int
            value of the emina scale
       """

        self.emina_scale.set(data)

    def show_error(self, data_error):
        """
        Calls the popup function to display the errors found.

        Parameters
        ----------
        error : list
           wrong input data field's name
        """

        if "CODE_ERROR" in data_error:
            self.popupmsg("El codi ha de contenir 4 dígits")
        if "AGE_ERROR" in data_error:
            self.popupmsg("L'any de naixement ha de contenir 4 enters")
        if "N_IMM_ERROR" in data_error:
            self.popupmsg("Format no vàlid: Temps d'immobilització")
        if "N_HOSP_ERROR" in data_error:
            self.popupmsg("Format no vàlid: Temps d'hospitalització")
        if "N_INST_ERROR" in data_error:
            self.popupmsg("Format no vàlid: Temps d'institucionalització")
        if "DATE_ERROR" in data_error:
            self.popupmsg("Format no vàlid: Data")
        if "N_CONTEN_ERROR" in data_error:
            self.popupmsg("Format no vàlid: Contenció mecànica")

    def ask_flash_confirmation(self, img_cv2_mask, img_flash_reduced):
        """
        Displays a popup window to ask user confirmation about the flash reduction result.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected by user to reduce its flash
        """

        cv2.destroyAllWindows()
        # Crear la finestra
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 1920
        h = 1080
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Confirmar regió")
        # Definir títol del popup
        title = ttk.Label(self.popup, text="Flash Reduction", font=FONT_TITOL)
        label_warning = ttk.Label(self.popup, text="Waring: method is still developing and testing. Please check the result:", font=FONT_MSG)
        label_info = ttk.Label(self.popup, text="Original image // Flash reduced image", font=FONT_MSG)
        title.configure(anchor="center")
        label_warning.configure(anchor="center")
        label_info.configure(anchor="center")
        title.pack(side="top", fill="x", pady=10)
        label_warning.pack(side="top", fill="x", pady=10)
        label_info.pack(side="top", fill="x", pady=10)
        # Carregar la roi i la imatge
        im_rgb = cv2.cvtColor(img_cv2_mask, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im_rgb)
        flash_reduced_rgb = cv2.cvtColor(img_flash_reduced, cv2.COLOR_BGR2RGB)
        flash_reduced = Image.fromarray(flash_reduced_rgb)
        images_frame = ttk.Frame(self.popup)
        imgtk = ImageTk.PhotoImage(image=im)
        flash_reduced_tk = ImageTk.PhotoImage(image=flash_reduced)
        img_label = tk.Label(images_frame, image=imgtk)
        flash_label = tk.Label(images_frame, image=flash_reduced_tk)
        img_label.grid(row=1, column=1, padx=5, pady=5)
        flash_label.grid(row=1, column=2, padx=5, pady=5)
        images_frame.pack(pady=30)
        # Botons GUI
        button1 = ttk.Button(self.popup, text="Accept", command=lambda: self.flash_ok(img_flash_reduced))
        button2 = ttk.Button(self.popup, text="Decline", command=self.flash_ko)
        button1.pack()
        button2.pack()
        self.popup.mainloop()

    def flash_ok(self, img_cv2_roi):
        """
        Sends a request to Controller with the image's flash reduction result.
        Closes popup window.

        Parameters
        ----------
        img_cv2_roi : image cv2
           image selected and validated by user to reduce its flash
        """

        self.popup.destroy()
        pub.sendMessage("FLASH_CONFIRMATED", img_cv2_flash=img_cv2_roi)

    def flash_ko(self):
        """
        Closes popup and all cv2 windows.
        """

        cv2.destroyAllWindows()
        self.popup.destroy()

    def update_flash_label(self, img_cv2_flash):
        """
        Updates the image's label of GUI processing with the flash reduced one.

        Parameters
        ----------
        img_cv2_flash : image cv2
           image selected and validated by user to reduce its flash
        """

        flash_reduced_rgb = cv2.cvtColor(img_cv2_flash, cv2.COLOR_BGR2RGB)
        flash_reduced = Image.fromarray(flash_reduced_rgb)
        flash_reduced_tk = ImageTk.PhotoImage(image=flash_reduced)
        self.img_show.configure(image=flash_reduced_tk)
        self.img_show.image = flash_reduced_tk

    def img_processed_accepted(self):
        """
        Sends the request that image has been processed.
        """

        self.popup_img.destroy()
        pub.sendMessage("IMG_ACCEPTED")

    def reset_view(self):
        """
        Resets image label (after processing process).
        """

        path = Path(__file__).parent / "resources/load_img.png"
        img = ImageTk.PhotoImage(Image.open(path))
        self.p1_img_label.configure(image=img)
        self.p1_img_label.image = img
        self.p1_button_img.grid_forget()

    def update_data_n_elements(self, num):
        """
        Updates the label_info of page 2
        with the number of elements found in the storage directory.

        Parameters
        ----------
        num : int
           number of images found in the storage directory
        """

        self.p2_label_info.config(text="Elements trobats: "+str(num))
        self.update_list(num)

    def update_list(self, num):
        """
        Displays all found elements on the list.
        Creates the "double click" event to select an element.
        """

        self.llista.delete(0, tk.END)
        for i in range(num):
            self.llista.insert(tk.END, "Imatge: "+str(i+1))
        self.llista.bind('<Double-1>', self.select_element)

    def select_element(self, event):
        """
        Sends the request with the id of list's selected element.

        Parameters
        ----------
        event : event
           event from the mouse
        """

        n_elements = self.llista.curselection()
        for i in n_elements:
            pub.sendMessage("ASK_IMAGE_i", i=i+1)

    def crear_elements_p2(self):
        """
        Creates and places the main frames and labels of page 2 (View images).
        """

        self.p2_frame_list = tk.Frame(self.page_2, borderwidth=2, relief="groove")
        self.p2_label_info = ttk.Label(self.p2_frame_list, text="Elements trobats: ", font=FONT_TITOL)
        self.p2_label_info.pack()
        scrollbar = tk.Scrollbar(self.p2_frame_list)
        scrollbar.pack(side= tk.RIGHT, fill=tk.Y)
        self.llista = tk.Listbox(self.p2_frame_list, yscrollcommand= scrollbar.set)
        self.llista.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command= self.llista.yview)
        self.p2_frame_elements = tk.Frame(self.page_2)
        self.p2_frame_img = tk.Frame(self.p2_frame_elements)
        self.p2_frame_metadata = tk.Frame(self.p2_frame_elements)
        self.assemble_img_frame()

    def assemble_img_frame(self):
        """
        Creates and places the label_img of page 2 (View images).
        """

        self.p2_label_img = ttk.Label(self.p2_frame_img, text="Doble clic per carregar un element de la llista", font=FONT_MSG)
        self.p2_label_img.grid(row=1, column=2, padx=5, pady=5)

    def load_image_i(self, img_tk):
        """
        Loads the image to the label_img of page 2 (View images).

        Parameters
        ----------
        img_tk : PIL Image
           image ready to be loaded to a label
        """

        self.p2_label_img.configure(image=img_tk)
        self.p2_label_img.image = img_tk

    def load_metadata_i(self, metadata):
        """
        Loads the metadata to the metadata labels of page 2 (View images).

        Parameters
        ----------
        metadata : JSON Object
           data sent to be loaded into a label
        """

        p2_label_metadata_code = ttk.Label(self.p2_frame_metadata, text="Codi: "+metadata["metadata"]["code"], font=FONT_MSG)
        p2_label_metadata_code.grid(row=1, column=2, padx=5, pady=5)
        p2_label_metadata_grade = ttk.Label(self.p2_frame_metadata, text="Grau: "+metadata["metadata"]["grade"], font=FONT_MSG)
        p2_label_metadata_grade.grid(row=2, column=2, padx=5, pady=5)
