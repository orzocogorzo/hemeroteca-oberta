# BUILT-INS
import os
import re

# VENDOR
import cv2
import numpy as np
import pytesseract
import pdf2image
from matplotlib import pyplot as plt


def increase_contrast(img: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


# def get_grayscale(img: np.ndarray) -> np.ndarray:
#     return cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_LAB2BGR)


def binarize(img: np.ndarray) -> np.ndarray:
    return cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )


def remove_noise(img: np.ndarray) -> np.ndarray:
    return cv2.medianBlur(img, 7)


def thresholding(img: np.ndarray) -> np.ndarray:
    return cv2.threshold(img, 0.0, 255.0, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def dilate(img: np.ndarray) -> np.ndarray:
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)


def erode(img: np.ndarray) -> np.ndarray:
    kernel = np.ones((1, 1), np.uint8)
    return cv2.erode(img, kernel, iterations=1)


def opening(img: np.ndarray) -> np.ndarray:
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


def canny(img: np.ndarray) -> np.ndarray:
    return cv2.Canny(img, 100, 200)


def deskew(img: np.ndarray) -> np.ndarray:
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[1]
    if angle < 45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.wrapAffine(
        img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def match_template(img: np.ndarray, template: str) -> np.ndarray:
    return cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)


def get_rotation(img: np.ndarray) -> np.ndarray:
    osd = pytesseract.image_to_osd(img)
    angle = re.search(r"(?<=Rotate: )\d+", osd)
    return angle


def pdf_to_images(file_path: str) -> list[str]:
    doc_name = os.path.basename(os.path.splitext(file_path)[0])
    directory = re.sub(r"\/pdfs.*$", "/images", file_path)
    if not os.path.isdir(directory):
        os.mkdir(directory)

    # directory = os.path.relpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../images"))
    subdirectory = os.path.join(directory, doc_name)
    if os.path.isdir(subdirectory):
        for file_name in os.listdir(subdirectory):
            os.remove(os.path.join(subdirectory, file_name))
        os.rmdir(subdirectory)

    os.mkdir(subdirectory)

    imgs = pdf2image.convert_from_path(file_path, dpi=300)
    img_paths = []
    for i, img in enumerate(imgs):
        img_path = os.path.join(subdirectory, f"{i}.png")
        img.save(img_path)
        img_paths.append(img_path)

    return img_paths


class ImageParser:
    def __init__(self, file_path: str) -> None:
        if not file_path or type(file_path) != str:
            raise ValueError("file_path arguments is not a valid type")
        elif not os.path.isfile(file_path):
            raise FileExistsError("Can't find nothing at the end of the path")

        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.images = [cv2.imread(img_path) for img_path in pdf_to_images(file_path)]
        self.preprocess()

    @property
    def text(self) -> str:
        text = ""
        for img in self.images:
            text += "\n" + re.sub(
                r"(\n+|  +)", "  ", pytesseract.image_to_string(img, lang="spa")
            )

        return text

    def preprocess(self) -> None:
        preprocessed = []
        for img in self.images:
            img = increase_contrast(img)
            # img = get_grayscale(img)
            img = remove_noise(img)
            # img = thresholding(img)
            # img = binarize(img)
            # img = opening(img)
            # img = erode(img)
            # img = dilate(img)

            preprocessed.append(img)

        self.images = preprocessed

    def show_image(self, name: str, img: np.ndarray) -> None:
        plt.subplot(121)
        plt.imshow(img)
        plt.title(name)
        plt.xticks([])
        plt.yticks([])
        plt.show()
        # cv2.imshow(name, img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    file_path = os.path.normpath(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "../data/pdfs/facsimil num. 0.pdf",
        )
    )

    parser = ImageParser(file_path)
    print(parser.text)
    i = 1
    out_path = os.path.join("../images")
    for img in parser.images:
        cv2.imwrite(os.path.join(out_path, "test-%s.png" % i), img)
