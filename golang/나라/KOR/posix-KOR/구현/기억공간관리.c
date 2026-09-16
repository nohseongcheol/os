/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <일반함수.h>
#include <문자열과기억내용.h>
#include <입출력과실행.h>
#include <정수형.h>
#include <정수한계.h>
#include <오류번호.h>

/* Single-thread runtime. Reuse and coalesce freed blocks; do not shrink brk.
 * A block header and every returned address are 16-byte aligned on i386.
 * Callers must not move brk backwards across live allocations. */
struct 기억공간구획 {
    크기형 수용크기;
    struct 기억공간구획 *다음구획;
    int 사용가능여부;
    unsigned int 정렬채움크기;
};
static struct 기억공간구획 *첫구획;

void *기억공간확보하기(크기형 크기)
{
    struct 기억공간구획 *진행위치 = 첫구획, *마지막구획 = 빈주소, *확보원주소;
    크기형 전체크기, 정렬채움크기;
    void *주소;
    if (!크기) 크기 = 1;
    if (크기 > (크기형)정수최댓값 - 2 * sizeof(struct 기억공간구획)) { 오류번호 = 오류기억공간부족; return 빈주소; }
    크기 = (크기 + 15U) & ~15U;
    while (진행위치) {
        if (진행위치->사용가능여부 && 진행위치->수용크기 >= 크기) {
            if (진행위치->수용크기 - 크기 >= sizeof(struct 기억공간구획) + 16U) {
                확보원주소 = (struct 기억공간구획 *)((unsigned char *)(진행위치 + 1) + 크기);
                확보원주소->수용크기 = 진행위치->수용크기 - 크기 - sizeof(*확보원주소);
                확보원주소->다음구획 = 진행위치->다음구획;
                확보원주소->사용가능여부 = 1;
                진행위치->다음구획 = 확보원주소;
                진행위치->수용크기 = 크기;
            }
            진행위치->사용가능여부 = 0;
            return 진행위치 + 1;
        }
        마지막구획 = 진행위치; 진행위치 = 진행위치->다음구획;
    }
    주소 = 동적기억끝옮기기(0);
    if (주소 == (void *)-1) return 빈주소;
    정렬채움크기 = (0U - (주소크기부호없는정수)주소) & 15U;
    전체크기 = 정렬채움크기 + sizeof(struct 기억공간구획) + 크기;
    if ((주소크기부호없는정수)주소 > (주소크기부호없는정수)정수최댓값 - 전체크기) { 오류번호 = 오류기억공간부족; return 빈주소; }
    주소 = 동적기억끝옮기기((int)전체크기);
    if (주소 == (void *)-1) return 빈주소;
    확보원주소 = (struct 기억공간구획 *)((unsigned char *)주소 + 정렬채움크기);
    확보원주소->수용크기 = 크기; 확보원주소->다음구획 = 빈주소; 확보원주소->사용가능여부 = 0;
    if (마지막구획) 마지막구획->다음구획 = 확보원주소;
    else 첫구획 = 확보원주소;
    return 확보원주소 + 1;
}

void 기억공간반납하기(void *주소)
{
    struct 기억공간구획 *진행위치;
    if (!주소) return;
    ((struct 기억공간구획 *)주소 - 1)->사용가능여부 = 1;
    진행위치 = 첫구획;
    while (진행위치 && 진행위치->다음구획) {
        struct 기억공간구획 *다음구획 = 진행위치->다음구획;
        if (진행위치->사용가능여부 && 다음구획->사용가능여부 &&
            (unsigned char *)(진행위치 + 1) + 진행위치->수용크기 == (unsigned char *)다음구획) {
            진행위치->수용크기 += sizeof(*다음구획) + 다음구획->수용크기;
            진행위치->다음구획 = 다음구획->다음구획;
        } else 진행위치 = 다음구획;
    }
}

void *영으로채운배열공간확보하기(크기형 수량, 크기형 원소크기)
{
    void *주소;
    if (원소크기 && 수량 > (크기형)-1 / 원소크기) { 오류번호 = 오류기억공간부족; return 빈주소; }
    주소 = 기억공간확보하기(수량 * 원소크기);
    if (주소) 기억영역값채우기(주소, 0, 수량 * 원소크기);
    return 주소;
}

void *기억공간크기바꾸기(void *주소, 크기형 크기)
{
    void *옮길곳;
    struct 기억공간구획 *진행위치;
    if (!주소) return 기억공간확보하기(크기);
    /* Documented zero-size choice: retain a valid, freeable minimum block. */
    if (!크기) 크기 = 1;
    진행위치 = (struct 기억공간구획 *)주소 - 1;
    if (크기 <= 진행위치->수용크기) return 주소;
    옮길곳 = 기억공간확보하기(크기);
    if (!옮길곳) return 빈주소;
    기억내용복사하기(옮길곳, 주소, 진행위치->수용크기);
    기억공간반납하기(주소);
    return 옮길곳;
}
