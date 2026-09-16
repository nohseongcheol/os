#include <errno.h>
#include <fcntl.h>
#include <प्रणाली/stat.h>
#include <प्रणाली/संतान_प्रतीक्षा.h>
#include <unistd.h>
#include <प्रणाली/syscall.h>

enum {
    SYS_तुरंत_समाप्त_करना = 1,
    SYS_संतान_प्रक्रिया_बनाना = 2,
    SYS_पढ़ना = 3,
    SYS_लिखना = 4,
    SYS_बंद_करना = 6,
    SYS_निष्पादन_सामग्री_बदलना = 11,
    SYS_कार्य_निर्देशिका_बदलना = 12,
    SYS_पठन_लेखन_स्थिति_बदलना = 19,
    SYS_प्रक्रिया_पहचान_पाना = 20,
    SYS_उपयोगकर्ता_पहचान_पाना = 24,
    SYS_पहुँच_अनुमति_जाँचना = 33,
    SYS_सभी_अभिलेख_समकालित_करना = 36,
    SYS_खुली_संचिका_संदर्भ_की_प्रतिलिपि_बनाना = 41,
    SYS_गतिशील_स्मृति_अंत_निर्धारित_करना = 45,
    SYS_समूह_पहचान_पाना = 47,
    SYS_प्रभावी_उपयोगकर्ता_पहचान_पाना = 49,
    SYS_प्रभावी_समूह_पहचान_पाना = 50,
    SYS_नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना = 63,
    SYS_जनक_प्रक्रिया_पहचान_पाना = 64,
    SYS_संचिका_अभिलेख_समकालित_करना = 118,
    SYS_कार्य_निर्देशिका_पथ_पाना = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void तुरंत_समाप्त_करना(int स्थिति)
{
    SC1(SYS_तुरंत_समाप्त_करना, स्थिति);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t पढ़ना(int संचिका_विवरणक, void *स्थानांतरण_का_अस्थायी_भंडार, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_पढ़ना, संचिका_विवरणक, स्थानांतरण_का_अस्थायी_भंडार, count));
}

ssize_t लिखना(int संचिका_विवरणक, const void *स्थानांतरण_का_अस्थायी_भंडार, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_लिखना, संचिका_विवरणक, स्थानांतरण_का_अस्थायी_भंडार, count));
}

int बंद_करना(int संचिका_विवरणक)
{
    return (int)__syscall_result(SC1(SYS_बंद_करना, संचिका_विवरणक));
}

off_t पठन_लेखन_स्थिति_बदलना(int संचिका_विवरणक, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_पठन_लेखन_स्थिति_बदलना, संचिका_विवरणक, offset, whence));
}

pid_t संतान_प्रक्रिया_बनाना(void)
{
    return (pid_t)__syscall_result(SC0(SYS_संतान_प्रक्रिया_बनाना));
}

int निष्पादन_सामग्री_बदलना(const char *पथ, char *const तर्क_सूची_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_निष्पादन_सामग्री_बदलना, पथ, तर्क_सूची_2, envp));
}

pid_t प्रक्रिया_पहचान_पाना(void) { return (pid_t)SC0(SYS_प्रक्रिया_पहचान_पाना); }
pid_t जनक_प्रक्रिया_पहचान_पाना(void) { return (pid_t)SC0(SYS_जनक_प्रक्रिया_पहचान_पाना); }
uid_t उपयोगकर्ता_पहचान_पाना(void) { return (uid_t)SC0(SYS_उपयोगकर्ता_पहचान_पाना); }
uid_t प्रभावी_उपयोगकर्ता_पहचान_पाना(void) { return (uid_t)SC0(SYS_प्रभावी_उपयोगकर्ता_पहचान_पाना); }
gid_t समूह_पहचान_पाना(void) { return (gid_t)SC0(SYS_समूह_पहचान_पाना); }
gid_t प्रभावी_समूह_पहचान_पाना(void) { return (gid_t)SC0(SYS_प्रभावी_समूह_पहचान_पाना); }

int पहुँच_अनुमति_जाँचना(const char *पथ, int mode)
{
    return (int)__syscall_result(SC2(SYS_पहुँच_अनुमति_जाँचना, पथ, mode));
}

int कार्य_निर्देशिका_बदलना(const char *पथ)
{
    return (int)__syscall_result(SC1(SYS_कार्य_निर्देशिका_बदलना, पथ));
}

char *कार्य_निर्देशिका_पथ_पाना(char *स्थानांतरण_का_अस्थायी_भंडार, size_t अंकों_की_संख्या)
{
    long result = __syscall_result(SC2(SYS_कार्य_निर्देशिका_पथ_पाना, स्थानांतरण_का_अस्थायी_भंडार, अंकों_की_संख्या));
    return result < 0 ? (char *)0 : स्थानांतरण_का_अस्थायी_भंडार;
}

int खुली_संचिका_संदर्भ_की_प्रतिलिपि_बनाना(int संचिका_विवरणक)
{
    return (int)__syscall_result(SC1(SYS_खुली_संचिका_संदर्भ_की_प्रतिलिपि_बनाना, संचिका_विवरणक));
}

int नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना, oldfd, newfd));
}

int संचिका_अभिलेख_समकालित_करना(int संचिका_विवरणक)
{
    return (int)__syscall_result(SC1(SYS_संचिका_अभिलेख_समकालित_करना, संचिका_विवरणक));
}

void सभी_अभिलेख_समकालित_करना(void)
{
    SC0(SYS_सभी_अभिलेख_समकालित_करना);
}

int अंतक_है_या_नहीं_जाँचना(int संचिका_विवरणक)
{
    struct संचिका_स्थिति st;
    if (खुली_संचिका_स्थिति_पाना(संचिका_विवरणक, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int गतिशील_स्मृति_अंत_निर्धारित_करना(void *address)
{
    long result = SC1(SYS_गतिशील_स्मृति_अंत_निर्धारित_करना, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *गतिशील_स्मृति_अंत_बदलना(int increment)
{
    long current = SC1(SYS_गतिशील_स्मृति_अंत_निर्धारित_करना, 0);
    long requested = current + increment;
    if (increment != 0 && गतिशील_स्मृति_अंत_निर्धारित_करना((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t नियत_संतान_की_प्रतीक्षा_करना(pid_t pid, int *स्थिति, int options)
{
    long result;
    do {
        result = SC3(7, pid, स्थिति, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t संतान_की_प्रतीक्षा_करना(int *स्थिति)
{
    return नियत_संतान_की_प्रतीक्षा_करना(-1, स्थिति, 0);
}
