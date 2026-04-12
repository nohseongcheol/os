#ifndef MULTILINGUAL_POSIX_H
#define MULTILINGUAL_POSIX_H

#ifdef __cplusplus
extern "C" {
#endif

/* UTF-8 source file expected. */

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
#include <sys/select.h>

#ifdef __linux__
#include <sys/epoll.h>
#endif

/* Build examples:
 *   gcc -std=gnu11 -Wall -Wextra -finput-charset=UTF-8 -c multilingual_posix.c
 *   gcc -std=gnu11 -Wall -Wextra -finput-charset=UTF-8 example.c multilingual_posix.c -pthread
 */

typedef void (*ko_신호처리기)(int);
typedef void (*ja_シグナル処理器)(int);

/* 파일 입출력 / ファイル入出力 */
int ko_파일열기(const char *경로, int 플래그, mode_t 모드);
int ja_ファイル開く(const char *パス, int フラグ, mode_t モード);
int ko_기준경로파일열기(int 기준디렉터리파일기술자, const char *경로, int 플래그, mode_t 모드);
int ja_基準パスファイル開く(int 基準ディレクトリファイル記述子, const char *パス, int フラグ, mode_t モード);
int ko_파일생성(const char *경로, mode_t 모드);
int ja_ファイル作成(const char *パス, mode_t モード);
int ko_파일닫기(int 파일기술자);
int ja_ファイル閉じる(int ファイル記述子);
ssize_t ko_읽기(int 파일기술자, void *버퍼, size_t 크기);
ssize_t ja_読む(int ファイル記述子, void *バッファ, size_t サイズ);
ssize_t ko_쓰기(int 파일기술자, const void *버퍼, size_t 크기);
ssize_t ja_書く(int ファイル記述子, const void *バッファ, size_t サイズ);
ssize_t ko_위치지정읽기(int 파일기술자, void *버퍼, size_t 크기, off_t 위치);
ssize_t ja_位置指定読取(int ファイル記述子, void *バッファ, size_t サイズ, off_t 位置);
ssize_t ko_위치지정쓰기(int 파일기술자, const void *버퍼, size_t 크기, off_t 위치);
ssize_t ja_位置指定書込(int ファイル記述子, const void *バッファ, size_t サイズ, off_t 位置);
ssize_t ko_벡터읽기(int 파일기술자, const struct iovec *벡터, int 개수);
ssize_t ja_ベクタ読取(int ファイル記述子, const struct iovec *ベクタ, int 個数);
ssize_t ko_벡터쓰기(int 파일기술자, const struct iovec *벡터, int 개수);
ssize_t ja_ベクタ書込(int ファイル記述子, const struct iovec *ベクタ, int 個数);
off_t ko_파일위치이동(int 파일기술자, off_t 오프셋, int 기준);
off_t ja_ファイル位置移動(int ファイル記述子, off_t オフセット, int 基準);
int ko_파일동기화(int 파일기술자);
int ja_ファイル同期(int ファイル記述子);
int ko_파일데이터동기화(int 파일기술자);
int ja_ファイルデータ同期(int ファイル記述子);
int ko_파일기술자복제(int 기존파일기술자);
int ja_ファイル記述子複製(int 기존ファイル記述子);
int ko_파일기술자복제지정(int 기존파일기술자, int 새파일기술자);
int ja_ファイル記述子複製指定(int 기존ファイル記述子, int 새ファイル記述子);
int ko_파일제어(int 파일기술자, int 명령, long 인자);
int ja_ファイル制御(int ファイル記述子, int コマンド, long 引数);
int ko_입출력제어(int 파일기술자, unsigned long 요청, void *인자);
int ja_入出力制御(int ファイル記述子, unsigned long 要求, void *引数);
int ko_터미널확인(int 파일기술자);
int ja_端末確認(int ファイル記述子);
int ko_파이프생성(int 파일기술자쌍[2]);
int ja_パイプ作成(int ファイル記述子쌍[2]);

/* 파일/경로 속성 / ファイル・パス属性 */
int ko_상태조회(const char *경로, struct stat *상태);
int ja_状態取得(const char *パス, struct stat *状態);
int ko_파일상태조회(int 파일기술자, struct stat *상태);
int ja_ファイル状態取得(int ファイル記述子, struct stat *状態);
int ko_링크상태조회(const char *경로, struct stat *상태);
int ja_リンク状態取得(const char *パス, struct stat *状態);
int ko_접근확인(const char *경로, int 모드);
int ja_アクセス確認(const char *パス, int モード);
int ko_권한변경(const char *경로, mode_t 모드);
int ja_権限変更(const char *パス, mode_t モード);
int ko_파일권한변경(int 파일기술자, mode_t 모드);
int ja_ファイル権限変更(int ファイル記述子, mode_t モード);
int ko_소유자변경(const char *경로, uid_t 사용자, gid_t 그룹);
int ja_所有者変更(const char *パス, uid_t ユーザー, gid_t グループ);
int ko_파일소유자변경(int 파일기술자, uid_t 사용자, gid_t 그룹);
int ja_ファイル所有者変更(int ファイル記述子, uid_t ユーザー, gid_t グループ);
mode_t ko_기본권한마스크설정(mode_t 마스크);
mode_t ja_作成時権限マスク設定(mode_t マスク);
int ko_디렉터리생성(const char *경로, mode_t 모드);
int ja_ディレクトリ作成(const char *パス, mode_t モード);
int ko_디렉터리삭제(const char *경로);
int ja_ディレクトリ削除(const char *パス);
int ko_이름변경(const char *기존경로, const char *새경로);
int ja_名前変更(const char *기존パス, const char *새パス);
int ko_하드링크생성(const char *기존경로, const char *새경로);
int ja_ハードリンク作成(const char *기존パス, const char *새パス);
int ko_파일삭제(const char *경로);
int ja_ファイル削除(const char *パス);
int ko_심볼릭링크생성(const char *대상경로, const char *링크경로);
int ja_シンボリックリンク作成(const char *대상パス, const char *링크パス);
ssize_t ko_링크읽기(const char *경로, char *버퍼, size_t 버퍼크기);
ssize_t ja_リンク読取(const char *パス, char *バッファ, size_t バッファサイズ);
int ko_파일잘라내기(const char *경로, off_t 길이);
int ja_ファイル切詰め(const char *パス, off_t 長さ);
int ko_파일기반잘라내기(int 파일기술자, off_t 길이);
int ja_ファイル基準切詰め(int ファイル記述子, off_t 長さ);
int ko_시간갱신(const char *경로, const struct utimbuf *시간정보);
int ja_時刻更新(const char *パス, const struct utimbuf *時刻情報);
int ko_시간들갱신(const char *경로, const struct timeval 시간들[2]);
int ja_時刻群更新(const char *パス, const struct timeval 時刻群[2]);
char * ko_실제경로얻기(const char *경로, char *해결경로);
char * ja_実パス取得(const char *パス, char *해결パス);
int ko_디렉터리변경(const char *경로);
int ja_ディレクトリ変更(const char *パス);
int ko_파일기반디렉터리변경(int 파일기술자);
int ja_ファイル基準ディレクトリ変更(int ファイル記述子);
char * ko_현재디렉터리얻기(char *버퍼, size_t 크기);
char * ja_現在ディレクトリ取得(char *バッファ, size_t サイズ);

/* 프로세스 / プロセス */
pid_t ko_프로세스분기(void);
pid_t ja_プロセス分岐(void);
int ko_프로그램실행(const char *경로, char *const 인자[], char *const 환경[]);
int ja_プログラム実行(const char *パス, char *const 引数[], char *const 환경[]);
void ko_즉시종료(int 상태코드);
void ja_即時終了(int 状態코드);
void ko_종료(int 상태코드);
void ja_終了(int 状態코드);
void ko_비정상중단(void);
void ja_異常中断(void);
pid_t ko_프로세스아이디얻기(void);
pid_t ja_プロセスID取得(void);
pid_t ko_부모프로세스아이디얻기(void);
pid_t ja_親プロセスID取得(void);
pid_t ko_프로세스그룹아이디얻기(pid_t 프로세스아이디);
pid_t ja_プロセスグループID取得(pid_t プロセスID);
pid_t ko_프로세스그룹얻기(void);
pid_t ja_プロセスグループ取得(void);
int ko_프로세스그룹설정(pid_t 프로세스아이디, pid_t 프로세스그룹아이디);
int ja_プロセスグループ設定(pid_t プロセスID, pid_t 프로세스グループ아이디);
pid_t ko_세션생성(void);
pid_t ja_セッション作成(void);
pid_t ko_세션아이디얻기(pid_t 프로세스아이디);
pid_t ja_セッションID取得(pid_t プロセスID);
int ko_우선순위조정(int 증가값);
int ja_優先度調整(int 増加値);
int ko_우선순위얻기(int 대상종류, id_t 대상);
int ja_優先度取得(int 対象種類, id_t 대상);
int ko_우선순위설정(int 대상종류, id_t 대상, int 우선순위);
int ja_優先度設定(int 対象種類, id_t 대상, int 優先度);
pid_t ko_자식대기(int *상태코드);
pid_t ja_子待機(int *状態코드);
pid_t ko_프로세스대기(pid_t 프로세스아이디, int *상태코드, int 옵션);
pid_t ja_プロセス待機(pid_t プロセスID, int *状態코드, int 옵션);

/* 신호 / シグナル */
ko_신호처리기 ko_신호처리설정(int 신호번호, ko_신호처리기 처리기);
ko_신호처리기 ja_シグナル処理設定(int シグナル番号, ko_신호処理器 処理器);
int ko_신호동작설정(int 신호번호, const struct sigaction *새동작, struct sigaction *이전동작);
int ja_シグナル動作設定(int シグナル番号, const struct sigaction *新動作, struct sigaction *旧動作);
int ko_신호보내기(pid_t 프로세스아이디, int 신호번호);
int ja_シグナル送信(pid_t プロセスID, int シグナル番号);
int ko_자기신호발생(int 신호번호);
int ja_自己シグナル発生(int シグナル番号);
int ko_신호마스크설정(int 방법, const sigset_t *새마스크, sigset_t *이전마스크);
int ja_シグナルマスク設定(int 方法, const sigset_t *새マスク, sigset_t *이전マスク);
int ko_대기중신호조회(sigset_t *대기중신호집합);
int ja_保留シグナル取得(sigset_t *保留シグナル集合);
int ko_신호대기일시중지(const sigset_t *마스크);
int ja_シグナル待機一時停止(const sigset_t *マスク);
int ko_신호대기(const sigset_t *집합, int *신호번호);
int ja_シグナル待機(const sigset_t *集合, int *シグナル番号);

/* 사용자/환경 / ユーザー・環境 */
uid_t ko_사용자아이디얻기(void);
uid_t ja_ユーザーID取得(void);
uid_t ko_실효사용자아이디얻기(void);
uid_t ja_実効ユーザーID取得(void);
gid_t ko_그룹아이디얻기(void);
gid_t ja_グループID取得(void);
gid_t ko_실효그룹아이디얻기(void);
gid_t ja_実効グループID取得(void);
int ko_사용자아이디설정(uid_t 사용자아이디);
int ja_ユーザーID設定(uid_t ユーザー아이디);
int ko_실효사용자아이디설정(uid_t 사용자아이디);
int ja_実効ユーザーID設定(uid_t ユーザー아이디);
int ko_그룹아이디설정(gid_t 그룹아이디);
int ja_グループID設定(gid_t グループ아이디);
int ko_실효그룹아이디설정(gid_t 그룹아이디);
int ja_実効グループID設定(gid_t グループ아이디);
int ko_보조그룹얻기(int 크기, gid_t 목록[]);
int ja_補助グループ取得(int サイズ, gid_t 一覧[]);
char * ko_환경변수얻기(const char *이름);
char * ja_環境変数取得(const char *名前);
int ko_환경변수설정(const char *이름, const char *값, int 덮어쓰기);
int ja_環境変数設定(const char *名前, const char *値, int 上書き);
int ko_환경변수해제(const char *이름);
int ja_環境変数解除(const char *名前);
int ko_환경문자열설정(char *문자열);
int ja_環境文字列設定(char *文字列);

/* 시간/시스템 / 時間・システム */
time_t ko_현재시간얻기(time_t *저장위치);
time_t ja_現在時刻取得(time_t *저장位置);
int ko_시계시간얻기(clockid_t 시계아이디, struct timespec *시간);
int ja_時計時刻取得(clockid_t 時計ID, struct timespec *時刻);
int ko_시계시간설정(clockid_t 시계아이디, const struct timespec *시간);
int ja_時計時刻設定(clockid_t 時計ID, const struct timespec *時刻);
int ko_시계해상도얻기(clockid_t 시계아이디, struct timespec *해상도);
int ja_時計分解能取得(clockid_t 時計ID, struct timespec *分解能);
unsigned int ko_알람설정(unsigned int 초);
unsigned int ja_アラーム設定(unsigned int 초);
int ko_일시정지대기(void);
int ja_一時停止待機(void);
unsigned int ko_잠자기(unsigned int 초);
unsigned int ja_スリープ(unsigned int 초);
int ko_나노잠자기(const struct timespec *요청시간, struct timespec *남은시간);
int ja_ナノスリープ(const struct timespec *要求時刻, struct timespec *남은時刻);
int ko_시간과날짜얻기(struct timeval *시간, struct timezone *시간대);
int ja_時刻日付取得(struct timeval *時刻, struct timezone *時刻대);
int ko_시스템정보얻기(struct utsname *정보);
int ja_システム情報取得(struct utsname *情報);
long ko_시스템구성얻기(int 이름);
long ja_システム構成取得(int 名前);
long ko_경로구성얻기(const char *경로, int 이름);
long ja_パス構成取得(const char *パス, int 名前);
long ko_파일경로구성얻기(int 파일기술자, int 이름);
long ja_ファイルパス構成取得(int ファイル記述子, int 名前);
int ko_호스트이름얻기(char *이름버퍼, size_t 길이);
int ja_ホスト名取得(char *名前バッファ, size_t 長さ);
int ko_호스트이름설정(const char *이름, size_t 길이);
int ja_ホスト名設定(const char *名前, size_t 長さ);

/* 메모리 / メモリ */
void * ko_메모리매핑(void *주소, size_t 길이, int 보호, int 플래그, int 파일기술자, off_t 오프셋);
void * ja_メモリマップ(void *アドレス, size_t 長さ, int 保護, int フラグ, int ファイル記述子, off_t オフセット);
int ko_메모리매핑해제(void *주소, size_t 길이);
int ja_メモリマップ解除(void *アドレス, size_t 長さ);
int ko_메모리보호설정(void *주소, size_t 길이, int 보호);
int ja_メモリ保護設定(void *アドレス, size_t 長さ, int 保護);
int ko_메모리동기화(void *주소, size_t 길이, int 플래그);
int ja_メモリ同期(void *アドレス, size_t 長さ, int フラグ);
int ko_메모리고정(const void *주소, size_t 길이);
int ja_メモリ固定(const void *アドレス, size_t 長さ);
int ko_메모리고정해제(const void *주소, size_t 길이);
int ja_メモリ固定解除(const void *アドレス, size_t 長さ);
int ko_전체메모리고정(int 플래그);
int ja_全メモリ固定(int フラグ);
int ko_전체메모리고정해제(void);
int ja_全メモリ固定解除(void);
void * ko_힙증감(intptr_t 증가량);
void * ja_ヒープ増減(intptr_t 増加量);

/* 소켓/다중화 / ソケット・多重化 */
int ko_소켓생성(int 도메인, int 형식, int 프로토콜);
int ja_ソケット作成(int ドメイン, int 種別, int プロトコル);
int ko_소켓쌍생성(int 도메인, int 형식, int 프로토콜, int 소켓쌍[2]);
int ja_ソケット対作成(int ドメイン, int 種別, int プロトコル, int ソケット対[2]);
int ko_주소결합(int 소켓파일기술자, const struct sockaddr *주소, socklen_t 주소길이);
int ja_アドレス結合(int 소켓ファイル記述子, const struct sockaddr *アドレス, socklen_t アドレス長さ);
int ko_연결대기(int 소켓파일기술자, int 대기열크기);
int ja_接続待機(int 소켓ファイル記述子, int 대기열サイズ);
int ko_연결수락(int 소켓파일기술자, struct sockaddr *주소, socklen_t *주소길이);
int ja_接続受諾(int 소켓ファイル記述子, struct sockaddr *アドレス, socklen_t *アドレス長さ);
int ko_연결요청(int 소켓파일기술자, const struct sockaddr *주소, socklen_t 주소길이);
int ja_接続要求(int 소켓ファイル記述子, const struct sockaddr *アドレス, socklen_t アドレス長さ);
int ko_통신종료(int 소켓파일기술자, int 방법);
int ja_通信終了(int 소켓ファイル記述子, int 方法);
ssize_t ko_전송(int 소켓파일기술자, const void *버퍼, size_t 길이, int 플래그);
ssize_t ja_送信(int 소켓ファイル記述子, const void *バッファ, size_t 長さ, int フラグ);
ssize_t ko_대상전송(int 소켓파일기술자, const void *버퍼, size_t 길이, int 플래그, const struct sockaddr *대상주소, socklen_t 주소길이);
ssize_t ja_宛先送信(int 소켓ファイル記述子, const void *バッファ, size_t 長さ, int フラグ, const struct sockaddr *대상アドレス, socklen_t アドレス長さ);
ssize_t ko_수신(int 소켓파일기술자, void *버퍼, size_t 길이, int 플래그);
ssize_t ja_受信(int 소켓ファイル記述子, void *バッファ, size_t 長さ, int フラグ);
ssize_t ko_대상수신(int 소켓파일기술자, void *버퍼, size_t 길이, int 플래그, struct sockaddr *대상주소, socklen_t *주소길이);
ssize_t ja_送信元受信(int 소켓ファイル記述子, void *バッファ, size_t 長さ, int フラグ, struct sockaddr *대상アドレス, socklen_t *アドレス長さ);
int ko_소켓이름얻기(int 소켓파일기술자, struct sockaddr *주소, socklen_t *주소길이);
int ja_ソケット名取得(int 소켓ファイル記述子, struct sockaddr *アドレス, socklen_t *アドレス長さ);
int ko_상대이름얻기(int 소켓파일기술자, struct sockaddr *주소, socklen_t *주소길이);
int ja_相手名取得(int 소켓ファイル記述子, struct sockaddr *アドレス, socklen_t *アドレス長さ);
int ko_소켓옵션얻기(int 소켓파일기술자, int 레벨, int 옵션이름, void *옵션값, socklen_t *옵션길이);
int ja_ソケットオプション取得(int 소켓ファイル記述子, int 레벨, int 옵션名前, void *옵션値, socklen_t *옵션長さ);
int ko_소켓옵션설정(int 소켓파일기술자, int 레벨, int 옵션이름, const void *옵션값, socklen_t 옵션길이);
int ja_ソケットオプション設定(int 소켓ファイル記述子, int 레벨, int 옵션名前, const void *옵션値, socklen_t 옵션長さ);
int ko_다중선택대기(int 최대파일기술자플러스1, fd_set *읽기집합, fd_set *쓰기집합, fd_set *예외집합, struct timeval *시간제한);
int ja_多重選択待機(int 최대ファイル記述子플러스1, fd_set *읽기集合, fd_set *쓰기集合, fd_set *예외集合, struct timeval *時刻제한);
int ko_상태감시(struct pollfd 파일기술자배열[], nfds_t 개수, int 시간제한밀리초);
int ja_状態監視(struct pollfd ファイル記述子배열[], nfds_t 個数, int 時刻제한밀리초);

/* 스레드 / スレッド */
int ko_스레드생성(pthread_t *스레드, const pthread_attr_t *속성, void *(*시작루틴)(void *), void *인자);
int ja_スレッド作成(pthread_t *スレッド, const pthread_attr_t *属性, void *(*開始ルーチン)(void *), void *引数);
void ko_스레드종료(void *반환값);
void ja_スレッド終了(void *반환値);
int ko_스레드합류(pthread_t 스레드, void **반환값위치);
int ja_スレッド合流(pthread_t スレッド, void **반환値位置);
int ko_스레드분리(pthread_t 스레드);
int ja_スレッド分離(pthread_t スレッド);
pthread_t ko_현재스레드얻기(void);
pthread_t ja_現在スレッド取得(void);
int ko_스레드동일비교(pthread_t 첫번째, pthread_t 두번째);
int ja_スレッド同一比較(pthread_t 一つ目, pthread_t 二つ目);
int ko_스레드취소(pthread_t 스레드);
int ja_スレッド取消(pthread_t スレッド);
int ko_한번실행(pthread_once_t *제어객체, void (*초기화함수)(void));
int ja_一回実行(pthread_once_t *制御オブジェクト, void (*初期化関数)(void));

/* 동기화 / 同期 */
int ko_뮤텍스초기화(pthread_mutex_t *뮤텍스, const pthread_mutexattr_t *속성);
int ja_ミューテックス初期化(pthread_mutex_t *ミューテックス, const pthread_mutexattr_t *属性);
int ko_뮤텍스파기(pthread_mutex_t *뮤텍스);
int ja_ミューテックス破棄(pthread_mutex_t *ミューテックス);
int ko_뮤텍스잠금(pthread_mutex_t *뮤텍스);
int ja_ミューテックスロック(pthread_mutex_t *ミューテックス);
int ko_뮤텍스잠금시도(pthread_mutex_t *뮤텍스);
int ja_ミューテックスロック試行(pthread_mutex_t *ミューテックス);
int ko_뮤텍스해제(pthread_mutex_t *뮤텍스);
int ja_ミューテックス解除(pthread_mutex_t *ミューテックス);
int ko_조건변수초기화(pthread_cond_t *조건변수, const pthread_condattr_t *속성);
int ja_条件変数初期化(pthread_cond_t *条件変数, const pthread_condattr_t *属性);
int ko_조건변수파기(pthread_cond_t *조건변수);
int ja_条件変数破棄(pthread_cond_t *条件変数);
int ko_조건대기(pthread_cond_t *조건변수, pthread_mutex_t *뮤텍스);
int ja_条件待機(pthread_cond_t *条件変数, pthread_mutex_t *ミューテックス);
int ko_조건시간대기(pthread_cond_t *조건변수, pthread_mutex_t *뮤텍스, const struct timespec *절대시간);
int ja_条件時間待機(pthread_cond_t *条件変数, pthread_mutex_t *ミューテックス, const struct timespec *절대時刻);
int ko_조건하나깨우기(pthread_cond_t *조건변수);
int ja_条件単一通知(pthread_cond_t *条件変数);
int ko_조건전체깨우기(pthread_cond_t *조건변수);
int ja_条件全体通知(pthread_cond_t *条件変数);
int ko_읽기쓰기잠금초기화(pthread_rwlock_t *잠금, const pthread_rwlockattr_t *속성);
int ja_読書きロック初期化(pthread_rwlock_t *ロック, const pthread_rwlockattr_t *属性);
int ko_읽기쓰기잠금파기(pthread_rwlock_t *잠금);
int ja_読書きロック破棄(pthread_rwlock_t *ロック);
int ko_읽기잠금(pthread_rwlock_t *잠금);
int ja_読取ロック(pthread_rwlock_t *ロック);
int ko_쓰기잠금(pthread_rwlock_t *잠금);
int ja_書込ロック(pthread_rwlock_t *ロック);
int ko_읽기쓰기잠금해제(pthread_rwlock_t *잠금);
int ja_読書きロック解除(pthread_rwlock_t *ロック);
int ko_세마포어초기화(sem_t *세마포어, int 프로세스간공유, unsigned int 초기값);
int ja_セマフォ初期化(sem_t *セマフォ, int プロセス間共有, unsigned int 초기値);
int ko_세마포어파기(sem_t *세마포어);
int ja_セマフォ破棄(sem_t *セマフォ);
int ko_세마포어대기(sem_t *세마포어);
int ja_セマフォ待機(sem_t *セマフォ);
int ko_세마포어대기시도(sem_t *세마포어);
int ja_セマフォ待機試行(sem_t *セマフォ);
int ko_세마포어시간대기(sem_t *세마포어, const struct timespec *절대시간);
int ja_セマフォ時間待機(sem_t *セマフォ, const struct timespec *절대時刻);
int ko_세마포어해제(sem_t *세마포어);
int ja_セマフォ解放(sem_t *セマフォ);

/* 디렉터리 / ディレクトリ */
DIR * ko_디렉터리열기(const char *경로);
DIR * ja_ディレクトリ開く(const char *パス);
DIR * ko_파일기반디렉터리열기(int 파일기술자);
DIR * ja_ファイル基準ディレクトリ開く(int ファイル記述子);
struct dirent * ko_디렉터리읽기(DIR *디렉터리);
struct dirent * ja_ディレクトリ読取(DIR *ディレクトリ);
int ko_디렉터리닫기(DIR *디렉터리);
int ja_ディレクトリ閉じる(DIR *ディレクトリ);
void ko_디렉터리처음으로(DIR *디렉터리);
void ja_ディレクトリ先頭戻し(DIR *ディレクトリ);
void ko_디렉터리위치이동(DIR *디렉터리, long 위치);
void ja_ディレクトリ位置移動(DIR *ディレクトリ, long 位置);
long ko_디렉터리위치얻기(DIR *디렉터리);
long ja_ディレクトリ位置取得(DIR *ディレクトリ);

/* 표준 입출력 / 標準入出力 */
FILE * ko_스트림열기(const char *경로, const char *모드);
FILE * ja_ストリーム開く(const char *パス, const char *モード);
int ko_스트림닫기(FILE *스트림);
int ja_ストリーム閉じる(FILE *스트림);
size_t ko_스트림읽기(void *버퍼, size_t 항목크기, size_t 항목개수, FILE *스트림);
size_t ja_ストリーム読取(void *バッファ, size_t 항목サイズ, size_t 항목個数, FILE *스트림);
size_t ko_스트림쓰기(const void *버퍼, size_t 항목크기, size_t 항목개수, FILE *스트림);
size_t ja_ストリーム書込(const void *バッファ, size_t 항목サイズ, size_t 항목個数, FILE *스트림);
int ko_스트림비우기(FILE *스트림);
int ja_ストリーム排出(FILE *스트림);

/* Linux epoll wrappers */
#ifdef __linux__
int ko_이벤트감시생성(int 플래그);
int ja_イベント監視作成(int フラグ);
int ko_이벤트감시설정(int 이벤트감시파일기술자, int 동작, int 대상파일기술자, struct epoll_event *이벤트);
int ja_イベント監視制御(int イベント監視ファイル記述子, int 動作, int 対象ファイル記述子, struct epoll_event *イベント);
int ko_이벤트대기(int 이벤트감시파일기술자, struct epoll_event 이벤트배열[], int 최대이벤트수, int 시간제한밀리초);
int ja_イベント待機(int イベント監視ファイル記述子, struct epoll_event イベント배열[], int 최대イベント수, int 時間制限ミリ秒);
#endif

/* printf-style wrappers / printf系ラッパー */
int ko_출력형식쓰기(const char *형식, ...);
int ko_파일출력형식쓰기(FILE *스트림, const char *형식, ...);
int ko_문자열출력형식쓰기(char *버퍼, const char *형식, ...);
int ko_길이제한문자열출력형식쓰기(char *버퍼, size_t 버퍼크기, const char *형식, ...);
int ja_書式出力(const char *書式, ...);
int ja_ファイル書式出力(FILE *ストリーム, const char *書式, ...);
int ja_文字列書式出力(char *バッファ, const char *書式, ...);
int ja_長さ制限文字列書式出力(char *バッファ, size_t バッファサイズ, const char *書式, ...);

#ifdef __cplusplus
}
#endif

#endif
