# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui
import numpy as np

import matplotlib as mpl
mpl.rcParams['font.size'] = 10
mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['lines.color'] = 'g'
mpl.rcParams['text.color'] = 'white'
mpl.rc('axes', facecolor='#1E1E1E', edgecolor='white', lw=1, labelcolor='white')
mpl.rc('xtick', color='white')
mpl.rc('ytick', color='white')
mpl.rc('figure', facecolor='#1E1E1E', edgecolor='black')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class TemperatureGraphWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(TemperatureGraphWidget, self).__init__(*args, **kwargs)
        self.create_figure()
        self.create_subplots()
        self.create_graph_content()
        self.set_graph_style()
        self.create_intensity_indicator_color_map()
        self._hidden = False

    def create_figure(self):
        self.figure = Figure(None, dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                  QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        self.graph_layout = QtGui.QVBoxLayout()
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_layout.setSpacing(0)
        self.graph_layout.setMargin(0)
        self.graph_layout.addWidget(self.canvas)
        self.setLayout(self.graph_layout)

    def create_subplots(self):
        self.us_axes = self.figure.add_subplot(122)
        self.ds_axes = self.figure.add_subplot(121)

    def create_graph_content(self):
        self.create_upstream_graph_content()
        self.create_downstream_graph_content()

    def create_upstream_graph_content(self):
        self.us_data_line, self.us_fit_line, self.us_temp_txt, \
        self.us_int_txt, self.us_warning_txt, self.us_calib_file_txt, \
        self.us_indicator_rectangle_line, self.us_indicator_rectangle_fill = \
            self.create_axes_content(self.us_axes)

    def create_downstream_graph_content(self):
        self.ds_data_line, self.ds_fit_line, self.ds_temp_txt, \
        self.ds_int_txt, self.ds_warning_txt, self.ds_calib_file_txt, \
        self.ds_indicator_rectangle_line, self.ds_indicator_rectangle_fill = \
            self.create_axes_content(self.ds_axes)

    def set_graph_style(self):
        self.set_upstream_graph_style()
        self.set_downstream_graph_style()

    def set_upstream_graph_style(self):
        self.us_axes.yaxis.set_visible(False)
        self.us_axes.set_xlabel('$\lambda$ $(nm)$', size=11)
        self.us_axes.set_title('UPSTREAM', color=(1, 0.55, 0), weight='bold', va='bottom')

    def set_downstream_graph_style(self):
        self.ds_axes.yaxis.set_visible(False)
        self.ds_axes.set_xlabel('$\lambda$ $(nm)$', size=11)
        self.ds_axes.set_title('DOWNSTREAM', color=(1, 1, 0), weight='bold', va='bottom')

    def create_axes_content(self, axes):
        data_line, = axes.plot([], [], '-', color=(0.7, 0.9, 0.9), lw=1)
        fit_line, = axes.plot([], [], 'r-', lw=3)
        temperature_txt = axes.text(0, 0, '', size=20, ha='left', va='top')
        intensity_txt = axes.text(0, 0, '', size=13, color=(0.04, 0.76, 0.17), ha='right')
        warning_txt = axes.text(0, 0, '', size=25, color='r', va='center', ha='center', weight='bold')
        indicator_rectangle_line = self.create_rectangle(axes)
        indicator_rectangle_fill = self.create_rectangle(axes, lw=0, zorder=10000)
        calib_file_warning_txt = axes.text(0, 0, '', size=9, color='r', ha='left', va='top')
        return data_line, fit_line, temperature_txt, intensity_txt, warning_txt, calib_file_warning_txt, indicator_rectangle_line, indicator_rectangle_fill

    def create_rectangle(self, axes, color=(0.12, 0.12, 0.12), lw=1, ec=(0.9, 0.9, 0.9), zorder=9999):
        rectangle = mpl.patches.Rectangle((0, 0), 10, 10, fill=True, color=color, lw=lw, ec=ec, zorder=zorder)
        axes.add_artist(rectangle)
        return rectangle

    def create_intensity_indicator_color_map(self):
        color_dict = {
            'red': ( (0.0, 1.0, 1.0),
                     (0.023, 0.04, 0.04),
                     (0.7, 0.04, 0.04),
                     (0.7, 0.0, 0.0),
                     (1.0, 1.0, 1.0)),
            'green': ( (0.0, 0.0, 0.0),
                       (0.023, 0.76, 0.76),
                       (0.7, 0.76, 0.76),
                       (0.85, 0.0, 0.0),
                       (1.0, 0.0, 0.0)),
            'blue': ( (0.0, 0.0, 0.0),
                      (0.023, 0.17, 0.17),
                      (0.7, 0.17, 0.17),
                      (0.85, 0.0, 0.0),
                      (1.0, 0.0, 0.0))
        }
        self.cmap = mpl.colors.LinearSegmentedColormap('own_color_map', color_dict)

    def update_graph(self, ds_spectrum, us_spectrum, ds_max_int, us_max_int, ds_calib_fname, us_calib_fname):
        self.set_own_object_parameters(ds_calib_fname, ds_max_int, ds_spectrum, us_calib_fname, us_max_int, us_spectrum)
        self.update_data_line()
        self.update_plot_limits()
        self.update_temperature_labels()
        self.update_maximum_intensity_labels()
        self.update_intensity_indicator_bar(width=0.025, height=1)
        self.update_intensity_warning()
        self.update_calibration_file_warning()
        self.canvas.draw()

    def set_own_object_parameters(self, ds_calib_fname, ds_max_int, ds_spectrum, us_calib_fname, us_max_int,
                                  us_spectrum):
        if isinstance(ds_spectrum, list):
            self.ds_exp_spectrum = ds_spectrum[0]
            self.ds_fit_spectrum = ds_spectrum[1]
        else:
            self.ds_exp_spectrum = ds_spectrum
            self.ds_fit_spectrum = None

        if isinstance(us_spectrum, list):
            self.us_exp_spectrum = us_spectrum[0]
            self.us_fit_spectrum = us_spectrum[1]
        else:
            self.us_exp_spectrum = us_spectrum
            self.us_fit_spectrum = None

        self.ds_max_int = ds_max_int
        self.us_max_int = us_max_int
        self.ds_calib_fname = ds_calib_fname
        self.us_calib_fname = us_calib_fname

    def update_data_line(self):
        self.ds_data_line.set_data(self.ds_exp_spectrum.data)
        self.us_data_line.set_data(self.us_exp_spectrum.data)

    def update_plot_limits(self):
        self.us_axes.set_xlim(self.us_exp_spectrum.get_x_limits())
        self.us_axes.set_ylim(self.us_exp_spectrum.get_y_limits())
        self.ds_axes.set_xlim(self.ds_exp_spectrum.get_x_limits())
        self.ds_axes.set_ylim(self.ds_exp_spectrum.get_y_limits())

    def get_ds_x_absolute_position(self, relative_x_position):
        if len(self.ds_exp_spectrum):
            return min(self.ds_exp_spectrum._x) + relative_x_position * self.ds_exp_spectrum.get_x_range()
        return 0

    def get_ds_y_absolute_position(self, relative_y_position):
        if len(self.ds_exp_spectrum):
            return min(self.ds_exp_spectrum._y) + relative_y_position * self.ds_exp_spectrum.get_y_range() * 1.05
        return 0

    def get_us_x_absolute_position(self, relative_x_position):
        if len(self.us_exp_spectrum):
            return min(self.us_exp_spectrum._x) + relative_x_position * self.us_exp_spectrum.get_x_range()
        return 0

    def get_us_y_absolute_position(self, relative_y_position):
        if len(self.us_exp_spectrum):
            return min(self.us_exp_spectrum._y) + relative_y_position * self.us_exp_spectrum.get_y_range() * 1.05
        return 0

    def update_temperature_labels(self):
        if self.ds_fit_spectrum == None:
            self.ds_temp_txt.set_text('')
            self.ds_fit_line.set_data([[], []])
        else:
            self.ds_temp_txt.set_text(
                '{0:.0f} K $\pm$ {1:.0f}'.format(self.ds_fit_spectrum.T, self.ds_fit_spectrum.T_err))
            self.ds_fit_line.set_data(self.ds_fit_spectrum.get_data())
            self.ds_temp_txt.set_x(self.get_ds_x_absolute_position(0.07))
            self.ds_temp_txt.set_y(self.get_ds_y_absolute_position(0.9))

        if self.us_fit_spectrum == None:
            self.us_temp_txt.set_text('')
            self.us_fit_line.set_data([[], []])
        else:
            self.us_temp_txt.set_text(
                '{0:.0f} K $\pm$ {1:.0f}'.format(self.us_fit_spectrum.T, self.us_fit_spectrum.T_err))
            self.us_fit_line.set_data(self.us_fit_spectrum.get_data())
            self.us_temp_txt.set_x(self.get_us_x_absolute_position(0.07))
            self.us_temp_txt.set_y(self.get_us_y_absolute_position(0.9))

    def plot_ds_temperature_fit(self, ds_temperature, ds_temperature_error, ds_fit_spectrum):
        self.ds_temp_txt.set_text(
                '{0:.0f} K $\pm$ {1:.0f}'.format(ds_temperature,
                                             ds_temperature_error))
        self.ds_temp_txt.set_x(self.get_ds_x_absolute_position(0.07))
        self.ds_temp_txt.set_y(self.get_ds_y_absolute_position(0.9))

        self.ds_fit_line.set_data(ds_fit_spectrum.data)

    def plot_us_temperature_fit(self, us_temperature, us_temperature_error, us_fit_spectrum):
        self.us_temp_txt.set_text(
                '{0:.0f} K $\pm$ {1:.0f}'.format(us_temperature,
                                                 us_temperature_error))
        self.us_temp_txt.set_x(self.get_us_x_absolute_position(0.07))
        self.us_temp_txt.set_y(self.get_us_y_absolute_position(0.9))

        self.us_fit_line.set_data(us_fit_spectrum.data)


    def update_maximum_intensity_labels(self):
        self.ds_int_txt.set_text('Max Int: {0:.0f}'.format(self.ds_max_int))
        self.ds_int_txt.set_x(self.get_ds_x_absolute_position(0.97))
        self.ds_int_txt.set_y(self.get_ds_y_absolute_position(0.03))

        self.us_int_txt.set_text('Max Int: {0:.0f}'.format(self.us_max_int))
        self.us_int_txt.set_x(self.get_us_x_absolute_position(0.97))
        self.us_int_txt.set_y(self.get_us_y_absolute_position(0.03))

    def update_intensity_indicator_bar(self, width, height):
        if not (len(self.ds_exp_spectrum) and len(self.us_exp_spectrum)):
            return
        self.ds_indicator_rectangle_line.set_x(min(self.ds_exp_spectrum.x))
        self.ds_indicator_rectangle_line.set_y(min(self.ds_exp_spectrum.y))
        self.ds_indicator_rectangle_line.set_width(width * self.ds_exp_spectrum.get_x_range())
        self.ds_indicator_rectangle_line.set_height(height * self.ds_exp_spectrum.get_y_range() * 1.05)

        self.ds_indicator_rectangle_fill.set_x(min(self.ds_exp_spectrum.x))
        self.ds_indicator_rectangle_fill.set_y(min(self.ds_exp_spectrum.y))
        self.ds_indicator_rectangle_fill.set_width(width * self.ds_exp_spectrum.get_x_range())
        self.ds_indicator_rectangle_fill.set_height(
            self.ds_max_int / 64400.0 * height * self.ds_exp_spectrum.get_y_range() * 1.05)

        self.ds_indicator_rectangle_fill.set_facecolor(self.cmap(self.ds_max_int / 64400.0))

        if self.ds_max_int < 100:
            self.ds_indicator_rectangle_line.set_facecolor((1, 0, 0))
        else:
            self.ds_indicator_rectangle_line.set_facecolor((0.12, 0.12, 0.12))

        if self.us_max_int < 100:
            self.us_indicator_rectangle_line.set_facecolor((1, 0, 0))
        else:
            self.us_indicator_rectangle_line.set_facecolor((0.12, 0.12, 0.12))

        self.us_indicator_rectangle_line.set_x(min(self.us_exp_spectrum.x))
        self.us_indicator_rectangle_line.set_y(min(self.us_exp_spectrum.y))
        self.us_indicator_rectangle_line.set_width(width * self.us_exp_spectrum.get_x_range())
        self.us_indicator_rectangle_line.set_height(height * self.us_exp_spectrum.get_y_range() * 1.05)

        self.us_indicator_rectangle_fill.set_x(min(self.us_exp_spectrum.x))
        self.us_indicator_rectangle_fill.set_y(min(self.us_exp_spectrum.y))
        self.us_indicator_rectangle_fill.set_width(width * self.us_exp_spectrum.get_x_range())
        self.us_indicator_rectangle_fill.set_height(
            self.us_max_int / 64400.0 * height * self.us_exp_spectrum.get_y_range() * 1.05)

        self.us_indicator_rectangle_fill.set_facecolor(self.cmap(self.us_max_int / 64400.0))

    def update_intensity_warning(self):
        self.ds_warning_txt.set_x(self.get_ds_x_absolute_position(0.5))
        self.ds_warning_txt.set_y(self.get_ds_y_absolute_position(0.5))
        if self.ds_max_int >= 63500:
            self.ds_warning_txt.set_text('SATURATION')
        elif self.ds_max_int <= 100:
            self.ds_warning_txt.set_text('TOO LOW\nINTENSITY')
        else:
            self.ds_warning_txt.set_text('')

        self.us_warning_txt.set_x(self.get_us_x_absolute_position(0.5))
        self.us_warning_txt.set_y(self.get_us_y_absolute_position(0.5))
        if self.us_max_int >= 63500:
            self.us_warning_txt.set_text('SATURATION')
        elif self.us_max_int <= 100:
            self.us_warning_txt.set_text('TOO LOW\n INTENSITY')
        else:
            self.us_warning_txt.set_text('')

    def update_calibration_file_warning(self):
        if self.ds_fit_spectrum == None:
            self.ds_calib_file_txt.set_text('Load calibration with correct dimensions!')
            self.ds_calib_file_txt.set_x(self.get_ds_x_absolute_position(0.05))
            self.ds_calib_file_txt.set_y(self.get_ds_y_absolute_position(0.96))
        else:
            self.ds_calib_file_txt.set_text('')

        if self.us_fit_spectrum == None:
            self.us_calib_file_txt.set_text('Load calibration with correct dimensions!')
            self.us_calib_file_txt.set_x(self.get_us_x_absolute_position(0.05))
            self.us_calib_file_txt.set_y(self.get_us_y_absolute_position(0.96))
        else:
            self.us_calib_file_txt.set_text('')

    def hide(self):
        self._parent.hide()
        self._hidden = True

    def show(self):
        self._parent.show()
        self.redraw_figure()
        self._hidden = False

    def resize_graph(self, new_size):
        if not self._hidden:
            self.figure.set_size_inches([new_size.width() / 100.0, new_size.height() / 100.0])
            self.redraw_figure()

    def redraw_figure(self):
        self.figure.tight_layout(None, 1, None, None)
        self.canvas.draw()
