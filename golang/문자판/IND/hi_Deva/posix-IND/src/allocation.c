/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <पूर्णांक_प्रकार.h>
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

void *malloc(size_t अंकों_की_संख्या)
{
    struct heap_block *cursor = heap_head, *last_block = NULL, *raw;
    size_t total, padding;
    void *address;
    if (!अंकों_की_संख्या) अंकों_की_संख्या = 1;
    if (अंकों_की_संख्या > (size_t)INT_MAX - 2 * sizeof(struct heap_block)) { errno = ENOMEM; return NULL; }
    अंकों_की_संख्या = (अंकों_की_संख्या + 15U) & ~15U;
    while (cursor) {
        if (cursor->available && cursor->capacity >= अंकों_की_संख्या) {
            if (cursor->capacity - अंकों_की_संख्या >= sizeof(struct heap_block) + 16U) {
                raw = (struct heap_block *)((unsigned char *)(cursor + 1) + अंकों_की_संख्या);
                raw->capacity = cursor->capacity - अंकों_की_संख्या - sizeof(*raw);
                raw->next_block = cursor->next_block;
                raw->available = 1;
                cursor->next_block = raw;
                cursor->capacity = अंकों_की_संख्या;
            }
            cursor->available = 0;
            return cursor + 1;
        }
        last_block = cursor; cursor = cursor->next_block;
    }
    address = गतिशील_स्मृति_अंत_बदलना(0);
    if (address == (void *)-1) return NULL;
    padding = (0U - (uintptr_t)address) & 15U;
    total = padding + sizeof(struct heap_block) + अंकों_की_संख्या;
    if ((uintptr_t)address > (uintptr_t)INT_MAX - total) { errno = ENOMEM; return NULL; }
    address = गतिशील_स्मृति_अंत_बदलना((int)total);
    if (address == (void *)-1) return NULL;
    raw = (struct heap_block *)((unsigned char *)address + padding);
    raw->capacity = अंकों_की_संख्या; raw->next_block = NULL; raw->available = 0;
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

void *realloc(void *address, size_t अंकों_की_संख्या)
{
    void *destination;
    struct heap_block *cursor;
    if (!address) return malloc(अंकों_की_संख्या);
    /* Documented zero-size choice: retain a valid, freeable minimum block. */
    if (!अंकों_की_संख्या) अंकों_की_संख्या = 1;
    cursor = (struct heap_block *)address - 1;
    if (अंकों_की_संख्या <= cursor->capacity) return address;
    destination = malloc(अंकों_की_संख्या);
    if (!destination) return NULL;
    memcpy(destination, address, cursor->capacity);
    free(address);
    return destination;
}
