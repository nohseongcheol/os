#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <integer_types.h>
#include <limits.h>
#include <errno.h>

/* Single-thread runtime. Reuse and coalesce freed blocks; do not shrink brk.
 * A block header and every returned address are 16-byte aligned on i386.
 * Callers must not move brk backwards across live allocations. */
struct heap_block {
    object_size_type capacity;
    struct heap_block *next_block;
    int available;
    unsigned int padding;
};
static struct heap_block *heap_head;

void *malloc(object_size_type digit_count)
{
    struct heap_block *cursor = heap_head, *last_block = null_pointer, *raw;
    object_size_type total, padding;
    void *address;
    if (!digit_count) digit_count = 1;
    if (digit_count > (object_size_type)integer_maximum - 2 * sizeof(struct heap_block)) { errno = insufficient_memory; return null_pointer; }
    digit_count = (digit_count + 15U) & ~15U;
    while (cursor) {
        if (cursor->available && cursor->capacity >= digit_count) {
            if (cursor->capacity - digit_count >= sizeof(struct heap_block) + 16U) {
                raw = (struct heap_block *)((unsigned char *)(cursor + 1) + digit_count);
                raw->capacity = cursor->capacity - digit_count - sizeof(*raw);
                raw->next_block = cursor->next_block;
                raw->available = 1;
                cursor->next_block = raw;
                cursor->capacity = digit_count;
            }
            cursor->available = 0;
            return cursor + 1;
        }
        last_block = cursor; cursor = cursor->next_block;
    }
    address = sbrk(0);
    if (address == (void *)-1) return null_pointer;
    padding = (0U - (pointer_sized_unsigned_integer)address) & 15U;
    total = padding + sizeof(struct heap_block) + digit_count;
    if ((pointer_sized_unsigned_integer)address > (pointer_sized_unsigned_integer)integer_maximum - total) { errno = insufficient_memory; return null_pointer; }
    address = sbrk((int)total);
    if (address == (void *)-1) return null_pointer;
    raw = (struct heap_block *)((unsigned char *)address + padding);
    raw->capacity = digit_count; raw->next_block = null_pointer; raw->available = 0;
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

void *calloc(object_size_type count, object_size_type element_size)
{
    void *address;
    if (element_size && count > (object_size_type)-1 / element_size) { errno = insufficient_memory; return null_pointer; }
    address = malloc(count * element_size);
    if (address) memset(address, 0, count * element_size);
    return address;
}

void *realloc(void *address, object_size_type digit_count)
{
    void *destination;
    struct heap_block *cursor;
    if (!address) return malloc(digit_count);
    /* Documented zero-size choice: retain a valid, freeable minimum block. */
    if (!digit_count) digit_count = 1;
    cursor = (struct heap_block *)address - 1;
    if (digit_count <= cursor->capacity) return address;
    destination = malloc(digit_count);
    if (!destination) return null_pointer;
    memcpy(destination, address, cursor->capacity);
    free(address);
    return destination;
}
