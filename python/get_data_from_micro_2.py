import serial
import time

from package.open_close_file import open_close_file
from package.data_arduino import data_arduino
from package.coordinate_generate import coordinate_generate

from package.open_close_file import open_close_file
from package.printer_control import printer_control

printing = printer_control(0x04b8, 0x0202)

def downsample_character(string_data, factor_h=2, factor_w=1):
    lines = [line for line in string_data.strip().split("\n")]
    
    original_height = len(lines)
    original_width = max(len(line) for line in lines)

    # Pastikan semua baris memiliki lebar yang sama (padding jika perlu)
    lines = [line.ljust(original_width) for line in lines]

    # Tentukan ukuran baru
    new_height = original_height // factor_h
    new_width = original_width // factor_w

    # Buffer untuk menyimpan hasil
    downsampled = []

    # Iterasi dengan langkah `factor_h` untuk tinggi dan `factor_w` untuk lebar
    for i in range(0, original_height - factor_h + 1, factor_h):
        new_line = ""
        for j in range(0, original_width - factor_w + 1, factor_w):
            # Ambil blok (factor_h x factor_w)
            block = [lines[i + k][j:j+factor_w] for k in range(factor_h) if i + k < original_height]
            
            # Jika ada 'X' dalam blok, pertahankan bentuk
            if any("X" in row for row in block):
                new_line += "X"
            else:
                new_line += " "  # Atau bisa juga " "
        
        downsampled.append(new_line)

    return "\n".join(downsampled)

def process_string_data_function(string_data):    
    process_data = data_arduino()
    # print(raw_data.read_txt_file())
    string_result_data = ""
    for read_character in string_data:
    # for read_character in "@0000E3F4276#":
        # print(read_character)
        # process_data.process_string_data(read_character)
        if(process_data.process_string_data(read_character)):
            # coordinate_raw.append_csv([process_data.address,process_data.abcde,process_data.timer])
            data_port = process_data.temp_data_before
            timer_selisih = process_data.timer_selisih
            loop_data = int(0)
            if timer_selisih > 8:
                string_result_data = string_result_data + '\n'
                string_result_data = string_result_data + '\n'
                string_result_data = string_result_data + '\n'
                string_result_data = string_result_data + '\n'
            for loop_port in data_port:
                if loop_data%5 == 0:
                    string_result_data = string_result_data + '    '
                if loop_port == '1':
                    string_result_data = string_result_data + 'X'
                else:
                    string_result_data = string_result_data + ' '
                    # print(' ',end='')
                loop_data = loop_data + 1
            string_result_data = string_result_data + '\n' #+ '  ' + str(timer_selisih)
            # print()
    # print(string_result_data)
    filter_downsample_character = downsample_character(string_result_data)
    # print(downsample_character(string_result_data))
    enter_detect = False
    data_detect = False
    temp_data = []
    string_data = []
    for loop_row in filter_downsample_character.split("\n"):
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

# # Konfigurasi port dan baudrate
# PORT = "COM4"  # Ganti sesuai dengan port yang digunakan
# BAUDRATE = 500000

PORT = "/dev/ttyUSB0"  # Gunakan /dev/ttyS0 jika pakai UART bawaan, atau /dev/ttyUSB0 untuk modul USB-Serial
BAUDRATE = 500000


def main():    
    loop_i = 0
    string_data = ""
    last_data_time = time.time()  # Simpan waktu terakhir menerima data

    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"Membuka port {PORT} dengan baudrate {BAUDRATE}")
            while True:
                try:
                    data = ser.readline().decode('utf-8', errors="ignore").strip()
                    
                    if data:
                        string_data += data
                        print(string_data)
                        loop_i = 0  # Reset counter
                        last_data_time = time.time()  # Perbarui waktu terakhir data masuk
                    else:
                        loop_i += 1

                        # Cek jika lebih dari 500 iterasi * timeout = sekitar 5 detik tanpa data
                        if (time.time() - last_data_time) > 1:  
                            if string_data:
                                process_string_data_function(string_data)
                                print("Proses data:", string_data)
                                string_data = ""  # Reset setelah diproses
                            loop_i = 0  # Reset counter setelah timeout

                except KeyboardInterrupt:
                    print("\nMenutup koneksi serial...")
                    break
    except serial.SerialException as e:
        print(f"Gagal membuka port: {e}")    

if __name__ == "__main__":
    main()

"""
@00000090816807E#
@00000090916807F#
@000000910168077#
@000000911168076#
@000000912168075#
@000000913168074#
"""