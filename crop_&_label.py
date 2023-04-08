from PIL import Image
import xml.etree.ElementTree as ET
import os

data_folder = 'Data/data_and_label'
data_foler_output = 'Data/cropped-data_and_label'

for xml_file in os.listdir(data_folder):
    if xml_file.endswith('.xml'):
        # Load the XML file and extract the bounding box coordinates
        tree = ET.parse(os.path.join(data_folder, xml_file))
        root = tree.getroot()
        object_list = root.findall("object")
        bounding_boxes = []
        for obj in object_list:
            bndbox = obj.find("bndbox")
            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)
            bounding_boxes.append((xmin, ymin, xmax, ymax))

        # Load the image and calculate the dimensions of the smaller images
        # image_file = "pur-004.jpg"
        img_filename = os.path.splitext(xml_file)[0] + '.jpg'
        img_path = os.path.join(data_folder, img_filename)
        img = Image.open(img_path)
        width, height = img.size
        # crop_size = 6
        # num_cols = width // crop_size
        # num_rows = height // crop_size
        crop_size = width // 6
        num_cols = 6
        num_rows = 6

        # Iterate through each of the smaller images and their corresponding bounding boxes
        for i in range(num_rows):
            for j in range(num_cols):
                x_min = j * crop_size
                y_min = i * crop_size
                x_max = (j + 1) * crop_size
                y_max = (i + 1) * crop_size
                cropped_img = img.crop((x_min, y_min, x_max, y_max))
                cropped_bounding_boxes = []

                for bbox in bounding_boxes:
                    bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max = bbox
                    if bbox_x_min >= x_max or bbox_x_max <= x_min or bbox_y_min >= y_max or bbox_y_max <= y_min:
                        # The bounding box is outside of the cropped image, skip it
                        continue
                    cropped_bbox_x_min = max(0, bbox_x_min - x_min)
                    cropped_bbox_y_min = max(0, bbox_y_min - y_min)
                    cropped_bbox_x_max = min(crop_size, bbox_x_max - x_min)
                    cropped_bbox_y_max = min(crop_size, bbox_y_max - y_min)

                    if cropped_bbox_x_max - cropped_bbox_x_min <= 30 or cropped_bbox_y_max - cropped_bbox_y_min <= 30: #augmenter ? <=30 ? c'était à 20 avant
                        continue
                    # if bbox_x_min < x_min:
                    #     # The bounding box extends beyond the left boundary of the cropped image
                    #     bbox_width = bbox_x_max - bbox_x_min
                    #     cropped_bbox_x_min = 0
                    #     cropped_bbox_x_max = min(
                    #         bbox_width, crop_size - (x_min - bbox_x_min))
                    # if bbox_x_max > x_max:
                    #     # The bounding box extends beyond the right boundary of the cropped image
                    #     bbox_width = bbox_x_max - bbox_x_min
                    #     cropped_bbox_x_min = max(
                    #         0, crop_size - (bbox_x_max - x_max))
                    #     cropped_bbox_x_max = crop_size
                    # if bbox_y_min < y_min:
                    #     # The bounding box extends beyond the top boundary of the cropped image
                    #     bbox_height = bbox_y_max - bbox_y_min
                    #     cropped_bbox_y_min = 0
                    #     cropped_bbox_y_max = min(
                    #         bbox_height, crop_size - (y_min - bbox_y_min))
                    # if bbox_y_max > y_max:
                    #     # The bounding box extends beyond the bottom boundary of the cropped image
                    #     bbox_height = bbox_y_max - bbox_y_min
                    #     cropped_bbox_y_min = max(
                    #         0, crop_size - (bbox_y_max - y_max))
                    #     cropped_bbox_y_max = crop_size
                    cropped_bounding_boxes.append(
                        (cropped_bbox_x_min, cropped_bbox_y_min, cropped_bbox_x_max, cropped_bbox_y_max))

                    #---------------

                # for bbox in bounding_boxes:
                #     bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max = bbox
                #     if bbox_x_min >= x_min and bbox_x_max <= x_max and bbox_y_min >= y_min and bbox_y_max <= y_max:
                #         # Adjust the bounding box coordinates for the cropped image
                #         cropped_bbox_x_min = bbox_x_min - x_min
                #         cropped_bbox_y_min = bbox_y_min - y_min
                #         cropped_bbox_x_max = bbox_x_max - x_min
                #         cropped_bbox_y_max = bbox_y_max - y_min
                #         cropped_bounding_boxes.append(
                #             (cropped_bbox_x_min, cropped_bbox_y_min, cropped_bbox_x_max, cropped_bbox_y_max))

                # Save the cropped image and its updated annotations as a new XML file
                cropped_image_file = os.path.splitext(
                    xml_file)[0] + f"_{i}_{j}.jpg"
                cropped_xml_file = os.path.splitext(
                    xml_file)[0] + f"_{i}_{j}.xml"
                # cropped_img.save(cropped_image_file)
                cropped_img.save(os.path.join(
                    data_foler_output, cropped_image_file))

                root_cropped = ET.Element("annotation")
                for obj, bbox in zip(object_list, cropped_bounding_boxes):
                    # --- TEST WRITE FILENAME ----

                    fname = ET.SubElement(root_cropped,"filename").text = str(cropped_image_file)

                    # --- TEST WRITE FILENAME ----
                    obj_cropped = ET.SubElement(root_cropped, "object")
                    obj_cropped.extend(obj.findall("name"))
                    bndbox_cropped = ET.SubElement(obj_cropped, "bndbox")
                    bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max = bbox
                    ET.SubElement(bndbox_cropped, "xmin").text = str(
                        bbox_x_min)
                    ET.SubElement(bndbox_cropped, "ymin").text = str(
                        bbox_y_min)
                    ET.SubElement(bndbox_cropped, "xmax").text = str(
                        bbox_x_max)
                    ET.SubElement(bndbox_cropped, "ymax").text = str(
                        bbox_y_max)

                tree_cropped = ET.ElementTree(root_cropped)
                # tree_cropped.write(cropped_xml_file)
                tree_cropped.write(os.path.join(
                    data_foler_output, cropped_xml_file))
