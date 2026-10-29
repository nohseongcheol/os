#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define អ្នកប្រើ_រូបថត_បញ្ចប់ 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define អ្នកប្រើ_គរ_អ៊ីម៉ែល 0x02f00000ul
#define អ្នកប្រើ_បញ្ចប់ 0x03000000ul
#define 사용자쪽수 ((អ្នកប្រើ_បញ្ចប់ - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define អ្នកប្រើ_ទិន្នន័យ_កំហុស (-1001)
#define 사용자실행오류 (-1002)
#define អ្នកប្រើ_មិនត្រឹមត្រូវ_ការណែនាំ (-1003)
#define អ្នកប្រើ_អស់ម៉ោង (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t ចុះឈ្មោះ_ទិន្នន័យ[31], ពាក្យបញ្ជា_កំណត់ទីតាំង, ភាព_កូដ, គរ_អ៊ីម៉ែល; } អ្នកប្រើ_រូប;
void 사용자체계준비(void);
int អ្នកប្រើ_ការលើកលែង(អ្នកប្រើ_រូប *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ផ្ទាំង_អ្នកប្រើ_ដំណើរការ(uintptr_t);
uintptr_t ផ្ទាំង_អ្នកប្រើ_ធ្វើអោយមានសុពលភាព(void);
uintptr_t ផ្ទាំង_កុងត្រូលអ្នកប្រើប្រាស់(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
