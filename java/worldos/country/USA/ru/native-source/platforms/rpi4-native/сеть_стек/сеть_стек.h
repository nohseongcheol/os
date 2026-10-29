#ifndef собственный_сеть_Заголовок
#define собственный_сеть_Заголовок
#include <stdint.h>
#include <stddef.h>
void Подготовить_сеть(void);
void 통신망살피기(void);
int Create_сокет_участник(int ТИП_область);
int NET_BIND(int дескриптор_файла, uint32_t АДРЕС, unsigned номер_порта);
int NET_ожидать_передачи_данных(int дескриптор_файла);
void 통신주소재사용(int дескриптор_файла);
int NET_Connect(int дескриптор_файла, uint32_t АДРЕС, unsigned номер_порта);
int NET_принять(int дескриптор_файла);
int NET_чтение(int дескриптор_файла, void *данные, unsigned товар_СЧЁТ);
int NET_запись(int дескриптор_файла, const void *данные, unsigned товар_СЧЁТ);
int написать_датаграмма(int дескриптор_файла, const void *данные, unsigned товар_СЧЁТ, uint32_t АДРЕС, unsigned номер_порта);
int получить_датаграмма(int дескриптор_файла, void *данные, unsigned товар_СЧЁТ);
unsigned сеть_номер_порта(int дескриптор_файла);
unsigned одноранговый_номер_порта(int дескриптор_файла);
uint32_t NET_одноранговый_АДРЕС(int дескриптор_файла);
void Close_сеть(int дескриптор_файла);
int передача_файла_управление(int Действие);
void 파일전송살피기(void);
uint32_t чтение_сеть_статус(unsigned ввод_ЗНАЧЕН, unsigned ИНДЕКС);
int настроить_сеть(unsigned Действие, uint32_t АДРЕС, uint32_t маска_ЗНАЧЕН, uint32_t шлюз_ЗНАЧЕН);
int Пуск_ответ_тест(uint32_t АДРЕС, unsigned заказ_ЗНАЧЕН);
int чтение_ответ_тест(unsigned ввод_ЗНАЧЕН);
#endif
