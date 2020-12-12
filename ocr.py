import dateutil.parser
import easyocr
import cv2
import numpy as np

import form
import sessions

DPI=300

class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        self.bounds = None

    def read_file(self, fname):
        self.image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        return self.image

    def find_circles(self, image):
        original = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
        cv2.imshow("main", image)
        cv2.waitKey(0)
        image = cv2.dilate(image, kernel=self.kernel, iterations=2)
        image = cv2.erode(image, kernel=self.kernel, iterations=2)
        cv2.imshow("main", image)
        cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(
            image,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)
        new_contours = []
        centroids = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000 and area < 100000:
                m = cv2.moments(contour)
                centroid = ((m['m10']/m['m00']),(m['m01']/m['m00']))
                centroids.append(centroid)
                new_contours.append(contour)
        print(centroids)
        cv2.drawContours(original, new_contours, -1, color=(255,0,0))
        for c in centroids:
            c = (int(c[0]), int(c[1]))
            cv2.drawMarker(original, c, color=(0,255,0), markerSize=10)
        for rects in self.get_bounds():
            for rect in rects:
                a = (rect[0], rect[2])
                b = (rect[1], rect[3])
                cv2.rectangle(original, pt1=a, pt2=b, color=(0,0,255))
        cv2.imshow("main", original)
        cv2.waitKey(0)
        return centroids

    def get_bounds(self):
        if self.bounds is None:
            bounds = form.PDF.get_bounds()
            bounds[:, :, 0:2] += 0.5
            bounds[:, :, 2:4] -= 0.5
            boxes = bounds.copy()
            boxes[:, :, 1] = bounds[:, :, 2]
            boxes[:, :, 2] = bounds[:, :, 1]
            boxes *= DPI / 25.4
            self.bounds = boxes.astype("int")
        return self.bounds

    def read_times(self):
        bounds = self.get_bounds()
        times = self.reader.recognize(self.image, list(bounds[1:,0,:]), free_list=[], allowlist="0123456789:", detail=0)
        return times

    def read_names(self):
        bounds = self.get_bounds()
        names = self.reader.recognize(self.image, list(bounds[1:,1,:]), free_list=[], detail=0)
        return names

    def read_dobs(self):
        bounds = self.get_bounds()
        dobs = self.reader.recognize(self.image, list(bounds[1:,2,:]), allowlist="0123456789-", free_list=[], detail=0)
        dobs = [dateutil.parser.parse(dob) for dob in dobs]
        return dobs

    def read_nhs_nums(self):
        bounds = self.get_bounds()
        nhss = self.reader.recognize(self.image, list(bounds[1:,3,:]), allowlist="0123456789", free_list=[], detail=0)
        return nhss


ocrreader = OCR()

if __name__=="__main__":
    image = ocrreader.read_file("filled-1.tif")
    print(image)
    ocrreader.find_circles(image)
    bounds = ocrreader.get_bounds()
    print(ocrreader.read_times())
    print(ocrreader.read_names())
    print(ocrreader.read_dobs())
    print(ocrreader.read_nhs_nums())
    #print(ocrreader.reader.readtext(image))