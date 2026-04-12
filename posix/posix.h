// ===== multilingual_posix.h =====
#ifndef MULTILINGUAL_POSIX_H
#define MULTILINGUAL_POSIX_H

#ifdef __cplusplus
extern "C" {
#endif

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <sys/utsname.h>
#include <sys/uio.h>
#include <sys/ioctl.h>
#include <sys/resource.h>
#include <dirent.h>
#include <fcntl.h>
#include <poll.h>
#include <pthread.h>
#include <semaphore.h>
#include <signal.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <utime.h>
#include <netinet/in.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>

#ifdef __linux__
#include <sys/epoll.h>
#endif

/* Build example:
 *   gcc -std=gnu11 -Wall -Wextra -finput-charset=UTF-8 -c multilingual_posix.c
 */

int ko_파일열기(const char *경로, int 플래그, mode_t 모드);
int ko_파일닫기(int 파일기술자);
ssize_t ko_읽기(int 파일기술자, void *버퍼, size_t 크기);
ssize_t ko_쓰기(int 파일기술자, const void *버퍼, size_t 크기);
off_t ko_파일위치이동(int 파일기술자, off_t 오프셋, int 기준);
int ko_디렉터리생성(const char *경로, mode_t 모드);
int ko_디렉터리삭제(const char *경로);
int ko_이름변경(const char *기존경로, const char *새경로);
int ko_파일삭제(const char *경로);
int ko_프로세스분기(void);
pid_t ko_프로세스아이디얻기(void);
pid_t ko_부모프로세스아이디얻기(void);
unsigned int ko_잠자기(unsigned int 초);
int ko_시계시간얻기(clockid_t 시계아이디, struct timespec *시간);
void *ko_메모리매핑(void *주소, size_t 길이, int 보호, int 플래그, int 파일기술자, off_t 오프셋);
int ko_메모리매핑해제(void *주소, size_t 길이);
int ko_소켓생성(int 도메인, int 형식, int 프로토콜);
int ko_연결요청(int 소켓파일기술자, const struct sockaddr *주소, socklen_t 주소길이);
ssize_t ko_전송(int 소켓파일기술자, const void *버퍼, size_t 길이, int 플래그);
ssize_t ko_수신(int 소켓파일기술자, void *버퍼, size_t 길이, int 플래그);
int ko_스레드생성(pthread_t *스레드, const pthread_attr_t *속성, void *(*시작루틴)(void *), void *인자);
int ko_스레드합류(pthread_t 스레드, void **반환값위치);
int ko_뮤텍스잠금(pthread_mutex_t *뮤텍스);
int ko_뮤텍스해제(pthread_mutex_t *뮤텍스);
int ko_세마포어대기(sem_t *세마포어);
int ko_세마포어해제(sem_t *세마포어);
DIR *ko_디렉터리열기(const char *경로);
struct dirent *ko_디렉터리읽기(DIR *디렉터리);
int ko_디렉터리닫기(DIR *디렉터리);
int ko_출력형식쓰기(const char *형식, ...);
FILE *ko_스트림열기(const char *경로, const char *모드);
int ko_스트림닫기(FILE *스트림);

int ja_ファイル開く(const char *パス, int フラグ, mode_t モード);
int ja_ファイル閉じる(int ファイル記述子);
ssize_t ja_読む(int ファイル記述子, void *バッファ, size_t サイズ);
ssize_t ja_書く(int ファイル記述子, const void *バッファ, size_t サイズ);
off_t ja_ファイル位置移動(int ファイル記述子, off_t オフセット, int 基準);
int ja_ディレクトリ作成(const char *パス, mode_t モード);
int ja_ディレクトリ削除(const char *パス);
int ja_名前変更(const char *旧パス, const char *新パス);
int ja_ファイル削除(const char *パス);
int ja_プロセス分岐(void);
pid_t ja_プロセスID取得(void);
pid_t ja_親プロセスID取得(void);
unsigned int ja_スリープ(unsigned int 秒);
int ja_時計時刻取得(clockid_t 時計ID, struct timespec *時刻);
void *ja_メモリマップ(void *アドレス, size_t 長さ, int 保護, int フラグ, int ファイル記述子, off_t オフセット);
int ja_メモリマップ解除(void *アドレス, size_t 長さ);
int ja_ソケット作成(int ドメイン, int 種別, int プロトコル);
int ja_接続要求(int ソケットファイル記述子, const struct sockaddr *アドレス, socklen_t アドレス長);
ssize_t ja_送信(int ソケットファイル記述子, const void *バッファ, size_t 長さ, int フラグ);
ssize_t ja_受信(int ソケットファイル記述子, void *バッファ, size_t 長さ, int フラグ);
int ja_スレッド作成(pthread_t *スレッド, const pthread_attr_t *属性, void *(*開始ルーチン)(void *), void *引数);
int ja_スレッド合流(pthread_t スレッド, void **戻り値位置);
