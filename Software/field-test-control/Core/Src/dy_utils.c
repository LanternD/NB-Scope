#include <dy_utils.h>

uint8_t dy_itoa(int num, char *buf) {
  char *p = buf + INT_DIGITS + 1; // points to the terminating '\0'.
  uint8_t is_negative = False;
  uint8_t dg = 0;

  if (num == 0) {
    *--p = '0';
  }
  if (num < 0) {
    is_negative = True;
    num = -num;
  }

  if (num > 0) {
    while (num != 0) {
      *--p = '0' + (num % 10);
      num /= 10;
    }
  }
  if (is_negative) {
    *--p = '-';
  }

  // Count the number of valid chars
  dg = buf + INT_DIGITS + 1 - p;
  return dg;
}

uint8_t dy_itoa_with_leading_0(int num, uint8_t num_digit, char *dest_buf) {
  uint8_t dg = 0;
  char int_buf[ITOA_BUF_LEN] = {'\0'};
  dg = dy_itoa(num, int_buf);
  dy_shift_leading_null_chars(int_buf);
  if (0<=num_digit - dg) {
    for (uint8_t i = 0; i < num_digit - dg; i++) {
      dest_buf[i] = '0'; // fill the leading 0s.
    }
    strcat(dest_buf, int_buf);
    return dg;
  } else {
    memset(dest_buf, 0, num_digit); // not enough digits.
    return dg;
  }
}

char *dy_ftoa(float num, char *buf) {

  char *p = buf + INT_DIGITS + 1; // points to the terminating '\0'.
  uint8_t is_negative = False;
  uint8_t is_heading_zero_needed = False;
  if (num == 0 || num > 100000000) { // do not deal with large number
    *--p = '0';
    *--p = '.';
    *--p = '0';
    return buf;
  }

  if (num < 0) {
    num = -num;
    is_negative = True;
  }

  if (0 < num and 1 > num){
    is_heading_zero_needed = True;
  }

  // FIXME: this function could not handle small negative value like -0.01
  // Deal with the decimal digits.
  for (uint8_t i = 0; i < FTOA_DECIMAL_PLACES; ++i) {
    num *= 10;
  }

  for (uint8_t i = 0; i < FTOA_DECIMAL_PLACES; ++i) {
    *--p = '0' + ((int)num % 10); // tenth digit
    num /= 10;
  }
  *--p = '.';

  // Deal with the digits > 1
  while (num >= 1) {
    *--p = '0' + ((int)num % 10);
    num /= 10;
  }

  if (is_heading_zero_needed) {
    *--p = '0';  // for 0.xxx and -0.xxx
  }

  if (is_negative) {
    *--p = '-';
  }

  return buf;
}

char *dy_shift_leading_null_chars(char *buf) {
  // FIXME: if the buffer has 10 bytes, and the first 9 are all '\0', this
  // function will not work properly. Add a param to indicate the max_len
  char *p_slow = buf;
  char *p_fast = buf;
  const uint8_t max_len = 17; // bounds it
  while ((p_fast - p_slow <= max_len) and (*p_fast == '\0')) {
    // Locate the first non empty char
    p_fast++;
  }
  while ((p_fast - buf <= max_len) and (*p_fast != '\0')) {
    // Switch the two pointers.
    *p_slow++ = *p_fast;
    *p_fast++ = '\0';
  }
  return buf;
}

char *dy_cancat_sensor_string(char *result_buf, int start_idx, char *buf) {
  char *p_buf = buf;
  char *p_res_buf = result_buf;
  while (*p_buf == '\0') {
    p_buf++;
  }
  if (p_buf - buf >= ITOA_BUF_LEN) {
    // Travel too far, the buf may not be valid.
    *(p_res_buf++ + start_idx) = 'N';
    *(p_res_buf++ + start_idx) = '/';
    *(p_res_buf++ + start_idx) = 'A';
    return result_buf;
  }

  while (*p_buf != '\0' && p_buf - buf < 11) {
    *(p_res_buf++ + start_idx) = *p_buf;
    p_buf++;
  }
  return result_buf;
}

uint8_t *dy_int16_to_byte_array(uint16_t data, uint8_t *dest_buf) {
  uint8_t *p = dest_buf;
  *p++ = data & 0xFF;
  *p = (data >> 8) & 0xFF;
  return dest_buf;
}

uint8_t *dy_int32_to_byte_array(uint32_t data, uint8_t *dest_buf) {
  uint8_t *p = dest_buf;
  for (uint8_t i = 0; i < 4; i++) {
    *p++ = data & 0xFF;
    data >>= 8;
  }
  return dest_buf;
}

uint16_t dy_int8_arr_to_int16(uint8_t *src_buf) {
  return (uint16_t)src_buf[1] << 8 | src_buf[0];
}

uint32_t dy_int8_arr_to_int32(uint8_t *src_buf) {
  return (uint32_t)src_buf[3] << 24 | src_buf[2] << 16 | src_buf[1] << 8 |
         src_buf[0];
}

char *dy_append_newline(char *input) {
  char *p = input;
  while (*p != '\0' && *p != '\n') {
    p++; // skip normal text.
  }
  if (*p == '\n') {
    return input;
  } else {
    *p = '\n';
  }
  return input;
}

uint16_t dy_rand(uint16_t range) {
  uint32_t tick = HAL_GetTick();
  uint32_t res = tick % range;
  return (uint16_t)res;
}

char *dy_htoa(uint8_t *hex_array, uint16_t hex_len, uint8_t *dest_buf) {
  for (int i = 0; i < hex_len; ++i) {
    uint8_t higher_4_bits = (hex_array[i] & 0xF0) >> 4;
    uint8_t lower_4_bits = hex_array[i] & 0x0F;
    dest_buf[2 * i] = dy_htoa_single(higher_4_bits);
    dest_buf[2 * i + 1] = dy_htoa_single(lower_4_bits);
  }
  return dest_buf;
}

char dy_htoa_single(uint8_t one_hex) {
  if (one_hex < 10) {
    return one_hex + '0';
  } else {
    return one_hex - 10 + 'A'; // upper case by default.
  }
}


long  atol(const char *nptr)
{
  int c;              
  long total;
  int sign;
  while ( isspace((int)(unsigned char)*nptr) )
      ++nptr;
  c = (int)(unsigned char)*nptr++;
  sign = c;
  if (c == '-' || c == '+')
      c = (int)(unsigned char)*nptr++;    
  total = 0;
  while (isdigit(c)) {
      total = 10 * total + (c - '0');     
      c = (int)(unsigned char)*nptr++;   
  }
  if (sign == '-')
      return -total;
  else
      return total;  
}

int  atoi(const char *nptr)
{
  return (int)atol(nptr);
}