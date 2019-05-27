#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import matplotlib.pyplot as plt
import math
from numpy import linalg as la

MAP = "newmaze"
MODE = 1

class LidarMethodsComparing():

    def __init__(self):
        if MODE:
            self.gmapping_data = self.load_gmapping(MAP)
            self.hector_data = self.load_hector()
            self.ground_truth = self.load_ground_truth(0)
            self.cartographer_data = self.load_cartographer()
        else:
            self.gmap = self.load_gmapping("mit_def_new")
            self.gmap1_1 = self.load_gmapping("mit_1_1_new")
            self.gmap1_2 = self.load_gmapping("mit_1_2_new")
            self.gmap1_3 = self.load_gmapping("mit_1_3_new")
            self.gmap1_4 = self.load_gmapping("mit_1_4_new")
            self.gmap2_1 = self.load_gmapping("mit_2_1_new")
            self.gmap2_2 = self.load_gmapping("mit_2_2")
            self.gmap2_3 = self.load_gmapping("mit_2_3")
            self.gmap2_4 = self.load_gmapping("mit_2_4")
            self.gmap3_1 = self.load_gmapping("mit_3_1")
            self.gmap3_2 = self.load_gmapping("mit_3_2")
            self.gmap3_3 = self.load_gmapping("mit_3_3_new")
            self.gmap3_4 = self.load_gmapping("mit_3_4")
            self.ground_truth = self.load_ground_truth(1)
            self.num = 0
        self.comparison()

    def comparison(self):
        if MODE:
            print ''
            print 'Porovnání cartographer...'
            self.square_error_comparison(self.cartographer_data)
            self.compare_methods(self.cartographer_data)
            print 'Porovnání gMapping...'
            self.square_error_comparison(self.gmapping_data)
            self.compare_methods(self.gmapping_data)
            print 'Porovnání Hector...'
            self.square_error_comparison(self.hector_data)
            self.compare_methods(self.hector_data)
            self.plot_method(self.cartographer_data, self.ground_truth, self.gmapping_data, self.hector_data)
        else:
            print ''
            #print 'Porovnání gMapping default'
            #self.square_error_comparison(self.gmap)
            #self.compare_methods(self.gmap)
            #print 'Porovnání gMapping 1-1...'
            #elf.square_error_comparison(self.gmap1_1)
            #self.compare_methods(self.gmap1_1)
            #rint 'Porovnání gMapping 1-2...'
            #self.square_error_comparison(self.gmap1_2)
            #self.compare_methods(self.gmap1_2)
            #rint 'Porovnání gMapping 1-3...'
            #self.square_error_comparison(self.gmap1_3)
            #self.compare_methods(self.gmap1_3)
            #print 'Porovnání gMapping 1-4...'
            #self.square_error_comparison(self.gmap1_4)
            #self.compare_methods(self.gmap1_4)
            #print 'Porovnání gMapping 2-1...'
            #self.square_error_comparison(self.gmap2_1)
            #self.compare_methods(self.gmap2_1)
            #rint 'Porovnání gMapping 2-2...'
            #elf.square_error_comparison(self.gmap2_2)
            #self.compare_methods(self.gmap2_2)
            #print 'Porovnání gMapping 2-3...'
            #self.square_error_comparison(self.gmap2_3)
            #self.compare_methods(self.gmap2_3)
            #print 'Porovnání gMapping 2-4...'
            #self.square_error_comparison(self.gmap2_4)
            #self.compare_methods(self.gmap2_4)
            #print 'Porovnání gMapping 3-1...'
            #self.square_error_comparison(self.gmap3_1)
            #elf.compare_methods(self.gmap3_1)
            #print 'Porovnání gMapping 3-2...'
            #self.square_error_comparison(self.gmap3_2)
            #elf.compare_methods(self.gmap3_2)
            #rint 'Porovnání gMapping 3-3...'
            #elf.square_error_comparison(self.gmap3_3)
            #elf.compare_methods(self.gmap3_3)
            #rint 'Porovnání gMapping 3-4...'
            #elf.square_error_comparison(self.gmap3_4)
            #elf.compare_methods(self.gmap3_4)
            self.plot_method(self.gmap1_1, self.gmap1_2, self.gmap1_3, self.gmap1_4, self.gmap, self.ground_truth)
            self.num += 1
            self.plot_method(self.gmap2_1, self.gmap2_2, self.gmap2_3, self.gmap2_4, self.gmap, self.ground_truth)
            self.num += 1
            self.plot_method(self.gmap3_1, self.gmap3_2, self.gmap3_3, self.gmap3_4, self.gmap, self.ground_truth)

        pass

    def plot_method(self, data1, data2, data3, data4, data5=None, data6=None):
        if MODE:
            plt.plot(data2[0], data2[1], label='ground truth')
            plt.plot(data3[0], data3[1], label='gmapping')
            plt.plot(data4[0], data4[1], label='hector')
            plt.plot(data1[0], data1[1], label='cartographer')
        else:
            if self.num != 1:
                plt.plot(data1[0], data1[1], label='settings 1')
                plt.plot(data2[0], data2[1], label='settings 2')
                plt.plot(data5[0], data5[1], label='settings 3')
                plt.plot(data3[0], data3[1], label='settings 4')
                plt.plot(data4[0], data4[1], label='settings 5')
                plt.plot(data6[0], data6[1], label='ground truth')
            else:
                plt.plot(data2[0], data2[1], label='settings 1')
                plt.plot(data5[0], data5[1], label='settings 2')
                plt.plot(data4[0], data4[1], label='settings 3')
                plt.plot(data6[0], data6[1], label='ground truth')
        plt.legend()
        plt.show()


    def square_error_comparison(self, met):
        index = 0
        diff = 0
        num = 0
        for i in range(len(met[0]) - 1):
            for j in range(len(self.ground_truth[2])):
                if self.ground_truth[2][j] == met[2][i]:
                    index = j
                    num += 1
                    break
            x = [met[0][i] - self.ground_truth[0][index], met[1][i] - self.ground_truth[1][index]]
            norm_x = la.norm(x)
            diff += math.pow(norm_x, 2)
        overall_diff = math.sqrt(diff/num)
        print "square error: ", overall_diff

    def compare_methods(self, met):
        index2 = 0
        position_diff = []
        rotation_diff = []
        rotation_diff_overall = 0
        position_diff_overall = 0
        num = 0
        for i in range(len(met[0])-1):
            index1 = index2
            for j in range(len(self.ground_truth[2])):
                if self.ground_truth[2][j] == met[2][i+1]:
                    index2 = j
                    num += 1
                    break
            rot_diff_met = abs(met[4][i+1] - met[4][i])
            rot_diff_ground_truth = abs(self.ground_truth[4][index2] - self.ground_truth[4][index1])
            rot_diff_mutually = abs(rot_diff_met - rot_diff_ground_truth)
            rot_diff_value = min(2*math.pi-rot_diff_mutually, rot_diff_mutually)
            rotation_diff.append(rot_diff_value)

            x = [(met[0][i + 1] - met[0][i]) - (self.ground_truth[0][index2] - self.ground_truth[0][index1]),
                    (met[1][i + 1] - met[1][i]) - (self.ground_truth[1][index2] - self.ground_truth[1][index1])]
            norm_x = la.norm(x)
            position_diff.append(norm_x)
            rotation_diff_overall += math.pow(rot_diff_value, 2)
            position_diff_overall += math.pow(norm_x, 2)
        rotation_diff_overall = rotation_diff_overall / (num-1)
        position_diff_overall = position_diff_overall / (num-1)
        print 'Chyba orientace robota: ', rotation_diff_overall
        print 'Chyba určení polohy robota: ', position_diff_overall
        overall_difference = rotation_diff_overall + position_diff_overall
        print 'Chyba určení stavu robota: ', overall_difference
        print ''

    def angle_transform(self, data):
        angles = []
        for i in data:
            angles.append(i*2*math.pi-math.pi)
        return angles

    def load_cartographer(self):
        with open('cartographer_'+MAP+'.txt') as cart_file:
            axe_x = []
            axe_y = []
            processed_time = []
            orientation_z = []
            orientation_w = []
            for row in cart_file:
                values = row.split(',')
                axe_x.append(float(values[5]))
                axe_y.append(float(values[6]))
                processed_time.append(float(values[0])/1000000000)
                orientation_z.append(float(values[10]))
                orientation_w.append(float(values[11]))
            for i in range(len(processed_time)):
                processed_time[i] += 0.05
                processed_time[i] = float(int(processed_time[i]*10))/10

            orientation_w = self.angle_transform(orientation_w)
            data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
            return data

    def load_gmapping(self, data):
        with open('gmapping_'+data+'.txt') as gmap_file:
            help_x = 0
            number_x = 0
            number_y = 0
            axe_x = []
            help_y = 0
            axe_y = []
            sim_time = []
            time_of_stamp = ''
            orientation_z = []
            orientation_w = []
            help_z = 0
            number_z = 0
            number_w = 0
            for row in gmap_file:
                try:
                    if row[10] is 'x':
                        if help_x == 0:
                            help_x = (help_x + 1) % 2
                            x_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[26] is 'e' or row[27] is 'e':
                                    x_value = x_value / 100000
                            except Exception:
                                pass
                            axe_x.append(x_value)
                            number_x += 1
                        else:
                            help_x = (help_x + 1) % 2
                    if row[10] is 'y':
                        if help_y == 0:
                            help_y = (help_y + 1) % 2
                            y_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[26] is 'e' or row[27] is 'e':
                                    y_value = y_value / 100000
                            except Exception:
                                pass
                            axe_y.append(y_value)
                            number_y += 1
                        else:
                            help_y = (help_y + 1) % 2
                    if row[10] is 's':
                        time_of_stamp = ''
                        time_of_stamp = re.findall(r"\d+", row)[0] + '.'
                    if row[10] is 'n':
                        time_of_stamp = time_of_stamp + re.findall(r"\d+", row)[0]
                        time_of_stamp = int(float(time_of_stamp)*10)
                        sim_time.append(time_of_stamp)
                    if row[10] is 'z':
                        if help_z == 1:
                            help_z = (help_z + 1) % 2
                            z_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    z_value = z_value / 100000
                            except Exception:
                                pass
                            orientation_z.append(z_value)
                            number_z += 1
                        else:
                            help_z = (help_z + 1) % 2
                    if row[10] is 'w':
                        w_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                        try:
                            if row[20] is 'e' or row[21] is 'e':
                                w_value = w_value / 100000
                        except Exception:
                            pass
                        orientation_w.append(w_value)
                        number_w += 1
                except Exception:
                    pass

        processed_time = []
        for time_stamp in sim_time:
            time_stamp = float(time_stamp) / 10
            processed_time.append(time_stamp)
        orientation_w = self.angle_transform(orientation_w)
        data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
        return data

    def load_hector(self):
        # with open('hector_traj_ground.txt') as gmap_file:
        with open('hector_'+MAP+'.txt') as hector_file:
            help_x = 0
            number_x = 0
            number_y = 0
            axe_x = []
            help_y = 0
            axe_y = []
            sim_time = []
            time_of_stamp = ''
            orientation_z = []
            orientation_w = []
            help_z = 0
            number_z = 0
            number_w = 0
            for row in hector_file:
                try:
                    if row[4] is 'x':
                        if help_x == 0:
                            help_x = (help_x + 1) % 2
                            x_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    x_value = x_value / 100000
                            except Exception:
                                pass
                            axe_x.append(x_value)
                            number_x += 1
                        else:
                            help_x = (help_x + 1) % 2
                    if row[4] is 'y':
                        if help_y == 0:
                            help_y = (help_y + 1) % 2
                            y_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    y_value = y_value / 100000
                            except Exception:
                                pass
                            axe_y.append(y_value)
                            number_y += 1
                        else:
                            help_y = (help_y + 1) % 2
                    if row[4] is 's':
                        time_of_stamp = ''
                        time_of_stamp = re.findall(r"\d+", row)[0] + '.'
                    if row[4] is 'n':
                        time_of_stamp = time_of_stamp + re.findall(r"\d+", row)[0]
                        time_of_stamp = int(float(time_of_stamp) * 10)
                        sim_time.append(time_of_stamp)
                    if row[4] is 'z':
                        if help_z == 1:
                            help_z = (help_z + 1) % 2
                            z_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    z_value = z_value / 100000
                            except Exception:
                                pass
                            orientation_z.append(z_value)
                            number_z += 1
                        else:
                            help_z = (help_z + 1) % 2
                    if row[4] is 'w':
                        w_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                        try:
                            if row[20] is 'e' or row[21] is 'e':
                                w_value = w_value / 100000
                        except Exception:
                            pass
                        orientation_w.append(w_value)
                        number_w += 1
                except Exception:
                    pass
        processed_time = []
        for time_stamp in sim_time:
            time_stamp = float(time_stamp) / 10
            processed_time.append(time_stamp)
        orientation_w = self.angle_transform(orientation_w)
        data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
        return data

    def load_ground_truth(self, mode):
        with open('ground_truth_'+MAP+'.txt') as ground_file:
            help_x = 0
            number_x = 0
            number_y = 0
            axe_x = []
            help_y = 0
            axe_y = []
            sim_time = []
            time_of_stamp = ''
            orientation_z = []
            orientation_w = []
            help_z = 0
            number_z = 0
            number_w = 0
            if mode == 0:
                for row in ground_file:
                    try:
                        if row[6] is 'x':
                            if help_x == 0:
                                help_x = (help_x + 1) % 4
                                x_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                                try:
                                    if row[26] is 'e' or row[22] is 'e':
                                        x_value = x_value / 100000
                                except Exception:
                                    pass
                                axe_x.append(x_value)
                                number_x += 1
                            else:
                                help_x = (help_x + 1) % 4
                        if row[6] is 'y':
                            if help_y == 0:
                                help_y = (help_y + 1) % 4
                                axe_y.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                                number_y += 1
                            else:
                                help_y = (help_y + 1) % 4
                        if row[4] is 's':
                            time_of_stamp = ''
                            time_of_stamp = re.findall(r"\d+", row)[0] + '.'
                        if row[4] is 'n':
                            time_of_stamp = time_of_stamp + re.findall(r"\d+", row)[0]
                            time_of_stamp = int(float(time_of_stamp)*10)
                            sim_time.append(time_of_stamp)
                        if row[6] is 'z':
                            if help_z == 1:
                                help_z = (help_z + 1) % 4
                                z_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                                orientation_z.append(z_value)
                                number_z += 1
                            else:
                                help_z = (help_z + 1) % 4
                        if row[6] is 'w':
                            w_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            orientation_w.append(w_value)
                            number_w += 1
                    except Exception:
                        pass
                axe_x_0 = axe_x[0]
                axe_y_0 = axe_y[0]
                for i in range(len(axe_x)):
                    axe_x[i] -= axe_x_0
                    axe_y[i] -= axe_y_0
                processed_time = []
                for time_stamp in sim_time:
                    time_stamp = float(time_stamp) / 10
                    processed_time.append(time_stamp)
                orientation_w = self.angle_transform(orientation_w)
                data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
                return data

            else:
                processed_time = []
                for row in ground_file:
                    values = row.split(',')
                    axe_x.append(float(values[1]))
                    axe_y.append(float(values[2]))
                    processed_time.append(float(values[0]) / 1000000)
                    orientation_z.append(0)
                    orientation_w.append(float(values[3]))
                start_x = axe_x[0]
                start_y = axe_y[0]
                diff_w = math.pi - orientation_w[0]
                s = math.sin(diff_w)
                c = math.cos(diff_w)
                for i in range(len(processed_time)):
                    processed_time[i] += 0.05
                    processed_time[i] = float(int(processed_time[i] * 10)) / 10
                    axe_x[i] -= start_x
                    axe_y[i] -= start_y
                    tmp_diff = orientation_w[i] + diff_w
                    if tmp_diff > math.pi:
                        tmp_diff = -2*math.pi + tmp_diff
                    orientation_w[i] = tmp_diff
                    axe_x[i] = -(axe_x[i]*c - axe_y[i]*s)
                    axe_y[i] = -(axe_x[i]*s + axe_y[i]*c)
                data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
                return data


def main():
    LidarMethodsComparing()


if __name__ == '__main__':
    main()
