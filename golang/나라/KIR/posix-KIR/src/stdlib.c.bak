#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <unistd.h>

static int digit_value(unsigned char character)
{
    if (isdigit(character)) return character - '0';
    if (isalpha(character)) return tolower(character) - 'a' + 10;
    return 36;
}

static unsigned long parse_unsigned(const char *text, char **end_pointer,
                                    int radix, int is_unsigned, int *negative, int *overflow)
{
    const char *cursor = text, *first_match;
    unsigned long magnitude = 0, maximum;
    int digit;
    if (end_pointer) *end_pointer = (char *)text;
    *negative = 0;
    *overflow = 0;
    if (radix && (radix < 2 || radix > 36)) { errno = invalid_argument; return 0; }
    while (isspace((unsigned char)*cursor)) ++cursor;
    if (*cursor == '+' || *cursor == '-') { *negative = *cursor == '-'; ++cursor; }
    if ((radix == 0 || radix == 16) && cursor[0] == '0' &&
        (cursor[1] == 'x' || cursor[1] == 'X') && digit_value((unsigned char)cursor[2]) < 16) {
        cursor += 2; radix = 16;
    }
    if (!radix) radix = *cursor == '0' ? 8 : 10;
    maximum = is_unsigned ? unsigned_long_maximum : (unsigned long)long_integer_maximum + (unsigned long)*negative;
    first_match = cursor;
    while ((digit = digit_value((unsigned char)*cursor)) < radix) {
        if (magnitude > (maximum - (unsigned long)digit) / (unsigned long)radix)
            *overflow = 1;
        else if (!*overflow)
            magnitude = magnitude * (unsigned long)radix + (unsigned long)digit;
        ++cursor;
    }
    if (cursor == first_match) return 0;
    if (end_pointer) *end_pointer = (char *)cursor;
    if (*overflow) { errno = value_out_of_range; return maximum; }
    return magnitude;
}

long strtol(const char *text, char **end_pointer, int radix)
{
    int negative, overflow;
    unsigned long magnitude = parse_unsigned(text, end_pointer, radix, 0, &negative, &overflow);
    if (!negative) return (long)magnitude;
    return magnitude == (unsigned long)long_integer_maximum + 1UL ? long_integer_minimum : -(long)magnitude;
}

unsigned long strtoul(const char *text, char **end_pointer, int radix)
{
    int negative, overflow;
    unsigned long magnitude = parse_unsigned(text, end_pointer, radix, 1, &negative, &overflow);
    if (overflow) return unsigned_long_maximum;
    return negative ? 0UL - magnitude : magnitude;
}

int atoi(const char *text) { return (int)strtol(text, null_pointer, 10); }
long atol(const char *text) { return strtol(text, null_pointer, 10); }
int abs(int value) { return value < 0 ? -value : value; }
long labs(long value) { return value < 0 ? -value : value; }
div_t div(int left, int right) { div_t result = {left / right, left % right}; return result; }
ldiv_t ldiv(long left, long right) { ldiv_t result = {left / right, left % right}; return result; }

static void swap_elements(unsigned char *left, unsigned char *right, object_size_type element_size)
{
    while (element_size--) { unsigned char temporary = *left; *left++ = *right; *right++ = temporary; }
}

static void sift_down(unsigned char *elements, object_size_type hole, object_size_type count,
                      object_size_type element_size, int (*compare)(const void *, const void *))
{
    while (hole < count / 2) {
        object_size_type child = hole * 2 + 1;
        if (child + 1 < count && compare(elements + child * element_size, elements + (child + 1) * element_size) < 0)
            ++child;
        if (compare(elements + hole * element_size, elements + child * element_size) >= 0) return;
        swap_elements(elements + hole * element_size, elements + child * element_size, element_size);
        hole = child;
    }
}

void qsort(void *elements, object_size_type count, object_size_type element_size,
           int (*compare)(const void *, const void *))
{
    unsigned char *cursor = elements;
    object_size_type index;
    if (count < 2 || !element_size || count > (object_size_type)-1 / element_size) return;
    /* Heap sort: bounded stack, O(n log n), comparator receives array elements. */
    for (index = count / 2; index; ) sift_down(cursor, --index, count, element_size, compare);
    for (index = count - 1; index; --index) {
        swap_elements(cursor, cursor + index * element_size, element_size);
        sift_down(cursor, 0, index, element_size, compare);
    }
}

void *bsearch(const void *source, const void *elements, object_size_type count,
              object_size_type element_size, int (*compare)(const void *, const void *))
{
    object_size_type low = 0, high = count;
    const unsigned char *cursor = elements;
    if (!element_size || count > (object_size_type)-1 / element_size) return null_pointer;
    while (low < high) {
        object_size_type middle = low + (high - low) / 2;
        int result = compare(source, cursor + middle * element_size);
        if (!result) return (void *)(cursor + middle * element_size);
        if (result < 0) high = middle;
        else low = middle + 1;
    }
    return null_pointer;
}

char *getenv(const char *system_identity)
{
    object_size_type length = strlen(system_identity);
    char **cursor = environ;
    if (!length || strchr(system_identity, '=') || !cursor) return null_pointer;
    while (*cursor) {
        if (!strncmp(*cursor, system_identity, length) && (*cursor)[length] == '=') return *cursor + length + 1;
        ++cursor;
    }
    return null_pointer;
}
