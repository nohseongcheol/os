#include <संचार_पता_परिवर्तन/अष्टक_क्रम.h>
#include <errno.h>
#include <प्रणाली/socket.h>
#include <unistd.h>

static unsigned int length_of(const char *s)
{
    unsigned int n = 0;
    while (s[n] != 0) n++;
    return n;
}

static void say(const char *s) { (void)लिखना(STDOUT_FILENO, s, length_of(s)); }

static void report(const char *प्रणाली_की_पहचान, int pass)
{
    say(pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    say(प्रणाली_की_पहचान);
    say("\n");
}

int main(void)
{
    struct अंतरजाल_छोर_पता server_address = {0};
    struct अंतरजाल_छोर_पता source = {0};
    पता_लंबाई_प्रकार source_length = sizeof(source);
    char स्थानांतरण_का_अस्थायी_भंडार_2[8] = {0};
    int server = संचार_छोर_बनाना(अंतरजाल_पता_परिवार_संकेत, आँकड़ा_संदेश_छोर, उपयोगकर्ता_आँकड़ा_संदेश_नियम);
    int client = संचार_छोर_बनाना(अंतरजाल_पता_परिवार_संकेत, आँकड़ा_संदेश_छोर, 0);

    report("socket-server", server >= 3);
    report("socket-client", client >= 3 && client != server);
    server_address.अंतरजाल_पता_परिवार = अंतरजाल_पता_परिवार_संकेत;
    server_address.संचार_द्वार_संख्या = _16_अंकों_को_संजाल_क्रम_में_बदलना(32345);
    server_address.अंतरजाल_पता_सामग्री.पता_मान = _32_अंकों_को_संजाल_क्रम_में_बदलना(स्वयं_वापसी_पता);
    report("bind", स्थानीय_पता_बाँधना(server, (const struct संचार_छोर_पता *)&server_address,
                        sizeof(server_address)) == 0);
    report("connect", दूसरे_छोर_से_जुड़ना(client, (const struct संचार_छोर_पता *)&server_address,
                              sizeof(server_address)) == 0);
    report("send", भेजना(client, "ping", 4, 0) == 4);
    report("recvfrom", प्रेषक_पते_सहित_प्राप्त_करना(server, स्थानांतरण_का_अस्थायी_भंडार_2, sizeof(स्थानांतरण_का_अस्थायी_भंडार_2), 0,
                                (struct संचार_छोर_पता *)&source, &source_length) == 4 &&
                       स्थानांतरण_का_अस्थायी_भंडार_2[0] == 'p' && स्थानांतरण_का_अस्थायी_भंडार_2[3] == 'g' && source_length == 16);
    errno = 0;
    report("empty-eagain", प्राप्त_करना(server, स्थानांतरण_का_अस्थायी_भंडार_2, sizeof(स्थानांतरण_का_अस्थायी_भंडार_2), 0) == -1 && errno == EAGAIN);
    report("getsockname", स्थानीय_छोर_पता_पाना(server, (struct संचार_छोर_पता *)&source,
                                      &source_length) == 0 && source.संचार_द्वार_संख्या == _16_अंकों_को_संजाल_क्रम_में_बदलना(32345));
    errno = 0;
    report("udp-listen-not-supported", जुड़ाव_अनुरोध_के_लिए_तैयार_होना(server, 1) == -1 && errno == EOPNOTSUPP);
    report("close-client", बंद_करना(client) == 0);
    report("close-server", बंद_करना(server) == 0);
    say("NTEST:DONE\n");
    return 0;
}
