class coordinate_generate_2:
    def __init__(self):
        self.data = [0] * 100
        self.temp_timer = int(0)
        self.loop_timer = int(0)
        self.loop_timer_enter = int(0)
        self.isBegin = True

    def print_address(self,address, abcde, timer):
        address_int = int(address)
        timer_int = int(timer)
        time_devide = 100
        time_devide_enter = 5000
        timer_selisih = 0

        if self.isBegin:
            self.isBegin = False
        else:
            timer_selisih = min(abs(int(timer_int)-int(self.temp_timer)),abs(int(self.temp_timer)-int(timer_int)))
            self.loop_timer = timer_selisih + self.loop_timer
            self.loop_timer_enter = timer_selisih + self.loop_timer_enter
        self.temp_timer = timer_int
        # print(self.loop_timer)
        # if self.loop_timer_enter > time_devide_enter:
        #     self.loop_timer_enter = self.loop_timer_enter % time_devide_enter
        #     print()
        #     print()
        #     print()
            
        if self.loop_timer > time_devide:
            self.loop_timer = self.loop_timer % time_devide
            i=0
            for loop_data in self.data:
                if loop_data == 1:
                    print('X',end='')
                else:
                    print(' ',end='')

                i = i+1

                if i%5 == 0:
                    print('  ',end='')
            print()
            self.data = [0] * 100

        if address_int < 20:
            i = 0
            self.temp_timer = timer
            for loop_abcde in abcde:
                # print(loop_abcde)
                if loop_abcde == "1":
                    self.data[address_int*5+i] = 1
                i = i+1
            # print(self.data)

    def set_address(self, address, abcde, timer):
        self.print_address(address, abcde, timer)