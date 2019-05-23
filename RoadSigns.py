import cv2
import numpy as np


def show_img_and_exit(to_show):
    cv2.imshow("My Answer", to_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit(0)


def process_triangle(fun_approx):
    print(fun_approx)
    if 110 < fun_approx[1][0][0] < 170 or 110 < fun_approx[0][0][0] < 170:
        print("Warning sign")
        if len(clean_contours) == 3:
            print("Bumpy Road sign")

            show_img_and_exit(color_img)
        elif len(clean_contours) == 4:
            print("Traffic light sign")
            show_img_and_exit(color_img)
        else:
            print("Dangerous Descent sign")
            show_img_and_exit(color_img)

    else:
        print("Prohibitory sign, and it means 'give way'")
        show_img_and_exit(color_img)
    return


def process_circle(fun_approx):
    if len(clean_contours) == 1:
        print("Prohibitory sign")
        print("No Parking sign")
        show_img_and_exit(color_img)
    elif len(clean_contours) == 2:
        print("Prohibitory sign")
        print("Means: No Entry")
        show_img_and_exit(color_img)
    elif len(clean_contours) == 3:
        print("It's an instructions Sign, Speed Limit")
    else:
        pass
    return


def process_arrows(fun_approx):
    first_point = fun_approx[0][0]
    if first_point[0] > 200 and (100 < first_point[1] < 140):
        print("Direction signs, go right!")
        show_img_and_exit(color_img)
    elif first_point[0] < 100 and (100 < first_point[1] < 140):
        print("Direction signs, go left!")
        show_img_and_exit(color_img)
    else:
        print("Direction sign, go straight!")
        print(first_point)
        show_img_and_exit(color_img)
    print(first_point)
    return


def process_rectangles(fun_approx):
    if len(clean_contours) == 18 or len(clean_contours) == 17:
        print("Directions Sign, Exit Sign!")
        show_img_and_exit(color_img)
    else:
        print("It's a directions Sign. Means: Major Road Sign")
        print(len(clean_contours))

    return


def process_directions(fun_approx):
    if len(clean_contours) > 25:
        print("Tourist Destination!")
        show_img_and_exit(color_img)
    else:
        print("Local Destination")
        show_img_and_exit(color_img)
    return


def read_image_and_resize():
    img_name = input("Enter image name with extension\n")
    try:
        color_img_std = cv2.imread("C:\\Users\\Wala\\PycharmProjects\\RoadSigns\\images\\" + img_name, 1)
        fun_color_img = cv2.resize(color_img_std, (250, 300))
        img = cv2.imread("C:\\Users\\Wala\\PycharmProjects\\RoadSigns\\images\\" + img_name, cv2.IMREAD_GRAYSCALE)
        fun_resize_image = cv2.resize(img, (250, 300))

        return fun_color_img, fun_resize_image
    except:
        print("Image not found, make sure you entered the correct name")
        return read_image_and_resize()


font = cv2.FONT_HERSHEY_COMPLEX
color_img, resize_image = read_image_and_resize()
kernel = np.ones((5, 5), np.float32) / 25  # cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
filtered = cv2.filter2D(resize_image, -1, kernel)

_, threshold = cv2.threshold(filtered, 150, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("sds", threshold)

contours, hierach = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# contours.pop(0)
blank_image = np.zeros((500, 500, 3), np.uint8)
first_contour = contours[0]
to_remove = []
for index, cnt in enumerate(contours):
    if [0, 0] in cnt:
        to_remove.append(index)
for i in range(len(to_remove)):
    contours.pop(to_remove[i])

clean_contours = []
for cnt in contours:
    epsilon = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    clean_contours.append(approx)
temp_array = []
for cnt in clean_contours:  # If Y coordinate was larger than 200, this probably means it's text under the sign.
    print(cnt[0][0][1])
    if cnt[0][0][1] < 220:
        temp_array.append(cnt)
print("-----------")
print(temp_array[0])

cv2.drawContours(blank_image, temp_array, -1, (0, 255, 0), 2)
#show_img_and_exit(blank_image)
# approx = cv2.approxPolyDP(contours[0], 0.001 * cv2.arcLength(contours[0] + 4, True), True)
clean_contours = temp_array
approx = temp_array[0]

if len(approx) == 3:
    # cv2.putText(threshold, "Triangle", (x, y), font, 1, (0))
    process_triangle(approx)  # If triangle, call function to process it to know exactly what sign it is
    print("It's a triangle!")

elif len(approx) == 4:
    # cv2.putText(threshold, "Rectangle", (x, y), font, 1, (0))
    print("It's a rectangle!")
    process_rectangles(approx)
    show_img_and_exit(blank_image)

elif len(approx) == 6:
    # cv2.putText(threshold, "For Direction", (x, y), font, 1, (0))
    print("It's a directions sign. Means: HighWay.")
    # print(clean_contours)
    show_img_and_exit(blank_image)

elif len(approx) == 5:
    print("It's a directions sign!")
    process_directions(approx)
    show_img_and_exit(blank_image)

elif len(approx) == 8:  # Eight sides means it's a stop sign, no need for more logic here
    print("It's a Stop sign")
    show_img_and_exit(color_img)

elif 8 < len(approx) < 14:
    process_arrows(approx)
    show_img_and_exit(blank_image)
else:
    process_circle(approx)
    show_img_and_exit(blank_image)
