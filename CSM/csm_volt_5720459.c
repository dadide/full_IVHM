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
 * This file was generated by cantools version 35.3.0 Sat Aug 29 16:22:18 2020.
 */

#include <string.h>

#include "csm_volt_5720459.h"

static inline uint8_t pack_left_shift_u16(
    uint16_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint8_t)((uint8_t)(value << shift) & mask);
}

static inline uint8_t pack_right_shift_u16(
    uint16_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint8_t)((uint8_t)(value >> shift) & mask);
}

static inline uint16_t unpack_left_shift_u16(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint16_t)((uint16_t)(value & mask) << shift);
}

static inline uint16_t unpack_right_shift_u16(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint16_t)((uint16_t)(value & mask) >> shift);
}

int csm_volt_5720459_admm_05431_msg0_pack(
    uint8_t *dst_p,
    const struct csm_volt_5720459_admm_05431_msg0_t *src_p,
    size_t size)
{
    uint16_t admm_05431_a01;
    uint16_t admm_05431_a02;
    uint16_t admm_05431_a03;
    uint16_t admm_05431_a04;

    if (size < 8u) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    admm_05431_a01 = (uint16_t)src_p->admm_05431_a01;
    dst_p[0] |= pack_left_shift_u16(admm_05431_a01, 0u, 0xffu);
    dst_p[1] |= pack_right_shift_u16(admm_05431_a01, 8u, 0xffu);
    admm_05431_a02 = (uint16_t)src_p->admm_05431_a02;
    dst_p[2] |= pack_left_shift_u16(admm_05431_a02, 0u, 0xffu);
    dst_p[3] |= pack_right_shift_u16(admm_05431_a02, 8u, 0xffu);
    admm_05431_a03 = (uint16_t)src_p->admm_05431_a03;
    dst_p[4] |= pack_left_shift_u16(admm_05431_a03, 0u, 0xffu);
    dst_p[5] |= pack_right_shift_u16(admm_05431_a03, 8u, 0xffu);
    admm_05431_a04 = (uint16_t)src_p->admm_05431_a04;
    dst_p[6] |= pack_left_shift_u16(admm_05431_a04, 0u, 0xffu);
    dst_p[7] |= pack_right_shift_u16(admm_05431_a04, 8u, 0xffu);

    return (8);
}

int csm_volt_5720459_admm_05431_msg0_unpack(
    struct csm_volt_5720459_admm_05431_msg0_t *dst_p,
    const uint8_t *src_p,
    size_t size)
{
    uint16_t admm_05431_a01;
    uint16_t admm_05431_a02;
    uint16_t admm_05431_a03;
    uint16_t admm_05431_a04;

    if (size < 8u) {
        return (-EINVAL);
    }

    admm_05431_a01 = unpack_right_shift_u16(src_p[0], 0u, 0xffu);
    admm_05431_a01 |= unpack_left_shift_u16(src_p[1], 8u, 0xffu);
    dst_p->admm_05431_a01 = (int16_t)admm_05431_a01;
    admm_05431_a02 = unpack_right_shift_u16(src_p[2], 0u, 0xffu);
    admm_05431_a02 |= unpack_left_shift_u16(src_p[3], 8u, 0xffu);
    dst_p->admm_05431_a02 = (int16_t)admm_05431_a02;
    admm_05431_a03 = unpack_right_shift_u16(src_p[4], 0u, 0xffu);
    admm_05431_a03 |= unpack_left_shift_u16(src_p[5], 8u, 0xffu);
    dst_p->admm_05431_a03 = (int16_t)admm_05431_a03;
    admm_05431_a04 = unpack_right_shift_u16(src_p[6], 0u, 0xffu);
    admm_05431_a04 |= unpack_left_shift_u16(src_p[7], 8u, 0xffu);
    dst_p->admm_05431_a04 = (int16_t)admm_05431_a04;

    return (0);
}

