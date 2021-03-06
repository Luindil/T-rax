# -*- coding: utf-8 -*-
# T-Rax - GUI program for analysis of spectroscopy data during
# diamond anvil cell experiments
# Copyright (C) 2016 Clemens Prescher (clemens.prescher@gmail.com)
# Institute for Geology and Mineralogy, University of Cologne
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from qtpy import QtCore
import numpy as np
from scipy.optimize import curve_fit
import h5py
import math

from .Spectrum import Spectrum
from .RoiData import RoiDataManager, Roi, get_roi_max, get_roi_sum
from .SpeFile import SpeFile
from .helper import FileNameIterator

T_LOG_FILE = 'T_log.txt'
LOG_HEADER = '# File\tPath\tT_DS\tT_US\tDetector\tExposure Time [sec]\n'


class TemperatureModel(QtCore.QObject):
    data_changed = QtCore.Signal()
    ds_calculations_changed = QtCore.Signal()
    us_calculations_changed = QtCore.Signal()

    def __init__(self):
        super(TemperatureModel, self).__init__()

        self.filename = None
        self.data_img_file = None
        self._data_img = None
        self.log_file = None

        self.ds_calibration_img_file = None
        self.us_calibration_img_file = None

        self.ds_calibration_filename = None
        self.us_calibration_filename = None

        self._filename_iterator = FileNameIterator()

        self.roi_data_manager = RoiDataManager(2)

        self.current_frame = 0
        self.ds_temperature_model = SingleTemperatureModel(0, self.roi_data_manager)
        self.us_temperature_model = SingleTemperatureModel(1, self.roi_data_manager)

    # loading spe image files:
    #########################################################################
    def load_data_image(self, filename):
        if not self.filename or not os.path.dirname(self.filename) == os.path.dirname(filename):
            self.create_log_file(os.path.dirname(filename))
        self.filename = filename
        self.data_img_file = SpeFile(filename)

        if self.data_img_file.num_frames > 1:
            self._data_img = self.data_img_file.img[0]
            self.current_frame = 0
        else:
            self._data_img = self.data_img_file.img
        self._update_temperature_models_data()
        self._filename_iterator.update_filename(filename)
        self.data_changed.emit()

    def load_next_data_image(self):
        new_filename = self._filename_iterator.get_next_filename()
        if new_filename is not None:
            self.load_data_image(new_filename)

    def load_previous_data_image(self):
        new_filename = self._filename_iterator.get_previous_filename()
        if new_filename is not None:
            self.load_data_image(new_filename)

    def load_next_img_frame(self):
        return self.set_img_frame_number_to(self.current_frame + 1)

    def load_previous_img_frame(self):
        return self.set_img_frame_number_to(self.current_frame - 1)

    def set_img_frame_number_to(self, frame_number):
        if frame_number < 0 or frame_number >= self.data_img_file.num_frames:
            return False
        self.current_frame = frame_number
        self._data_img = self.data_img_file.img[frame_number]
        self._update_temperature_models_data()
        self.data_changed.emit()
        return True

    def create_log_file(self, file_path):
        try:
            self.log_file = open(os.path.join(file_path, T_LOG_FILE), 'a')
            self.log_file.write(LOG_HEADER)
            return self.log_file
        except PermissionError:
            return None

    def write_to_log_file(self):
        if not math.isnan(self.ds_temperature):
            ds_temp = str(int(self.ds_temperature))
        else:
            ds_temp = 'NaN'
        if not math.isnan(self.us_temperature):
            us_temp = str(int(self.us_temperature))
        else:
            us_temp = 'NaN'

        log_data = (os.path.basename(self.filename), os.path.dirname(self.filename), ds_temp, us_temp,
                    self.data_img_file.detector, str(self.data_img_file.exposure_time))
        self.log_file.write('\t'.join(log_data) + '\n')
        self.log_file.flush()

    def _update_temperature_models_data(self):
        self.ds_temperature_model.set_data(self._data_img,
                                           self.data_img_file.x_calibration)
        self.us_temperature_model.set_data(self._data_img,
                                           self.data_img_file.x_calibration)

    @property
    def data_img(self):
        return self._data_img

    @data_img.setter
    def data_img(self, value):
        self._data_img = value
        self._update_temperature_models_data()
        self.data_changed.emit()

    def has_data(self):
        return self._data_img is not None

    @property
    def file_info(self):
        return "Exp. Time: {}s | Grating: {} | Detector: {}".format(self.data_img_file.exposure_time,
                                                                    self.data_img_file.grating,
                                                                    self.data_img_file.detector)

    # calibration image files:
    #########################################################################
    def load_ds_calibration_image(self, filename):
        self.ds_calibration_img_file = SpeFile(filename)
        self.ds_calibration_filename = filename
        self.ds_temperature_model.set_calibration_data(self.ds_calibration_img_file.img,
                                                       self.ds_calibration_img_file.x_calibration)
        self.ds_calculations_changed.emit()

    def load_us_calibration_image(self, filename):
        self.us_calibration_img_file = SpeFile(filename)
        self.us_calibration_filename = filename
        self.us_temperature_model.set_calibration_data(self.us_calibration_img_file.img,
                                                       self.us_calibration_img_file.x_calibration)
        self.us_calculations_changed.emit()

    # setting etalon interface
    #########################################################################
    def load_ds_etalon_spectrum(self, filename):
        self.ds_temperature_model.load_etalon_spectrum(filename)
        self.ds_calculations_changed.emit()

    def load_us_etalon_spectrum(self, filename):
        self.us_temperature_model.load_etalon_spectrum(filename)
        self.us_calculations_changed.emit()

    def set_ds_calibration_modus(self, modus):
        self.ds_temperature_model.set_calibration_modus(modus)
        self.ds_calculations_changed.emit()

    def set_us_calibration_modus(self, modus):
        self.us_temperature_model.set_calibration_modus(modus)
        self.us_calculations_changed.emit()

    def set_ds_calibration_temperature(self, temperature):
        self.ds_temperature_model.set_calibration_temperature(temperature)
        self.ds_calculations_changed.emit()

    def set_us_calibration_temperature(self, temperature):
        self.us_temperature_model.set_calibration_temperature(temperature)
        self.us_calculations_changed.emit()

    def save_setting(self, filename):
        f = h5py.File(filename, 'w')

        f.create_group('downstream_calibration')
        ds_group = f['downstream_calibration']
        if self.ds_calibration_img_file is not None:
            ds_group['image'] = self.ds_calibration_img_file.img
            ds_group['image'].attrs['filename'] = self.ds_calibration_img_file.filename
            ds_group['image'].attrs['x_calibration'] = self.ds_calibration_img_file.x_calibration
        ds_group['roi'] = self.ds_roi.as_list()
        ds_group['modus'] = self.ds_temperature_model.calibration_parameter.modus
        ds_group['temperature'] = self.ds_temperature_model.calibration_parameter.temperature
        ds_group['etalon_spectrum'] = self.ds_temperature_model.calibration_parameter.get_etalon_spectrum().data
        ds_group['etalon_spectrum'].attrs['filename'] = \
            self.ds_temperature_model.calibration_parameter.get_etalon_filename()

        f.create_group('upstream_calibration')
        us_group = f['upstream_calibration']
        if self.us_calibration_img_file is not None:
            us_group['image'] = self.us_calibration_img_file.img
            us_group['image'].attrs['filename'] = self.us_calibration_img_file.filename
            us_group['image'].attrs['x_calibration'] = self.us_calibration_img_file.x_calibration
        us_group['roi'] = self.us_roi.as_list()
        us_group['modus'] = self.us_temperature_model.calibration_parameter.modus
        us_group['temperature'] = self.us_temperature_model.calibration_parameter.temperature
        us_group['etalon_spectrum'] = self.us_temperature_model.calibration_parameter.get_etalon_spectrum().data
        us_group['etalon_spectrum'].attrs['filename'] = \
            self.us_temperature_model.calibration_parameter.get_etalon_filename()

        f.close()

    def load_setting(self, filename):
        f = h5py.File(filename, 'r')
        ds_group = f['downstream_calibration']
        if 'image' in ds_group:
            self.ds_temperature_model.set_calibration_data(ds_group['image'][...],
                                                           ds_group['image'].attrs['x_calibration'][...])
            try:
                self.ds_calibration_filename = ds_group['image'].attrs['filename'].decode('utf-8')
            except AttributeError:
                self.ds_calibration_filename = ds_group['image'].attrs['filename']
            img_dimension = (self.ds_temperature_model.calibration_img.shape[1],
                             self.ds_temperature_model.calibration_img.shape[0])
            self.roi_data_manager.set_roi(0, img_dimension, ds_group['roi'][...])
            self.ds_temperature_model._update_all_spectra()
        else:
            self.ds_temperature_model.reset_calibration_data()
            self.ds_calibration_filename = None
            self.ds_roi = [0, 0, 0, 0]

        etalon_data = ds_group['etalon_spectrum'][...]
        self.ds_temperature_model.calibration_parameter.set_etalon_spectrum(Spectrum(etalon_data[0, :],
                                                                                     etalon_data[1, :]))

        try:
            self.ds_temperature_model.calibration_parameter.etalon_file_name = \
                ds_group['etalon_spectrum'].attrs['filename'].decode('utf-8')
        except AttributeError:
            self.ds_temperature_model.calibration_parameter.etalon_file_name = \
                ds_group['etalon_spectrum'].attrs['filename']

        modus = ds_group['modus'][...]
        self.ds_temperature_model.calibration_parameter.set_modus(modus)
        temperature = ds_group['temperature'][...]
        self.ds_temperature_model.calibration_parameter.set_temperature(temperature)

        us_group = f['upstream_calibration']
        if 'image' in us_group:
            self.us_temperature_model.set_calibration_data(us_group['image'][...],
                                                           us_group['image'].attrs['x_calibration'][...])
            try:
                self.us_calibration_filename = us_group['image'].attrs['filename'].decode('utf-8')
            except AttributeError:
                self.us_calibration_filename = us_group['image'].attrs['filename']
            img_dimension = (self.us_temperature_model.calibration_img.shape[1],
                             self.us_temperature_model.calibration_img.shape[0])
            self.roi_data_manager.set_roi(1, img_dimension, us_group['roi'][...])
            self.us_temperature_model._update_all_spectra()
        else:
            self.us_temperature_model.reset_calibration_data()
            self.us_calibration_filename = None
            self.us_roi = [0, 0, 0, 0]

        etalon_data = us_group['etalon_spectrum'][...]
        self.us_temperature_model.calibration_parameter.set_etalon_spectrum(Spectrum(etalon_data[0, :],
                                                                                     etalon_data[1, :]))
        try:
            self.us_temperature_model.calibration_parameter.etalon_file_name = \
                us_group['etalon_spectrum'].attrs['filename'].decode('utf-8')
        except AttributeError:
            self.us_temperature_model.calibration_parameter.etalon_file_name = \
                us_group['etalon_spectrum'].attrs['filename']

        self.us_temperature_model.calibration_parameter.set_modus(us_group['modus'][...])
        self.us_temperature_model.calibration_parameter.set_temperature(us_group['temperature'][...])

        self.ds_temperature_model._update_all_spectra()
        self.us_temperature_model._update_all_spectra()

        self.ds_temperature_model.fit_data()
        self.us_temperature_model.fit_data()

        self.us_calculations_changed.emit()
        self.ds_calculations_changed.emit()
        self.data_changed.emit()

    def save_txt(self, filename):
        """
        Saves the fitted temperatures, original spectra and fitted spectra into a txt file
        Format:
            Header
                Downstream (K): temperatures...
                Upstream (K): temperatures...
            column names:
            lambda(nm), DS_data, DS_fit, US_data, US_fit, ....

        if the original spe file contains several frames, all frames will be saved in order with always data and then
        fit.
        :param filename: path to save the file to
        :return:
        """

        # creating the header:
        header = "Fitted Temperatures:\n"
        header += "Downstream (K): {:.1f}\t{:.1f}\n".format(self.ds_temperature, self.ds_temperature_error)
        header += "Upstream (K): {:.1f}\t{:.1f}\n\n".format(self.us_temperature, self.us_temperature_error)
        header += "Datacolumns:\n"
        header_ds = header + "\t".join(("lambda(nm)", "DS_data", "DS_fit"))
        header_us = header + "\t".join(("lambda(nm)", "US_data", "US_fit"))

        output_matrix_ds = np.vstack((self.ds_data_spectrum.x,
                                      self.ds_corrected_spectrum.y, self.ds_fit_spectrum.y))

        output_matrix_us = np.vstack((self.us_data_spectrum.x,
                                      self.us_corrected_spectrum.y, self.us_fit_spectrum.y))

        ds_filename = filename.rsplit('.', 1)[0] + '_ds.txt'
        us_filename = filename.rsplit('.', 1)[0] + '_us.txt'

        np.savetxt(ds_filename, output_matrix_ds.T, header=header_ds)
        np.savetxt(us_filename, output_matrix_us.T, header=header_us)

    # updating roi values
    @property
    def ds_roi(self):
        try:
            return self.roi_data_manager.get_roi(0, self.data_img_file.get_dimension())
        except AttributeError:
            return Roi([0, 0, 0, 0])

    @ds_roi.setter
    def ds_roi(self, ds_limits):
        self.roi_data_manager.set_roi(0, self.data_img_file.get_dimension(), ds_limits)
        self.ds_temperature_model._update_all_spectra()
        self.ds_temperature_model.fit_data()
        self.ds_calculations_changed.emit()

    @property
    def us_roi(self):
        try:
            return self.roi_data_manager.get_roi(1, self.data_img_file.get_dimension())
        except:
            return Roi([0, 0, 0, 0])

    @us_roi.setter
    def us_roi(self, us_limits):
        self.roi_data_manager.set_roi(1, self.data_img_file.get_dimension(), us_limits)
        self.us_temperature_model._update_all_spectra()
        self.us_temperature_model.fit_data()
        self.us_calculations_changed.emit()

    def set_rois(self, ds_limits, us_limits):
        self.us_roi = us_limits
        self.ds_roi = ds_limits

    def get_roi_data_list(self):
        ds_roi = self.ds_roi.as_list()
        us_roi = self.us_roi.as_list()
        return [ds_roi, us_roi]

    # Spectrum interfaces
    #########################################################
    @property
    def ds_data_spectrum(self):
        return self.ds_temperature_model.data_spectrum

    @property
    def us_data_spectrum(self):
        return self.us_temperature_model.data_spectrum

    @property
    def ds_calibration_spectrum(self):
        return self.ds_temperature_model.calibration_spectrum

    @property
    def us_calibration_spectrum(self):
        return self.us_temperature_model.calibration_spectrum

    @property
    def ds_corrected_spectrum(self):
        return self.ds_temperature_model.corrected_spectrum

    @property
    def us_corrected_spectrum(self):
        return self.us_temperature_model.corrected_spectrum

    @property
    def ds_fit_spectrum(self):
        return self.ds_temperature_model.fit_spectrum

    @property
    def us_fit_spectrum(self):
        return self.us_temperature_model.fit_spectrum

    # temperature_properties

    @property
    def ds_temperature(self):
        return self.ds_temperature_model.temperature

    @property
    def us_temperature(self):
        return self.us_temperature_model.temperature

    @property
    def ds_temperature_error(self):
        return self.ds_temperature_model.temperature_error

    @property
    def us_temperature_error(self):
        return self.us_temperature_model.temperature_error

    @property
    def ds_etalon_filename(self):
        return self.ds_temperature_model.calibration_parameter.etalon_file_name

    @property
    def us_etalon_filename(self):
        return self.us_temperature_model.calibration_parameter.etalon_file_name

    @property
    def ds_roi_max(self):
        return self.ds_temperature_model.data_roi_max

    @property
    def us_roi_max(self):
        return self.us_temperature_model.data_roi_max

    # TODO: Think aboout refactoring this function away from here
    def get_wavelength_from(self, index):
        return self.data_img_file.get_wavelength_from(index)

    def get_index_from(self, wavelength):
        return self.data_img_file.get_index_from(wavelength)

    def get_x_limits(self):
        return np.array([self.data_img_file.x_calibration[0], self.data_img_file.x_calibration[-1]])

    def fit_all_frames(self):
        if self.data_img_file is None:
            return [], [], [], []

        if self.data_img_file.num_frames == 1:
            return [], [], [], []

        cur_frame = self.current_frame
        self.blockSignals(True)

        us_temperature = []
        ds_temperature = []

        us_temperature_error = []
        ds_temperature_error = []

        for frame_ind in range(self.data_img_file.num_frames):
            self.set_img_frame_number_to(frame_ind)
            # self.fit_data()
            us_temperature.append(self.us_temperature)
            ds_temperature.append(self.ds_temperature)

            us_temperature_error.append(self.us_temperature_error)
            ds_temperature_error.append(self.ds_temperature_error)

        self.set_img_frame_number_to(cur_frame)
        self.blockSignals(False)

        return us_temperature, us_temperature_error, ds_temperature, ds_temperature_error


