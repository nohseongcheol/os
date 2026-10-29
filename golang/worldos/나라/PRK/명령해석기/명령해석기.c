#include <통신주소/여덟자리묶음순서.h>
#include <오류번호.h>
#include <자료철제어.h>
#include <상호연결망/주소.h>
#include <기본정의.h>
#include <체계/통신끝점.h>
#include <체계/자료철상태.h>
#include <체계/체제정보.h>
#include <체계/자식대기.h>
#include <입출력과실행.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { 입력줄_수용량 = 512, 최대_인수_개수 = 16, 최대_명령자료철_중첩 = 4 };
static int 명령자료철_중첩_깊이;
struct 입력자료흐름 {
    int 입력_서술번호;
    char 전달_완충공간[256];
    크기형 위치;
    크기형 길이;
};

static 크기형 문자열_여덟자리묶음_길이(const char *문자열)
{
    크기형 길이 = 0;
    while (문자열[길이] != '\0')
        길이++;
    return 길이;
}

static int 문자열_일치(const char *왼쪽, const char *오른쪽)
{
    크기형 위치 = 0;
    while (왼쪽[위치] == 오른쪽[위치]) {
        if (왼쪽[위치] == '\0')
            return 1;
        위치++;
    }
    return 0;
}

static void 문자열_쓰기(const char *문자열)
{
    크기형 길이 = 문자열_여덟자리묶음_길이(문자열);
    while (길이 > 0U) {
        부호있는크기형 쓴_여덟자리묶음수 = 쓰기(표준출력번호, 문자열, 길이);
        if (쓴_여덟자리묶음수 <= 0)
            return;
        문자열 += 쓴_여덟자리묶음수;
        길이 -= (크기형)쓴_여덟자리묶음수;
    }
}

static void 정수_쓰기(int 값)
{
    char 숫자_문자들[16];
    unsigned int 자릿수;
    unsigned int 부호없는_크기;

    if (값 < 0) {
        문자열_쓰기("-");
        부호없는_크기 = (unsigned int)(-(값 + 1)) + 1U;
    } else {
        부호없는_크기 = (unsigned int)값;
    }
    자릿수 = 0;
    do {
        숫자_문자들[자릿수++] = (char)('0' + 부호없는_크기 % 10U);
        부호없는_크기 /= 10U;
    } while (부호없는_크기 != 0U);
    while (자릿수 > 0U) {
        자릿수--;
        (void)쓰기(표준출력번호, &숫자_문자들[자릿수], 1);
    }
}

static void 오류_알리기(const char *실행_연산)
{
    문자열_쓰기("error: ");
    문자열_쓰기(실행_연산);
    문자열_쓰기(" errno=");
    정수_쓰기(오류번호);
    문자열_쓰기("\n");
}

