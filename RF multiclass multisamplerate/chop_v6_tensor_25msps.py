import os
import pickle
import random
import numpy as np
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QPushButton, QLineEdit, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from random import choices

class load_pic_v2_2(QtWidgets.QWidget):

    def __init__(self):
        super(load_pic_v2_2, self).__init__()
        # Initialize necessary stuff
        self.items = []
        self.images = []
        readButton = QPushButton("Read Files")
        readButton.clicked.connect(self.readFilesPressed)
        labelWidth = QLabel()
        labelWidth.setText("set width to chop each data")
        labelHeight = QLabel()
        labelHeight.setText("set height to chop each data")
        labelRand = QLabel()
        labelRand.setText("set number of chops you want")
        self.widthText = QLineEdit()
        self.heightText = QLineEdit()
        self.randText = QLineEdit()
        # Initialize scrollarea widget
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(readButton)
        lay.addWidget(labelWidth)
        lay.addWidget(self.widthText)
        lay.addWidget(labelHeight)
        lay.addWidget(self.heightText)
        lay.addWidget(labelRand)
        lay.addWidget(self.randText)
        self.scrollArea = QtWidgets.QScrollArea()
        lay.addWidget(self.scrollArea)
        chopButton = QPushButton('Chop Chop Chop')
        chopButton.clicked.connect(self.buttonPressed)
        lay.addWidget(chopButton)
        self.resize(1900, 900)

    def readFilesPressed(self):
        # read multiple files
        self.fnames= []
        self.fnames = QFileDialog.getOpenFileNames(self, 'Open Files', './data_temp')
        self.items = []
        for fname in self.fnames[0]:
            with open(fname, 'rb') as f:
                self.items.append(pickle.load(f))
        self.top_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QVBoxLayout()
        # read all the data and initialize necessary GUI widgets
        for idx, item in enumerate(self.items):
            path = self.fnames[0]
            fname = path[idx]
            group_box = QtWidgets.QGroupBox()
            group_box.setTitle(fname)
            layout = QtWidgets.QVBoxLayout(group_box)
            # label1
            label1 = QtWidgets.QLabel()
            label1.setText('data overview: ')
            layout.addWidget(label1)
            # info text
            info_text = QTextEdit()
            str = ''
            str += '<<<<IQbound ' + (idx + 1).__str__() + '>>>>' + '\n'
            str += 'Shape of bounded IQ sample: '
            str += item['bounded'].shape.__str__()
            str += '\n'
            for k, v in item.items():
                str += '<<' + k + '>>'
                str += '\n'
                str += v.__str__()
                str += '\n'
            str += '\n'
            info_text.setText(str)
            info_text.setReadOnly(True)
            info_text.setFixedSize(1600, 360)
            layout.addWidget(info_text)
            fig = plt.figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            temp = item['bounded'][:,:,0]
            print('data type temp = ', temp, 'shape is = ', temp.shape)
            eps = 1e-15
            ax.pcolormesh(20*np.log10(np.abs(temp+eps)),vmin=-70, vmax=5)
#            plt.imshow(stft_plot, vmin=-70, vmax=5, aspect='auto', origin='lower')
            layout.addWidget(canvas)
            canvas.draw()
            split = fname.split('/')
            self.fn = split[-1]
            self.data_folder_name = split[-3]
            if not os.path.exists('./data_temp/{}/bound-plots'.format(self.data_folder_name)):
                os.mkdir('./data_temp/{}/bound-plots'.format(self.data_folder_name))

            plt.savefig('./data_temp/{}/bound-plots/{}.png'.format(self.data_folder_name, self.fn))
            self.top_layout.addWidget(group_box)

        # add widgets to main window
        self.top_widget.setLayout(self.top_layout)
        self.scrollArea.setWidget(self.top_widget)

    def buttonPressed(self):
        col = int(self.widthText.text())
        row = int(self.heightText.text())
        chopped = []
        desire = int(self.randText.text())

        for item in self.items:
            IQ = item['bounded']
            for _ in range(desire):
                randCol = random.randint(0, len(IQ[0]) - col)
                randRow = random.randint(0, len(IQ) - row)
                print('random row = ', randRow, 'print col = ', randCol)
                chop = {}
                chop['bounded'] = IQ[randRow:randRow+row, randCol:randCol+col,:]
                chopped.append(chop)

        for idx, item in enumerate(chopped):
            chop = item['bounded']
            if chop.shape[0] == row and chop.shape[1] == col:
                path = './data_temp/{}/chopped-data-{}-{}'.format(self.data_folder_name, self.widthText.text(),
                                                             self.heightText.text())
                if not os.path.exists(path):
                    os.mkdir(path)
                fname = path + '/{}-chop{}'.format(self.fn, idx)
                with open(fname + '.pickle', 'wb') as f:
                    pickle.dump(item, f)
                    print(fname, " dumped")
# run main
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = load_pic_v2_2()
    widget.show()
    sys.exit(app.exec_())
