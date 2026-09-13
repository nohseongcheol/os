#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdlib.h>
#include <limits.h>
#include <integer_types.h>
#include <errno.h>
#include <unistd.h>

#define CHECK(value) do { if (!(value)) return __LINE__; } while (0)

static int compare_int(const void *left, const void *right)
{
    int result = *(const int *)left, value = *(const int *)right;
    return (result > value) - (result < value);
}

int __posix_library_test(void)
{
    char transfer_buffer_2[64], source[64], *end_pointer, *saved_state, *address, *destination;
    const char *text = "abca", *input = " 	-0x80rest";
    int elements[257], index, value;
    object_size_type length;
    div_t result;
    ldiv_t decoded_value;
    char **saved_environment = environ;
    char *envp[] = {"ONE=first", "ONE_MORE=second", "EMPTY=", null_pointer};

    CHECK(memset(transfer_buffer_2, 0xab, sizeof(transfer_buffer_2)) == transfer_buffer_2);
    CHECK((unsigned char)transfer_buffer_2[63] == 0xab);
    CHECK(memcpy(transfer_buffer_2, "abcdef", 7) == transfer_buffer_2);
    CHECK(memmove(transfer_buffer_2 + 2, transfer_buffer_2, 5) == transfer_buffer_2 + 2);
    CHECK(memcmp(transfer_buffer_2, "ababcde", 7) == 0);
    CHECK(memmove(transfer_buffer_2, transfer_buffer_2 + 2, 5) == transfer_buffer_2);
    CHECK(memcmp(transfer_buffer_2, "abcde", 5) == 0);
    CHECK(memmove(transfer_buffer_2, transfer_buffer_2, 0) == transfer_buffer_2);
    CHECK(memcmp("\x80", "\x7f", 1) > 0);
    CHECK(memcmp(transfer_buffer_2, source, 0) == 0);
    CHECK(memchr(text, 'c', 4) == text + 2);
    CHECK(memchr(text, 0, 5) == text + 4);
    CHECK(memchr(text, 'z', 4) == null_pointer);
    CHECK(strlen("한국어") == 9 && strnlen("한국어", 4) == 4);
    CHECK(strnlen("", 3) == 0 && strnlen("abc", 0) == 0);
    CHECK(strcpy(transfer_buffer_2, text) == transfer_buffer_2 && strcmp(transfer_buffer_2, text) == 0);
    CHECK(stpcpy(transfer_buffer_2, "xy") == transfer_buffer_2 + 2 && transfer_buffer_2[2] == 0);
    memset(transfer_buffer_2, 7, sizeof(transfer_buffer_2));
    CHECK(strncpy(transfer_buffer_2, "xy", 5) == transfer_buffer_2);
    CHECK(!memcmp(transfer_buffer_2, "xy\0\0\0", 5) && transfer_buffer_2[5] == 7);
    CHECK(stpncpy(transfer_buffer_2, "abcdef", 3) == transfer_buffer_2 + 3 && transfer_buffer_2[3] == 0);
    CHECK(stpncpy(transfer_buffer_2, "a", 4) == transfer_buffer_2 + 1 && transfer_buffer_2[3] == 0);
    CHECK(strncpy(transfer_buffer_2, "z", 0) == transfer_buffer_2 && transfer_buffer_2[0] == 'a');
    strcpy(transfer_buffer_2, "a");
    CHECK(strcat(transfer_buffer_2, "bc") == transfer_buffer_2 && !strcmp(transfer_buffer_2, "abc"));
    CHECK(strncat(transfer_buffer_2, "def", 2) == transfer_buffer_2 && !strcmp(transfer_buffer_2, "abcde"));
    CHECK(strncat(transfer_buffer_2, "xyz", 0) == transfer_buffer_2 && !strcmp(transfer_buffer_2, "abcde"));
    CHECK(strcmp("", "a") < 0 && strcmp("\xff", "\x7f") > 0);
    CHECK(strncmp("abc", "abd", 2) == 0 && strncmp("abc", "abd", 3) < 0);
    CHECK(strncmp("a", "b", 0) == 0 && strcoll("a", "b") < 0);
    CHECK(strxfrm(null_pointer, "abc", 0) == 3);
    CHECK(strxfrm(transfer_buffer_2, "abc", 4) == 3 && !strcmp(transfer_buffer_2, "abc"));
    CHECK(strchr(text, 'a') == text && strrchr(text, 'a') == text + 3);
    CHECK(strchr(text, 0) == text + 4 && strrchr(text, 0) == text + 4);
    CHECK(strchr(text, 'z') == null_pointer && strrchr(text, 'z') == null_pointer);
    CHECK(strstr(text, "bc") == text + 1 && strstr(text, "") == text);
    CHECK(strstr(text, "abcaa") == null_pointer && strstr(text, "z") == null_pointer);
    CHECK(strspn("aaabbz", "ab") == 5 && strspn("abc", "") == 0);
    CHECK(strcspn("aaabbz", "bz") == 3 && strcspn("abc", "") == 3);
    CHECK(strpbrk(text, "cz") == text + 2 && strpbrk(text, "z") == null_pointer);
    strcpy(transfer_buffer_2, ",,one;two,,");
    CHECK(!strcmp(strtok_r(transfer_buffer_2, ",;", &saved_state), "one"));
    strcpy(source, "x:y");
    CHECK(!strcmp(strtok(source, ":"), "x"));
    CHECK(!strcmp(strtok_r(null_pointer, ",;", &saved_state), "two"));
    CHECK(strtok_r(null_pointer, ",;", &saved_state) == null_pointer);
    CHECK(!strcmp(strtok(null_pointer, ":"), "y") && strtok(null_pointer, ":") == null_pointer);
    strcpy(source, "x,y");
    CHECK(!strcmp(strtok_r(source, "", &saved_state), "x,y"));
    CHECK(strtok_r(null_pointer, "", &saved_state) == null_pointer);
    CHECK(strcasecmp("aBc", "AbC") == 0 && strcasecmp("a", "B") < 0);
    CHECK(strncasecmp("aBcX", "AbCy", 3) == 0 && strncasecmp("a", "B", 1) < 0);

    for (value = -1; value <= 255; ++value) {
        int low = value >= 'a' && value <= 'z', high = value >= 'A' && value <= 'Z';
        int digit = value >= '0' && value <= '9';
        CHECK(!!isalpha(value) == (low || high));
        CHECK(!!isalnum(value) == (low || high || digit));
        CHECK(!!isdigit(value) == digit);
        CHECK(!!islower(value) == low && !!isupper(value) == high);
        CHECK(!!isblank(value) == (value == ' ' || value == '\t'));
        CHECK(!!isspace(value) == (value == ' ' || (value >= 9 && value <= 13)));
        CHECK(!!iscntrl(value) == ((value >= 0 && value < 32) || value == 127));
        CHECK(!!isprint(value) == (value >= 32 && value <= 126));
        CHECK(!!isgraph(value) == (value >= 33 && value <= 126));
        CHECK(!!ispunct(value) == (value >= 33 && value <= 126 && !low && !high && !digit));
        CHECK(!!isxdigit(value) == (digit || (value >= 'a' && value <= 'f') || (value >= 'A' && value <= 'F')));
        CHECK(tolower(value) == (high ? value + 32 : value));
        CHECK(toupper(value) == (low ? value - 32 : value));
    }
    errno = input_output_error;
    CHECK(strtol(input, &end_pointer, 0) == -128 && !strcmp(end_pointer, "rest") && errno == input_output_error);
    CHECK(strtol("2147483647", null_pointer, 10) == long_integer_maximum);
    CHECK(strtol("-2147483648", null_pointer, 10) == long_integer_minimum);
    errno = 0;
    CHECK(strtol("2147483648xxx", &end_pointer, 10) == long_integer_maximum && errno == value_out_of_range && *end_pointer == 'x');
    errno = 0;
    CHECK(strtol("-99999999999999999z", &end_pointer, 10) == long_integer_minimum && errno == value_out_of_range && *end_pointer == 'z');
    CHECK(strtol("077", null_pointer, 0) == 63 && strtol("0Xff", null_pointer, 16) == 255);
    text = "-0x";
    CHECK(strtol(text, &end_pointer, 0) == 0 && end_pointer == text + 2);
    text = "  +z";
    CHECK(strtol(text, &end_pointer, 10) == 0 && end_pointer == text);
    errno = 0;
    CHECK(strtol(text, &end_pointer, 1) == 0 && errno == invalid_argument && end_pointer == text);
    CHECK(strtol("z", null_pointer, 36) == 35 && strtol("101", null_pointer, 2) == 5);
    errno = input_output_error;
    CHECK(strtoul("4294967295", null_pointer, 10) == unsigned_long_maximum && errno == input_output_error);
    CHECK(strtoul("-1", null_pointer, 10) == unsigned_long_maximum && errno == input_output_error);
    errno = value_out_of_range;
    CHECK(strtoul("-2", null_pointer, 10) == unsigned_long_maximum - 1 && errno == value_out_of_range);
    errno = 0;
    CHECK(strtoul("-4294967296x", &end_pointer, 10) == unsigned_long_maximum && errno == value_out_of_range && *end_pointer == 'x');
    CHECK(atoi(" -123tail") == -123 && atol("+456") == 456);
    CHECK(abs(-4) == 4 && abs(0) == 0 && labs(-99L) == 99L);
    result = div(-7, 3); decoded_value = ldiv(7L, -3L);
    CHECK(result.quot == -2 && result.rem == -1 && decoded_value.quot == -2 && decoded_value.rem == 1);

    for (length = 0; length <= 257; ++length) {
        for (index = 0; index < (int)length; ++index) elements[index] = ((index * 37 + (int)length) % 19) - 9;
        qsort(elements, length, sizeof(int), compare_int);
        for (index = 1; index < (int)length; ++index) CHECK(elements[index - 1] <= elements[index]);
        for (index = 0; index < (int)length; ++index) {
            int *found = bsearch(&elements[index], elements, length, sizeof(int), compare_int);
            CHECK(found && *found == elements[index]);
        }
        value = 100;
        CHECK(bsearch(&value, elements, length, sizeof(int), compare_int) == null_pointer);
    }
    environ = envp;
    CHECK(!strcmp(getenv("ONE"), "first") && !strcmp(getenv("EMPTY"), ""));
    CHECK(getenv("ON") == null_pointer && getenv("") == null_pointer && getenv("ONE=first") == null_pointer);
    environ = saved_environment;

    errno = input_output_error;
    free(null_pointer);
    CHECK(errno == input_output_error);
    address = malloc(17);
    CHECK(address && ((pointer_sized_unsigned_integer)address & 15U) == 0);
    memset(address, 0x59, 17);
    destination = realloc(address, 100);
    CHECK(destination);
    for (index = 0; index < 17; ++index) CHECK(destination[index] == 0x59);
    errno = 0;
    CHECK(realloc(destination, (object_size_type)-1) == null_pointer && errno == insufficient_memory);
    CHECK(destination[0] == 0x59);
    address = realloc(destination, 3);
    CHECK(address == destination && address[0] == 0x59);
    address = realloc(destination, 0);
    CHECK(address && address[0] == 0x59);
    errno = input_output_error;
    free(address);
    CHECK(errno == input_output_error);
    errno = 0;
    CHECK(calloc((object_size_type)-1, 2) == null_pointer && errno == insufficient_memory);
    CHECK(malloc((object_size_type)-1) == null_pointer && errno == insufficient_memory);
    address = calloc(19, 3);
    CHECK(address);
    for (index = 0; index < 57; ++index) CHECK(address[index] == 0);
    free(address);
    address = malloc(0); CHECK(address); free(address);
    address = realloc(null_pointer, 11); CHECK(address); free(address);
    address = strdup("자료"); CHECK(address && !strcmp(address, "자료")); free(address);
    address = strndup("abcdef", 3); CHECK(address && !strcmp(address, "abc")); free(address);
    address = strndup("abc", 0); CHECK(address && !strcmp(address, "")); free(address);
    /* Repeated use must reuse freed storage instead of growing brk each time. */
    address = malloc(4096); CHECK(address); free(address);
    destination = sbrk(0);
    for (index = 0; index < 100; ++index) {
        address = malloc(1024); CHECK(address); memset(address, index, 1024); free(address);
    }
    CHECK(sbrk(0) == destination);
    return 0;
}
