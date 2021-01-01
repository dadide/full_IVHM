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
 * This file was generated by cantools version 35.3.0 Mon Nov 23 13:58:40 2020.
 */

#include <string.h>

#include "xian_imu2.h"

static inline uint8_t pack_left_shift_u16(
    uint16_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint8_t)((uint8_t)(value << shift) & mask);
}

static inline uint8_t pack_left_shift_u32(
    uint32_t value,
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

static inline uint8_t pack_right_shift_u32(
    uint32_t value,
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

static inline uint32_t unpack_left_shift_u32(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint32_t)((uint32_t)(value & mask) << shift);
}

static inline uint16_t unpack_right_shift_u16(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint16_t)((uint16_t)(value & mask) >> shift);
}

static inline uint32_t unpack_right_shift_u32(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint32_t)((uint32_t)(value & mask) >> shift);
}

int xian_imu2_imu1_pack(
    uint8_t *dst_p,
    const struct xian_imu2_imu1_t *src_p,
    size_t size)
{
    uint16_t t_x;
    uint32_t acc_x;
    uint32_t gyro_x;

    if (size < 8u) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    gyro_x = (uint32_t)src_p->gyro_x;
    dst_p[0] |= pack_right_shift_u32(gyro_x, 16u, 0xffu);
    dst_p[1] |= pack_right_shift_u32(gyro_x, 8u, 0xffu);
    dst_p[2] |= pack_left_shift_u32(gyro_x, 0u, 0xffu);
    acc_x = (uint32_t)src_p->acc_x;
    dst_p[3] |= pack_right_shift_u32(acc_x, 16u, 0xffu);
    dst_p[4] |= pack_right_shift_u32(acc_x, 8u, 0xffu);
    dst_p[5] |= pack_left_shift_u32(acc_x, 0u, 0xffu);
    t_x = (uint16_t)src_p->t_x;
    dst_p[6] |= pack_right_shift_u16(t_x, 8u, 0xffu);
    dst_p[7] |= pack_left_shift_u16(t_x, 0u, 0xffu);

    return (8);
}

int xian_imu2_imu1_unpack(
    struct xian_imu2_imu1_t *dst_p,
    const uint8_t *src_p,
    size_t size)
{
    uint16_t t_x;
    uint32_t acc_x;
    uint32_t gyro_x;

    if (size < 8u) {
        return (-EINVAL);
    }

    gyro_x = unpack_left_shift_u32(src_p[0], 16u, 0xffu);
    gyro_x |= unpack_left_shift_u32(src_p[1], 8u, 0xffu);
    gyro_x |= unpack_right_shift_u32(src_p[2], 0u, 0xffu);

    if ((gyro_x & (1u << 23)) != 0u) {
        gyro_x |= 0xff000000u;
    }

    dst_p->gyro_x = (int32_t)gyro_x;
    acc_x = unpack_left_shift_u32(src_p[3], 16u, 0xffu);
    acc_x |= unpack_left_shift_u32(src_p[4], 8u, 0xffu);
    acc_x |= unpack_right_shift_u32(src_p[5], 0u, 0xffu);

    if ((acc_x & (1u << 23)) != 0u) {
        acc_x |= 0xff000000u;
    }

    dst_p->acc_x = (int32_t)acc_x;
    t_x = unpack_left_shift_u16(src_p[6], 8u, 0xffu);
    t_x |= unpack_right_shift_u16(src_p[7], 0u, 0xffu);
    dst_p->t_x = (int16_t)t_x;

    return (0);
}

int32_t xian_imu2_imu1_gyro_x_encode(double value)
{
    return (int32_t)(value / 0.001);
}

double xian_imu2_imu1_gyro_x_decode(int32_t value)
{
    return ((double)value * 0.001);
}

bool xian_imu2_imu1_gyro_x_is_in_range(int32_t value)
{
    return ((value >= -8388608) && (value <= 8388607));
}

int32_t xian_imu2_imu1_acc_x_encode(double value)
{
    return (int32_t)(value / 0.00001);
}

