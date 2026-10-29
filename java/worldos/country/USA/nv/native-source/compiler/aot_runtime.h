/* Runtime for the closed-world, single-thread AOT profile. No bytecode interpreter.
 * Generated metadata precedes this file. Requires IEEE binary32/binary64 and
 * 64-bit pointers. Object storage is bounded, with no garbage collection yet. */
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
typedef uint64_t J;
typedef struct { int type, length; unsigned monitor, unused; J data[]; } JO;
extern void aot_abort(const char *) __attribute__((noreturn));
static J j_heap[J_HEAP_WORDS], j_exception;
static size_t j_used;
static struct { int type, length; unsigned monitor, unused; J data[1]; } j_emergency;
static J j_allocate(int type, int count) {
    size_t words = 2 + (size_t)(count > 0 ? count : 1);
    if (count < 0 || words > J_HEAP_WORDS - j_used) return 0;
    JO *p = (JO *)(j_heap + j_used); j_used += words;
    p->type = type; p->length = count; p->monitor = 0;
    for (int i = 0; i < count; ++i) p->data[i] = 0;
    return (J)(uintptr_t)p;
}
static void j_raise(int type) {
    if (j_exception) return;
    j_exception = j_allocate(type, j_fields[type]);
    if (!j_exception) {
        j_emergency.type = J_OOM; j_emergency.length = 1;
        j_exception = (J)(uintptr_t)&j_emergency;
    }
}
static JO *j_obj(J ref) {
    if (!ref) { j_raise(J_NULL); return 0; }
    return (JO *)(uintptr_t)ref;
}
static int j_is(J ref, int target) {
    return ref && j_assign[((JO *)(uintptr_t)ref)->type][target];
}
static J j_new(int type) {
    J ref = j_allocate(type, j_fields[type]);
    if (!ref) j_raise(J_OOM);
    return ref;
}
static J j_array(int type, int32_t n) {
    if (n < 0) { j_raise(J_NEGATIVE); return 0; }
    J ref = j_allocate(type, n);
    if (!ref) j_raise(J_OOM);
    return ref;
}
static J j_multi(int type, const int32_t *sizes, unsigned count) {
    J ref = j_array(type, sizes[0]);
    if (count > 1 && !j_exception) {
        JO *p = (JO *)(uintptr_t)ref;
        for (int i = 0; i < p->length && !j_exception; ++i)
            p->data[i] = j_multi(j_component[type], sizes + 1, count - 1);
    }
    return ref;
}
static J *j_element(J ref, int32_t index) {
    JO *p = j_obj(ref);
    if (!p) return 0;
    if (index < 0 || index >= p->length) { j_raise(J_BOUNDS); return 0; }
    return p->data + index;
}
static J j_load(J ref, int32_t index, int op) {
    J *p = j_element(ref, index);
    if (!p) return 0;
    if (op == 51) return (uint32_t)(int32_t)(int8_t)*p;
    if (op == 52) return (uint16_t)*p;
    if (op == 53) return (uint32_t)(int32_t)(int16_t)*p;
    return *p;
}
static void j_store(J ref, int32_t index, J value, int op) {
    J *p = j_element(ref, index);
    if (!p) return;
    if (op == 83) {
        int component = j_component[((JO *)(uintptr_t)ref)->type];
        if (value && !j_is(value, component)) { j_raise(J_STORE); return; }
    }
    if (op == 84) value = j_component[((JO *)(uintptr_t)ref)->type] == J_BOOLEAN ? value & 1 : (uint8_t)value;
    if (op == 85 || op == 86) value = (uint16_t)value;
    *p = value;
}
static J j_field(J ref, unsigned index) { JO *p = j_obj(ref); return p ? p->data[index] : 0; }
static void j_putfield(J ref, unsigned index, J value) { JO *p = j_obj(ref); if (p) p->data[index] = value; }
static J j_cast(J ref, int type) {
    if (ref && !j_is(ref, type)) { j_raise(J_CAST); return 0; }
    return ref;
}
static J j_length(J ref) { JO *p = j_obj(ref); return p ? (uint32_t)p->length : 0; }
static void j_monitor(J ref, int enter) {
    JO *p = j_obj(ref); if (!p) return;
    if (enter) { if (p->monitor == UINT_MAX) j_raise(J_OOM); else p->monitor++; }
    else if (!p->monitor) j_raise(J_MONITOR);
    else p->monitor--;
}
static J j_div(J a, J b, int wide, int remainder) {
    if (wide) {
        int64_t x = (int64_t)a, y = (int64_t)b;
        if (!y) { j_raise(J_ARITH); return 0; }
        if (x == INT64_MIN && y == -1) return remainder ? 0 : a;
        return (J)(remainder ? x % y : x / y);
    }
    int32_t x = (int32_t)a, y = (int32_t)b;
    if (!y) { j_raise(J_ARITH); return 0; }
    if (x == INT32_MIN && y == -1) return remainder ? 0 : (uint32_t)a;
    return (uint32_t)(remainder ? x % y : x / y);
}
static J j_shift(J a, J b, int wide, int kind) {
    unsigned bits = wide ? 64 : 32, n = (unsigned)b & (bits - 1);
    if (!wide) a = (uint32_t)a;
    if (kind == 0) return wide ? a << n : (uint32_t)(a << n);
    if (kind == 2 || !n) return a >> n;
    J value = a >> n;
    if (a & ((J)1 << (bits - 1))) value |= (~(J)0) << (bits - n);
    return wide ? value : (uint32_t)value;
}
static float j_f(J x) { union { uint32_t u; float f; } v = { (uint32_t)x }; return v.f; }
static double j_d(J x) { union { J u; double d; } v = { x }; return v.d; }
static J j_fb(float f) { union { float f; uint32_t u; } v = { f }; return v.u; }
static J j_db(double d) { union { double d; J u; } v = { d }; return v.u; }
/* Remainder via integer significands; handles subnormals, infinities and -0
 * without libm, signed overflow, or an out-of-range floating-to-integer cast. */
