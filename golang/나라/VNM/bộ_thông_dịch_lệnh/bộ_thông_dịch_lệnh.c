/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stddef.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/wait.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { sức_chứa_dòng_nhập = 512, số_đối_số_tối_đa = 16, độ_lồng_tệp_lệnh_tối_đa = 4 };
static int độ_sâu_lồng_tệp_lệnh;
struct luồng_đầu_vào {
    int bộ_mô_tả_đầu_vào;
    char bộ_đệm_truyền_2[256];
    size_t vị_trí;
    size_t độ_dài;
};

static size_t độ_dài_văn_bản_theo_byte(const char *văn_bản)
{
    size_t độ_dài = 0;
    while (văn_bản[độ_dài] != '\0')
        độ_dài++;
    return độ_dài;
}

static int văn_bản_bằng_nhau(const char *trái, const char *phải)
{
    size_t vị_trí = 0;
    while (trái[vị_trí] == phải[vị_trí]) {
        if (trái[vị_trí] == '\0')
            return 1;
        vị_trí++;
    }
    return 0;
}

static void ghi_văn_bản(const char *văn_bản)
{
    size_t độ_dài = độ_dài_văn_bản_theo_byte(văn_bản);
    while (độ_dài > 0U) {
        ssize_t số_byte_đã_ghi = Ghi(STDOUT_FILENO, văn_bản, độ_dài);
        if (số_byte_đã_ghi <= 0)
            return;
        văn_bản += số_byte_đã_ghi;
        độ_dài -= (size_t)số_byte_đã_ghi;
    }
}

static void ghi_số_nguyên(int giá_trị)
{
    char ký_tự_chữ_số[16];
    unsigned int số_chữ_số;
    unsigned int độ_lớn_không_dấu;

    if (giá_trị < 0) {
        ghi_văn_bản("-");
        độ_lớn_không_dấu = (unsigned int)(-(giá_trị + 1)) + 1U;
    } else {
        độ_lớn_không_dấu = (unsigned int)giá_trị;
    }
    số_chữ_số = 0;
    do {
        ký_tự_chữ_số[số_chữ_số++] = (char)('0' + độ_lớn_không_dấu % 10U);
        độ_lớn_không_dấu /= 10U;
    } while (độ_lớn_không_dấu != 0U);
    while (số_chữ_số > 0U) {
        số_chữ_số--;
        (void)Ghi(STDOUT_FILENO, &ký_tự_chữ_số[số_chữ_số], 1);
    }
}

static void báo_lỗi(const char *thao_tác)
{
    ghi_văn_bản("error: ");
    ghi_văn_bản(thao_tác);
    ghi_văn_bản(" errno=");
    ghi_số_nguyên(errno);
    ghi_văn_bản("\n");
}

