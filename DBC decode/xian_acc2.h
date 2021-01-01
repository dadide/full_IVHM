/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2018-2019 Erik Moqvist
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/**
 * This file was generated by cantools version 35.3.0 Mon Nov 23 13:58:15 2020.
 */

#ifndef XIAN_ACC2_H
#define XIAN_ACC2_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifndef EINVAL
#    define EINVAL 22
#endif

/* Frame ids. */
#define XIAN_ACC2_ACC_FRAME_ID (0x1a1u)

/* Frame lengths in bytes. */
#define XIAN_ACC2_ACC_LENGTH (8u)

/* Extended or standard frame types. */
#define XIAN_ACC2_ACC_IS_EXTENDED (0)

/* Frame cycle times in milliseconds. */


/* Signal choices. */


/**
 * Signals in message Acc.
 *
 * All signal values are as on the CAN bus.
 */
struct xian_acc2_acc_t {
    /**
     * Range: -30000.07500018750046875117188..30000.07500018750046875117188 (-40..40 g)
     * Scale: 0.00133333
     * Offset: 0
     */
    int16_t acc_x;

    /**
     * Range: -30000.07500018750046875117188..30000.07500018750046875117188 (-40..40 g)
     * Scale: 0.00133333
     * Offset: 0
     */
    int16_t acc_y;

    /**
     * Range: -30000.07500018750046875117188..30000.07500018750046875117188 (-40..40 g)
     * Scale: 0.00133333
     * Offset: 0
     */
    int16_t acc_z;

    /**
     * Range: -
     * Scale: 0.01
     * Offset: 0
     */
    int16_t t;
};

/**
 * Pack message Acc.
 *
 * @param[out] dst_p Buffer to pack the message into.
 * @param[in] src_p Data to pack.
 * @param[in] size Size of dst_p.
 *
 * @return Size of packed data, or negative error code.
 */
int xian_acc2_acc_pack(
    uint8_t *dst_p,
    const struct xian_acc2_acc_t *src_p,
    size_t size);

/**
 * Unpack message Acc.
 *
 * @param[out] dst_p Object to unpack the message into.
 * @param[in] src_p Message to unpack.
 * @param[in] size Size of src_p.
 *
 * @return zero(0) or negative error code.
 */
int xian_acc2_acc_unpack(
    struct xian_acc2_acc_t *dst_p,
    const uint8_t *src_p,
    size_t size);

/**
 * Encode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to encode.
 *
 * @return Encoded signal.
 */
int16_t xian_acc2_acc_acc_x_encode(double value);

/**
 * Decode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to decode.
 *
 * @return Decoded signal.
 */
double xian_acc2_acc_acc_x_decode(int16_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool xian_acc2_acc_acc_x_is_in_range(int16_t value);

/**
 * Encode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to encode.
 *
 * @return Encoded signal.
 */
int16_t xian_acc2_acc_acc_y_encode(double value);

/**
 * Decode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to decode.
 *
 * @return Decoded signal.
 */
double xian_acc2_acc_acc_y_decode(int16_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool xian_acc2_acc_acc_y_is_in_range(int16_t value);

/**
 * Encode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to encode.
 *
 * @return Encoded signal.
 */
int16_t xian_acc2_acc_acc_z_encode(double value);

/**
 * Decode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to decode.
 *
 * @return Decoded signal.
 */
double xian_acc2_acc_acc_z_decode(int16_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool xian_acc2_acc_acc_z_is_in_range(int16_t value);

/**
 * Encode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to encode.
 *
 * @return Encoded signal.
 */
int16_t xian_acc2_acc_t_encode(double value);

/**
 * Decode given signal by applying scaling and offset.
 *
 * @param[in] value Signal to decode.
 *
 * @return Decoded signal.
 */
double xian_acc2_acc_t_decode(int16_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool xian_acc2_acc_t_is_in_range(int16_t value);


#ifdef __cplusplus
}
#endif

#endif
