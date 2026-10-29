#include "통신규약.h"

int Start_кулланучы_кушымта(int 인수) {
    (void)인수;
    struct 인터넷통신주소 адрес = {0};
    адрес.адрес_Гаилә = болыт_Гаилә;
    адрес.접속번호 = 망차례짧은수(9260);
    адрес.Интернеттагы_адрес.адрес_VALUE = Челтәр_бөтен_сан(되돌림주소);
    int сервер_VALUE = 통신종단점만들기(болыт_Гаилә, агым_Челтәр, 흐름전송규약);
    if (сервер_VALUE < 0 || BIND_адрес(сервер_VALUE, (struct 통신주소 *)&адрес, sizeof(адрес)) < 0 ||
        통신연결기다리기(сервер_VALUE, 4) < 0) return 1;
    if (кабул_итү_челтәр_аша_тоташу(сервер_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int кунак_VALUE = 통신종단점만들기(болыт_Гаилә, агым_Челтәр, 흐름전송규약);
    if (кунак_VALUE < 0 || ялгау_Челтәр(кунак_VALUE, (struct 통신주소 *)&адрес, sizeof(адрес)) < 0) return 3;
    int ялгау = кабул_итү_челтәр_аша_тоташу(сервер_VALUE, 0, 0);
    if (ялгау < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_элемент[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int озынлык_VALUE = язу_файл_мәгълүмат(кунак_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (озынлык_VALUE <= 0) return 5;
        보낸수 += озынлык_VALUE;
    }
    if (язу_файл_мәгълүмат(кунак_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Артка_VALUE EOF가 된다. */
    чик_файл(кунак_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int озынлык_VALUE = 파일자료읽기(ялгау, RECEIVED_элемент + RECEIVED_COUNT, sizeof(RECEIVED_элемент) - RECEIVED_COUNT);
        if (озынлык_VALUE <= 0) return 7;
        RECEIVED_COUNT += озынлык_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_элемент[수] != 보낼것[수]) return 8;
    if (파일자료읽기(ялгау, RECEIVED_элемент, 1) != 0) return 9;
    if (язу_файл_мәгълүмат(ялгау, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    чик_файл(ялгау); чик_файл(сервер_VALUE);
    const char үлчәм[] = "C posix-kor 연결형 통신 PASS\n";
    язу_файл_мәгълүмат(1, үлчәм, sizeof(үлчәм) - 1);
    return 0;
}
