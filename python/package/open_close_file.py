import csv
class open_close_file:
    def __init__(self, location_file):
        self.location_file = location_file
    
    def append_string(self, string_append):
        with open(self.location_file,"a") as file:
            file.write(string_append)
    
    def read_txt_file(self):
        with open(self.location_file, "r") as file:
            return file.read()
    
    def read_txt_file_to_array(self):
        with open(self.location_file,"r") as file:
            hasil_file = file.read()
            convert_to_array =  hasil_file.split("\n")
            return convert_to_array

        
    def append_csv(self, data_append):
        with open(self.location_file, mode="a", newline="") as file:  # Mode "a" untuk (append)
            writer = csv.writer(file)
            writer.writerow(data_append)  # Menambahkan satu baris data dalam bentuk array
    
    def read_csv_file(self):
        data = []  # Array untuk menyimpan data CSV
        with open(self.location_file, mode="r", newline="") as file:
            reader = csv.reader(file)  
            next(reader)  # Lewati header jika ada

            for row in reader:
                data.append(row)  # Tambahkan setiap baris ke array
        
        return data  # Kembalikan array