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
        self.read_file("blankform.tif")
        self.target_size = tuple(reversed(self.image.shape))
        self.reference_points = self.find_circles()
        cv2.namedWindow("main", cv2.WINDOW_GUI_NORMAL)

    def point_angle(self, point):
        x = point[0]-1500
        y = point[1]-1500
        return np.arctan2(x,y)

    def read_file(self, fname):
        self.image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        return self.image

    def map_image(self):
        self.image_points = self.find_circles()
        h = cv2.getPerspectiveTransform(self.image_points, self.reference_points)
        self.image = cv2.warpPerspective(self.image, h, self.target_size)
        results = self.draw_bounds()
        cv2.imwrite("results.png", results)
        cv2.imshow("main", results)
        cv2.waitKey(0)

    @staticmethod
    def isCircle(contour):
        area = cv2.contourArea(contour)
        return area > 1000 and area < 100000

    @staticmethod
    def get_centroid(contour):
        m = cv2.moments(contour)
        centroid = ((m['m10'] / m['m00']), (m['m01'] / m['m00']))
        return centroid

    def find_circles(self):
        image = self.image.copy()
        ret, image  = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
        image = cv2.dilate(image, kernel=self.kernel, iterations=2)
        image = cv2.erode(image, kernel=self.kernel, iterations=2)
        contours, hierarchy = cv2.findContours(
            image,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)
        centroids = [self.get_centroid(c) for c in contours if self.isCircle(c)]
        centroids = sorted(centroids, key=self.point_angle)
        assert(len(centroids)==4)
        return np.array(centroids, dtype="float32")

    def draw_bounds(self):
        copy = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        for rects in self.get_bounds():
            for rect in rects:
                a = (rect[0], rect[2])
                b = (rect[1], rect[3])
                cv2.rectangle(copy, pt1=a, pt2=b, color=(0, 0, 255))
        return copy


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

    def get_all_details(self):
        times = self.read_times()
        dobs = self.read_dobs()
        nhss = self.read_nhs_nums()
        result = [{'time': t, 'dob': d, 'nhs': n} for t,d,n in zip(times, dobs, nhss)]
        return result

ocrreader = OCR()

if __name__=="__main__":
    img = ocrreader.read_file("filled-1.tif")
    print(img)
    ocrreader.find_circles(img)
    bounds = ocrreader.get_bounds()
    print(ocrreader.read_times())
    print(ocrreader.read_names())
    print(ocrreader.read_dobs())
    print(ocrreader.read_nhs_nums())
    #print(ocrreader.reader.readtext(image))