/**
  @file: dy_utils.h
  @brief: Common utils for the project. None of the method here are related to
  the STM32 chip itself. Will continue growing with the time. Usually it is
  backward compatible.
  @author: Deliang Yang
  @date_created: 2019.11.07
  @version: 0.1
*/

#ifndef DY_UTILS_H
#define DY_UTILS_H

#include "dy_syntax.h"
#include "stm32f1xx.h" // need the uint8_t etc. definition
#include "string.h"

#ifdef __cplusplus
extern "C" {
#endif

/** Number of digits needed. */
#define INT_DIGITS 10 // enough for project use, update if necessary
#define ITOA_BUF_LEN INT_DIGITS + 2 // possible minus sign and tailing '\0'
#define FTOA_DECIMAL_PLACES 2 // number of decimal digits after "0."

/**
   An 'int to ASCII' converter function that can take care of both positive and
   negative numbers.
   @param An integer.
   @param An array of chars. Length >= INT_DIGITS + 2. char buf[12] in this
   case. The value should be initialized as all '\0' elements.
   @return An array of chars, containing the possible negative sign, up to 10
   digits (2^32), and the tailing '\0'. The heading may contain arbitrary number
   of '\0'. \n Example: ['\0', '-', 'x', 'x', 'x', 'x', 'x', '\0']
  @return The number of valid chars, minus sign is counted.
 */
uint8_t dy_itoa(int i, char *buf);

/**
   A 'float to ASCII' converter function. By default, only tenth digit will be
   kept
   @param A float number.
   @param An array of chars. Length = INT_DIGITS + 2. char buf[12] in this case.
   @return An array of chars, containing the possible negative sign, up to 8
   digits, and the tailing '\0'. The heading may contain arbitrary number of
   '\0'. \n
   Example: ['\0', '-', 'x', 'x', 'x', 'x', '.', 'x', '\0']
 */
char *dy_ftoa(float num, char *buf);

/**
   @brief Left shift a char array, such that the leading '\0' is removed.
   @param buf: a char array
   @return the same char array
   @note The input would be like ['\0', '\0', 'x', 'x', 'x', 'x', '\0'], after
   shifting, it becomes ['x', 'x', 'x', 'x', '\0', '\0', '\0'].
*/
char *dy_shift_leading_null_chars(char *buf);

/**
   Append the sensor reading char array to another string.
   kept
   @param result_buf: A buffer for the returned char array.
   @param start_idx: the offset where replacement should begin. 0-indexed.
   @param buf: A buffer containing the result from dy_iota() or dy_ftoa(). It
   may contain arbitrary number of heading '\0'.
   @return An array of chars, containing the possible negative sign, up to 6
   digits, and the tailing '\0'. The heading may contain arbitrary number of
   '\0'. \n
   Example: ['T', 'e', 'm', 'p', ':', '\0', '\0', '\0', '\0', '\0'] +
   ['\0', '-', 'x', 'x', 'x', 'x', '.', 'x', '\0'] = ['T', 'e', 'm', 'p', ':',
   '-', 'x', 'x', 'x', 'x', '.', 'x', '\0']
 */
char *dy_cancat_sensor_string(char *result_buf, int start_idx, char *buf);
#ifdef __cplusplus
}
#endif

/**
   Convert the uint16_t type into a 2-byte array. Little-endian.
   @param uint16_t data
   @param uint8_t *dest_buf: length=2 array.
   @return an array with 2 bytes.
 */
uint8_t *dy_int16_to_byte_array(uint16_t data, uint8_t *dest_buf);

/**
   Convert the uint16_t type into a 4-byte array. Little-endian.
   @param uint16_t data
   @param uint8_t *dest_buf: length=4 array.
   @return an array with 4 bytes.
 */
uint8_t *dy_int32_to_byte_array(uint32_t data, uint8_t *dest_buf);
#endif /* __MAIN_H */

/**
   Convert an array of uint8_t type into a uint16_t value. Little-endian.
   @param uint8_t *src_buf: length=2 array.
   @return a uint16_t variable.
 */
uint16_t dy_int8_arr_to_int16(uint8_t *src_buf);

/**
   Convert an array of uint8_t type into a uint32_t value. Little-endian.
   @param uint8_t *src_buf: length=4 array.
   @return a uint32_t variable.
 */
uint32_t dy_int8_arr_to_int32(uint8_t *src_buf);

/**
   Append newline \n at the end of the string. Make sure there is enough room.
   @param char array
   @return char array.
 */
char *dy_append_newline(char *input);

/**
   @brief DY's version, generate a random number within the given range.
   @param range: 0 to 65535.
   @return A random uint16_t number.
   @note If you want range like 300-500, set range=200, and then add 300 by
   yourself.
*/
uint16_t dy_rand(uint16_t range);

/**
   @brief Convert Hex value to its ASCII representation.
   @param hex_array: an array storing the hex bytes.
   @param hex_len: length of the hex array.
   @param dest_buf: a buffer storing the conversion results.
   @return char array with the conversion results
   @note Example: input [0xFA, 0x98, 0xBA, 0x12], output: "FA98BA12". If you
   would like to convert uint32_t to ascii, you can call the
   dy_int32_to_byte_array first.
*/
char *dy_htoa(uint8_t *hex_array, uint16_t hex_len, uint8_t *dest_buf);

/**
   @brief Convert one hex digit to ascii char.
   @param one_hex: a hex digit, 4 bits.
   @return Converted results, char.
   @note 0x00-0x09 to '0'-'9', 0x0A to 'A', 0x0F to 'F', etc.
*/
char dy_htoa_single(uint8_t one_hex);

/**
   @brief iota special version. Convert to char with leading 0
   @param num: integer
   @param num_digit: total digits of the return buffer
   @return number of valid char. dest_buf is modified in-place.
   @note Example: num=-143, num_digit=5 => dest_buf = "0-143"
*/
uint8_t dy_itoa_with_leading_0(int num, uint8_t num_digit, char *dest_buf);


long  atol(const char *nptr);

int  atoi(const char *nptr);