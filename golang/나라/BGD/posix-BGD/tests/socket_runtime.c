#include <arpa/inet.h>
#include <errno.h>
#include <sys/socket.h>
#include <unistd.h>

static unsigned int length_of(const char *s)
{
    unsigned int n = 0;
    while (s[n] != 0) n++;
    return n;
}

static void say(const char *s) { (void)lekha(STDOUT_FILENO, s, length_of(s)); }

static void report(const char *ব্যবস্থার_পরিচয়, int pass)
{
    say(pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    say(ব্যবস্থার_পরিচয়);
    say("\n");
}

int main(void)
{
    struct sockaddr_in server_address = {0};
    struct sockaddr_in source = {0};
    socklen_t source_length = sizeof(source);
    char স্থানান্তরের_অস্থায়ী_ভান্ডার_2[8] = {0};
    int server = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    int client = socket(AF_INET, SOCK_DGRAM, 0);

    report("socket-server", server >= 3);
    report("socket-client", client >= 3 && client != server);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(32345);
    server_address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    report("bind", bind(server, (const struct sockaddr *)&server_address,
                        sizeof(server_address)) == 0);
    report("connect", connect(client, (const struct sockaddr *)&server_address,
                              sizeof(server_address)) == 0);
    report("send", send(client, "ping", 4, 0) == 4);
    report("recvfrom", recvfrom(server, স্থানান্তরের_অস্থায়ী_ভান্ডার_2, sizeof(স্থানান্তরের_অস্থায়ী_ভান্ডার_2), 0,
                                (struct sockaddr *)&source, &source_length) == 4 &&
                       স্থানান্তরের_অস্থায়ী_ভান্ডার_2[0] == 'p' && স্থানান্তরের_অস্থায়ী_ভান্ডার_2[3] == 'g' && source_length == 16);
    errno = 0;
    report("empty-eagain", recv(server, স্থানান্তরের_অস্থায়ী_ভান্ডার_2, sizeof(স্থানান্তরের_অস্থায়ী_ভান্ডার_2), 0) == -1 && errno == EAGAIN);
    report("getsockname", getsockname(server, (struct sockaddr *)&source,
                                      &source_length) == 0 && source.sin_port == htons(32345));
    errno = 0;
    report("udp-listen-not-supported", listen(server, 1) == -1 && errno == EOPNOTSUPP);
    report("close-client", close(client) == 0);
    report("close-server", close(server) == 0);
    say("NTEST:DONE\n");
    return 0;
}
