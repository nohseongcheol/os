#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define 확인(ເງື່ອນໄຂ) do { if (!(ເງື່ອນໄຂ)) { puts("POSIX UDP CHECK FAILED: " #ເງື່ອນໄຂ); return 1; } } while (0)
int main(int 인수개수, char **ຂໍ້ພິສູດ_ລາຍຊື່) {
    확인(인수개수 == 2);
    int ຫມາຍເລກພອດ = 0;
    for (int ຊ່ອງ_ເຂົ້າໃນ = 0; ຂໍ້ພິສູດ_ລາຍຊື່[1][ຊ່ອງ_ເຂົ້າໃນ]; ຊ່ອງ_ເຂົ້າໃນ++) {
        확인(ຂໍ້ພິສູດ_ລາຍຊື່[1][ຊ່ອງ_ເຂົ້າໃນ] >= '0' && ຂໍ້ພິສູດ_ລາຍຊື່[1][ຊ່ອງ_ເຂົ້າໃນ] <= '9');
        ຫມາຍເລກພອດ = ຫມາຍເລກພອດ * 10 + ຂໍ້ພິສູດ_ລາຍຊື່[1][ຊ່ອງ_ເຂົ້າໃນ] - '0';
        확인(ຫມາຍເລກພອດ <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    확인(종단점 == 3);
    struct sockaddr_in ໃນເຄື່ອງ_ຂອບ_ເຂດ = {0}, ລຸ້ນດຽວກັນ_ຄ່າ = {0}, 받은주소 = {0};
    ໃນເຄື່ອງ_ຂອບ_ເຂດ.sin_family = AF_INET;
    socklen_t ຄວາມຍາວ_ຄ່າ = sizeof ໃນເຄື່ອງ_ຂອບ_ເຂດ;
    확인(통신주소읽기(종단점, (struct sockaddr *)&ໃນເຄື່ອງ_ຂອບ_ເຂດ, &ຄວາມຍາວ_ຄ່າ) == 0 && ໃນເຄື່ອງ_ຂອບ_ເຂດ.sin_port == 0);
    확인(ຜູກ_ມັດ_ອີເມວ(종단점, (struct sockaddr *)&ໃນເຄື່ອງ_ຂອບ_ເຂດ, sizeof ໃນເຄື່ອງ_ຂອບ_ເຂດ) == 0);
    확인(통신주소읽기(종단점, (struct sockaddr *)&ໃນເຄື່ອງ_ຂອບ_ເຂດ, &ຄວາມຍາວ_ຄ່າ) == 0 && ntohs(ໃນເຄື່ອງ_ຂອບ_ເຂດ.sin_port) >= 49152);
    확인(ຜູກ_ມັດ_ອີເມວ(종단점, (struct sockaddr *)&ໃນເຄື່ອງ_ຂອບ_ເຂດ, sizeof ໃນເຄື່ອງ_ຂອບ_ເຂດ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    확인(bind(둘째, (struct sockaddr *)&ໃນເຄື່ອງ_ຂອບ_ເຂດ, sizeof ໃນເຄື່ອງ_ຂອບ_ເຂດ) == -1 && errno == EADDRINUSE);
    확인(close(둘째) == 0);
    둘째 = dup(종단점);
    확인(close(종단점) == 0); 종단점 = 둘째;
    ລຸ້ນດຽວກັນ_ຄ່າ.sin_family = AF_INET; ລຸ້ນດຽວກັນ_ຄ່າ.sin_port = 망차례짧은수(ຫມາຍເລກພອດ);
    확인(ການແຈກຄໍາສັບ_ເຄືອຂ່າຍ_ອີເມວ(AF_INET, "10.0.2.2", &ລຸ້ນດຽວກັນ_ຄ່າ.sin_addr) == 1);
    struct timeval ລໍຖ້າ_ຄ່າ = {0, 200000};
    확인(ປ່ຽນ_ແປງ_ເຄືອຂ່າຍ_ການຕັ້ງຄ່າ(종단점, SOL_SOCKET, SO_RCVTIMEO, &ລໍຖ້າ_ຄ່າ, sizeof ລໍຖ້າ_ຄ່າ) == 0);
    char ຂໍ້ມູນ[32];
    확인(자료전문받기(종단점, ຂໍ້ມູນ, sizeof ຂໍ້ມູນ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ລຸ້ນດຽວກັນ_ຄ່າ, sizeof ລຸ້ນດຽວກັນ_ຄ່າ) == 9);
    ຄວາມຍາວ_ຄ່າ = sizeof 받은주소;
    확인(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    확인(자료전문받기(종단점, ຂໍ້ມູນ, sizeof ຂໍ້ມູນ, 0, (struct sockaddr *)&받은주소, &ຄວາມຍາວ_ຄ່າ) == 9);
    확인(memcmp(ຂໍ້ມູນ, "posix-udp", 9) == 0 && ຄວາມຍາວ_ຄ່າ == 16);
    확인(받은주소.sin_port == ລຸ້ນດຽວກັນ_ຄ່າ.sin_port && 받은주소.sin_addr.s_addr == ລຸ້ນດຽວກັນ_ຄ່າ.sin_addr.s_addr);
    확인(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ລຸ້ນດຽວກັນ_ຄ່າ, sizeof ລຸ້ນດຽວກັນ_ຄ່າ) == 8);
    확인(recvfrom(종단점, ຂໍ້ມູນ, 3, 0, NULL, NULL) == 3 && memcmp(ຂໍ້ມູນ, "tru", 3) == 0);
    확인(recvfrom(종단점, ຂໍ້ມູນ, sizeof ຂໍ້ມູນ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ລຸ້ນດຽວກັນ_ຄ່າ, sizeof ລຸ້ນດຽວກັນ_ຄ່າ) == 0);
    확인(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    확인(recvfrom(종단점, ຂໍ້ມູນ, sizeof ຂໍ້ມູນ, 0, NULL, NULL) == -1 && errno == EAGAIN);
    확인(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
