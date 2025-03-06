from package.open_close_file import open_close_file
from package.data_arduino import data_arduino
from package.coordinate_generate import coordinate_generate

from package.open_close_file import open_close_file
from package.printer_control import printer_control

printing = printer_control(0x04b8, 0x0202)

def main():    
    process_data = data_arduino()
    raw_data = open_close_file("file_processing/raw_data.txt")
    result_data = open_close_file("file_processing/result_data.txt")
    # print(raw_data.read_txt_file())
    string_data = ""
    for read_character in raw_data.read_txt_file():
    # for read_character in "@0000E3F4276#":
        # print(read_character)
        # process_data.process_string_data(read_character)
        if(process_data.process_string_data(read_character)):
            # coordinate_raw.append_csv([process_data.address,process_data.abcde,process_data.timer])
            data_port = process_data.temp_data_before
            timer_selisih = process_data.timer_selisih
            loop_data = int(0)
            if timer_selisih > 8:
                string_data = string_data + '\n'
                string_data = string_data + '\n'
            for loop_port in data_port:
                if loop_data%5 == 0:
                    string_data = string_data + '  '
                if loop_port == '1':
                    string_data = string_data + 'X'
                else:
                    string_data = string_data + ' '
                    # print(' ',end='')
                loop_data = loop_data + 1
            string_data = string_data + '\n'
            # print()
    # print(string_data)
    
    enter_detect = False
    data_detect = False
    temp_data = []
    string_data = []
    for loop_row in string_data.split("\n"):
        if enter_detect:
            if loop_row.strip() == "":
                if data_detect:
                    # break
                    temp_data.append(string_data)
                    enter_detect = False
                    data_detect = False
                    string_data = []
                else:
                    continue
            else:
                data_detect = True
                string_data.append(loop_row)
        else:
            if loop_row.strip() == "":
                # print("Enter")
                enter_detect = True
    for loop_data in temp_data:
        # List untuk menyimpan koordinat (x, y)
        coordinates = []

        # Baris terbawah menjadi y = 0
        max_y = len(loop_data) - 1

        for y, row in enumerate(reversed(loop_data)):  # Balik agar baris terbawah jadi y = 0
            for x, char in enumerate(row):
                if char == 'X':
                    coordinates.append([x, y])  # Simpan koordinat (x, y)
        printing.printing_byte(coordinates)


if __name__ == "__main__":
    main()