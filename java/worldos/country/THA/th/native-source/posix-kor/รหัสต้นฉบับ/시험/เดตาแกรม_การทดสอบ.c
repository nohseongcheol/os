#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ยืนยัน(โรค) do { if (!(โรค)) { puts("POSIX UDP CHECK FAILED: " #โรค); return 1; } } while (0)
int main(int 인수개수, char **อาร์กิวเมนต์_รายการ) {
    ยืนยัน(인수개수 == 2);
    int หมายเลขพอร์ต = 0;
    for (int 칸 = 0; อาร์กิวเมนต์_รายการ[1][칸]; 칸++) {
        ยืนยัน(อาร์กิวเมนต์_รายการ[1][칸] >= '0' && อาร์กิวเมนต์_รายการ[1][칸] <= '9');
        หมายเลขพอร์ต = หมายเลขพอร์ต * 10 + อาร์กิวเมนต์_รายการ[1][칸] - '0';
        ยืนยัน(หมายเลขพอร์ต <= 65535);
    }
    int ปลายทาง_ค่า = เปิด_ปลายทาง(AF_INET, SOCK_DGRAM, 0);
    ยืนยัน(ปลายทาง_ค่า == 3);
    struct sockaddr_in ท้องถิ่น_ขอบเขต = {0}, ชั้น_ค่า = {0}, 받은주소 = {0};
    ท้องถิ่น_ขอบเขต.sin_family = AF_INET;
    socklen_t 길이 = sizeof ท้องถิ่น_ขอบเขต;
    ยืนยัน(통신주소읽기(ปลายทาง_ค่า, (struct sockaddr *)&ท้องถิ่น_ขอบเขต, &길이) == 0 && ท้องถิ่น_ขอบเขต.sin_port == 0);
    ยืนยัน(ผูก_อีเมล(ปลายทาง_ค่า, (struct sockaddr *)&ท้องถิ่น_ขอบเขต, sizeof ท้องถิ่น_ขอบเขต) == 0);
    ยืนยัน(통신주소읽기(ปลายทาง_ค่า, (struct sockaddr *)&ท้องถิ่น_ขอบเขต, &길이) == 0 && ntohs(ท้องถิ่น_ขอบเขต.sin_port) >= 49152);
    ยืนยัน(ผูก_อีเมล(ปลายทาง_ค่า, (struct sockaddr *)&ท้องถิ่น_ขอบเขต, sizeof ท้องถิ่น_ขอบเขต) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ยืนยัน(bind(둘째, (struct sockaddr *)&ท้องถิ่น_ขอบเขต, sizeof ท้องถิ่น_ขอบเขต) == -1 && errno == EADDRINUSE);
    ยืนยัน(close(둘째) == 0);
    둘째 = dup(ปลายทาง_ค่า);
    ยืนยัน(close(ปลายทาง_ค่า) == 0); ปลายทาง_ค่า = 둘째;
    ชั้น_ค่า.sin_family = AF_INET; ชั้น_ค่า.sin_port = 망차례짧은수(หมายเลขพอร์ต);
    ยืนยัน(แยกวิเคราะห์_รหัสเครือข่าย(AF_INET, "10.0.2.2", &ชั้น_ค่า.sin_addr) == 1);
    struct timeval รอเดี๋ยว_ค่า = {0, 200000};
    ยืนยัน(เปลี่ยนแปลง_เครือข่าย_การตั้งค่า(ปลายทาง_ค่า, SOL_SOCKET, SO_RCVTIMEO, &รอเดี๋ยว_ค่า, sizeof รอเดี๋ยว_ค่า) == 0);
    char ข้อมูล[32];
    ยืนยัน(รับ_เดตาแกรม_ข้อมูล(ปลายทาง_ค่า, ข้อมูล, sizeof ข้อมูล, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ยืนยัน(ส่ง_เดตาแกรม_ข้อมูล(ปลายทาง_ค่า, "posix-udp", 9, 0, (struct sockaddr *)&ชั้น_ค่า, sizeof ชั้น_ค่า) == 9);
    길이 = sizeof 받은주소;
    ยืนยัน(recvfrom(ปลายทาง_ค่า, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ยืนยัน(รับ_เดตาแกรม_ข้อมูล(ปลายทาง_ค่า, ข้อมูล, sizeof ข้อมูล, 0, (struct sockaddr *)&받은주소, &길이) == 9);
    ยืนยัน(memcmp(ข้อมูล, "posix-udp", 9) == 0 && 길이 == 16);
    ยืนยัน(받은주소.sin_port == ชั้น_ค่า.sin_port && 받은주소.sin_addr.s_addr == ชั้น_ค่า.sin_addr.s_addr);
    ยืนยัน(sendto(ปลายทาง_ค่า, "truncate", 8, 0, (struct sockaddr *)&ชั้น_ค่า, sizeof ชั้น_ค่า) == 8);
    ยืนยัน(recvfrom(ปลายทาง_ค่า, ข้อมูล, 3, 0, NULL, NULL) == 3 && memcmp(ข้อมูล, "tru", 3) == 0);
    ยืนยัน(recvfrom(ปลายทาง_ค่า, ข้อมูล, sizeof ข้อมูล, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ยืนยัน(sendto(ปลายทาง_ค่า, NULL, 0, 0, (struct sockaddr *)&ชั้น_ค่า, sizeof ชั้น_ค่า) == 0);
    ยืนยัน(recvfrom(ปลายทาง_ค่า, NULL, 0, 0, NULL, NULL) == 0);
    ยืนยัน(recvfrom(ปลายทาง_ค่า, ข้อมูล, sizeof ข้อมูล, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ยืนยัน(close(ปลายทาง_ค่า) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