double xian_imu2_imu1_acc_x_decode(int32_t value)
{
    return ((double)value * 0.00001);
}

bool xian_imu2_imu1_acc_x_is_in_range(int32_t value)
{
    return ((value >= -8388608) && (value <= 8388607));
}

int16_t xian_imu2_imu1_t_x_encode(double value)
{
    return (int16_t)(value / 0.01);
}

double xian_imu2_imu1_t_x_decode(int16_t value)
{
    return ((double)value * 0.01);
}

bool xian_imu2_imu1_t_x_is_in_range(int16_t value)
{
    (void)value;

    return (true);
}

int xian_imu2_imu2_pack(
    uint8_t *dst_p,
    const struct xian_imu2_imu2_t *src_p,
    size_t size)
{
    uint16_t t_y;
    uint32_t acc_y;
    uint32_t gyro_y;

    if (size < 8u) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    gyro_y = (uint32_t)src_p->gyro_y;
    dst_p[0] |= pack_right_shift_u32(gyro_y, 16u, 0xffu);
    dst_p[1] |= pack_right_shift_u32(gyro_y, 8u, 0xffu);
    dst_p[2] |= pack_left_shift_u32(gyro_y, 0u, 0xffu);
    acc_y = (uint32_t)src_p->acc_y;
    dst_p[3] |= pack_right_shift_u32(acc_y, 16u, 0xffu);
    dst_p[4] |= pack_right_shift_u32(acc_y, 8u, 0xffu);
    dst_p[5] |= pack_left_shift_u32(acc_y, 0u, 0xffu);
    t_y = (uint16_t)src_p->t_y;
    dst_p[6] |= pack_right_shift_u16(t_y, 8u, 0xffu);
    dst_p[7] |= pack_left_shift_u16(t_y, 0u, 0xffu);

    return (8);
}

int xian_imu2_imu2_unpack(
    struct xian_imu2_imu2_t *dst_p,
    const uint8_t *src_p,
    size_t size)
{
    uint16_t t_y;
    uint32_t acc_y;
    uint32_t gyro_y;

    if (size < 8u) {
        return (-EINVAL);
    }

    gyro_y = unpack_left_shift_u32(src_p[0], 16u, 0xffu);
    gyro_y |= unpack_left_shift_u32(src_p[1], 8u, 0xffu);
    gyro_y |= unpack_right_shift_u32(src_p[2], 0u, 0xffu);

    if ((gyro_y & (1u << 23)) != 0u) {
        gyro_y |= 0xff000000u;
    }

    dst_p->gyro_y = (int32_t)gyro_y;
    acc_y = unpack_left_shift_u32(src_p[3], 16u, 0xffu);
    acc_y |= unpack_left_shift_u32(src_p[4], 8u, 0xffu);
    acc_y |= unpack_right_shift_u32(src_p[5], 0u, 0xffu);

    if ((acc_y & (1u << 23)) != 0u) {
        acc_y |= 0xff000000u;
    }

    dst_p->acc_y = (int32_t)acc_y;
    t_y = unpack_left_shift_u16(src_p[6], 8u, 0xffu);
    t_y |= unpack_right_shift_u16(src_p[7], 0u, 0xffu);
    dst_p->t_y = (int16_t)t_y;

    return (0);
}

int32_t xian_imu2_imu2_gyro_y_encode(double value)
{
    return (int32_t)(value / 0.001);
}

double xian_imu2_imu2_gyro_y_decode(int32_t value)
{
    return ((double)value * 0.001);
}

bool xian_imu2_imu2_gyro_y_is_in_range(int32_t value)
{
    return ((value >= -8388608) && (value <= 8388607));
}

int32_t xian_imu2_imu2_acc_y_encode(double value)
{
    return (int32_t)(value / 0.00001);
}

double xian_imu2_imu2_acc_y_decode(int32_t value)
{
    return ((double)value * 0.00001);
}

bool xian_imu2_imu2_acc_y_is_in_range(int32_t value)
{
    return ((value >= -8388608) && (value <= 8388607));
}

int16_t xian_imu2_imu2_t_y_encode(double value)
{
    return (int16_t)(value / 0.01);
}

