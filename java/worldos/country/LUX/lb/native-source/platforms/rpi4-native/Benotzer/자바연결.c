#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fichier/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "Bëndel.h"
typedef uintptr_t Computer_Word;
static int Kategorie_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static Computer_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned Element_COUNT, Computer_Word 첫째값, Computer_Word SECOND_VALUE, Computer_Word Zeechecode) {
    return 사용자호출(Element_COUNT, 첫째값, SECOND_VALUE, Zeechecode, 0, 0, 0);
}
static void 바이트들(const char *Daten_positionéieren, size_t Element_COUNT) { 호출(1, 1, (Computer_Word)Daten_positionéieren, Element_COUNT); }
static void Zeechen(unsigned Zeechecode) {
    unsigned char Daten[4]; unsigned Element_COUNT = 0;
    if (Zeechecode < 128) Daten[Element_COUNT++] = Zeechecode;
    else if (Zeechecode < 2048) { Daten[Element_COUNT++] = 0xc0 | (Zeechecode >> 6); Daten[Element_COUNT++] = 0x80 | (Zeechecode & 63); }
    else if (Zeechecode < 65536) { Daten[Element_COUNT++] = 0xe0 | (Zeechecode >> 12); Daten[Element_COUNT++] = 0x80 | ((Zeechecode >> 6) & 63); Daten[Element_COUNT++] = 0x80 | (Zeechecode & 63); }
    else { Daten[Element_COUNT++] = 0xf0 | (Zeechecode >> 18); Daten[Element_COUNT++] = 0x80 | ((Zeechecode >> 12) & 63); Daten[Element_COUNT++] = 0x80 | ((Zeechecode >> 6) & 63); Daten[Element_COUNT++] = 0x80 | (Zeechecode & 63); }
    바이트들((const char *)Daten, Element_COUNT);
}
Computer_Word Tool_Zeechen(Computer_Word VALUE) {
    unsigned Zeechecode = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (Zeechecode >= 0xdc00 && Zeechecode <= 0xdfff) { Zeechen(0x10000 + ((높은부분 - 0xd800) << 10) + Zeechecode - 0xdc00); return 1; }
        Zeechen(0xfffd);
    }
    if (Zeechecode >= 0xd800 && Zeechecode <= 0xdbff) 대기중짝글자 = Zeechecode;
    else Zeechen(Zeechecode > 0x10ffff || (Zeechecode >= 0xdc00 && Zeechecode <= 0xdfff) ? 0xfffd : Zeechecode);
    return 1;
}
Computer_Word 도구출력(Computer_Word VALUE) {
    const Computer_Word *Zeechefolleg_Daten = (const Computer_Word *)VALUE;
    for (Computer_Word 순번 = 0; 순번 < Zeechefolleg_Daten[0]; 순번++) Tool_Zeechen(Zeechefolleg_Daten[순번 + 1]);
    return Zeechefolleg_Daten[0];
}
static int Wee(Computer_Word Objet_Referenzen, char Mooss_Daten[512]) {
    const Computer_Word *첫째값 = (const Computer_Word *)Objet_Referenzen;
    unsigned 사용량 = 0;
    for (Computer_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned Zeechecode = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] Method_MODE 경로와 호환한다.
        if (Zeechecode >= 0xd800 && Zeechecode <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; Zeechecode = 0x10000 + ((Zeechecode - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (Zeechecode >= 0xd800 && Zeechecode <= 0xdfff) return -22;
        unsigned Element_COUNT = Zeechecode < 128 ? 1 : Zeechecode < 2048 ? 2 : Zeechecode < 65536 ? 3 : 4;
        if (사용량 + Element_COUNT > 511) return -36;
        if (Element_COUNT == 1) Mooss_Daten[사용량++] = Zeechecode;
        else {
            Mooss_Daten[사용량++] = (Element_COUNT == 2 ? 0xc0 : Element_COUNT == 3 ? 0xe0 : 0xf0) | (Zeechecode >> (6 * (Element_COUNT - 1)));
            for (unsigned 안쪽순번 = Element_COUNT - 1; 안쪽순번; 안쪽순번--) Mooss_Daten[사용량++] = 0x80 | ((Zeechecode >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    Mooss_Daten[사용량] = 0; return 사용량 ? 0 : -22;
}
Computer_Word Tool_ariichten(Computer_Word Numm, Computer_Word 설정비트) {
    char Daten_positionéieren[512]; int Feeler = Wee(Numm, Daten_positionéieren);
    return (uint32_t)(Feeler ? Feeler : 호출(3, (Computer_Word)Daten_positionéieren, 설정비트, 0));
}
Computer_Word Tool_Clôture(Computer_Word Fichier_Handle) { return (uint32_t)호출(4, Fichier_Handle, 0, 0); }
Computer_Word 도구바이트읽기(Computer_Word Fichier_Handle) {
    unsigned char SECOND_VALUE; intptr_t Element_COUNT = 호출(2, Fichier_Handle, (Computer_Word)&SECOND_VALUE, 1);
    return (uint32_t)(Element_COUNT == 1 ? SECOND_VALUE : Element_COUNT == 0 ? 256 : Element_COUNT);
}
Computer_Word Tool_schreiwen_Byte(Computer_Word Fichier_Handle, Computer_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Fichier_Handle, (Computer_Word)&SECOND_VALUE, 1);
}
Computer_Word 도구읽기(Computer_Word Numm, Computer_Word Zil_Daten_Adress) {
    if (꾸러미사용중) {
        char Daten_positionéieren[512]; int Feeler = Wee(Numm, Daten_positionéieren); if (Feeler) return (uint32_t)Feeler;
        unsigned Element_COUNT = 0; while (Daten_positionéieren[Element_COUNT]) Element_COUNT++;
        if (Element_COUNT >= 6) for (unsigned 순번 = 0; 순번 < Element_COUNT - 6; 순번++) if (Daten_positionéieren[순번] == '.') Daten_positionéieren[순번] = '/';
        unsigned char 바이트들[16384]; Computer_Word *Zil_VALUE_positionéieren = (Computer_Word *)Zil_Daten_Adress;
        int RECEIVED_COUNT = 꾸러미읽기(Daten_positionéieren, 바이트들, Zil_VALUE_positionéieren[0] < sizeof(바이트들) ? Zil_VALUE_positionéieren[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) Zil_VALUE_positionéieren[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Fichier_Handle = 꾸러미사용중 ? -2 : (int32_t)Tool_ariichten(Numm, 0);
    if (Fichier_Handle < 0) {
        char Daten_positionéieren[512]; int Feeler = Wee(Numm, Daten_positionéieren); if (Feeler) return (uint32_t)Feeler;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Weider_OFFSET = 자바클래스들[순번].Numm; unsigned 안쪽순번 = 0;
            while (Daten_positionéieren[안쪽순번] && Daten_positionéieren[안쪽순번] == Weider_OFFSET[안쪽순번]) 안쪽순번++;
            if (Daten_positionéieren[안쪽순번] || Weider_OFFSET[안쪽순번]) continue;
            Computer_Word *Zil_VALUE_positionéieren = (Computer_Word *)Zil_Daten_Adress;
            if (Zil_VALUE_positionéieren[0] < 자바클래스들[순번].d_Gréisst_veränneren) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].d_Gréisst_veränneren; 안쪽순번++) Zil_VALUE_positionéieren[안쪽순번 + 1] = 자바클래스들[순번].Daten[안쪽순번];
            return 자바클래스들[순번].d_Gréisst_veränneren;
        }
        return (uint32_t)Fichier_Handle;
    }
    Computer_Word *첫째값 = (Computer_Word *)Zil_Daten_Adress;
    intptr_t d_Gréisst_veränneren = 호출(9, Fichier_Handle, 0, 0), 완료량 = 0;
    if (d_Gréisst_veränneren < 0 || (Computer_Word)d_Gréisst_veränneren > 첫째값[0]) { Tool_Clôture(Fichier_Handle); return (uint32_t)(d_Gréisst_veränneren < 0 ? d_Gréisst_veränneren : -27); }
    unsigned char Daten_blockéieren[256];
    while (완료량 < d_Gréisst_veränneren) {
        intptr_t Element_COUNT = 호출(2, Fichier_Handle, (Computer_Word)Daten_blockéieren, d_Gréisst_veränneren - 완료량 < 256 ? d_Gréisst_veränneren - 완료량 : 256);
        if (Element_COUNT <= 0) { Tool_Clôture(Fichier_Handle); return (uint32_t)(Element_COUNT ? Element_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < Element_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = Daten_blockéieren[순번];
        완료량 += Element_COUNT;
    }
    Tool_Clôture(Fichier_Handle); return 완료량;
}
Computer_Word Tool_schreiwen(Computer_Word Numm, Computer_Word 원본자료, Computer_Word Agab_COUNT) {
    const Computer_Word *첫째값 = (const Computer_Word *)원본자료;
    if (Agab_COUNT > 첫째값[0] || Agab_COUNT > 16384) return (uint32_t)-27;
    int Fichier_Handle = (int32_t)Tool_ariichten(Numm, 577); if (Fichier_Handle < 0) return (uint32_t)Fichier_Handle;
    unsigned char Daten_blockéieren[256]; Computer_Word 완료량 = 0;
    while (완료량 < Agab_COUNT) {
        Computer_Word Element_COUNT = Agab_COUNT - 완료량 < 256 ? Agab_COUNT - 완료량 : 256;
        for (Computer_Word 순번 = 0; 순번 < Element_COUNT; 순번++) Daten_blockéieren[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t Mooss = 호출(1, Fichier_Handle, (Computer_Word)Daten_blockéieren, Element_COUNT);
        if (Mooss <= 0) { Tool_Clôture(Fichier_Handle); return (uint32_t)(Mooss ? Mooss : -5); }
        완료량 += Mooss;
    }
    Tool_Clôture(Fichier_Handle); return Agab_COUNT;
}
Computer_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
Computer_Word Tool_Argument(Computer_Word LOOKUP_INDEX) {
    static const Computer_Word eidel_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (Computer_Word)eidel_VALUE;
    unsigned char 입력결과[256]; intptr_t Element_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *Daten_positionéieren = 꾸러미진입클래스(); Element_COUNT = 0; while (Daten_positionéieren[Element_COUNT] && Element_COUNT < 255) { 입력결과[Element_COUNT] = Daten_positionéieren[Element_COUNT]; Element_COUNT++; } }
    else Element_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (Computer_Word)입력결과, sizeof(입력결과));
    if (Element_COUNT < 0) return (Computer_Word)eidel_VALUE;
    Computer_Word *Mooss_Daten = 전달인수[LOOKUP_INDEX]; unsigned Agab_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < Element_COUNT;) {
        unsigned Zeechecode = 입력결과[순번++], 더있음 = Zeechecode < 128 ? 0 : Zeechecode >= 0xc2 && Zeechecode < 0xe0 ? 1 : Zeechecode < 0xf0 && Zeechecode >= 0xe0 ? 2 : Zeechecode >= 0xf0 && Zeechecode <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > Element_COUNT) { Mooss_Daten[++Agab_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) Zeechecode &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { Zeechecode = (Zeechecode << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || Zeechecode < 최소값 || Zeechecode > 0x10ffff || (Zeechecode >= 0xd800 && Zeechecode <= 0xdfff)) Zeechecode = 0xfffd;
        if (Zeechecode >= 65536) { Zeechecode -= 65536; Mooss_Daten[++Agab_COUNT] = 0xd800 | (Zeechecode >> 10); Mooss_Daten[++Agab_COUNT] = 0xdc00 | (Zeechecode & 1023); }
        else Mooss_Daten[++Agab_COUNT] = Zeechecode;
    }
    Mooss_Daten[0] = Agab_COUNT; return (Computer_Word)Mooss_Daten;
}
Computer_Word 도구분류(void) { return Kategorie_VALUE; }
void 커널중단(const char *알림문) {
    const char *Daten_positionéieren = 알림문; while (*Daten_positionéieren) Daten_positionéieren++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, Daten_positionéieren - 알림문); Zeechen(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_Benotzer_App(int Method_MODE) {
    Kategorie_VALUE = Method_MODE;
    unsigned char 첫항목[256]; intptr_t Element_COUNT = 호출(15, 0, (Computer_Word)첫항목, sizeof(첫항목));
    if (Method_MODE == 2 || (Method_MODE == 1 && Element_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = Method_MODE == 2 ? 0 : 1;
        char Fichier_Agab_Numm[256]; intptr_t Längt_Daten = 호출(15, 꾸러미인수이동, (Computer_Word)Fichier_Agab_Numm, sizeof(Fichier_Agab_Numm));
        if (Längt_Daten <= 0 || 꾸러미열기(Fichier_Agab_Numm) < 0) {
            static const char Feeler[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Feeler, sizeof(Feeler) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int Mooss = 자바진입();
    if (대기중짝글자) Zeechen(0xfffd);
    return Mooss;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Famill, 접속번호; uint32_t Adress; unsigned char 영값[8]; };
static struct 자바주소 UDP_Adress(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
Computer_Word Tool_UDP_ariichten(Computer_Word 접속번호) {
    intptr_t Fichier_Handle = 호출(32, 2, 2, 17); if (Fichier_Handle < 0) return (uint32_t)Fichier_Handle;
    struct 자바주소 첫째값 = UDP_Adress(접속번호);
    첫째값.Adress = 0;
    intptr_t Status_VALUE = 호출(33, Fichier_Handle, (Computer_Word)&첫째값, sizeof(첫째값));
    if (Status_VALUE < 0) { Tool_Clôture(Fichier_Handle); return (uint32_t)Status_VALUE; }
    return Fichier_Handle;
}
Computer_Word Tool_UDP_mailen(Computer_Word Fichier_Handle, Computer_Word 접속번호, Computer_Word ARRAY_VALUE, Computer_Word Längt_VALUE) {
    const Computer_Word *원본주소 = (const Computer_Word *)ARRAY_VALUE; unsigned char Daten[512];
    if (Längt_VALUE > 512 || Längt_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (Computer_Word 순번 = 0; 순번 < Längt_VALUE; 순번++) Daten[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_Adress(접속번호);
    return (uint32_t)사용자호출(34, Fichier_Handle, (Computer_Word)Daten, Längt_VALUE, 0, (Computer_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t Element_COUNT) { return (Element_COUNT>>24)|((Element_COUNT>>8)&0xff00)|((Element_COUNT<<8)&0xff0000)|(Element_COUNT<<24); }
Computer_Word Tool_UDP_mailen_Adress(Computer_Word Fichier_Handle, Computer_Word Adress, Computer_Word 접속번호, Computer_Word ARRAY_VALUE, Computer_Word Längt_VALUE) {
    const Computer_Word *원본주소 = (const Computer_Word *)ARRAY_VALUE; unsigned char Daten[512];
    if (Längt_VALUE > 512 || Längt_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (Computer_Word 순번 = 0; 순번 < Längt_VALUE; 순번++) Daten[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_Adress(접속번호); 첫째값.Adress = 바이트순서뒤집기(Adress);
    return (uint32_t)사용자호출(34, Fichier_Handle, (Computer_Word)Daten, Längt_VALUE, 0, (Computer_Word)&첫째값, sizeof(첫째값));
}
Computer_Word Tool_Verbannen(Computer_Word Fichier_Handle, Computer_Word Adress, Computer_Word 접속번호) {
    struct 자바주소 첫째값 = UDP_Adress(접속번호); 첫째값.Adress = 바이트순서뒤집기(Adress);
    uint32_t Laf = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t Mooss = 호출(37, Fichier_Handle, (Computer_Word)&첫째값, sizeof(첫째값));
        if (Mooss != -115) return (uint32_t)Mooss;
        if ((uint32_t)(호출(7, 0, 0, 0) - Laf) >= 1000) return (uint32_t)-110;
    }
}
Computer_Word 도구전문받기(Computer_Word Fichier_Handle, Computer_Word ARRAY_VALUE, Computer_Word 수용량) {
    Computer_Word *Zil_Adress_08bbd577 = (Computer_Word *)ARRAY_VALUE; unsigned char Daten[512];
    if (수용량 > 512 || Zil_Adress_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned Längt_Daten = sizeof(첫째값);
    intptr_t Element_COUNT = 사용자호출(35, Fichier_Handle, (Computer_Word)Daten, 수용량, 0, (Computer_Word)&첫째값, (Computer_Word)&Längt_Daten);
    if (Element_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < Element_COUNT; 순번++) Zil_Adress_08bbd577[순번 + 1] = Daten[순번]; Zil_Adress_08bbd577[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; Zil_Adress_08bbd577[514] = 바이트순서뒤집기(첫째값.Adress); }
    return (uint32_t)Element_COUNT;
}
Computer_Word Tool_UDP_Port(Computer_Word Fichier_Handle) {
    struct 자바주소 첫째값; unsigned Längt_Daten = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Fichier_Handle, (Computer_Word)&첫째값, (Computer_Word)&Längt_Daten);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
Computer_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
Computer_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
Computer_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
Computer_Word Tool_Grafiken_Waart(void) { return (uint32_t)화면키기다리기(); }
Computer_Word 도구사각형(Computer_Word X_Koordinat, Computer_Word 세로좌표, Computer_Word 너비값, Computer_Word 높이값, Computer_Word 색상) {
    return (uint32_t)사용자호출(13, X_Koordinat, 세로좌표, 색상, 너비값, 높이값, 0);
}

Computer_Word Tool_Stream(Computer_Word Aktioun,Computer_Word Fichier_Handle,Computer_Word VALUE){
    if(Aktioun==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_Adress(VALUE);
    if(Aktioun==1){첫째값.Adress=0;intptr_t 반환값=호출(33,Fichier_Handle,(Computer_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Fichier_Handle,4,0));}
    if(Aktioun==2)return (uint32_t)호출(37,Fichier_Handle,(Computer_Word)&첫째값,sizeof(첫째값));
    if(Aktioun==3)return (uint32_t)호출(39,Fichier_Handle,0,0);
    if(Aktioun==4)return Tool_UDP_Port(Fichier_Handle);
    if(Aktioun==5)return (uint32_t)호출(40,Fichier_Handle,0,0);
    return (uint32_t)-22;
}
Computer_Word Tool_GUI(Computer_Word Aktioun,Computer_Word Identifikateur_VALUE,Computer_Word 첫째값,Computer_Word SECOND_VALUE,Computer_Word Zeechecode,Computer_Word Zil_Daten){return (uint32_t)사용자호출(20,Aktioun,Identifikateur_VALUE,첫째값,SECOND_VALUE,Zeechecode,Zil_Daten);}
Computer_Word Tool_GUI_SMS(Computer_Word Identifikateur_VALUE,Computer_Word ARRAY_VALUE,Computer_Word Element_COUNT){
    const Computer_Word *원본주소=(const Computer_Word *)ARRAY_VALUE;uint32_t Daten[127];unsigned Agab_COUNT=0;
    if(Element_COUNT>원본주소[0])return (uint32_t)-22;
    for(Computer_Word 순번=0;순번<Element_COUNT;순번++){unsigned Zeechen_Codéierung=원본주소[순번+1];if(Zeechen_Codéierung>=0xd800&&Zeechen_Codéierung<=0xdbff&&순번+1<Element_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;Zeechen_Codéierung=0x10000+((Zeechen_Codéierung-0xd800)<<10)+낮은값-0xdc00;}if(Agab_COUNT==127)return (uint32_t)-22;Daten[Agab_COUNT++]=Zeechen_Codéierung;}
    return (uint32_t)사용자호출(21,Identifikateur_VALUE,(Computer_Word)Daten,Agab_COUNT,0,0,0);
}