int16_t csm_volt_5720459_admm_05431_msg0_admm_05431_a01_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg0_admm_05431_a01_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg0_admm_05431_a01_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05431_msg0_admm_05431_a02_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg0_admm_05431_a02_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg0_admm_05431_a02_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05431_msg0_admm_05431_a03_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg0_admm_05431_a03_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg0_admm_05431_a03_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05431_msg0_admm_05431_a04_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg0_admm_05431_a04_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg0_admm_05431_a04_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int csm_volt_5720459_admm_05431_msg1_pack(
    uint8_t *dst_p,
    const struct csm_volt_5720459_admm_05431_msg1_t *src_p,
    size_t size)
{
    uint16_t admm_05431_a05;
    uint16_t admm_05431_a06;
    uint16_t admm_05431_a07;
    uint16_t admm_05431_a08;

    if (size < 8u) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    admm_05431_a05 = (uint16_t)src_p->admm_05431_a05;
    dst_p[0] |= pack_left_shift_u16(admm_05431_a05, 0u, 0xffu);
    dst_p[1] |= pack_right_shift_u16(admm_05431_a05, 8u, 0xffu);
    admm_05431_a06 = (uint16_t)src_p->admm_05431_a06;
    dst_p[2] |= pack_left_shift_u16(admm_05431_a06, 0u, 0xffu);
    dst_p[3] |= pack_right_shift_u16(admm_05431_a06, 8u, 0xffu);
    admm_05431_a07 = (uint16_t)src_p->admm_05431_a07;
    dst_p[4] |= pack_left_shift_u16(admm_05431_a07, 0u, 0xffu);
    dst_p[5] |= pack_right_shift_u16(admm_05431_a07, 8u, 0xffu);
    admm_05431_a08 = (uint16_t)src_p->admm_05431_a08;
    dst_p[6] |= pack_left_shift_u16(admm_05431_a08, 0u, 0xffu);
    dst_p[7] |= pack_right_shift_u16(admm_05431_a08, 8u, 0xffu);

    return (8);
}

int csm_volt_5720459_admm_05431_msg1_unpack(
    struct csm_volt_5720459_admm_05431_msg1_t *dst_p,
    const uint8_t *src_p,
    size_t size)
{
    uint16_t admm_05431_a05;
    uint16_t admm_05431_a06;
    uint16_t admm_05431_a07;
    uint16_t admm_05431_a08;

    if (size < 8u) {
        return (-EINVAL);
    }

    admm_05431_a05 = unpack_right_shift_u16(src_p[0], 0u, 0xffu);
    admm_05431_a05 |= unpack_left_shift_u16(src_p[1], 8u, 0xffu);
    dst_p->admm_05431_a05 = (int16_t)admm_05431_a05;
    admm_05431_a06 = unpack_right_shift_u16(src_p[2], 0u, 0xffu);
    admm_05431_a06 |= unpack_left_shift_u16(src_p[3], 8u, 0xffu);
    dst_p->admm_05431_a06 = (int16_t)admm_05431_a06;
    admm_05431_a07 = unpack_right_shift_u16(src_p[4], 0u, 0xffu);
    admm_05431_a07 |= unpack_left_shift_u16(src_p[5], 8u, 0xffu);
    dst_p->admm_05431_a07 = (int16_t)admm_05431_a07;
    admm_05431_a08 = unpack_right_shift_u16(src_p[6], 0u, 0xffu);
    admm_05431_a08 |= unpack_left_shift_u16(src_p[7], 8u, 0xffu);
    dst_p->admm_05431_a08 = (int16_t)admm_05431_a08;

    return (0);
}

