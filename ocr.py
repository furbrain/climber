import easyocr
import cv2
import numpy as np

import form
from person import Person

DPI = 300


class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.bounds = None
        self.read_file("blank.jpg")
        self.target_size = tuple(reversed(self.image.shape))
        self.reference_points = self.find_circles()
        self.bounds = self.get_bounds()
        self.display = False
        self.image = None
        self.image_points = None
        self.thresholded = None

    def set_display(self):
        self.display = True
        cv2.namedWindow("main", cv2.WINDOW_NORMAL)

    @staticmethod
    def point_angle(point):
        x = point[0] - 1500
        y = point[1] - 1500
        return np.arctan2(x, y)

    def read_file(self, fname):
        self.image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        return self.image

    def map_image(self):
        if self.display:
            cv2.imshow("main", self.image)
            cv2.waitKey(0)
        self.image_points = self.find_circles()
        h = cv2.getPerspectiveTransform(self.image_points, self.reference_points)
        self.image = cv2.warpPerspective(self.image, h, self.target_size)
        self.thresholded = cv2.warpPerspective(self.thresholded, h, self.target_size)
        if self.display:
            results = self.draw_bounds()
            cv2.imwrite("results.png", results)
            cv2.imshow("main", results)
            cv2.waitKey(0)

    @staticmethod
    def is_circle(contour):
        area = cv2.contourArea(contour)
        return 3000 < area < 100000

    @staticmethod
    def get_centroid(contour):
        m = cv2.moments(contour)
        centroid = ((m['m10'] / m['m00']), (m['m01'] / m['m00']))
        return centroid

    def find_circles(self):
        ret, self.thresholded = cv2.threshold(self.image, 160, 255, cv2.THRESH_BINARY)
        image = cv2.dilate(self.thresholded, kernel=self.kernel, iterations=2)
        image = cv2.erode(image, kernel=self.kernel, iterations=2)
        # blank out uninteresting bits of image...
        image[600:-600, :] = 255
        image[:, 600:-600] = 255
        contours, hierarchy = cv2.findContours(
            image,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)
        centroids = [self.get_centroid(c) for c in contours if self.is_circle(c)]
        centroids = sorted(centroids, key=self.point_angle)
        if len(centroids)!=4:
            raise ValueError("Number of circles found incorrect: %d (" % len(centroids))
        return np.array(centroids, dtype="float32")

    def has_mark(self, rect):
        test_area = self.thresholded[rect[2]:rect[3], rect[0]:rect[1]]
        dark_prop = 1 - (np.count_nonzero(test_area) / ((rect[1] - rect[0]) * (rect[3] - rect[2])))
        return dark_prop > 0.025

    def draw_bounds(self):
        copy = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        for rects in self.get_bounds():
            for rect in rects:
                a = (rect[0], rect[2])
                b = (rect[1], rect[3])
                cv2.rectangle(copy, pt1=a, pt2=b, color=(0, 0, 255))
        return copy

    @staticmethod
    def get_bounds():
        bounds = form.DataEntryPDF.get_bounds()
        bounds[:, :, 0:2] += 0.5
        bounds[:, :, 2:4] -= 0.5
        boxes = bounds.copy()
        boxes[:, :, 1] = bounds[:, :, 2]
        boxes[:, :, 2] = bounds[:, :, 1]
        boxes *= DPI / 25.4
        bounds = boxes.astype("int")
        return bounds

    def read_times(self):
        times = self.reader.recognize(self.image, list(self.bounds[1:, 0, :]), free_list=[], allowlist="0123456789:",
                                      detail=0)
        return times

    def read_names(self):
        names = self.reader.recognize(self.image, list(self.bounds[1:, 1, :]), free_list=[], detail=0)
        return names

    def read_dobs(self):
        dobs = self.reader.recognize(self.image, list(self.bounds[1:, 2, :]), allowlist="0123456789-", free_list=[],
                                     detail=0)
        return dobs

    def read_nhs_nums(self):
        nhss = self.reader.recognize(self.image, list(self.bounds[1:, 3, :]), allowlist="0123456789", free_list=[],
                                     detail=0)
        return nhss

    def get_images(self):
        tls = self.bounds[1:, 0, 0:3:2] - 5
        brs = self.bounds[1:, 10, 1:4:2] + 5
        results = []
        for ((x1, y1), (x2, y2)) in zip(tls, brs):
            img = self.image[y1:y2, x1:x2]
            img = cv2.pyrDown(img)
            results.append(cv2.imencode(".png", img)[1])
        return results

    def get_vaccinators(self):
        vaccinators = self.reader.recognize(self.image, list(self.bounds[0, 4:, :]), free_list=[], detail=0)
        return vaccinators

    def get_marks(self):
        results = []
        copy = cv2.cvtColor(self.thresholded, cv2.COLOR_GRAY2BGR)
        for row in self.bounds[1:, 4:, :]:
            indices = []
            for i, rect in enumerate(row):
                found = self.has_mark(rect)
                a = (rect[0], rect[2])
                b = (rect[1], rect[3])
                if found:
                    indices.append(i)
                    if self.display:
                        cv2.rectangle(copy, pt1=a, pt2=b, color=(0, 255, 0), thickness=3)
                else:
                    if self.display:
                        cv2.rectangle(copy, pt1=a, pt2=b, color=(0, 0, 255), thickness=3)
            results.append(indices)
        if self.display:
            cv2.imshow("main", copy)
            cv2.waitKey(0)
        return results

    def get_all_details(self, fname, vaccinators):
        self.read_file(fname)
        self.map_image()
        dobs = self.read_dobs()
        nhss = self.read_nhs_nums()
        boxes = self.get_marks()
        images = self.get_images()
        people = [Person(dob=d, nhs=n, status="scanned", image=i.tobytes()) for d, n, i in zip(dobs, nhss, images) if
                  d != "" or n != ""]
        for p, b in zip(people, boxes):
            if len(b) == 0:
                p.set_error("No boxes ticked (DNA?)")
            elif len(b) == 1:
                if b[0] >= len(vaccinators):
                    p.set_error("Invalid box ticked")
                else:
                    p.vaccinator = vaccinators[b[0]]
            else:
                p.set_error("Too many boxes ticked")
        return people


ocrreader = OCR()
