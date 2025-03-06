import serial
from package.open_close_file import open_close_file

# Konfigurasi port dan baudrate
PORT = "COM4"  # Ganti sesuai dengan port yang digunakan
BAUDRATE = 500000

loop_i = int(0)

def main():    
    raw_data = open_close_file("file_processing/raw_data.txt")
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"Membuka port {PORT} dengan baudrate {BAUDRATE}")
            while True:
                try:
                    data = ser.readline().decode('utf-8', errors="ignore").strip()
                    # i = i+1

                    print(data)
                    raw_data.append_string(data)
                except KeyboardInterrupt:
                    print("\nMenutup koneksi serial...")
                    break
    except serial.SerialException as e:
        print(f"Gagal membuka port: {e}")
        # sys.exit(1)
    

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