int16_t csm_volt_5720459_admm_05431_msg1_admm_05431_a05_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg1_admm_05431_a05_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg1_admm_05431_a05_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05431_msg1_admm_05431_a06_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg1_admm_05431_a06_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg1_admm_05431_a06_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05431_msg1_admm_05431_a07_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg1_admm_05431_a07_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg1_admm_05431_a07_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05431_msg1_admm_05431_a08_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05431_msg1_admm_05431_a08_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05431_msg1_admm_05431_a08_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int csm_volt_5720459_admm_05432_msg0_pack(
    uint8_t *dst_p,
    const struct csm_volt_5720459_admm_05432_msg0_t *src_p,
    size_t size)
{
    uint16_t admm_05432_a01;
    uint16_t admm_05432_a02;
    uint16_t admm_05432_a03;
    uint16_t admm_05432_a04;

    if (size < 8u) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    admm_05432_a01 = (uint16_t)src_p->admm_05432_a01;
    dst_p[0] |= pack_left_shift_u16(admm_05432_a01, 0u, 0xffu);
    dst_p[1] |= pack_right_shift_u16(admm_05432_a01, 8u, 0xffu);
    admm_05432_a02 = (uint16_t)src_p->admm_05432_a02;
    dst_p[2] |= pack_left_shift_u16(admm_05432_a02, 0u, 0xffu);
    dst_p[3] |= pack_right_shift_u16(admm_05432_a02, 8u, 0xffu);
    admm_05432_a03 = (uint16_t)src_p->admm_05432_a03;
    dst_p[4] |= pack_left_shift_u16(admm_05432_a03, 0u, 0xffu);
    dst_p[5] |= pack_right_shift_u16(admm_05432_a03, 8u, 0xffu);
    admm_05432_a04 = (uint16_t)src_p->admm_05432_a04;
    dst_p[6] |= pack_left_shift_u16(admm_05432_a04, 0u, 0xffu);
    dst_p[7] |= pack_right_shift_u16(admm_05432_a04, 8u, 0xffu);

    return (8);
}

int csm_volt_5720459_admm_05432_msg0_unpack(
    struct csm_volt_5720459_admm_05432_msg0_t *dst_p,
    const uint8_t *src_p,
    size_t size)
{
    uint16_t admm_05432_a01;
    uint16_t admm_05432_a02;
    uint16_t admm_05432_a03;
    uint16_t admm_05432_a04;

    if (size < 8u) {
        return (-EINVAL);
    }

    admm_05432_a01 = unpack_right_shift_u16(src_p[0], 0u, 0xffu);
    admm_05432_a01 |= unpack_left_shift_u16(src_p[1], 8u, 0xffu);
    dst_p->admm_05432_a01 = (int16_t)admm_05432_a01;
    admm_05432_a02 = unpack_right_shift_u16(src_p[2], 0u, 0xffu);
    admm_05432_a02 |= unpack_left_shift_u16(src_p[3], 8u, 0xffu);
    dst_p->admm_05432_a02 = (int16_t)admm_05432_a02;
    admm_05432_a03 = unpack_right_shift_u16(src_p[4], 0u, 0xffu);
    admm_05432_a03 |= unpack_left_shift_u16(src_p[5], 8u, 0xffu);
    dst_p->admm_05432_a03 = (int16_t)admm_05432_a03;
    admm_05432_a04 = unpack_right_shift_u16(src_p[6], 0u, 0xffu);
    admm_05432_a04 |= unpack_left_shift_u16(src_p[7], 8u, 0xffu);
    dst_p->admm_05432_a04 = (int16_t)admm_05432_a04;

    return (0);
}

