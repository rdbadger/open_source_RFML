import os
import torch
from PyQt5 import Qt
import numpy as np
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QTextEdit, QFileDialog, \
    QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector
import pickle
import time
from shutil import copyfile
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import math

class signal_boxing_GUI_main(QWidget):

    def __init__(self, parent=None):
        super(signal_boxing_GUI_main, self).__init__(parent)
        # initialize GUI stuff
        self.fname = None
        self.IQ_t = None
        self.IQ_f = None
        self.IQ_bounded = None
        self.figureIQ, self.ax = plt.subplots(1)
        self.canvasIQ = FigureCanvas(self.figureIQ)
        self.toolbarIQ = NavigationToolbar(self.canvasIQ, self)
        self.figure_bounded, self.ax_bounded = plt.subplots(2)
        self.canvas_bounded = FigureCanvas(self.figure_bounded)
        self.index = 0
        self.all_bounded_data_raw = []
        self.all_bounded = []
        self.setWindowTitle('signal boxing GUI')
        win = QMainWindow()
        win.setFixedSize(1280, 900)
        menu_widget = QWidget()

        # buttons
        button = QPushButton('read data', menu_widget)
        read_bound_button = QPushButton('save current bound', menu_widget)
        overview_button = QPushButton('bounds overview', menu_widget)
        remove_last_button = QPushButton('remove last bound', menu_widget)
        export_raw_button = QPushButton('export raw', menu_widget)
        layout = QHBoxLayout(menu_widget)
        layout.addWidget(button)
        layout.addWidget(read_bound_button)
        layout.addWidget(remove_last_button)
        layout.addWidget(overview_button)
        layout.addWidget(export_raw_button)
        button.clicked.connect(self.button_pressed)
        read_bound_button.clicked.connect(self.read_bound_button_pressed)
        overview_button.clicked.connect(self.overview_pressed)
        remove_last_button.clicked.connect(self.remove_last_pressed)
        export_raw_button.clicked.connect(self.export_raw_pressed)
        self.bound_label = QLabel()
        self.bound_label.setAlignment(Qt.Qt.AlignCenter)
        # plot widgets
        plotWidget = QWidget()
        plotLayout = QVBoxLayout(plotWidget)
        plotLayout.addWidget(self.toolbarIQ)
        plotLayout.addWidget(self.bound_label)
        plotLayout.addWidget(self.canvasIQ)
        plotLayout.addWidget(self.canvas_bounded)
        win.setMenuWidget(menu_widget)
        win.setCentralWidget(plotWidget)
        win.show()
        app.exit(app.exec_())

    def gpu(self, db, n_fft):
        I = db[0::2]
        Q = db[1::2]
        w = n_fft
        den = 2
        win = torch.hann_window(w, periodic=True, dtype=None, layout=torch.strided, requires_grad=False)
        I_stft = torch.stft(torch.tensor(I), n_fft=w, hop_length=w//den, win_length=w, window=win, center=True, normalized=True, onesided=False)
        Q_stft = torch.stft(torch.tensor(Q), n_fft=w, hop_length=w//den, win_length=w, window=win, center=True, normalized=True, onesided=False)
        X_stft = I_stft[...,0] + Q_stft[...,0] + I_stft[...,1] + -1*Q_stft[...,1]
        print('X shape =', X_stft.shape)
        print('I shape =', I_stft.shape, 'Q shape = ', Q_stft.shape )
        Z_stft = torch.cat((I_stft,Q_stft),2)
        print('Z shape =', Z_stft.shape)
#        Z_stft = torch.cat((Z_stft[w//2:,:,:],Z_stft[:w//2,:,:])) # may not need to do this
        print('Z shape =', Z_stft.shape)
#        X_stft = torch.cat((X_stft[w//2:,:],X_stft[:w//2,:])) # may not need to do this
        X_stft = torch.unsqueeze(X_stft,2)
        print('X shape =', X_stft.shape)
        X_stft = torch.cat((X_stft,Z_stft),2) # trying to cat these two tensors...
        print('X shape final =', X_stft.shape)
        X_stft = X_stft.detach().cpu().numpy()
        # torch.cuda.empty_cache()
        return X_stft
    # read iq data from sigmf data file and saved it to this class
    def iq_read(self, file):
        fft = 1024*5
        UHF_dat = np.fromfile(file, dtype="float32")
        stft_gpu = self.gpu(UHF_dat, fft)
        self.stft_gpu_IQ = stft_gpu[:,:,1:]
        print('stft_gpu_IQ = ', self.stft_gpu_IQ.shape)
        eps = 1e-15
        self.stft_gpu =  10*np.log10(np.abs(stft_gpu[:,:,0]+eps))
        print('stft_gpu plot shape = ', self.stft_gpu.shape)
        self.IQ = self.stft_gpu_IQ
        return stft_gpu

    # read sigmf data file
    def button_pressed(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open Files', './')
        try:
            self.iq_read(self.fname[0])
            self.plot_IQ_initial(self.stft_gpu)
            self.IQ_bounded = None
            self.all_bounded = []
            self.spanIQ = RectangleSelector(self.ax, self.onselectIQ, interactive=True, useblit=True)
            self.figure_bounded.clear()
            self.ax_bounded = self.figure_bounded.subplots(2)
            self.canvas_bounded.draw()
        except FileNotFoundError:
            print("File not found");
            return

    def read_bound_button_pressed(self):
        if self.IQ_bounded is not None:
            curr_bound_data = {'IQ_bounded': self.IQ_bounded}
            self.all_bounded.append(curr_bound_data)

    def overview_pressed(self):
        plt.close(self.figureIQ)
        plt.close(self.figure_bounded)
        nFig = len(self.all_bounded)
        fig = plt.figure(figsize=(4., 4.))
        grid = ImageGrid(fig, 111,  # similar to subplot(111)
                         nrows_ncols=(math.ceil(math.sqrt(nFig)), math.ceil(math.sqrt(nFig))),  # creates 2x2 grid of axes
                         axes_pad=0.1,  # pad between axes in inch.
                         )
        for ax, data in zip(grid, self.all_bounded):
            bound = data['IQ_bounded']
            ax.pcolormesh(bound[:,:,0])
        plt.show()

    def export_raw_pressed(self):
        if self.all_bounded.__len__() == 0:
            print('you do not have any bounded data yet')
        else:
            ts = time.time()
            time_stamp = time.ctime(ts).replace(' ', '_').replace(':', '_')
            for idx, bound in enumerate(self.all_bounded):
                names = self.fname[0].split('.')
                fname = names[0]
                paths = fname.split('/')
                real_fname = paths[-1]

                if not os.path.exists('./data_temp'):
                    os.mkdir('./data_temp')

                if not os.path.exists('./data_temp/{}'.format(real_fname)):
                    os.mkdir('./data_temp/{}'.format(real_fname))

                if not os.path.exists('./data_temp/{}/sigmf-data'.format(real_fname)):
                    os.mkdir('./data_temp/{}/sigmf-data'.format(real_fname))

                data_folder_path = './data_temp/{}/sigmf-data'.format(real_fname)

                fullpath = './data_temp/{}/sigmf-data/bound_{}_{}'.format(real_fname, str(idx), time_stamp)
                IQ_bounded = bound['IQ_bounded']
                full = {'bounded': IQ_bounded}
                with open(fullpath + '.pickle', 'wb') as f:
                    pickle.dump(full, f)

                for fname in os.listdir('./dataset_temp'):
                    if fname.endswith('.sigmf-meta') and fname.startswith(real_fname):

                        if not os.path.exists('./data_temp/{}/sigmf-meta'.format(real_fname)):
                            os.mkdir('./data_temp/{}/sigmf-meta'.format(real_fname))

                        copyfile('./dataset_temp/{}.sigmf-meta'.format(real_fname),
                                 './data_temp/{}/sigmf-meta/{}.sigmf-meta'.format(real_fname, real_fname))

                        break
                else:
                    print('the metadata is not found on the same directory. meta-data should have the same name as the data file except for file extension')




    def remove_last_pressed(self):
        if self.all_bounded.__len__() >= 1:
            del self.all_bounded[-1]

    # this is called for bounding box region, and its data
    def onselectIQ(self, eclick, erelease):
        xmin = int(eclick.xdata)
        xmax = int(erelease.xdata)
        ymin = int(eclick.ydata)
        ymax = int(erelease.ydata)

        self.figure_bounded.clear()
        self.ax_bounded = self.figure_bounded.subplots(2)
        self.IQ_bounded = self.IQ[ymin:ymax, xmin:xmax,:]
        self.bound_label.setText("self.IQ[ymin {} : ymax {}, xmin {} : xmax {}] => size: [{} , {}]".format(ymin, ymax, xmin, xmax, abs(ymax-ymin), abs(xmax-xmin)))
        eps = 1e-15
        self.ax_bounded[0].pcolormesh(20*np.log10(np.abs(self.IQ_bounded[:,:,0]+eps)))
        self.ax_bounded[1].plot(20*np.log10(np.abs(self.IQ_bounded[:,:,0]+eps)))
        self.canvas_bounded.draw()

    # plotting Initial Inphase data
    def plot_IQ_initial(self, iq_plot):
        self.figureIQ.clear()
        self.ax = self.figureIQ.add_subplot(111)
        self.ax.imshow(iq_plot, aspect='auto', origin='lower') # matches validation segmented loader
        self.canvasIQ.draw()


if __name__ == '__main__':
    app = QApplication([])
    qt = signal_boxing_GUI_main()