static int 입력줄_읽기(struct 입력자료흐름 *입력, char *입력줄, 크기형 수용량)
{
    크기형 위치 = 0;
    int 잘못된_입력줄 = 0;
    char 문자;
    부호있는크기형 읽은_여덟자리묶음수;
    if (수용량 < 2U)
        return -2;
    for (;;) {
        if (입력->위치 == 입력->길이) {
            읽은_여덟자리묶음수 = 읽기(입력->입력_서술번호, 입력->전달_완충공간, sizeof(입력->전달_완충공간));
            if (읽은_여덟자리묶음수 < 0) {
                if (오류번호 == 오류동작중단됨)
                    continue;
                return -1;
            }
            if (읽은_여덟자리묶음수 == 0) {
                if (위치 == 0 && !잘못된_입력줄)
                    return -1;
                break;
            }
            입력->길이 = (크기형)읽은_여덟자리묶음수;
            입력->위치 = 0;
        }
        문자 = 입력->전달_완충공간[입력->위치++];
        if (문자 == '\n')
            break;
        if (입력->입력_서술번호 == 표준입력번호 && 문자 == 4) {
            if (위치 == 0 && !잘못된_입력줄)
                return -1;
            break;
        }
        if (입력->입력_서술번호 == 표준입력번호 && (문자 == 8 || 문자 == 127)) {
            if (위치 > 0) {
                do {
                    위치--;
                } while (위치 > 0 && ((unsigned char)입력줄[위치] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (문자 == '\r')
            continue;
        if (문자 == '\0') {
            잘못된_입력줄 = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (위치 + 1U < 수용량)
            입력줄[위치++] = 문자;
        else
            잘못된_입력줄 = 1;
    }
    입력줄[위치] = '\0';
    return 잘못된_입력줄 ? -2 : (int)위치;
}

static int 인수_나누기(char *입력줄, char **인수들)
{
    int 인수_개수 = 0;
    char *현재_위치 = 입력줄;
    char *출력_위치 = 입력줄;

    while (*현재_위치 != '\0') {
        char 따옴표 = '\0';
        while (*현재_위치 == ' ' || *현재_위치 == '\t')
            현재_위치++;
        if (*현재_위치 == '\0' || *현재_위치 == '#')
            break;
        if (인수_개수 == 최대_인수_개수 - 1)
            return -1;
        인수들[인수_개수++] = 출력_위치;
        while (*현재_위치 != '\0') {
            char 문자 = *현재_위치++;
            if (따옴표 == '\0' && (문자 == ' ' || 문자 == '\t'))
                break;
            if (문자 == '\\' && 따옴표 != '\'') {
                if (*현재_위치 == '\0')
                    return -1;
                *출력_위치++ = *현재_위치++;
            } else if (문자 == '\'' || 문자 == '"') {
                if (따옴표 == '\0')
                    따옴표 = 문자;
                else if (따옴표 == 문자)
                    따옴표 = '\0';
                else
                    *출력_위치++ = 문자;
            } else {
                *출력_위치++ = 문자;
            }
        }
        if (따옴표 != '\0')
            return -1;
        *출력_위치++ = '\0';
    }
    인수들[인수_개수] = (char *)0;
    return 인수_개수;
}

static void 도움말_표시(void)
{
    크기형 위치;
    문자열_쓰기(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    문자열_쓰기("Native command proposals (ASCII aliases remain available):\n");
    for (위치 = 0; 위치 < sizeof(기준_명령들) / sizeof(기준_명령들[0]); 위치++) {
        문자열_쓰기(현지어_명령_별칭[위치]);
        문자열_쓰기(" = ");
        문자열_쓰기(기준_명령들[위치]);
        문자열_쓰기("\n");
    }
}

static int 명령_일치(const char *문자열, const char *명령)
{
    크기형 위치;
    if (문자열_일치(문자열, 명령))
        return 1;
    for (위치 = 0; 위치 < sizeof(기준_명령들) / sizeof(기준_명령들[0]); 위치++)
        if (문자열_일치(명령, 기준_명령들[위치]))
            return 문자열_일치(문자열, 현지어_명령_별칭[위치]);
    return 0;
}

static int 입력_해석(int 입력_서술번호);

static int 명령자료철_해석(const char *자료철_이름)
{
    int 자료철_서술번호;
    int 상태;
    if (명령자료철_중첩_깊이 >= 최대_명령자료철_중첩) {
        문자열_쓰기("source: nesting limit\n");
        return 0;
    }
    자료철_서술번호 = 열기(자료철_이름, 읽기전용열기);
    if (자료철_서술번호 < 0) {
        오류_알리기(자료철_이름);
        return 0;
    }
    명령자료철_중첩_깊이++;
    상태 = 입력_해석(자료철_서술번호);
    명령자료철_중첩_깊이--;
    (void)닫기(자료철_서술번호);
    return 상태;
}

static void 인수_출력(int 인수_개수, char **인수들)
{
    int 위치;
    for (위치 = 1; 위치 < 인수_개수; 위치++) {
        if (위치 != 1)
            문자열_쓰기(" ");
        문자열_쓰기(인수들[위치]);
    }
    문자열_쓰기("\n");
}

static void 현재_경로_표시(void)
{
    char 경로[128];
    if (작업목록경로얻기(경로, sizeof(경로)) == (char *)0) {
        오류_알리기("pwd");
        return;
    }
    문자열_쓰기(경로);
    문자열_쓰기("\n");
}

static void 자료철_내용_표시(const char *자료철_이름)
{
    char 전달_완충공간[128];
    int 자료철_서술번호 = 열기(자료철_이름, 읽기전용열기);
    부호있는크기형 읽은_여덟자리묶음수;

    if (자료철_서술번호 < 0) {
        오류_알리기("cat");
        return;
    }
    while ((읽은_여덟자리묶음수 = 읽기(자료철_서술번호, 전달_완충공간, sizeof(전달_완충공간))) > 0)
        (void)쓰기(표준출력번호, 전달_완충공간, (크기형)읽은_여덟자리묶음수);
    if (읽은_여덟자리묶음수 < 0)
        오류_알리기("cat/read");
    (void)닫기(자료철_서술번호);
    문자열_쓰기("\n");
}

static void 자료철_정보_표시(const char *자료철_이름)
{
    struct 자료철상태 상태;
    if (자료철상태(자료철_이름, &상태) < 0) {
        오류_알리기("stat");
        return;
    }
    문자열_쓰기("size=");
    정수_쓰기((int)상태.자료철크기);
    문자열_쓰기(목록방식인지확인(상태.자료철종류와권한) ? " type=directory\n" : " type=file\n");
}

static void 실행과정_번호_표시(void)
{
    문자열_쓰기("pid=");
    정수_쓰기((int)실행과정번호얻기());
    문자열_쓰기(" ppid=");
    정수_쓰기((int)부모실행과정번호얻기());
    문자열_쓰기("\n");
}

static void 운영체제_정보_표시(void)
{
    struct 체제정보 운영체제_식별정보;
    if (체제정보얻기(&운영체제_식별정보) < 0) {
        오류_알리기("uname");
        return;
    }
    문자열_쓰기(운영체제_식별정보.체제이름);
    문자열_쓰기(" ");
    문자열_쓰기(운영체제_식별정보.체제배포판);
    문자열_쓰기(" ");
    문자열_쓰기(운영체제_식별정보.기계종류);
    문자열_쓰기("\n");
}

static void 실행자료철_가동(int 인수_개수, char **인수들)
{
    실행과정번호형 자식_실행과정_번호;
    int 자식_종료_상태 = 0;

    if (인수_개수 < 2) {
        문자열_쓰기("usage: run FILE [ARGS...]\n");
        return;
    }
    자식_실행과정_번호 = 실행과정갈라내기();
    if (자식_실행과정_번호 < 0) {
        오류_알리기("fork");
        return;
    }
    if (자식_실행과정_번호 == 0) {
        실행내용바꾸기(인수들[1], &인수들[1], (char *const *)0);
        오류_알리기("execve");
        즉시끝내기(127);
    }
    if (지정자식기다리기(자식_실행과정_번호, &자식_종료_상태, 0) < 0) {
        오류_알리기("waitpid");
        return;
    }
    문자열_쓰기("exit-status=");
    정수_쓰기(종료값꺼내기(자식_종료_상태));
    문자열_쓰기("\n");
}

static void 자료전문_되돌림_시험(const char *전문)
{
    struct 상호연결망끝점주소 수신_접속점_주소 = {0};
    struct 상호연결망끝점주소 송신_접속점_주소 = {0};
    주소길이형 송신주소_길이 = sizeof(송신_접속점_주소);
    char 수신_자료[96];
    크기형 전문_여덟자리묶음_길이 = 문자열_여덟자리묶음_길이(전문);
    int 수신_통신끝점 = -1;
    int 송신_통신끝점 = -1;
    부호있는크기형 수신_여덟자리묶음수;

    if (전문_여덟자리묶음_길이 >= sizeof(수신_자료)) {
        문자열_쓰기("udp: message exceeds 95 bytes\n");
        return;
    }
    수신_통신끝점 = 통신끝점만들기(상호연결망주소계열, 자료전문끝점, 사용자자료전문규약);
    송신_통신끝점 = 통신끝점만들기(상호연결망주소계열, 자료전문끝점, 사용자자료전문규약);
    if (수신_통신끝점 < 0 || 송신_통신끝점 < 0) {
        오류_알리기("socket");
        goto 통신끝점_닫기;
    }
    수신_접속점_주소.연결망주소계열 = 상호연결망주소계열;
    수신_접속점_주소.통신창구번호 = 통신망순서로16자리바꾸기(40404);
    수신_접속점_주소.연결망주소내용.주소값 = 통신망순서로32자리바꾸기(자기되돌림주소);
    if (지역주소맺기(수신_통신끝점, (const struct 통신끝점주소 *)&수신_접속점_주소, sizeof(수신_접속점_주소)) < 0) {
        오류_알리기("bind");
        goto 통신끝점_닫기;
    }
    if (상대끝점잇기(송신_통신끝점, (const struct 통신끝점주소 *)&수신_접속점_주소, sizeof(수신_접속점_주소)) < 0) {
        오류_알리기("connect");
        goto 통신끝점_닫기;
    }
    if (보내기(송신_통신끝점, 전문, 전문_여덟자리묶음_길이, 0) != (부호있는크기형)전문_여덟자리묶음_길이) {
        오류_알리기("send");
        goto 통신끝점_닫기;
    }
    수신_여덟자리묶음수 = 보낸곳과함께받기(수신_통신끝점, 수신_자료, sizeof(수신_자료) - 1U, 0,
                         (struct 통신끝점주소 *)&송신_접속점_주소, &송신주소_길이);
    if (수신_여덟자리묶음수 < 0) {
        오류_알리기("recvfrom");
        goto 통신끝점_닫기;
    }
    수신_자료[수신_여덟자리묶음수] = '\0';
    문자열_쓰기("udp-received: ");
    문자열_쓰기(수신_자료);
    문자열_쓰기("\n");

통신끝점_닫기:
    if (송신_통신끝점 >= 0)
        (void)닫기(송신_통신끝점);
    if (수신_통신끝점 >= 0)
        (void)닫기(수신_통신끝점);
}

static int 입력_해석(int 입력_서술번호)
{
    char 입력줄[입력줄_수용량];
    char *인수들[최대_인수_개수];
    struct 입력자료흐름 입력 = {0};
    입력.입력_서술번호 = 입력_서술번호;

    for (;;) {
        int 인수_개수;
        int 상태;
        if (입력_서술번호 == 표준입력번호)
            문자열_쓰기("worldos$ ");
        상태 = 입력줄_읽기(&입력, 입력줄, sizeof(입력줄));
        if (상태 == -1)
            return 0;
        if (상태 == -2) {
            문자열_쓰기("input rejected: overlong or binary line\n");
            continue;
        }
        인수_개수 = 인수_나누기(입력줄, 인수들);
        if (인수_개수 < 0) {
            문자열_쓰기("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (인수_개수 == 0)
            continue;
        if (명령_일치(인수들[0], "help"))
            도움말_표시();
        else if (명령_일치(인수들[0], "echo"))
            인수_출력(인수_개수, 인수들);
        else if (명령_일치(인수들[0], "pwd"))
            현재_경로_표시();
        else if (명령_일치(인수들[0], "cd")) {
            if (인수_개수 < 2)
                문자열_쓰기("usage: cd PATH\n");
            else if (작업목록바꾸기(인수들[1]) < 0)
                오류_알리기("cd");
        } else if (명령_일치(인수들[0], "cat")) {
            if (인수_개수 < 2)
                문자열_쓰기("usage: cat FILE\n");
            else
                자료철_내용_표시(인수들[1]);
        } else if (명령_일치(인수들[0], "stat")) {
            if (인수_개수 < 2)
                문자열_쓰기("usage: stat FILE\n");
            else
                자료철_정보_표시(인수들[1]);
        } else if (명령_일치(인수들[0], "pid"))
            실행과정_번호_표시();
        else if (명령_일치(인수들[0], "uname"))
            운영체제_정보_표시();
        else if (명령_일치(인수들[0], "run"))
            실행자료철_가동(인수_개수, 인수들);
        else if (명령_일치(인수들[0], "udp"))
            자료전문_되돌림_시험(인수_개수 >= 2 ? 인수들[1] : "ping");
        else if (명령_일치(인수들[0], "source")) {
            if (인수_개수 < 2)
                문자열_쓰기("usage: source FILE\n");
            else if (명령자료철_해석(인수들[1]))
                return 1;
        } else if (명령_일치(인수들[0], "exit"))
            return 1;
        else
            문자열_쓰기("unknown command; type help\n");
    }
}

int main(void)
{
    문자열_쓰기("WORLDOS-SHELL:READY\n");
    (void)입력_해석(표준입력번호);
    문자열_쓰기("WORLDOS-SHELL:EXIT\n");
    return 0;
}
