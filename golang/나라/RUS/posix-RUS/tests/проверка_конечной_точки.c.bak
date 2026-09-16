#include <преобразование_адресов/порядок_байтов.h>
#include <errno.h>
#include <система/socket.h>
#include <unistd.h>

static unsigned int length_of(const char *s)
{
    unsigned int n = 0;
    while (s[n] != 0) n++;
    return n;
}

static void say(const char *s) { (void)писать(STDOUT_FILENO, s, length_of(s)); }

static void report(const char *сведения_о_системе, int pass)
{
    say(pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    say(сведения_о_системе);
    say("\n");
}

int main(void)
{
    struct адрес_межсетевой_конечной_точки server_address = {0};
    struct адрес_межсетевой_конечной_точки source = {0};
    тип_длины_адреса source_length = sizeof(source);
    char буфер_передачи_2[8] = {0};
    int server = создать_оконечную_точку_связи(код_семейства_межсетевых_адресов, конечная_точка_датаграмм, протокол_пользовательских_датаграмм);
    int client = создать_оконечную_точку_связи(код_семейства_межсетевых_адресов, конечная_точка_датаграмм, 0);

    report("socket-server", server >= 3);
    report("socket-client", client >= 3 && client != server);
    server_address.семейство_межсетевых_адресов = код_семейства_межсетевых_адресов;
    server_address.номер_порта_связи = перевести_16_разрядов_в_сетевой_порядок(32345);
    server_address.содержимое_межсетевого_адреса.значение_адреса = перевести_32_разряда_в_сетевой_порядок(адрес_обратной_петли);
    report("bind", привязать_местный_адрес(server, (const struct адрес_конечной_точки_связи *)&server_address,
                        sizeof(server_address)) == 0);
    report("connect", соединить_с_другой_стороной(client, (const struct адрес_конечной_точки_связи *)&server_address,
                              sizeof(server_address)) == 0);
    report("send", отправить(client, "ping", 4, 0) == 4);
    report("recvfrom", получить_с_адресом_отправителя(server, буфер_передачи_2, sizeof(буфер_передачи_2), 0,
                                (struct адрес_конечной_точки_связи *)&source, &source_length) == 4 &&
                       буфер_передачи_2[0] == 'p' && буфер_передачи_2[3] == 'g' && source_length == 16);
    errno = 0;
    report("empty-eagain", получить(server, буфер_передачи_2, sizeof(буфер_передачи_2), 0) == -1 && errno == EAGAIN);
    report("getsockname", получить_местный_адрес_точки(server, (struct адрес_конечной_точки_связи *)&source,
                                      &source_length) == 0 && source.номер_порта_связи == перевести_16_разрядов_в_сетевой_порядок(32345));
    errno = 0;
    report("udp-listen-not-supported", подготовить_приём_соединений(server, 1) == -1 && errno == EOPNOTSUPP);
    report("close-client", закрыть(client) == 0);
    report("close-server", закрыть(server) == 0);
    say("NTEST:DONE\n");
    return 0;
}