class SingleTemperatureModel(QtCore.QObject):
    data_changed = QtCore.Signal()

    def __init__(self, ind, roi_data_manager):
        super(SingleTemperatureModel, self).__init__()
        self.ind = ind

        self.data_spectrum = Spectrum([], [])
        self.calibration_spectrum = Spectrum([], [])
        self.corrected_spectrum = Spectrum([], [])

        self._data_img = None
        self._data_img_x_calibration = None
        self._data_img_dimension = None

        self.data_roi_max = 0

        self.roi_data_manager = roi_data_manager

        self._calibration_img = None
        self._calibration_img_x_calibration = None
        self._calibration_img_dimension = None

        self.calibration_parameter = CalibrationParameter()

        self.temperature = np.NaN
        self.temperature_error = np.NaN
        self.fit_spectrum = Spectrum([], [])

    @property
    def data_img(self):
        return self._data_img

    def set_data(self, img_data, x_calibration):
        self._data_img = img_data
        self._data_img_x_calibration = x_calibration
        self._data_img_dimension = (img_data.shape[1], img_data.shape[0])

        self._update_data_spectrum()
        self._update_corrected_spectrum()
        self.fit_data()
        self.data_changed.emit()

    @property
    def calibration_img(self):
        return self._calibration_img

    def set_calibration_data(self, img_data, x_calibration):
        self._calibration_img = img_data
        self._calibration_img_x_calibration = x_calibration
        self._calibration_img_dimension = (img_data.shape[1], img_data.shape[0])

        self._update_calibration_spectrum()
        self._update_corrected_spectrum()
        self.fit_data()
        self.data_changed.emit()

    def reset_calibration_data(self):
        self._calibration_img = None
        self._calibration_img_x_calibration = None
        self._calibration_img_dimension = None

        self.calibration_spectrum = Spectrum([], [])
        self.corrected_spectrum = Spectrum([], [])
        self.fit_spectrum = Spectrum([], [])

        self.temperature = np.NaN
        self.temperature_error = np.NaN
        self.fit_spectrum = Spectrum([], [])
        self.data_changed.emit()

    # setting etalon interface
    #########################################################################
    def load_etalon_spectrum(self, filename):
        self.calibration_parameter.load_etalon_spectrum(filename)
        self._update_all_spectra()
        self.fit_data()
        self.data_changed.emit()

    def set_calibration_modus(self, modus):
        self.calibration_parameter.set_modus(modus)
        self._update_all_spectra()
        self.fit_data()
        self.data_changed.emit()

    def set_calibration_temperature(self, temperature):
        self.calibration_parameter.set_temperature(temperature)
        self._update_all_spectra()
        self.fit_data()
        self.data_changed.emit()

    # Spectrum calculations
    #########################################################################

    def _update_data_spectrum(self):
        if self._data_img is not None:
            roi = self.roi_data_manager.get_roi(self.ind, self._data_img_dimension)

            data_x = self._data_img_x_calibration[int(roi.x_min):int(roi.x_max) + 1]
            data_y = get_roi_sum(self.data_img, roi)

            self.data_roi_max = get_roi_max(self.data_img, roi)
            self.data_spectrum.data = data_x, data_y

    def _update_calibration_spectrum(self):
        if self.calibration_img is not None:
            roi = self.roi_data_manager.get_roi(self.ind, self._calibration_img_dimension)

            calibration_x = self._calibration_img_x_calibration[int(roi.x_min):int(roi.x_max) + 1]
            calibration_y = get_roi_sum(self._calibration_img, roi)

            self.calibration_spectrum.data = calibration_x, calibration_y

    def _update_corrected_spectrum(self):
        if len(self.data_spectrum) is 0:
            self.corrected_spectrum = Spectrum([], [])
            return

        if len(self.calibration_spectrum) == len(self.data_spectrum):
            x, _ = self.data_spectrum.data
            lamp_spectrum = self.calibration_parameter.get_lamp_spectrum(x)
            self.corrected_spectrum = calculate_real_spectrum(self.data_spectrum,
                                                              self.calibration_spectrum,
                                                              lamp_spectrum)
        else:
            self.corrected_spectrum = Spectrum([], [])

    def _update_all_spectra(self):
        self._update_data_spectrum()
        self._update_calibration_spectrum()
        self._update_corrected_spectrum()

    # finally the fitting function
    ##################################################################
    def fit_data(self):
        if len(self.corrected_spectrum):
            self.temperature, self.temperature_error, self.fit_spectrum = \
                fit_black_body_function(self.corrected_spectrum)
        else:
            self.temperature = np.NaN
            self.temperature_error = np.NaN
            self.fit_spectrum = Spectrum([], [])