int16_t csm_volt_5720459_admm_05432_msg0_admm_05432_a01_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg0_admm_05432_a01_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg0_admm_05432_a01_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05432_msg0_admm_05432_a02_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg0_admm_05432_a02_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg0_admm_05432_a02_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05432_msg0_admm_05432_a03_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg0_admm_05432_a03_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg0_admm_05432_a03_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05432_msg0_admm_05432_a04_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg0_admm_05432_a04_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg0_admm_05432_a04_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int csm_volt_5720459_admm_05432_msg1_pack(
    uint8_t *dst_p,
    const struct csm_volt_5720459_admm_05432_msg1_t *src_p,
    size_t size)
{
    uint16_t admm_05432_a05;
    uint16_t admm_05432_a06;
    uint16_t admm_05432_a07;
    uint16_t admm_05432_a08;

    if (size < 8u) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    admm_05432_a05 = (uint16_t)src_p->admm_05432_a05;
    dst_p[0] |= pack_left_shift_u16(admm_05432_a05, 0u, 0xffu);
    dst_p[1] |= pack_right_shift_u16(admm_05432_a05, 8u, 0xffu);
    admm_05432_a06 = (uint16_t)src_p->admm_05432_a06;
    dst_p[2] |= pack_left_shift_u16(admm_05432_a06, 0u, 0xffu);
    dst_p[3] |= pack_right_shift_u16(admm_05432_a06, 8u, 0xffu);
    admm_05432_a07 = (uint16_t)src_p->admm_05432_a07;
    dst_p[4] |= pack_left_shift_u16(admm_05432_a07, 0u, 0xffu);
    dst_p[5] |= pack_right_shift_u16(admm_05432_a07, 8u, 0xffu);
    admm_05432_a08 = (uint16_t)src_p->admm_05432_a08;
    dst_p[6] |= pack_left_shift_u16(admm_05432_a08, 0u, 0xffu);
    dst_p[7] |= pack_right_shift_u16(admm_05432_a08, 8u, 0xffu);

    return (8);
}

int csm_volt_5720459_admm_05432_msg1_unpack(
    struct csm_volt_5720459_admm_05432_msg1_t *dst_p,
    const uint8_t *src_p,
    size_t size)
{
    uint16_t admm_05432_a05;
    uint16_t admm_05432_a06;
    uint16_t admm_05432_a07;
    uint16_t admm_05432_a08;

    if (size < 8u) {
        return (-EINVAL);
    }

    admm_05432_a05 = unpack_right_shift_u16(src_p[0], 0u, 0xffu);
    admm_05432_a05 |= unpack_left_shift_u16(src_p[1], 8u, 0xffu);
    dst_p->admm_05432_a05 = (int16_t)admm_05432_a05;
    admm_05432_a06 = unpack_right_shift_u16(src_p[2], 0u, 0xffu);
    admm_05432_a06 |= unpack_left_shift_u16(src_p[3], 8u, 0xffu);
    dst_p->admm_05432_a06 = (int16_t)admm_05432_a06;
    admm_05432_a07 = unpack_right_shift_u16(src_p[4], 0u, 0xffu);
    admm_05432_a07 |= unpack_left_shift_u16(src_p[5], 8u, 0xffu);
    dst_p->admm_05432_a07 = (int16_t)admm_05432_a07;
    admm_05432_a08 = unpack_right_shift_u16(src_p[6], 0u, 0xffu);
    admm_05432_a08 |= unpack_left_shift_u16(src_p[7], 8u, 0xffu);
    dst_p->admm_05432_a08 = (int16_t)admm_05432_a08;

    return (0);
}

int16_t csm_volt_5720459_admm_05432_msg1_admm_05432_a05_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg1_admm_05432_a05_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg1_admm_05432_a05_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05432_msg1_admm_05432_a06_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg1_admm_05432_a06_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg1_admm_05432_a06_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05432_msg1_admm_05432_a07_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg1_admm_05432_a07_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg1_admm_05432_a07_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}

int16_t csm_volt_5720459_admm_05432_msg1_admm_05432_a08_encode(double value)
{
    return (int16_t)(value / 0.00061037019);
}

double csm_volt_5720459_admm_05432_msg1_admm_05432_a08_decode(int16_t value)
{
    return ((double)value * 0.00061037019);
}

bool csm_volt_5720459_admm_05432_msg1_admm_05432_a08_is_in_range(int16_t value)
{
    return ((value >= -32766) && (value <= 32766));
}
