#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <limits.h>
#include <errno.h>

/* Single-thread runtime. Reuse and coalesce freed blocks; do not shrink brk.
 * A block header and every returned address are 16-byte aligned on i386.
 * Callers must not move brk backwards across live allocations. */
struct heap_block {
    size_t capacity;
    struct heap_block *next_block;
    int available;
    unsigned int padding;
};
static struct heap_block *heap_head;

void *malloc(size_t വലുപ്പം)
{
    struct heap_block *cursor = heap_head, *last_block = NULL, *raw;
    size_t total, padding;
    void *address;
    if (!വലുപ്പം) വലുപ്പം = 1;
    if (വലുപ്പം > (size_t)INT_MAX - 2 * sizeof(struct heap_block)) { errno = ENOMEM; return NULL; }
    വലുപ്പം = (വലുപ്പം + 15U) & ~15U;
    while (cursor) {
        if (cursor->available && cursor->capacity >= വലുപ്പം) {
            if (cursor->capacity - വലുപ്പം >= sizeof(struct heap_block) + 16U) {
                raw = (struct heap_block *)((unsigned char *)(cursor + 1) + വലുപ്പം);
                raw->capacity = cursor->capacity - വലുപ്പം - sizeof(*raw);
                raw->next_block = cursor->next_block;
                raw->available = 1;
                cursor->next_block = raw;
                cursor->capacity = വലുപ്പം;
            }
            cursor->available = 0;
            return cursor + 1;
        }
        last_block = cursor; cursor = cursor->next_block;
    }
    address = sbrk(0);
    if (address == (void *)-1) return NULL;
    padding = (0U - (uintptr_t)address) & 15U;
    total = padding + sizeof(struct heap_block) + വലുപ്പം;
    if ((uintptr_t)address > (uintptr_t)INT_MAX - total) { errno = ENOMEM; return NULL; }
    address = sbrk((int)total);
    if (address == (void *)-1) return NULL;
    raw = (struct heap_block *)((unsigned char *)address + padding);
    raw->capacity = വലുപ്പം; raw->next_block = NULL; raw->available = 0;
    if (last_block) last_block->next_block = raw;
    else heap_head = raw;
    return raw + 1;
}

void free(void *address)
{
    struct heap_block *cursor;
    if (!address) return;
    ((struct heap_block *)address - 1)->available = 1;
    cursor = heap_head;
    while (cursor && cursor->next_block) {
        struct heap_block *next_block = cursor->next_block;
        if (cursor->available && next_block->available &&
            (unsigned char *)(cursor + 1) + cursor->capacity == (unsigned char *)next_block) {
            cursor->capacity += sizeof(*next_block) + next_block->capacity;
            cursor->next_block = next_block->next_block;
        } else cursor = next_block;
    }
}

void *calloc(size_t count, size_t element_size)
{
    void *address;
    if (element_size && count > (size_t)-1 / element_size) { errno = ENOMEM; return NULL; }
    address = malloc(count * element_size);
    if (address) memset(address, 0, count * element_size);
    return address;
}

void *realloc(void *address, size_t വലുപ്പം)
{
    void *destination;
    struct heap_block *cursor;
    if (!address) return malloc(വലുപ്പം);
    /* Documented zero-size choice: retain a valid, freeable minimum block. */
    if (!വലുപ്പം) വലുപ്പം = 1;
    cursor = (struct heap_block *)address - 1;
    if (വലുപ്പം <= cursor->capacity) return address;
    destination = malloc(വലുപ്പം);
    if (!destination) return NULL;
    memcpy(destination, address, cursor->capacity);
    free(address);
    return destination;
}
