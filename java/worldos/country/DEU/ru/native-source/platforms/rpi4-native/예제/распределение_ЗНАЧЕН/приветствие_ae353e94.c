#include <файл_ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Список) {
    if (인수개수 < 1 || !аргумент_Список[0]) return 2;
    const char приветствие[] = "свой 커널의 C와 русский POSIX\n";
    int 문서 = открыть_файл("приветствие_ae353e94.txt", для_чтения_и_записи | 없으면만들기 | усечь_Оглавление, 0600);
    if (문서 < 0) return 1;
    입출력결과형 длина_ЗНАЧЕН = запись_файл_данные(문서, приветствие, sizeof(приветствие) - 1);
    Close_файл(문서);
    запись_файл_данные(1, приветствие, sizeof(приветствие) - 1);
    return длина_ЗНАЧЕН == sizeof(приветствие) - 1 ? 0 : 3;
}
