#include <Arduino.h>

#define header_char '@'
#define tail_char '#'

#define maximum_data 20
#define maximum_serial_send 34

#define size_array_temp 255  // Maksimum 255 data untuk uint8_t
#define id_machine 1

volatile uint8_t temp_data_pinA = 0;
volatile uint8_t temp_data_pinC = 0;
volatile uint8_t temp_data_pinL = 0;
volatile uint8_t temp_data_pinB = 0;

volatile uint8_t temp_data_pinF = 0;
volatile uint8_t temp_data_pinK = 0;


volatile uint8_t copy_temp_data_pinA = 0;
volatile uint8_t copy_temp_data_pinC = 0;
volatile uint8_t copy_temp_data_pinL = 0;
volatile uint8_t copy_temp_data_pinB = 0;

volatile uint8_t copy_temp_data_pinF = 0;
volatile uint8_t copy_temp_data_pinK = 0;

char send_serial_data[maximum_serial_send] = "";

const char hex_char[16] = {'0', '1', '2', '3', '4', '5', '6', '7', 
  '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

// ISR(TIMER1_COMPA_vect) {
  // Kode yang akan dijalankan setiap 10 ms
void copy_data_ISR(){
  copy_temp_data_pinA = temp_data_pinA;
  copy_temp_data_pinC = temp_data_pinC;
  copy_temp_data_pinL = temp_data_pinL;
  copy_temp_data_pinB = temp_data_pinB;

  copy_temp_data_pinF = temp_data_pinF;
  copy_temp_data_pinK = temp_data_pinK;

  // copy_temp_data_pinA = 0;
  // copy_temp_data_pinC = 0;
  // copy_temp_data_pinL = 0;
  // copy_temp_data_pinB = 0;

  // copy_temp_data_pinF = 0;
  // copy_temp_data_pinK = 0;

  temp_data_pinA = 0;
  temp_data_pinC = 0;
  temp_data_pinL = 0;
  temp_data_pinB = 0;
  
  temp_data_pinF = 0;
  temp_data_pinK = 0;
}


void send_serial_to_pc(char* dataSerial){
  // Serial.println(dataSerial);
  send_serial_data[0] = '@';

  send_serial_data[1] = id_machine%10 + '0';

  for(int i=0;i<12;i++){
    send_serial_data[2+i] = dataSerial[i+1];
  }

  send_serial_data[14] = hex_char[copy_temp_data_pinA & 0xF];
  send_serial_data[15] = dataSerial[13];

  send_serial_data[16] = hex_char[copy_temp_data_pinC & 0xF];
  send_serial_data[17] = hex_char[(copy_temp_data_pinA >> 4) & 0xF];
  

  send_serial_data[18] = hex_char[copy_temp_data_pinL & 0xF];
  send_serial_data[19] = hex_char[(copy_temp_data_pinC >> 4) & 0xF];

  send_serial_data[20] = hex_char[copy_temp_data_pinB & 0xF];
  send_serial_data[21] = hex_char[(copy_temp_data_pinL >> 4) & 0xF];
  
  send_serial_data[22] = hex_char[copy_temp_data_pinF & 0xF];
  send_serial_data[23] = hex_char[(copy_temp_data_pinB >> 4) & 0xF];

  send_serial_data[24] = hex_char[copy_temp_data_pinK & 0xF];
  send_serial_data[25] = hex_char[(copy_temp_data_pinF >> 4) & 0xF];

  send_serial_data[26] = '0';
  send_serial_data[27] = hex_char[(copy_temp_data_pinK >> 4) & 0xF];

  send_serial_data[28] = dataSerial[14];
  send_serial_data[29] = dataSerial[15];
  send_serial_data[30] = dataSerial[16];
  send_serial_data[31] = dataSerial[17];

  // Hitung CRC sederhana (XOR semua karakter sebelumnya)
  uint8_t crc_hex = send_serial_data[0];
  for (int j = 1; j <= 31; j++) {
    crc_hex ^= send_serial_data[j];
  }

  send_serial_data[32] = hex_char[(crc_hex >> 4) & 0xF];
  send_serial_data[33] = hex_char[crc_hex & 0xF];

  send_serial_data[34] = '#';
  send_serial_data[35] = '\n';

  for(int i = 0;i<3;i++){
    Serial.write(send_serial_data, 36);
  }
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(500000);
  Serial2.begin(2000000);

  DDRA = 0x00;  PORTA = 0xFF;  // Set PORTA sebagai input dengan pull-up
  DDRC = 0x00;  PORTC = 0xFF;  // Set PORTC sebagai input dengan pull-up
  DDRL = 0x00;  PORTL = 0xFF;  // Set PORTL sebagai input dengan pull-up
  DDRB = 0x00;  PORTB = 0xFF;  // Set PORTB sebagai input dengan pull-up
  
  DDRF = 0x00;  PORTF = 0xFF;
  DDRK = 0x00;  PORTK = 0xFF;
  DDRD &= 0b11110000; PORTD |= 0b00001111; // Aktifkan pull-up resistor hanya untuk Bit0 - Bit3

  attachInterrupt(digitalPinToInterrupt(2), copy_data_ISR, RISING);

  temp_data_pinA = 0;
  temp_data_pinC = 0;
  temp_data_pinL = 0;
  temp_data_pinB = 0;

  temp_data_pinF = 0;
  temp_data_pinK = 0;

  copy_temp_data_pinA = 0;
  copy_temp_data_pinC = 0;
  copy_temp_data_pinL = 0;
  copy_temp_data_pinB = 0;
  
  copy_temp_data_pinF = 0;
  copy_temp_data_pinK = 0;


  memset(send_serial_data, 0, sizeof(send_serial_data));
}

void loop() {
  // put your main code here, to run repeatedly:
  temp_data_pinA = temp_data_pinA | PINA;
  temp_data_pinC = temp_data_pinC | PINC;
  temp_data_pinL = temp_data_pinL | PINL;
  temp_data_pinB = temp_data_pinB | PINB;
  
  temp_data_pinF = temp_data_pinF | PINF;
  temp_data_pinK = temp_data_pinK | PINK;


  static bool header_found = false;
  static uint8_t loop_index = 0;
  static char data_serial[maximum_data] = "";

  if(Serial2.available()){
    char data = Serial2.read();
    // Serial.write(data);
    if(header_found){
      if(data == tail_char){
        char hex_crc = '@';
        // char hex_hasil_crc[2] = "";
        for(int i =0;i<(loop_index-2);i++){
          hex_crc = hex_crc ^ data_serial[i];
        }
        if (((hex_char[(hex_crc >> 4) & 0xF] ^ data_serial[18]) | 
            (hex_char[hex_crc & 0xF] ^ data_serial[19])) == 0) 
        {
          send_serial_to_pc(data_serial);
          // Serial.write('\n');
          // for(int i=0;i<13;i++){ // Data
          //   Serial.write(data_serial[i+1]);
          // }
          // Serial.write('\n');
          // Serial.write('\n');
          // for(int i=13;i<17;i++){ // Timer
          //   Serial.write(data_serial[i+1]);
          // }
          // Serial.write('\n');
        }
        header_found = false;
        loop_index = 0;
      }else{
        if(loop_index > 20){
          header_found = false;
          loop_index = 0;
        }
        data_serial[loop_index] = data;
        loop_index++;
      }
    }else{
      if(data == header_char){
        header_found = true;
        loop_index = 0;
        memset(data_serial, 0, sizeof(data_serial));
      }
    }
    // Serial.print(data);
  }
}