static int đọc_dòng_nhập(struct luồng_đầu_vào *đầu_vào, char *dòng_nhập, size_t sức_chứa)
{
    size_t vị_trí = 0;
    int dòng_nhập_không_hợp_lệ = 0;
    char ký_tự;
    ssize_t số_byte_đã_đọc;
    if (sức_chứa < 2U)
        return -2;
    for (;;) {
        if (đầu_vào->vị_trí == đầu_vào->độ_dài) {
            số_byte_đã_đọc = Đọc(đầu_vào->bộ_mô_tả_đầu_vào, đầu_vào->bộ_đệm_truyền_2, sizeof(đầu_vào->bộ_đệm_truyền_2));
            if (số_byte_đã_đọc < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (số_byte_đã_đọc == 0) {
                if (vị_trí == 0 && !dòng_nhập_không_hợp_lệ)
                    return -1;
                break;
            }
            đầu_vào->độ_dài = (size_t)số_byte_đã_đọc;
            đầu_vào->vị_trí = 0;
        }
        ký_tự = đầu_vào->bộ_đệm_truyền_2[đầu_vào->vị_trí++];
        if (ký_tự == '\n')
            break;
        if (đầu_vào->bộ_mô_tả_đầu_vào == STDIN_FILENO && ký_tự == 4) {
            if (vị_trí == 0 && !dòng_nhập_không_hợp_lệ)
                return -1;
            break;
        }
        if (đầu_vào->bộ_mô_tả_đầu_vào == STDIN_FILENO && (ký_tự == 8 || ký_tự == 127)) {
            if (vị_trí > 0) {
                do {
                    vị_trí--;
                } while (vị_trí > 0 && ((unsigned char)dòng_nhập[vị_trí] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (ký_tự == '\r')
            continue;
        if (ký_tự == '\0') {
            dòng_nhập_không_hợp_lệ = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (vị_trí + 1U < sức_chứa)
            dòng_nhập[vị_trí++] = ký_tự;
        else
            dòng_nhập_không_hợp_lệ = 1;
    }
    dòng_nhập[vị_trí] = '\0';
    return dòng_nhập_không_hợp_lệ ? -2 : (int)vị_trí;
}

static int tách_đối_số(char *dòng_nhập, char **đối_số)
{
    int số_đối_số = 0;
    char *vị_trí_hiện_tại = dòng_nhập;
    char *vị_trí_xuất = dòng_nhập;

    while (*vị_trí_hiện_tại != '\0') {
        char dấu_ngoặc_kép = '\0';
        while (*vị_trí_hiện_tại == ' ' || *vị_trí_hiện_tại == '\t')
            vị_trí_hiện_tại++;
        if (*vị_trí_hiện_tại == '\0' || *vị_trí_hiện_tại == '#')
            break;
        if (số_đối_số == số_đối_số_tối_đa - 1)
            return -1;
        đối_số[số_đối_số++] = vị_trí_xuất;
        while (*vị_trí_hiện_tại != '\0') {
            char ký_tự = *vị_trí_hiện_tại++;
            if (dấu_ngoặc_kép == '\0' && (ký_tự == ' ' || ký_tự == '\t'))
                break;
            if (ký_tự == '\\' && dấu_ngoặc_kép != '\'') {
                if (*vị_trí_hiện_tại == '\0')
                    return -1;
                *vị_trí_xuất++ = *vị_trí_hiện_tại++;
            } else if (ký_tự == '\'' || ký_tự == '"') {
                if (dấu_ngoặc_kép == '\0')
                    dấu_ngoặc_kép = ký_tự;
                else if (dấu_ngoặc_kép == ký_tự)
                    dấu_ngoặc_kép = '\0';
                else
                    *vị_trí_xuất++ = ký_tự;
            } else {
                *vị_trí_xuất++ = ký_tự;
            }
        }
        if (dấu_ngoặc_kép != '\0')
            return -1;
        *vị_trí_xuất++ = '\0';
    }
    đối_số[số_đối_số] = (char *)0;
    return số_đối_số;
}

static void hiện_trợ_giúp(void)
{
    size_t vị_trí;
    ghi_văn_bản(
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
    ghi_văn_bản("Native command proposals (ASCII aliases remain available):\n");
    for (vị_trí = 0; vị_trí < sizeof(lệnh_chuẩn) / sizeof(lệnh_chuẩn[0]); vị_trí++) {
        ghi_văn_bản(tên_lệnh_bản_địa[vị_trí]);
        ghi_văn_bản(" = ");
        ghi_văn_bản(lệnh_chuẩn[vị_trí]);
        ghi_văn_bản("\n");
    }
}

static int lệnh_trùng_khớp(const char *văn_bản, const char *lệnh)
{
    size_t vị_trí;
    if (văn_bản_bằng_nhau(văn_bản, lệnh))
        return 1;
    for (vị_trí = 0; vị_trí < sizeof(lệnh_chuẩn) / sizeof(lệnh_chuẩn[0]); vị_trí++)
        if (văn_bản_bằng_nhau(lệnh, lệnh_chuẩn[vị_trí]))
            return văn_bản_bằng_nhau(văn_bản, tên_lệnh_bản_địa[vị_trí]);
    return 0;
}

static int thông_dịch_đầu_vào(int bộ_mô_tả_đầu_vào);

static int thông_dịch_tệp_lệnh(const char *tên_tệp)
{
    int bộ_mô_tả_tệp_2;
    int trạng_thái;
    if (độ_sâu_lồng_tệp_lệnh >= độ_lồng_tệp_lệnh_tối_đa) {
        ghi_văn_bản("source: nesting limit\n");
        return 0;
    }
    bộ_mô_tả_tệp_2 = Mở(tên_tệp, O_RDONLY);
    if (bộ_mô_tả_tệp_2 < 0) {
        báo_lỗi(tên_tệp);
        return 0;
    }
    độ_sâu_lồng_tệp_lệnh++;
    trạng_thái = thông_dịch_đầu_vào(bộ_mô_tả_tệp_2);
    độ_sâu_lồng_tệp_lệnh--;
    (void)Đóng(bộ_mô_tả_tệp_2);
    return trạng_thái;
}

static void hiện_đối_số(int số_đối_số, char **đối_số)
{
    int vị_trí;
    for (vị_trí = 1; vị_trí < số_đối_số; vị_trí++) {
        if (vị_trí != 1)
            ghi_văn_bản(" ");
        ghi_văn_bản(đối_số[vị_trí]);
    }
    ghi_văn_bản("\n");
}

static void hiện_thư_mục_hiện_tại(void)
{
    char đường_dẫn[128];
    if (getcwd(đường_dẫn, sizeof(đường_dẫn)) == (char *)0) {
        báo_lỗi("pwd");
        return;
    }
    ghi_văn_bản(đường_dẫn);
    ghi_văn_bản("\n");
}

static void hiện_nội_dung_tệp(const char *tên_tệp)
{
    char bộ_đệm_truyền_2[128];
    int bộ_mô_tả_tệp_2 = Mở(tên_tệp, O_RDONLY);
    ssize_t số_byte_đã_đọc;

    if (bộ_mô_tả_tệp_2 < 0) {
        báo_lỗi("cat");
        return;
    }
    while ((số_byte_đã_đọc = Đọc(bộ_mô_tả_tệp_2, bộ_đệm_truyền_2, sizeof(bộ_đệm_truyền_2))) > 0)
        (void)Ghi(STDOUT_FILENO, bộ_đệm_truyền_2, (size_t)số_byte_đã_đọc);
    if (số_byte_đã_đọc < 0)
        báo_lỗi("cat/read");
    (void)Đóng(bộ_mô_tả_tệp_2);
    ghi_văn_bản("\n");
}

static void hiện_thông_tin_tệp(const char *tên_tệp)
{
    struct stat trạng_thái;
    if (stat(tên_tệp, &trạng_thái) < 0) {
        báo_lỗi("stat");
        return;
    }
    ghi_văn_bản("size=");
    ghi_số_nguyên((int)trạng_thái.st_size);
    ghi_văn_bản(S_ISDIR(trạng_thái.st_mode) ? " type=directory\n" : " type=file\n");
}

static void hiện_mã_tiến_trình(void)
{
    ghi_văn_bản("pid=");
    ghi_số_nguyên((int)getpid());
    ghi_văn_bản(" ppid=");
    ghi_số_nguyên((int)getppid());
    ghi_văn_bản("\n");
}

static void hiện_thông_tin_hệ_thống(void)
{
    struct utsname thông_tin_hệ_thống;
    if (uname(&thông_tin_hệ_thống) < 0) {
        báo_lỗi("uname");
        return;
    }
    ghi_văn_bản(thông_tin_hệ_thống.sysname);
    ghi_văn_bản(" ");
    ghi_văn_bản(thông_tin_hệ_thống.release);
    ghi_văn_bản(" ");
    ghi_văn_bản(thông_tin_hệ_thống.machine);
    ghi_văn_bản("\n");
}

static void chạy_chương_trình(int số_đối_số, char **đối_số)
{
    pid_t mã_tiến_trình_con;
    int trạng_thái_kết_thúc_tiến_trình_con = 0;

    if (số_đối_số < 2) {
        ghi_văn_bản("usage: run FILE [ARGS...]\n");
        return;
    }
    mã_tiến_trình_con = fork();
    if (mã_tiến_trình_con < 0) {
        báo_lỗi("fork");
        return;
    }
    if (mã_tiến_trình_con == 0) {
        execve(đối_số[1], &đối_số[1], (char *const *)0);
        báo_lỗi("execve");
        _exit(127);
    }
    if (waitpid(mã_tiến_trình_con, &trạng_thái_kết_thúc_tiến_trình_con, 0) < 0) {
        báo_lỗi("waitpid");
        return;
    }
    ghi_văn_bản("exit-status=");
    ghi_số_nguyên(WEXITSTATUS(trạng_thái_kết_thúc_tiến_trình_con));
    ghi_văn_bản("\n");
}

static void thử_gói_dữ_liệu_vòng_về(const char *thông_điệp)
{
    struct sockaddr_in địa_chỉ_nhận = {0};
    struct sockaddr_in địa_chỉ_bên_gửi = {0};
    socklen_t độ_dài_địa_chỉ_bên_gửi = sizeof(địa_chỉ_bên_gửi);
    char dữ_liệu_đã_nhận[96];
    size_t độ_dài_thông_điệp_theo_byte = độ_dài_văn_bản_theo_byte(thông_điệp);
    int đầu_giao_tiếp_nhận = -1;
    int đầu_giao_tiếp_gửi = -1;
    ssize_t số_byte_đã_nhận;

    if (độ_dài_thông_điệp_theo_byte >= sizeof(dữ_liệu_đã_nhận)) {
        ghi_văn_bản("udp: message exceeds 95 bytes\n");
        return;
    }
    đầu_giao_tiếp_nhận = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    đầu_giao_tiếp_gửi = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (đầu_giao_tiếp_nhận < 0 || đầu_giao_tiếp_gửi < 0) {
        báo_lỗi("socket");
        goto đóng_các_đầu_giao_tiếp;
    }
    địa_chỉ_nhận.sin_family = AF_INET;
    địa_chỉ_nhận.sin_port = htons(40404);
    địa_chỉ_nhận.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(đầu_giao_tiếp_nhận, (const struct sockaddr *)&địa_chỉ_nhận, sizeof(địa_chỉ_nhận)) < 0) {
        báo_lỗi("bind");
        goto đóng_các_đầu_giao_tiếp;
    }
    if (connect(đầu_giao_tiếp_gửi, (const struct sockaddr *)&địa_chỉ_nhận, sizeof(địa_chỉ_nhận)) < 0) {
        báo_lỗi("connect");
        goto đóng_các_đầu_giao_tiếp;
    }
    if (send(đầu_giao_tiếp_gửi, thông_điệp, độ_dài_thông_điệp_theo_byte, 0) != (ssize_t)độ_dài_thông_điệp_theo_byte) {
        báo_lỗi("send");
        goto đóng_các_đầu_giao_tiếp;
    }
    số_byte_đã_nhận = recvfrom(đầu_giao_tiếp_nhận, dữ_liệu_đã_nhận, sizeof(dữ_liệu_đã_nhận) - 1U, 0,
                         (struct sockaddr *)&địa_chỉ_bên_gửi, &độ_dài_địa_chỉ_bên_gửi);
    if (số_byte_đã_nhận < 0) {
        báo_lỗi("recvfrom");
        goto đóng_các_đầu_giao_tiếp;
    }
    dữ_liệu_đã_nhận[số_byte_đã_nhận] = '\0';
    ghi_văn_bản("udp-received: ");
    ghi_văn_bản(dữ_liệu_đã_nhận);
    ghi_văn_bản("\n");

đóng_các_đầu_giao_tiếp:
    if (đầu_giao_tiếp_gửi >= 0)
        (void)Đóng(đầu_giao_tiếp_gửi);
    if (đầu_giao_tiếp_nhận >= 0)
        (void)Đóng(đầu_giao_tiếp_nhận);
}

static int thông_dịch_đầu_vào(int bộ_mô_tả_đầu_vào)
{
    char dòng_nhập[sức_chứa_dòng_nhập];
    char *đối_số[số_đối_số_tối_đa];
    struct luồng_đầu_vào đầu_vào = {0};
    đầu_vào.bộ_mô_tả_đầu_vào = bộ_mô_tả_đầu_vào;

    for (;;) {
        int số_đối_số;
        int trạng_thái;
        if (bộ_mô_tả_đầu_vào == STDIN_FILENO)
            ghi_văn_bản("worldos$ ");
        trạng_thái = đọc_dòng_nhập(&đầu_vào, dòng_nhập, sizeof(dòng_nhập));
        if (trạng_thái == -1)
            return 0;
        if (trạng_thái == -2) {
            ghi_văn_bản("input rejected: overlong or binary line\n");
            continue;
        }
        số_đối_số = tách_đối_số(dòng_nhập, đối_số);
        if (số_đối_số < 0) {
            ghi_văn_bản("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (số_đối_số == 0)
            continue;
        if (lệnh_trùng_khớp(đối_số[0], "help"))
            hiện_trợ_giúp();
        else if (lệnh_trùng_khớp(đối_số[0], "echo"))
            hiện_đối_số(số_đối_số, đối_số);
        else if (lệnh_trùng_khớp(đối_số[0], "pwd"))
            hiện_thư_mục_hiện_tại();
        else if (lệnh_trùng_khớp(đối_số[0], "cd")) {
            if (số_đối_số < 2)
                ghi_văn_bản("usage: cd PATH\n");
            else if (chdir(đối_số[1]) < 0)
                báo_lỗi("cd");
        } else if (lệnh_trùng_khớp(đối_số[0], "cat")) {
            if (số_đối_số < 2)
                ghi_văn_bản("usage: cat FILE\n");
            else
                hiện_nội_dung_tệp(đối_số[1]);
        } else if (lệnh_trùng_khớp(đối_số[0], "stat")) {
            if (số_đối_số < 2)
                ghi_văn_bản("usage: stat FILE\n");
            else
                hiện_thông_tin_tệp(đối_số[1]);
        } else if (lệnh_trùng_khớp(đối_số[0], "pid"))
            hiện_mã_tiến_trình();
        else if (lệnh_trùng_khớp(đối_số[0], "uname"))
            hiện_thông_tin_hệ_thống();
        else if (lệnh_trùng_khớp(đối_số[0], "run"))
            chạy_chương_trình(số_đối_số, đối_số);
        else if (lệnh_trùng_khớp(đối_số[0], "udp"))
            thử_gói_dữ_liệu_vòng_về(số_đối_số >= 2 ? đối_số[1] : "ping");
        else if (lệnh_trùng_khớp(đối_số[0], "source")) {
            if (số_đối_số < 2)
                ghi_văn_bản("usage: source FILE\n");
            else if (thông_dịch_tệp_lệnh(đối_số[1]))
                return 1;
        } else if (lệnh_trùng_khớp(đối_số[0], "exit"))
            return 1;
        else
            ghi_văn_bản("unknown command; type help\n");
    }
}

int main(void)
{
    ghi_văn_bản("WORLDOS-SHELL:READY\n");
    (void)thông_dịch_đầu_vào(STDIN_FILENO);
    ghi_văn_bản("WORLDOS-SHELL:EXIT\n");
    return 0;
}
