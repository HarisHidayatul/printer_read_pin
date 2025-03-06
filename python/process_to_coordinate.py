from package.open_close_file import open_close_file
from package.data_arduino import data_arduino
from package.coordinate_generate import coordinate_generate
def main():    
    process_data = data_arduino()
    raw_data = open_close_file("file_processing/raw_data.txt")
    coordinate_raw = open_close_file("file_processing/coordinate_raw.csv")
    # print(raw_data.read_txt_file())
    for read_character in raw_data.read_txt_file():
    # for read_character in "@0000E3F4276#":
        # print(read_character)
        # process_data.process_string_data(read_character)
        if(process_data.process_string_data(read_character)):
            # coordinate_raw.append_csv([process_data.address,process_data.abcde,process_data.timer])
            print(process_data.address,process_data.abcde,process_data.timer)

if __name__ == "__main__":
    main()