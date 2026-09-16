#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdlib.h>
#include <limits.h>
#include <целочисленные_типы.h>
#include <errno.h>
#include <unistd.h>

#define CHECK(значение) do { if (!(значение)) return __LINE__; } while (0)

static int compare_int(const void *left, const void *right)
{
    int result = *(const int *)left, значение = *(const int *)right;
    return (result > значение) - (result < значение);
}

int __posix_library_test(void)
{
    char буфер_передачи_2[64], source[64], *end_pointer, *saved_state, *address, *destination;
    const char *text = "abca", *input = " 	-0x80rest";
    int elements[257], index, значение;
    size_t длина;
    div_t result;
    ldiv_t decoded;
    char **saved_environment = environ;
    char *envp[] = {"ONE=first", "ONE_MORE=second", "EMPTY=", NULL};

    CHECK(memset(буфер_передачи_2, 0xab, sizeof(буфер_передачи_2)) == буфер_передачи_2);
    CHECK((unsigned char)буфер_передачи_2[63] == 0xab);
    CHECK(memcpy(буфер_передачи_2, "abcdef", 7) == буфер_передачи_2);
    CHECK(memmove(буфер_передачи_2 + 2, буфер_передачи_2, 5) == буфер_передачи_2 + 2);
    CHECK(memcmp(буфер_передачи_2, "ababcde", 7) == 0);
    CHECK(memmove(буфер_передачи_2, буфер_передачи_2 + 2, 5) == буфер_передачи_2);
    CHECK(memcmp(буфер_передачи_2, "abcde", 5) == 0);
    CHECK(memmove(буфер_передачи_2, буфер_передачи_2, 0) == буфер_передачи_2);
    CHECK(memcmp("\x80", "\x7f", 1) > 0);
    CHECK(memcmp(буфер_передачи_2, source, 0) == 0);
    CHECK(memchr(text, 'c', 4) == text + 2);
    CHECK(memchr(text, 0, 5) == text + 4);
    CHECK(memchr(text, 'z', 4) == NULL);
    CHECK(strlen("한국어") == 9 && strnlen("한국어", 4) == 4);
    CHECK(strnlen("", 3) == 0 && strnlen("abc", 0) == 0);
    CHECK(strcpy(буфер_передачи_2, text) == буфер_передачи_2 && strcmp(буфер_передачи_2, text) == 0);
    CHECK(stpcpy(буфер_передачи_2, "xy") == буфер_передачи_2 + 2 && буфер_передачи_2[2] == 0);
    memset(буфер_передачи_2, 7, sizeof(буфер_передачи_2));
    CHECK(strncpy(буфер_передачи_2, "xy", 5) == буфер_передачи_2);
    CHECK(!memcmp(буфер_передачи_2, "xy\0\0\0", 5) && буфер_передачи_2[5] == 7);
    CHECK(stpncpy(буфер_передачи_2, "abcdef", 3) == буфер_передачи_2 + 3 && буфер_передачи_2[3] == 0);
    CHECK(stpncpy(буфер_передачи_2, "a", 4) == буфер_передачи_2 + 1 && буфер_передачи_2[3] == 0);
    CHECK(strncpy(буфер_передачи_2, "z", 0) == буфер_передачи_2 && буфер_передачи_2[0] == 'a');
    strcpy(буфер_передачи_2, "a");
    CHECK(strcat(буфер_передачи_2, "bc") == буфер_передачи_2 && !strcmp(буфер_передачи_2, "abc"));
    CHECK(strncat(буфер_передачи_2, "def", 2) == буфер_передачи_2 && !strcmp(буфер_передачи_2, "abcde"));
    CHECK(strncat(буфер_передачи_2, "xyz", 0) == буфер_передачи_2 && !strcmp(буфер_передачи_2, "abcde"));
    CHECK(strcmp("", "a") < 0 && strcmp("\xff", "\x7f") > 0);
    CHECK(strncmp("abc", "abd", 2) == 0 && strncmp("abc", "abd", 3) < 0);
    CHECK(strncmp("a", "b", 0) == 0 && strcoll("a", "b") < 0);
    CHECK(strxfrm(NULL, "abc", 0) == 3);
    CHECK(strxfrm(буфер_передачи_2, "abc", 4) == 3 && !strcmp(буфер_передачи_2, "abc"));
    CHECK(strchr(text, 'a') == text && strrchr(text, 'a') == text + 3);
    CHECK(strchr(text, 0) == text + 4 && strrchr(text, 0) == text + 4);
    CHECK(strchr(text, 'z') == NULL && strrchr(text, 'z') == NULL);
    CHECK(strstr(text, "bc") == text + 1 && strstr(text, "") == text);
    CHECK(strstr(text, "abcaa") == NULL && strstr(text, "z") == NULL);
    CHECK(strspn("aaabbz", "ab") == 5 && strspn("abc", "") == 0);
    CHECK(strcspn("aaabbz", "bz") == 3 && strcspn("abc", "") == 3);
    CHECK(strpbrk(text, "cz") == text + 2 && strpbrk(text, "z") == NULL);
    strcpy(буфер_передачи_2, ",,one;two,,");
    CHECK(!strcmp(strtok_r(буфер_передачи_2, ",;", &saved_state), "one"));
    strcpy(source, "x:y");
    CHECK(!strcmp(strtok(source, ":"), "x"));
    CHECK(!strcmp(strtok_r(NULL, ",;", &saved_state), "two"));
    CHECK(strtok_r(NULL, ",;", &saved_state) == NULL);
    CHECK(!strcmp(strtok(NULL, ":"), "y") && strtok(NULL, ":") == NULL);
    strcpy(source, "x,y");
    CHECK(!strcmp(strtok_r(source, "", &saved_state), "x,y"));
    CHECK(strtok_r(NULL, "", &saved_state) == NULL);
    CHECK(strcasecmp("aBc", "AbC") == 0 && strcasecmp("a", "B") < 0);
    CHECK(strncasecmp("aBcX", "AbCy", 3) == 0 && strncasecmp("a", "B", 1) < 0);

    for (значение = -1; значение <= 255; ++значение) {
        int low = значение >= 'a' && значение <= 'z', high = значение >= 'A' && значение <= 'Z';
        int digit = значение >= '0' && значение <= '9';
        CHECK(!!isalpha(значение) == (low || high));
        CHECK(!!isalnum(значение) == (low || high || digit));
        CHECK(!!isdigit(значение) == digit);
        CHECK(!!islower(значение) == low && !!isupper(значение) == high);
        CHECK(!!isblank(значение) == (значение == ' ' || значение == '\t'));
        CHECK(!!isspace(значение) == (значение == ' ' || (значение >= 9 && значение <= 13)));
        CHECK(!!iscntrl(значение) == ((значение >= 0 && значение < 32) || значение == 127));
        CHECK(!!isprint(значение) == (значение >= 32 && значение <= 126));
        CHECK(!!isgraph(значение) == (значение >= 33 && значение <= 126));
        CHECK(!!ispunct(значение) == (значение >= 33 && значение <= 126 && !low && !high && !digit));
        CHECK(!!isxdigit(значение) == (digit || (значение >= 'a' && значение <= 'f') || (значение >= 'A' && значение <= 'F')));
        CHECK(tolower(значение) == (high ? значение + 32 : значение));
        CHECK(toupper(значение) == (low ? значение - 32 : значение));
    }
    errno = EIO;
    CHECK(strtol(input, &end_pointer, 0) == -128 && !strcmp(end_pointer, "rest") && errno == EIO);
    CHECK(strtol("2147483647", NULL, 10) == LONG_MAX);
    CHECK(strtol("-2147483648", NULL, 10) == LONG_MIN);
    errno = 0;
    CHECK(strtol("2147483648xxx", &end_pointer, 10) == LONG_MAX && errno == ERANGE && *end_pointer == 'x');
    errno = 0;
    CHECK(strtol("-99999999999999999z", &end_pointer, 10) == LONG_MIN && errno == ERANGE && *end_pointer == 'z');
    CHECK(strtol("077", NULL, 0) == 63 && strtol("0Xff", NULL, 16) == 255);
    text = "-0x";
    CHECK(strtol(text, &end_pointer, 0) == 0 && end_pointer == text + 2);
    text = "  +z";
    CHECK(strtol(text, &end_pointer, 10) == 0 && end_pointer == text);
    errno = 0;
    CHECK(strtol(text, &end_pointer, 1) == 0 && errno == EINVAL && end_pointer == text);
    CHECK(strtol("z", NULL, 36) == 35 && strtol("101", NULL, 2) == 5);
    errno = EIO;
    CHECK(strtoul("4294967295", NULL, 10) == ULONG_MAX && errno == EIO);
    CHECK(strtoul("-1", NULL, 10) == ULONG_MAX && errno == EIO);
    errno = ERANGE;
    CHECK(strtoul("-2", NULL, 10) == ULONG_MAX - 1 && errno == ERANGE);
    errno = 0;
    CHECK(strtoul("-4294967296x", &end_pointer, 10) == ULONG_MAX && errno == ERANGE && *end_pointer == 'x');
    CHECK(atoi(" -123tail") == -123 && atol("+456") == 456);
    CHECK(abs(-4) == 4 && abs(0) == 0 && labs(-99L) == 99L);
    result = div(-7, 3); decoded = ldiv(7L, -3L);
    CHECK(result.quot == -2 && result.rem == -1 && decoded.quot == -2 && decoded.rem == 1);

    for (длина = 0; длина <= 257; ++длина) {
        for (index = 0; index < (int)длина; ++index) elements[index] = ((index * 37 + (int)длина) % 19) - 9;
        qsort(elements, длина, sizeof(int), compare_int);
        for (index = 1; index < (int)длина; ++index) CHECK(elements[index - 1] <= elements[index]);
        for (index = 0; index < (int)длина; ++index) {
            int *found = bsearch(&elements[index], elements, длина, sizeof(int), compare_int);
            CHECK(found && *found == elements[index]);
        }
        значение = 100;
        CHECK(bsearch(&значение, elements, длина, sizeof(int), compare_int) == NULL);
    }
    environ = envp;
    CHECK(!strcmp(getenv("ONE"), "first") && !strcmp(getenv("EMPTY"), ""));
    CHECK(getenv("ON") == NULL && getenv("") == NULL && getenv("ONE=first") == NULL);
    environ = saved_environment;

    errno = EIO;
    free(NULL);
    CHECK(errno == EIO);
    address = malloc(17);
    CHECK(address && ((uintptr_t)address & 15U) == 0);
    memset(address, 0x59, 17);
    destination = realloc(address, 100);
    CHECK(destination);
    for (index = 0; index < 17; ++index) CHECK(destination[index] == 0x59);
    errno = 0;
    CHECK(realloc(destination, (size_t)-1) == NULL && errno == ENOMEM);
    CHECK(destination[0] == 0x59);
    address = realloc(destination, 3);
    CHECK(address == destination && address[0] == 0x59);
    address = realloc(destination, 0);
    CHECK(address && address[0] == 0x59);
    errno = EIO;
    free(address);
    CHECK(errno == EIO);
    errno = 0;
    CHECK(calloc((size_t)-1, 2) == NULL && errno == ENOMEM);
    CHECK(malloc((size_t)-1) == NULL && errno == ENOMEM);
    address = calloc(19, 3);
    CHECK(address);
    for (index = 0; index < 57; ++index) CHECK(address[index] == 0);
    free(address);
    address = malloc(0); CHECK(address); free(address);
    address = realloc(NULL, 11); CHECK(address); free(address);
    address = strdup("자료"); CHECK(address && !strcmp(address, "자료")); free(address);
    address = strndup("abcdef", 3); CHECK(address && !strcmp(address, "abc")); free(address);
    address = strndup("abc", 0); CHECK(address && !strcmp(address, "")); free(address);
    /* Repeated use must reuse freed storage instead of growing brk each time. */
    address = malloc(4096); CHECK(address); free(address);
    destination = сместить_конец_динамической_памяти(0);
    for (index = 0; index < 100; ++index) {
        address = malloc(1024); CHECK(address); memset(address, index, 1024); free(address);
    }
    CHECK(сместить_конец_динамической_памяти(0) == destination);
    return 0;
}
