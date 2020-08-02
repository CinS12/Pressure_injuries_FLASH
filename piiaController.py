"""Main code and packages manager
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Tool that allows the connection between the View and Model.
Handles all the incoming requests.
"""

from piiaView import View
from piiaModel import Model
from pressure_image import Pressure_img
from data_manager import Data_manager
from pubsub import pub
import tkinter as tk
import ctypes

class Controller:
    """
    A class used to handle requests

    ...

    Attributes
    ----------
    parent : Tk
        root window
    model : Model
        a class to process and manage data structures
    view : View
        a class for data representation and user interaction
    data_manager : Data_manager
        a class used to manage the files's data reading/writing

    Methods
    -------
    button_1_pressed()
        Prints that button_1 from view has been pressed.
    button_2_pressed()
        Prints that button_2 from view has been pressed and calls the function.
        load_data from Data_manager.
    button_3_pressed(data)
        Prints that button_3 from view has been pressed.
        Calls the functions to check metadata and images before saving.
    load_image()
        Calls the function to load an image from Pressure_img.
    image_loaded(image_tk)
        Defines a Pressure_img object and saves its image.
        Calls the update_image from View to update the label with the loaded image.
        Calls the function from View to show "process" button.
    barthel_data_sent(data)
        Calls the Model function to calculate barthel from data sent.
    emina_data_sent(data)
        Calls the Model function to calculate emina from data sent.
    update_barthel(data)
        Calls the update_barthel from View to update the Scale with the value.
    update_emina(data)
        Calls the update_emina from View to update the Scale with the value.
    error_barthel()
        View request to check barthel fields.
    error_emina()
        View request to check emina fields.
    analyse_image()
        Checks if Pressure_img has been processed and calls processing function if not.
    ask_mask_confirmation(img_cv2_mask, scale_factor)
        Calls the View function to ask user confirmation about a mask.
    ask_roi_confirmation(img_cv2_mask, scale_factor, tissue, scale_factor)
        Calls the View function to ask user confirmation about a roi.
    pre_segmentation_confirmated(img_imgtk_mask, img_cv2_mask)
        Calls the Pressure_img function for the first image segmentation.
    segmentation_gui(img_imgtk_mask, img_cv2_mask)
        Updates the Pressure_img mask image.
        Calls the View function to show GUI for img segmentation to the user.
    roi_granulation()
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the granulation roi.
    roi_necrosis()
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the necrosis roi.
    roi_slough()
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the slough roi.
    roi_confirmated()
        Calls the Pressure_img function to update granulation/necrosis/slough fields.
    ask_perimeter()
        Checks if perimeter has been cropped and calls the Pressure_img function if not.
    update_perimeter_count()
        Updates the View of perimeter label.
    update_granulation_count(number)
        Updates the View of granulation's label with the number of roi's already selected.
    update_necrosis_count(number)
        Updates the View of necrosis's label with the number of roi's already selected.
    update_slough_count(number)
        Updates the View of slough's label with the number of roi's already selected.
    tot_ple_ko()
        Calls a View function to warn the user that all metadata fields must be filled.
    data_ko(error)
        Calls a View function to warn the user what field has the wrong input data.
    data_ok()
        Sets Pressure_img loaded boolean to False.
        Calls View function to reset loaded image label.
        Calls the function to save all the data entered by the user.
    flash_reduction(img_cv2_mask)
        Checks if flash reduction has been called and calls
        Pressure_img function to reduce flash if not.
        Calls the View function to ask user confirmation.
    flash_confirmated(img_cv2_flash)
        Updates Pressure_img mask and flash_reduced boolean.
        Calls the View function to update image label.
    image_accepted()
        Updates Pressure_img processed boolean to True.
    save_data_file()
        Calls the Data_manager function to save user introduced data and images.
    data_files_ko()
        Calls the View function to warn the user about a file manager error.
    data_n_elements(num)
        Calls the View function to update the element's label counter with a new value.
    load_image_i(image_tk)
        Calls the View function to load the image_tk to the p2_label_img.
    load_metadata_i(metadata)
        Calls the View function to load the metadata to the p2_label_metadata.
    ask_image_i(i)
        Calls the Data_manager functions to read and load the image and metadata "i".
    """

    def __init__(self, parent):
        self.parent = parent
        self.model = Model()
        self.view = View(parent)
        self.data_manager = Data_manager()
        self.view.setup()

        pub.subscribe(self.button_1_pressed, "BUTTON_1_PRESSED")
        pub.subscribe(self.button_2_pressed, "BUTTON_2_PRESSED")
        pub.subscribe(self.button_3_pressed, "BUTTON_3_PRESSED")
        pub.subscribe(self.load_image, "LOAD_IMAGE")
        pub.subscribe(self.image_loaded, "IMAGE_LOADED")
        pub.subscribe(self.barthel_data_sent, "BARTHEL_DATA_SENT")
        pub.subscribe(self.update_barthel, "UPDATE_BARTHEL")
        pub.subscribe(self.error_barthel, "ERROR_BARTHEL")
        pub.subscribe(self.emina_data_sent, "EMINA_DATA_SENT")
        pub.subscribe(self.update_emina, "UPDATE_EMINA")
        pub.subscribe(self.error_emina, "ERROR_EMINA")
        pub.subscribe(self.analyse_image, "ANALYSE_IMAGE")
        pub.subscribe(self.ask_mask_confirmation, "ASK_MASK_CONFIRMATION")
        pub.subscribe(self.pre_segmentation_confirmated, "PRE_SEGMENTATION_CONFIRMATED")
        pub.subscribe(self.segmentation_gui, "SEGMENTATION_GUI")
        pub.subscribe(self.roi_granulation, "ROI_GRANULATION")
        pub.subscribe(self.roi_necrosis, "ROI_NECROSIS")
        pub.subscribe(self.roi_slough, "ROI_SLOUGH")
        pub.subscribe(self.ask_roi_confirmation, "ASK_ROI_CONFIRMATION")
        pub.subscribe(self.roi_confirmated, "ROI_CONFIRMATED")
        pub.subscribe(self.ask_perimeter, "ASK_PERIMETER")
        pub.subscribe(self.update_perimeter_count, "UPDATE_PERIMETER_COUNT")
        pub.subscribe(self.update_granulation_count, "UPDATE_GRANULATION_COUNT")
        pub.subscribe(self.update_necrosis_count, "UPDATE_NECROSIS_COUNT")
        pub.subscribe(self.update_slough_count, "UPDATE_SLOUGH_COUNT")
        pub.subscribe(self.tot_ple_ko, "TOT_PLE_KO")
        pub.subscribe(self.data_ko, "DATA_KO")
        pub.subscribe(self.data_ok, "DATA_OK")
        pub.subscribe(self.flash_reduction, "FLASH_REDUCTION")
        pub.subscribe(self.flash_confirmated, "FLASH_CONFIRMATED")
        pub.subscribe(self.image_accepted, "IMG_ACCEPTED")
        pub.subscribe(self.data_files_ko, "DATA_FILES_KO")
        pub.subscribe(self.data_n_elements, "DATA_N_ELEMENTS")
        pub.subscribe(self.ask_image_i, "ASK_IMAGE_i")
        pub.subscribe(self.load_image_i, "IMAGE_LOAD_i")
        pub.subscribe(self.load_metadata_i, "METADATA_LOAD_i")

    def button_1_pressed(self):
        """
        Prints that button_1 from view has been pressed.
        """

        print("controller - Botó 1!")

    def button_2_pressed(self):
        """
        Prints that button_2 from view has been pressed and calls the function.
        load_data from Data_manager.
        """

        print("controller - Botó 2!")
        self.data_manager.load_data()

    def button_3_pressed(self, data):
        """
        Prints that button_3 from view has been pressed.
        Calls the functions to check metadata and images before saving.

        Parameters
        ----------
        data : list
           a list with all the metadata field's information written by the user
        """

        print("controller - Botó 3!")
        try:
            if self.pressure_img.loaded:
                if self.pressure_img.processed:
                    self.model.getData(data)
                else:
                    self.view.popupmsg("És necessari processar la imatge.")
            else:
                self.view.popupmsg("És necessari carregar una imatge")
        except:
            self.view.popupmsg("És necessari carregar una imatge")

    def load_image(self):
        """
        Calls the function to load an image from Pressure_img.
        """

        print("controller - carregar imatge")
        self.pressure_img.path = self.model.carregar_imatge()

    def image_loaded(self, image_tk):
        """
        Defines a Pressure_img object and saves its image.
        Calls the update_image from View to update the label with the loaded image.
        Calls the function from View to show "process" button.

        Parameters
        ----------
        image_tk : PIL Image
           image ready to be loaded in a label
        """

        self.pressure_img = Pressure_img()
        self.pressure_img.img_origin = self.model.img_original
        self.pressure_img.loaded = True
        self.view.update_image(image_tk)
        self.view.botoImg()

    def barthel_data_sent(self, data):
        """
         Calls the Model function to calculate barthel from data sent.

         Parameters
        ----------
        data : list
           list with all the field's values selected by the user
        """

        print("controller - barthel_data_sent!")
        self.model.calculateBarthel(data)

    def emina_data_sent(self, data):
        """
         Calls the Model function to calculate emina from data sent.

         Parameters
        ----------
        data : list
           list with all the field's values selected by the user
        """

        print("controller - emina_data_sent!")
        self.model.calculateEmina(data)

    def update_barthel(self, data):
        """
        Calls the View function update_barthel to update barthel value.

        Parameters
        ----------
        data : int
            value of the barthel scale
       """

        print("controller - update_barthel")
        self.view.update_barthel(data)

    def update_emina(self, data):
        """
        Calls the View function update_emina to update emina value.

        Parameters
        ----------
        data : int
            value of the emina scale
       """

        print("controller - update_emina")
        self.view.update_emina(data)

    def error_barthel(self):
        """
       View request to check barthel fields.
       """

        print("controller - error barthel")
        self.view.popupmsg("S'han d'omplir tots els camps")

    def error_emina(self):
        """
        View request to check emina fields.
        """

        print("controller - error emina")
        self.view.popupmsg("S'han d'omplir tots els camps")

    def analyse_image(self):
        """
        Checks if Pressure_img has been processed and calls processing function if not.
        """

        print("controller - analyse_image!")
        if self.pressure_img.processed == False:
            self.pressure_img.crop_image(self.pressure_img.path)
        else:
            self.view.popupmsg("La imatge ja ha estat processada.")

    def ask_mask_confirmation(self, img_cv2_mask, scale_factor):
        """
        Calls the View function to ask user confirmation about an image's mask.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image that requires user confirmation
        scale_factor : int
           image resize value (default = 100)
        """

        print("controller - ask_mask_confirmation!")
        try:
            self.view.ask_mask_confirmation(img_cv2_mask, scale_factor)
        except:
            self.view.popupmsg("Alguna cosa ha fallat. Torna-ho a intentar!")

    def ask_roi_confirmation(self, img_cv2_mask, img_cv2_roi, tissue, scale_factor):
        """
        Calls the View function to ask user confirmation about a image's roi.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image before cropping roi
        img_cv2_roi : image cv2
           image that requires user confirmation
        tissue : String
            tissue of the roi
        scale_factor : int
           image resize value (default = 100)
        """

        print("controller - ask_roi_confirmation!")
        try:
            self.view.ask_roi_confirmation(img_cv2_mask, img_cv2_roi, tissue, scale_factor)
        except:
            self.view.popupmsg("Alguna cosa ha fallat. Torna-ho a intentar!")

    def pre_segmentation_confirmated(self, img_imgtk_mask, img_cv2_mask):
        """
        Calls the Pressure_img function for the first image segmentation.

        Parameters
        ----------
        img_imgtk_mask : PIL Image
           image before cropping roi
        img_cv2_mask : image cv2
           image that requires user confirmation
        """
        print("controller - pre_segmentation_confirmated!")
        scale_factor = 100
        self.pressure_img.begin_segmentation(img_imgtk_mask=img_imgtk_mask, img_cv2_mask=img_cv2_mask, scale_factor= scale_factor)

    def segmentation_gui(self, img_imgtk_mask, img_cv2_mask):
        """
        Updates the Pressure_img mask image.

        Parameters
        ----------
        img_imgtk_mask : PIL Image
           image before cropping roi
        img_cv2_mask : image cv2
           image that requires user confirmation
        """
        print("controller - segmentation_gui!")
        self.pressure_img.close_all()
        self.pressure_img.mask = img_cv2_mask
        self.view.segmentation_gui(img_imgtk_mask, img_cv2_mask)

    def roi_granulation(self):
        """
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the granulation roi.
        """

        print("controller - roi_granulation!")
        img_cv2_mask = self.pressure_img.mask
        self.pressure_img.roi_crop(img_cv2_mask, "Granulation")

    def roi_necrosis(self):
        """
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the necrosis roi.
        """

        print("controller - roi_necrosis!")
        img_cv2_mask = self.pressure_img.mask
        self.pressure_img.roi_crop(img_cv2_mask, "Necrosis")

    def roi_slough(self):
        """
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the slough roi.
        """
        print("controller - roi_slough!")
        img_cv2_mask = self.pressure_img.mask
        self.pressure_img.roi_crop(img_cv2_mask, "Slough")

    def roi_confirmated(self, img_cv2_roi, tissue):
        """
        Calls the Pressure_img function to update granulation/necrosis/slough fields.

        Parameters
        ----------
        img_cv2_roi : image cv2
           roi selected by the user
        tissue : String
            tissue of the roi
        """
        print("controller - roi_confirmated!")
        self.pressure_img.save_mask_data(img_cv2_roi, tissue)

    def ask_perimeter(self):
        """
        Checks if perimeter has been cropped and calls the Pressure_img function if not.
        """

        print("controller - ask_perimeter!")
        img_cv2_mask = self.pressure_img.mask
        if self.pressure_img.perimetre_done:
            self.view.popupmsg("El perímetre ja ha estat seleccionat")
        else:
            self.pressure_img.roi_crop(img_cv2_mask, "Perimeter")

    def update_perimeter_count(self):
        """
        Updates the View of perimeter label.
        """

        print("controller - update_perimeter_count!")
        self.view.update_perimeter_count()

    def update_granulation_count(self, number):
        """
        Updates the View of granulation's label with the number of roi's already selected.

        Parameters
        ----------
        number : int
           number of granulation rois already selected
        """
        print("controller - update_granulation_count!")
        self.view.update_granulation_count(number)

    def update_necrosis_count(self, number):
        """
        Updates the View of necrosis's label with the number of roi's already selected.

        Parameters
        ----------
        number : int
           number of necrosis rois already selected
        """

        print("controller - update_necrosis_count!")
        self.view.update_necrosis_count(number)

    def update_slough_count(self, number):
        """
        Updates the View of slough's label with the number of roi's already selected.

        Parameters
        ----------
        number : int
           number of slough rois already selected
        """

        print("controller - update_slough_count!")
        self.view.update_slough_count(number)

    def tot_ple_ko(self):
        """
        Calls a View function to warn the user that all metadata fields must be filled.
        """

        print("controller - tot_ple_ko!")
        self.view.popupmsg("S'han d'omplir tots els camps")

    def data_ko(self, error):
        """
        Calls a View function to warn the user what field has the wrong input data.

        Parameters
        ----------
        error : list
           wrong input data field's name
        """

        self.view.show_error(error)
        print("controller - data_ko")

    def data_ok(self):
        """
        Sets Pressure_img loaded boolean to False.
        Calls View function to reset loaded image label.
        Calls the function to save all the data entered by the user.
        """

        print("controller - data_ok")
        self.pressure_img.loaded = False
        self.view.reset_view()
        try:
            self.save_data_file()
            self.view.popupmsg("Procés finalitzat amb èxit. Prem OK per continuar.")
        except:
            self.view.popupmsg("Error de gestió de fitxers.")

    def flash_reduction(self, img_cv2_mask):
        """
        Checks if flash reduction has been called and calls
        Pressure_img function to reduce flash if not.
        Calls the View function to ask user confirmation.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected by user to reduce its flash
        """

        print("controller - flash_reduction!")
        if self.pressure_img.flash_reduced == False:
            try:
                img_flash_reduced = self.pressure_img.flash_reduction(img_cv2_mask)
                self.view.ask_flash_confirmation(img_cv2_mask, img_flash_reduced)
            except:
                self.view.popupmsg("Alguna cosa ha fallat. Torna-ho a intentar!")
        else:
            self.view.popupmsg("Ja s'ha aplicat la reducció.")

    def flash_confirmated(self, img_cv2_flash):
        """
        Updates Pressure_img mask and flash_reduced boolean.
        Calls the View function to update image label.

        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected and validated by user to reduce its flash
        """

        print("controller - flash_confirmated!")
        self.pressure_img.flash_reduced = True
        self.pressure_img.mask = img_cv2_flash
        self.view.update_flash_label(img_cv2_flash)

    def image_accepted(self):
        """
        Updates Pressure_img processed boolean to True.
        """

        print("controller - image_accepted!")
        self.pressure_img.processed = True

    def save_data_file(self):
        """
        Calls the Data_manager function to save user introduced data and images.
        """

        print("controller - save_data_file")
        self.data_manager.save_data(self.model.metadata, self.pressure_img)

    def data_files_ko(self):
        """
        Calls the View function to warn the user about a file manager error.
        """

        print("controller - data_files_ko")
        self.view.popupmsg("Error de gestió dels fitxers.")

    def data_n_elements(self, num):
        """
        Calls the View function to update the element's label counter with a new value.

        Parameters
        ----------
        num : int
           number of images found in the storage directory
        """

        print("controller - data_n_elements")
        self.view.update_data_n_elements(num)

    def load_image_i(self, img_tk):
        """
        Calls the View function to load the image_tk to the p2_label_img.

        Parameters
        ----------
        img_tk : PIL Image
           image ready to be loaded to a label
        """

        print("controller - load_img_i")
        self.view.load_image_i(img_tk)

    def load_metadata_i(self, metadata):
        """
        Calls the View function to load the metadata to the p2_label_metadata.

        Parameters
        ----------
        metadata : JSON Object
           data sent to be loaded into a label
        """

        print("controller - load_metadata_i")
        self.view.load_metadata_i(metadata)

    def ask_image_i(self, i):
        """
        Calls the Data_manager functions to read and load the image and metadata "i".

        Parameters
        ----------
        i : int
           id of the image and metadata that have to be read
        """

        print("controller - ask_img_i")
        self.data_manager.load_img_i(i)
        self.data_manager.load_metadata_i(i)

if __name__ == "__main__":
    root = tk.Tk()
    user32 = ctypes.windll.user32
    #screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    #print(screensize)
    #w = screensize[0]
    #h = screensize[1]
    w = 1920
    h = 1080
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 3) - (h / 3)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    # mainwin.resizable(0, 0)
    root.title("PIIA")

    app = Controller(root)
    root.mainloop()