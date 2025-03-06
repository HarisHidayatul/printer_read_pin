class coordinate_generate:
    def __init__(self):
        self.data = [0] * 100
        self.temp_address = 0
        self.temp_abcde = "00000"
        self.isBegin = True
        self.spacePrint = 0
        self.temp_data_string = ""
    # def print_data(self):

    def data_coordinate_generate(self):
        array_2d = [[item] for item in self.temp_data_string.split("\n")]
        # for loop_array in array_2d:

        #     for loop_char in loop_array:

        # print(array_2d)
        filtered_arrays = []
        full_zeros_added = False  # Variabel untuk melacak apakah sudah ada array full 0

        # Memproses setiap array
        for array in array_2d:
            # Mengabaikan array yang kosong
            if array == ['']:
                continue
    
            # Memeriksa apakah semua elemen di dalam array berisi '0'
            if all(char == ' ' for char in array[0]):
                # Jika sudah ada array penuh dengan 0 sebelumnya, abaikan array ini
                if full_zeros_added:
                    continue
                else:
                    full_zeros_added = True  # Tandai bahwa array penuh dengan 0 sudah ditambahkan
                filtered_arrays.append(array)
            else:
                full_zeros_added = False
            # Menambahkan array ke dalam filtered_arrays jika memenuhi kriteria
            filtered_arrays.append(array)
            # full_zeros_added = False
        # print(filtered_arrays)
        return filtered_arrays

    def print_char_biner(self, char_print):
        for print_data in char_print:
            if int(print_data) == 0:
                # print('0',end='')
                self.temp_data_string = self.temp_data_string + ' '
            else:
                # print('X',end='')
                self.temp_data_string = self.temp_data_string + 'X'
            self.spacePrint = self.spacePrint + 1
            if self.spacePrint >= 5:
                self.spacePrint = 0
                # print('0',end='')
                self.temp_data_string = self.temp_data_string + '   '

    def print_abcde(self, abcde):
        for loop_abcde in abcde:
            self.print_char_biner(loop_abcde)
            # print(loop_abcde, end='')
    def print_address(self, address, abcde):
        if self.isBegin:
            if address != 0:
                for i in range(0,5):
                    # print('0',end='')
                    self.print_abcde('0')
        for i in range(0, (int(address)-int(self.temp_address)-1)*5):  # 11 karena range tidak termasuk nilai stop
            # print('0', end='')
            self.print_char_biner('0')
        self.isBegin = False
        self.print_abcde(abcde)
        self.temp_address = int(address)
        self.temp_abcde = abcde
    def set_address(self, address, abcde, isEnter):
        # return abcde[2]
        # if int(address) > int(self.temp_address):
        if isEnter:
            if self.isBegin:
                for i in range(0,5):
                    # print('0',end='')
                    self.print_char_biner('0')
            for i in range(0,(19-int(self.temp_address))*5):
                # print('0', end='')
                self.print_char_biner('0')
            # print("") # Lakukan print enter dan data temp hapus
            self.temp_data_string = self.temp_data_string + '\n'
            self.temp_address = 0
            self.temp_abcde = "00000"
            self.isBegin = True
        else:
            if address < self.temp_address:
                self.set_address(address=address,abcde=abcde, isEnter=True)
                self.set_address(address=address,abcde=abcde, isEnter=False)
            if (self.temp_address != address):
                self.print_address(address=address, abcde=abcde)
            else:
                if (self.isBegin):
                    self.print_address(address=address, abcde=abcde)