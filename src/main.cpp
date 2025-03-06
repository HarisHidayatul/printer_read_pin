#include <Arduino.h>

#define size_array_temp 255  // Maksimum 255 data untuk uint8_t
#define id_machine 0

volatile uint8_t temp_data_pinA = 0;
volatile uint8_t temp_data_pinC = 0;
volatile uint8_t temp_data_pinL = 0;
volatile uint8_t temp_data_pinB = 0;

volatile uint16_t count_loop_timer = 0;

const char hex_char[16] = {'0', '1', '2', '3', '4', '5', '6', '7', 
  '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

char send_data[18] = "";  // Perbesar buffer agar cukup menampung data
uint8_t or_all_data = 0;

void sending_data(){
  send_data[0] = '@';

  send_data[1] = id_machine%10 + '0';

  send_data[2] = hex_char[(temp_data_pinA >> 4) & 0xF];
  send_data[3] = hex_char[temp_data_pinA & 0xF];

  send_data[4] = hex_char[(temp_data_pinC >> 4) & 0xF];
  send_data[5] = hex_char[temp_data_pinC & 0xF];

  send_data[6] = hex_char[(temp_data_pinL >> 4) & 0xF];
  send_data[7] = hex_char[temp_data_pinL & 0xF];
  
  send_data[8] = hex_char[(temp_data_pinB >> 4) & 0xF];
  send_data[9] = hex_char[temp_data_pinB & 0xF];

  send_data[10] = hex_char[(count_loop_timer >> 12) & 0xF];
  send_data[11] = hex_char[(count_loop_timer >> 8) & 0xF];
  send_data[12] = hex_char[(count_loop_timer >> 4) & 0xF];
  send_data[13] = hex_char[count_loop_timer & 0xF];

  // Hitung CRC sederhana (XOR semua karakter sebelumnya)
  uint8_t crc_hex = send_data[0];
  for (int j = 1; j <= 13; j++) {
    crc_hex ^= send_data[j];
  }

  send_data[14] = hex_char[(crc_hex >> 4) & 0xF];
  send_data[15] = hex_char[crc_hex & 0xF];

  send_data[16] = '#';
  send_data[17] = '\n';

  for(int i = 0;i<3;i++){
    Serial.write(send_data, 18);
  }

  temp_data_pinA = 0;
  temp_data_pinC = 0;
  temp_data_pinL = 0;
  temp_data_pinB = 0;
}

ISR(TIMER1_COMPA_vect) {
  // Kode yang akan dijalankan setiap 10 ms
  count_loop_timer++;
  or_all_data = temp_data_pinA | temp_data_pinC | temp_data_pinL | temp_data_pinB;
  if(or_all_data > 0){
    sending_data();
  }
}

void setup() {
  Serial.begin(500000);
  DDRA = 0x00;  PORTA = 0xFF;  // Set PORTA sebagai input dengan pull-up
  DDRC = 0x00;  PORTC = 0xFF;  // Set PORTC sebagai input dengan pull-up
  DDRL = 0x00;  PORTL = 0xFF;  // Set PORTL sebagai input dengan pull-up
  DDRB = 0x00;  PORTB = 0xFF;  // Set PORTB sebagai input dengan pull-up

  temp_data_pinA = 0;
  temp_data_pinC = 0;
  temp_data_pinL = 0;

  memset(send_data, 0, sizeof(send_data));

  // Konfigurasi Timer1
  noInterrupts();         // Matikan interrupt sementara
  TCCR1A = 0;             // Mode CTC
  TCCR1B = 0;
  TCNT1  = 0;
  OCR1A = 2499;           // Nilai untuk 10ms
  TCCR1B |= (1 << WGM12); // Mode CTC
  TCCR1B |= (1 << CS11) | (1 << CS10); // Prescaler 64
  TIMSK1 |= (1 << OCIE1A); // Aktifkan Timer1 Compare Match A interrupt
  interrupts();            // Aktifkan kembali interrupt
}

void loop() {
  temp_data_pinA = temp_data_pinA | PINA;
  temp_data_pinC = temp_data_pinC | PINC;
  temp_data_pinL = temp_data_pinL | PINL;
  temp_data_pinB = temp_data_pinB | PINB;
}
