/*
 * compile and run using:
 *      cc test_qsort.c -o ./test_qsort && ./test_qsort
 */


#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>


/* qsort comparator functions to sort in ascending order */
static int comp_ascending_uint8(const void *a, const void *b)
{
    return (*(int8_t *)a - *(int8_t *)b);
}
static int comp_ascending_uint8_unsigned(const void *a, const void *b)
{
    if (*(uint8_t *)a < *(uint8_t *)b)
    {
        return -1;
    }
    if (*(uint8_t *)a > *(uint8_t *)b)
    {
        return 1;
    }
    return 0;
}
static int comp_ascending_uint32(const void *a, const void *b)
{
    return (*(int32_t *)a - *(int32_t *)b);
}

/* sort an array on ascending order; used for checking frame priorities */
static void sort_ascending_uint8(uint8_t *arr, uint32_t arr_len)
{
    /* use qsort instead of rolling our own */
    qsort(arr, arr_len, sizeof(uint8_t), comp_ascending_uint8);
}
static void sort_ascending_uint8_unsigned(uint8_t *arr, uint32_t arr_len)
{
    /* use qsort instead of rolling our own */
    qsort(arr, arr_len, sizeof(uint8_t), comp_ascending_uint8_unsigned);
}
static void sort_ascending_uint32(uint32_t *arr, uint32_t arr_len)
{
    /* use qsort instead of rolling our own */
    qsort(arr, arr_len, sizeof(uint32_t), comp_ascending_uint32);
}


void main(void)
{
    #define VALNUM (12)
    uint8_t values_unsorted[VALNUM] = { 1, 18, 128, 127, 129, 0, 6, 4, 3, 0, 255, 253 };
    uint8_t values_sorted_0[VALNUM] = { 255, 255, 255, 255, 255, 255, 255, 255, 255, 255 };
    uint8_t values_sorted_1[VALNUM] = { 255, 255, 255, 255, 255, 255, 255, 255, 255, 255 };

    /* copy unsorted values because we sort in place */
    memcpy(values_sorted_0, values_unsorted, VALNUM);
    memcpy(values_sorted_1, values_unsorted, VALNUM);

    uint32_t index;

    /* show unsorted values */
    printf("US:");
    for (index = 0; index < VALNUM; index++)
    {
        printf("%2d|", values_unsorted[index]);
    }
    printf("\n");

    /* sort & show sorted values */
    sort_ascending_uint8(values_sorted_0, VALNUM);
    printf("S0:");
    for (index = 0; index < VALNUM; index++)
    {
        printf("%2d|", values_sorted_0[index]);
    }
    printf("\n");

    /* sort & show sorted values */
    sort_ascending_uint8_unsigned(values_sorted_1, VALNUM);
    printf("S1:");
    for (index = 0; index < VALNUM; index++)
    {
        printf("%2d|", values_sorted_1[index]);
    }
    printf("\n");


}
