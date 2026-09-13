/* Host-only fault injection. This fake heap is never installed in guest code. */
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>
#include <unistd.h>

static unsigned char test_heap[8192];
static unsigned int test_break = 3; /* Deliberately unaligned initial break. */
static int test_refuse_growth;

void *allocation_test_sbrk(int increment)
{
    void *old = test_heap + test_break;
    if (increment < 0 || (increment && test_refuse_growth) ||
        (unsigned int)increment > sizeof(test_heap) - test_break) {
        errno = ENOMEM;
        return (void *)-1;
    }
    test_break += (unsigned int)increment;
    return old;
}

#define EXPECT(condition) do { if (!(condition)) return __LINE__; } while (0)
int main(void)
{
    char *first = malloc(256), *second = malloc(256), *third = malloc(256), *joined;
    unsigned int before;
    int index;
    EXPECT(first && second && third);
    EXPECT(((uintptr_t)first & 15U) == 0 && ((uintptr_t)second & 15U) == 0);
    memset(third, 0x5a, 256);
    free(first); free(second);
    before = test_break;
    joined = malloc(500);
    EXPECT(joined == first && test_break == before); /* Coalescing. */
    free(joined);
    first = malloc(64); second = malloc(64);
    EXPECT(first && second && first != second && test_break == before); /* Splitting. */
    test_refuse_growth = 1;
    errno = EIO;
    EXPECT(realloc(third, 4096) == NULL && errno == ENOMEM);
    for (index = 0; index < 256; ++index) EXPECT(third[index] == 0x5a);
    EXPECT(malloc(4096) == NULL && errno == ENOMEM && test_break == before);
    errno = EIO;
    free(first); free(second); free(third);
    EXPECT(errno == EIO);
    joined = malloc(700); /* No growth needed after all adjacent blocks merge. */
    EXPECT(joined && test_break == before);
    free(joined);
    return write(1, "POSIX-ALLOCATOR:PASS\n", 21) == 21 ? 0 : 1;
}