double xian_imu2_imu2_t_y_decode(int16_t value)
{
    return ((double)value * 0.01);
}

bool xian_imu2_imu2_t_y_is_in_range(int16_t value)
{
    (void)value;

    return (true);
}

int xian_imu2_imu3_pack(
    uint8_t *dst_p,
    const struct xian_imu2_imu3_t *src_p,
    size_t size)
{
    uint16_t t_z;
    uint32_t acc_z;
    uint32_t gyro_z;

    if (size < 8u) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    gyro_z = (uint32_t)src_p->gyro_z;
    dst_p[0] |= pack_right_shift_u32(gyro_z, 16u, 0xffu);
    dst_p[1] |= pack_right_shift_u32(gyro_z, 8u, 0xffu);
    dst_p[2] |= pack_left_shift_u32(gyro_z, 0u, 0xffu);
    acc_z = (uint32_t)src_p->acc_z;
    dst_p[3] |= pack_right_shift_u32(acc_z, 16u, 0xffu);
    dst_p[4] |= pack_right_shift_u32(acc_z, 8u, 0xffu);
    dst_p[5] |= pack_left_shift_u32(acc_z, 0u, 0xffu);
    t_z = (uint16_t)src_p->t_z;
    dst_p[6] |= pack_right_shift_u16(t_z, 8u, 0xffu);
    dst_p[7] |= pack_left_shift_u16(t_z, 0u, 0xffu);

    return (8);
}

int xian_imu2_imu3_unpack(
    struct xian_imu2_imu3_t *dst_p,
    const uint8_t *src_p,
    size_t size)
{
    uint16_t t_z;
    uint32_t acc_z;
    uint32_t gyro_z;

    if (size < 8u) {
        return (-EINVAL);
    }

    gyro_z = unpack_left_shift_u32(src_p[0], 16u, 0xffu);
    gyro_z |= unpack_left_shift_u32(src_p[1], 8u, 0xffu);
    gyro_z |= unpack_right_shift_u32(src_p[2], 0u, 0xffu);

    if ((gyro_z & (1u << 23)) != 0u) {
        gyro_z |= 0xff000000u;
    }

    dst_p->gyro_z = (int32_t)gyro_z;
    acc_z = unpack_left_shift_u32(src_p[3], 16u, 0xffu);
    acc_z |= unpack_left_shift_u32(src_p[4], 8u, 0xffu);
    acc_z |= unpack_right_shift_u32(src_p[5], 0u, 0xffu);

    if ((acc_z & (1u << 23)) != 0u) {
        acc_z |= 0xff000000u;
    }

    dst_p->acc_z = (int32_t)acc_z;
    t_z = unpack_left_shift_u16(src_p[6], 8u, 0xffu);
    t_z |= unpack_right_shift_u16(src_p[7], 0u, 0xffu);
    dst_p->t_z = (int16_t)t_z;

    return (0);
}

int32_t xian_imu2_imu3_gyro_z_encode(double value)
{
    return (int32_t)(value / 0.001);
}

double xian_imu2_imu3_gyro_z_decode(int32_t value)
{
    return ((double)value * 0.001);
}

bool xian_imu2_imu3_gyro_z_is_in_range(int32_t value)
{
    return ((value >= -8388608) && (value <= 8388607));
}

int32_t xian_imu2_imu3_acc_z_encode(double value)
{
    return (int32_t)(value / 0.00001);
}

double xian_imu2_imu3_acc_z_decode(int32_t value)
{
    return ((double)value * 0.00001);
}

bool xian_imu2_imu3_acc_z_is_in_range(int32_t value)
{
    return ((value >= -8388608) && (value <= 8388607));
}

int16_t xian_imu2_imu3_t_z_encode(double value)
{
    return (int16_t)(value / 0.01);
}

double xian_imu2_imu3_t_z_decode(int16_t value)
{
    return ((double)value * 0.01);
}

bool xian_imu2_imu3_t_z_is_in_range(int16_t value)
{
    (void)value;

    return (true);
}
