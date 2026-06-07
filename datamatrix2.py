import sys
import cv2
import zxingcpp

def BarcodeText(pic, outfile):
    try:
        Image = cv2.imread(pic, cv2.IMREAD_UNCHANGED)
        Gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
        Ret, Thresh = cv2.threshold(Gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        results = zxingcpp.read_barcodes(Thresh)
        if results:
            DecodeStr = results[0].text
            print(DecodeStr)
            with open(outfile, "w", encoding="UTF-8") as file:
                file.write(DecodeStr)
        else:
            raise ValueError("DataMatrix код не найден на изображении")
    except Exception as ex:
        ErrTemplate = "ШТРИХКОД НЕ РАСПОЗНАН. Ошибка типа {0}"
        ErrMessage = ErrTemplate.format(type(ex).__name__)
        with open(outfile, "w", encoding="UTF-8") as file:
            print(ErrMessage)
            file.write(ErrMessage)

if __name__ == "__main__":
    pic = sys.argv[1]
    outfile = sys.argv[2]
    BarcodeText(pic, outfile)