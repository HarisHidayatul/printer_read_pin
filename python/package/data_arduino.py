class data_arduino:

    def __init__(self):
        self.isValidData = False
        self.data = "" #data berbentuk hex
        self.stringData = ""

        self.temp_time_arduino = 0
        self.temp_data_before = ""

        self.idDevice = 0

        self.header_found = False
        self.tail_found = False
        self.data_temp = ""

    def hex_to_binary(self,hex_string):
        return ''.join(f"{int(char, 16):04b}" for char in hex_string.upper())
    
    def process_string_data(self, charData):
        # print(charData)
        if self.header_found:
            self.data_temp += charData
            if charData == '#':
                self.tail_found: True
                # print(len(self.data_temp))
                # print(self.data_temp)
                if len(self.data_temp) == 17:
                    if self.verify_xor_checksum(self.data_temp):
                        self.isValidData = True
                        self.data = self.data_temp[1:14]
                        self.idDevice = int(self.data[0])
                        
                        biner_data_PORTA = self.hex_to_binary(self.data[1:3])[::-1]  # Balik hasil biner dimulai dari 0 sampai 7
                        biner_data_PORTC = self.hex_to_binary(self.data[3:5])[::-1]  # Balik hasil biner dimulai dari 0 sampai 7
                        biner_data_PORTL = self.hex_to_binary(self.data[5:7])[::-1]  # Balik hasil biner dimulai dari 0 sampai 7
                        biner_data_PORTB = self.hex_to_binary(self.data[7:9])[::-1]  # Balik hasil biner dimulai dari 0 sampai 7
                        
                        all_port = biner_data_PORTA + biner_data_PORTC+biner_data_PORTL+biner_data_PORTB
                        loop_data = 0

                        #Optimasi untuk menghilangkan pin error
                        total = sum(int(digit) for digit in all_port)
                        if total > 2:
                            if self.temp_data_before != all_port:
                                timer_arduino = int(self.data[9:13],16)
                                timer_arduino = timer_arduino  - 32768
                                timer_selisih = min(abs(int(timer_arduino)-int(self.temp_time_arduino)),abs(int(self.temp_time_arduino)-int(timer_arduino)))
                                self.temp_time_arduino = timer_arduino
                                if timer_selisih > 8:
                                    print()
                                    print()

                                for loop_port in all_port:
                                    if loop_data%5 == 0:
                                        print('  ',end='')
                                    if loop_port == '1':
                                        print('X',end='')
                                    else:
                                        print(' ',end='')
                                    loop_data = loop_data + 1
                                print(' ',end='')
                                print(all_port)
                                self.temp_data_before = all_port
                        # print(all_port)
                        # print(self.data_temp, self.data, self.idDevice, self.data[1:3], self.data[3:5], self.data[5:7], self.data[7:9])
                    else:
                        return False
                self.header_found = False
                self.tail_found = False
                self.data_temp = ""
        else:
            if charData == '@':
                self.header_found = True
                self.data_temp += charData
        return False
    def verify_xor_checksum(self,data):
        # Pastikan format data sesuai
        if not (data.startswith('@') and data.endswith('#') and len(data) > 3):
            return False

        # Pisahkan payload dan checksum
        payload = data[0:-3]  # Mengambil bagian antara @ dan checksum
        given_checksum = data[-3:-1]  # Ambil checksum yang diberikan (dua karakter sebelum '#')
    
        # print(given_checksum)
        # Hitung XOR dari semua karakter payload
        xor_result = 0
        for char in payload:
            xor_result ^= ord(char)  # XOR dengan nilai ASCII masing-masing karakter

        # Konversi hasil XOR ke bentuk hex (uppercase untuk dibandingkan)
        calculated_checksum = f"{xor_result:02X}"
        # print(calculated_checksum)
    
        # Bandingkan hasil XOR yang dihitung dengan yang diberikan
        return calculated_checksum == given_checksum