static J j_rem(J x, J y, unsigned fraction, unsigned exponent) {
    J hidden = (J)1 << fraction, mask = hidden - 1;
    J maxexp = ((J)1 << exponent) - 1, sign = x & ((J)1 << (fraction + exponent));
    x &= ((J)1 << (fraction + exponent)) - 1;
    y &= ((J)1 << (fraction + exponent)) - 1;
    unsigned ex = (unsigned)(x >> fraction), ey = (unsigned)(y >> fraction);
    if (ex == maxexp || !y || (ey == maxexp && (y & mask))) return (maxexp << fraction) | (hidden >> 1);
    if (x < y || !x) return x | sign;
    J mx = (x & mask) | (ex ? hidden : 0), my = (y & mask) | (ey ? hidden : 0);
    if (!ex) ex = 1; if (!ey) ey = 1;
    while (ex > ey) { mx %= my; mx <<= 1; --ex; }
    mx %= my;
    if (!mx) return sign;
    while (mx < hidden && ey > 1) { mx <<= 1; --ey; }
    return sign | ((mx >= hidden ? (J)ey : 0) << fraction) | (mx & mask);
}
static J j_fp(J a, J b, int wide, int kind) {
    if (kind == 4) return j_rem(a, b, wide ? 52 : 23, wide ? 11 : 8);
    if (wide) {
        double x = j_d(a), y = j_d(b);
        return j_db(kind == 0 ? x + y : kind == 1 ? x - y : kind == 2 ? x * y : x / y);
    }
    float x = j_f(a), y = j_f(b);
    return j_fb(kind == 0 ? x + y : kind == 1 ? x - y : kind == 2 ? x * y : x / y);
}
static J j_to_integer(double value, int wide) {
    if (value != value) return 0;
    if (wide) {
        if (value >= 0x1p63) return INT64_MAX;
        if (value <= -0x1p63) return (J)INT64_MIN;
        return (J)(int64_t)value;
    }
    if (value >= 0x1p31) return INT32_MAX;
    if (value <= -0x1p31) return (uint32_t)INT32_MIN;
    return (uint32_t)(int32_t)value;
}
static J j_convert(J a, int op) {
    switch (op) {
    case 133: return (J)(int64_t)(int32_t)a;
    case 134: return j_fb((float)(int32_t)a); case 135: return j_db((double)(int32_t)a);
    case 136: return (uint32_t)a;
    case 137: return j_fb((float)(int64_t)a); case 138: return j_db((double)(int64_t)a);
    case 139: return j_to_integer(j_f(a), 0); case 140: return j_to_integer(j_f(a), 1);
    case 141: return j_db(j_f(a));
    case 142: return j_to_integer(j_d(a), 0); case 143: return j_to_integer(j_d(a), 1);
    case 144: return j_fb((float)j_d(a));
    case 145: return (uint32_t)(int32_t)(int8_t)a;
    case 146: return (uint16_t)a;
    default: return (uint32_t)(int32_t)(int16_t)a;
    }
}
static J j_compare(J a, J b, int op) {
    if (op == 148) return (uint32_t)((int64_t)a < (int64_t)b ? -1 : (a == b ? 0 : 1));
    double x = op < 151 ? j_f(a) : j_d(a), y = op < 151 ? j_f(b) : j_d(b);
    if (x != x || y != y) return (uint32_t)((op == 149 || op == 151) ? -1 : 1);
    return (uint32_t)(x < y ? -1 : x == y ? 0 : 1);
}
#define PUSH(v) do { if (sp >= sizeof(s)/sizeof(s[0])) aot_abort("AOT stack overflow"); s[sp++] = (J)(v); } while(0)
#define POP() (sp ? s[--sp] : (aot_abort("AOT stack underflow"), (J)0))
#define PUSH2(v) do { J push_value = (v); PUSH(push_value); PUSH(0); } while(0)
#define POP2(v) do { (void)POP(); (v) = POP(); } while(0)
