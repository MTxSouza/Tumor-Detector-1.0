# libraries
from utils import *

import numpy as np
import tkinter
import os


# dev configs
BACKGROUND = '#4FD3D3'
MODEL_NAME = 'model.h5'
N_IMG = 70
IMG_SIZE = (448,448)
LABEL_MAP = {1:'Saudável', 0:'Tumor detectado'}


if __name__=='__main__':
    
    # init
    log = Logging()
    log.log('info', 'Initializing application.')
    
    RUNNING = True
    TEXT_LABEL = 'Diagnóstico: '
    PRED_LABEL = 'Predict: '
    def stop_application():
        global RUNNING
        RUNNING = False

    def next_image():
        global current_image, current_index, index, image_widget, label_img, pred_img, graph, root
        current_index += 1
        if not current_index <= index.max():
            current_index = 0
        id = index[current_index]
        current_image = load_image(IMAGES[id], IMG_SIZE)
        label_img.config(text=TEXT_LABEL + LABEL_MAP[LABELS[id]])
        pred_img.config(text=PRED_LABEL + LABEL_MAP[predict[id]])
        image_widget.config(image=current_image)
        image_widget.image = current_image

        graph.destroy()
        graph = display_graph(prob[index[current_index]], root)
        graph.place(
            relx=0.56,
            rely=0.235,
            relwidth=0.435,
            relheight=0.694
        )

    def prev_image():
        global current_image, current_index, index, image_widget, pred_img, graph, root
        current_index -= 1
        if not current_index >= 0:
            current_index = index.max()
        id = index[current_index]
        current_image = load_image(IMAGES[id], IMG_SIZE)
        label_img.config(text=TEXT_LABEL + LABEL_MAP[LABELS[id]])
        pred_img.config(text=PRED_LABEL + LABEL_MAP[predict[id]])
        image_widget.config(image=current_image)
        image_widget.image = current_image

        graph.destroy()
        graph = display_graph(prob[index[current_index]], root)
        graph.place(
            relx=0.56,
            rely=0.235,
            relwidth=0.435,
            relheight=0.694
        )

    # project path
    PATH=os.path.dirname(os.path.realpath(__file__))
    os.chdir(PATH)

    # loading weights
    model=Net(_model=MODEL_NAME, _log=log)

    # taking 5 images for each class randomly
    IMAGES, LABELS = get_images(_n_img=N_IMG, _log=log)

    # shuffling image order
    index = np.random.choice(
        np.arange(IMAGES.__len__()),
        IMAGES.__len__(),
        replace=False
    )
    current_index = 0

    # running inferences
    predict, prob, SCORE = model.inference(IMAGES, LABELS)

    log.log('info', 'Opening interface.')

    # main window
    root = tkinter.Tk()
    root.geometry('1500x900')
    root.resizable(False,False)
    root.title('Tumor Detector - (BRAIN)')
    root.config(background=BACKGROUND)

    # image widget
    current_image = load_image(IMAGES[index[current_index]], IMG_SIZE)
    image_widget = tkinter.Label(
        master=root,
        image=current_image,
        highlightbackground='#00777B',
        highlightthickness=3,
        background='black'
    )
    image_widget.image = current_image
    image_widget.place(
        relx=0.005,
        rely=0.01,
        relwidth=0.545,
        relheight=0.92 #0.65
    )

    # graph
    graph = display_graph(prob[index[current_index]], root)
    graph.place(
        relx=0.56,
        rely=0.235,
        relwidth=0.435,
        relheight=0.694
    )

    # quit button
    quit_button = tkinter.Button(
        master=root,
        text='SAIR',
        fg='white',
        command=stop_application,
        background='#BD400A'
    )
    quit_button.place(
        relx=0.906,
        rely=0.94,
        relwidth=0.09,
        relheight=0.05
    )

    # select images
    BUTTON_COLOR = '#4593E6'
    next_img_button = tkinter.Button(
        master=root,
        text='PROXIMA',
        fg='white',
        command=next_image,
        background=BUTTON_COLOR
    )
    next_img_button.place(
        relx=0.451,
        rely=0.94,
        relwidth=0.1,
        relheight=0.05
    )

    prev_img_button = tkinter.Button(
        master=root,
        text='ANTERIOR',
        fg='white',
        command=prev_image,
        background=BUTTON_COLOR
    )
    prev_img_button.place(
        relx=0.005,
        rely=0.94,
        relwidth=0.1,
        relheight=0.05
    )

    # real label image
    label_img = tkinter.Label(
        master=root,
        text=TEXT_LABEL + LABEL_MAP[LABELS[index[current_index]]],
        fg='yellow',
        font=('Helverica', 15, 'bold'),
        background='black',
        anchor='w'
    )
    label_img.place(
        relx=0.56, #0.36
        rely=0.01,
        relwidth=0.32,
        relheight=0.05
    )

    # predict label image
    pred_img = tkinter.Label(
        master=root,
        text=PRED_LABEL + LABEL_MAP[predict[index[current_index]]],
        fg='orange',
        font=('Helverica', 15, 'bold'),
        background='black',
        anchor='w'
    )
    pred_img.place(
        relx=0.56, #0.36
        rely=0.06,
        relwidth=0.32,
        relheight=0.05
    )

    # precision and recall information
    result_widget = tkinter.Label(
        master=root,
        highlightthickness=3,
        highlightbackground='#466A90'
    )
    result_widget.place(
        relx=0.56,
        rely=0.12,
        relwidth=0.435,
        relheight=0.1
    )
    class_info = tkinter.Label(
        master=result_widget,
        text=f'Classes:\t\t\tTumor\t\t\tSaudável',
        font=('Helverica', 12, 'bold'),
        anchor='w'
    )
    class_info.place(
        relx=0.01,
        rely=0.1,
        relwidth=0.95,
        relheight=0.16
    )
    precision_info = tkinter.Label(
        master=result_widget,
        text='Precisão:\t\t\t{:.1f}%\t\t\t{:.1f}%'.format(SCORE[0][0]*100, SCORE[0][1]*100),
        font=('Helverica', 12, 'bold'),
        anchor='w'
    )
    precision_info.place(
        relx=0.01,
        rely=0.4,
        relwidth=0.95,
        relheight=0.16
    )
    recall_info = tkinter.Label(
        master=result_widget,
        text='Recall:\t\t\t{:.1f}%\t\t\t{:.1f}%'.format(SCORE[1][0]*100, SCORE[1][1]*100),
        font=('Helverica', 12, 'bold'),
        anchor='w'
    )
    recall_info.place(
        relx=0.01,
        rely=0.6,
        relwidth=0.95,
        relheight=0.16
    )
    support_info = tkinter.Label(
        master=result_widget,
        text='Support:\t\t\t{}\t\t\t{}'.format(SCORE[3][0], SCORE[3][1]),
        font=('Helverica', 12, 'bold'),
        anchor='w'
    )
    support_info.place(
        relx=0.01,
        rely=0.8,
        relwidth=0.95,
        relheight=0.16
    )

    log.log('info', 'Runnning.')

    while RUNNING:
        root.update()
        root.update_idletasks()

    log.log('info', 'Appication has been stopped.')
    os.system('clear')

