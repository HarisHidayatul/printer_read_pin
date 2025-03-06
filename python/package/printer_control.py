from escpos.printer import Usb
class printer_control:
    def __init__(self, vendor_id, product_id):
        # print(vendor_id,product_id)
        # Inisialisasi printer
        try:
            # Inisialisasi printer
            # Vendor ID: 0x04b8, Product ID: 0x0202 Pada Raspi Saya
            # vendor_id = 0x04B8  Epson product_id = 0x0202  # TM-U220B #Pada PC saya
            self.printer = Usb(vendor_id, product_id)
            print("Printer berhasil dihubungkan.")
        except Exception as e:
            print(f"Error: Tidak dapat menghubungkan printer. {e}")
            self.printer = None  # Hindari error jika printer tidak terhubung

    def printing_byte_flip(self,array_byte):
        # Array byte ini dihitung secara horizontal
        bitmap_data = [0x00] * 200
        loop_index = 0
        for loop_byte in array_byte:
            bitmap_data[loop_index] = loop_byte
            loop_index = loop_index + 1
        # for i in range(0,8):
        #     for j in range(0,200):
        #         if (bitmap_data[j] >> (7 - i)) & 1:  # Cek bit ke-i dari MSB
        #             print('X', end='')
        #         else:
        #             print('0', end='')
        #     print()
        self.printer._raw(b'\x1B*\x00\xC8\x00')
        self.printer._raw(bytes(bitmap_data))    # Data bitmap
        self.printer.text("\n")

    def printing_byte(self, array_xy):
        # array_xy berisi matriks [[x,y],[x,y],[x,y],[x,y]]
        # Dimana didalam range 200 x 8, jadi x maksimal 199 dan y maksimal 7
        matrix_flip = [[0 for _ in range(200)] for _ in range(8)]
        for loop_xy in array_xy:
            if ((loop_xy[1]<8) & (loop_xy[0]<200)):
                matrix_flip[7-loop_xy[1]][loop_xy[0]] =  1
        # Mengubah setiap kolom menjadi byte (0x00 - 0xFF)
        result_bytes = []
        for col in range(200):  # Loop setiap kolom
            byte_value = 0
            for row in range(8):  # Loop bit dari atas ke bawah
                byte_value |= (matrix_flip[row][col] << (7 - row))  # Menyusun bit ke dalam byte
            result_bytes.append(byte_value)  # Menyimpan hasil byte untuk setiap kolom
        self.printing_byte_flip(result_bytes)