# HELPER FUNCTIONS
###############################################
###############################################

def calculate_real_spectrum(data_spectrum, calibration_spectrum, etalon_spectrum):
    response_y = calibration_spectrum._y / etalon_spectrum._y
    response_y[np.where(response_y == 0)] = np.NaN
    corrected_y = data_spectrum._y / response_y
    corrected_y = corrected_y / np.max(corrected_y) * np.max(data_spectrum._y)
    return Spectrum(data_spectrum._x, corrected_y)


def fit_black_body_function(spectrum):
    try:
        param, cov = curve_fit(black_body_function, spectrum._x, spectrum._y, p0=[2000, 1e-11])
        T = param[0]
        T_err = np.sqrt(cov[0, 0])

        return T, T_err, Spectrum(spectrum._x, black_body_function(spectrum._x, param[0], param[1]))
    except (RuntimeError, TypeError, ValueError):
        return np.NaN, np.NaN, Spectrum([], [])


def black_body_function(wavelength, temp, scaling):
    wavelength = np.array(wavelength) * 1e-9
    c1 = 3.7418e-16
    c2 = 0.014388
    return scaling * c1 * wavelength ** -5 / (np.exp(c2 / (wavelength * temp)) - 1)


class CalibrationParameter(object):
    def __init__(self, modus=0):
        self.modus = modus
        # modi: 0 - given temperature
        # 1 - etalon spectrum

        self.temperature = 2000
        self.etalon_spectrum_func = None
        self._etalon_x = np.array([])
        self._etalon_y = np.array([])
        self.etalon_file_name = 'Select File...'

    def set_modus(self, modus):
        self.modus = modus

    def set_temperature(self, temperature):
        self.temperature = temperature

    def load_etalon_spectrum(self, filename):
        try:
            data = np.loadtxt(filename, delimiter=',')
        except ValueError:
            try:
                data = np.loadtxt(filename, delimiter=' ')
            except ValueError:
                try:
                    data = np.loadtxt(filename, delimiter=';')
                except ValueError:
                    data = np.loadtxt(filename, delimiter='\t')
        self._etalon_x = data.T[0]
        self._etalon_y = data.T[1]

        self.etalon_file_name = filename

    def get_lamp_y(self, wavelength):
        if self.modus == 0:
            y = black_body_function(wavelength, self.temperature, 1)
            return y / max(y)
        elif self.modus == 1:
            try:
                # return self.etalon_spectrum_func(wavelength)
                # not used because scipy.interpolate is supported by pyinstaller...
                return np.interp(wavelength, self._etalon_x, self._etalon_y)
            except ValueError:
                return np.ones(np.size(wavelength))

    def get_lamp_spectrum(self, wavelength):
        return Spectrum(wavelength, self.get_lamp_y(wavelength))

    def get_etalon_filename(self):
        return self.etalon_file_name

    def set_etalon_filename(self, filename):
        self.etalon_file_name = filename

    def get_etalon_spectrum(self):
        return Spectrum(self._etalon_x, self._etalon_y)

    def set_etalon_spectrum(self, spectrum):
        try:
            self._etalon_x = spectrum.x
            self._etalon_y = spectrum.y
        except AttributeError:
            pass
