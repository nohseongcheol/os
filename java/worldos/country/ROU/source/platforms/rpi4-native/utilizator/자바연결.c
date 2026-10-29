#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fișier/Rezultat/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "set.h"
typedef uintptr_t mașină_Word;
static int zonă_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static mașină_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned element_COUNT, mașină_Word 첫째값, mașină_Word SECOND_VALUE, mașină_Word cod_caracter) {
    return 사용자호출(element_COUNT, 첫째값, SECOND_VALUE, cod_caracter, 0, 0, 0);
}
static void 바이트들(const char *date_poziție, size_t element_COUNT) { 호출(1, 1, (mașină_Word)date_poziție, element_COUNT); }
static void caracter(unsigned cod_caracter) {
    unsigned char date[4]; unsigned element_COUNT = 0;
    if (cod_caracter < 128) date[element_COUNT++] = cod_caracter;
    else if (cod_caracter < 2048) { date[element_COUNT++] = 0xc0 | (cod_caracter >> 6); date[element_COUNT++] = 0x80 | (cod_caracter & 63); }
    else if (cod_caracter < 65536) { date[element_COUNT++] = 0xe0 | (cod_caracter >> 12); date[element_COUNT++] = 0x80 | ((cod_caracter >> 6) & 63); date[element_COUNT++] = 0x80 | (cod_caracter & 63); }
    else { date[element_COUNT++] = 0xf0 | (cod_caracter >> 18); date[element_COUNT++] = 0x80 | ((cod_caracter >> 12) & 63); date[element_COUNT++] = 0x80 | ((cod_caracter >> 6) & 63); date[element_COUNT++] = 0x80 | (cod_caracter & 63); }
    바이트들((const char *)date, element_COUNT);
}
mașină_Word instrument_caracter(mașină_Word VALUE) {
    unsigned cod_caracter = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (cod_caracter >= 0xdc00 && cod_caracter <= 0xdfff) { caracter(0x10000 + ((높은부분 - 0xd800) << 10) + cod_caracter - 0xdc00); return 1; }
        caracter(0xfffd);
    }
    if (cod_caracter >= 0xd800 && cod_caracter <= 0xdbff) 대기중짝글자 = cod_caracter;
    else caracter(cod_caracter > 0x10ffff || (cod_caracter >= 0xdc00 && cod_caracter <= 0xdfff) ? 0xfffd : cod_caracter);
    return 1;
}
mașină_Word 도구출력(mașină_Word VALUE) {
    const mașină_Word *șir_date = (const mașină_Word *)VALUE;
    for (mașină_Word 순번 = 0; 순번 < șir_date[0]; 순번++) instrument_caracter(șir_date[순번 + 1]);
    return șir_date[0];
}
static int Cale(mașină_Word obiect_referință, char KR_date[512]) {
    const mașină_Word *첫째값 = (const mașină_Word *)obiect_referință;
    unsigned 사용량 = 0;
    for (mașină_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned cod_caracter = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metodă_mod 경로와 호환한다.
        if (cod_caracter >= 0xd800 && cod_caracter <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; cod_caracter = 0x10000 + ((cod_caracter - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (cod_caracter >= 0xd800 && cod_caracter <= 0xdfff) return -22;
        unsigned element_COUNT = cod_caracter < 128 ? 1 : cod_caracter < 2048 ? 2 : cod_caracter < 65536 ? 3 : 4;
        if (사용량 + element_COUNT > 511) return -36;
        if (element_COUNT == 1) KR_date[사용량++] = cod_caracter;
        else {
            KR_date[사용량++] = (element_COUNT == 2 ? 0xc0 : element_COUNT == 3 ? 0xe0 : 0xf0) | (cod_caracter >> (6 * (element_COUNT - 1)));
            for (unsigned 안쪽순번 = element_COUNT - 1; 안쪽순번; 안쪽순번--) KR_date[사용량++] = 0x80 | ((cod_caracter >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_date[사용량] = 0; return 사용량 ? 0 : -22;
}
mașină_Word instrument_crea(mașină_Word Nume, mașină_Word configurație_Serviciu_de_transfer_inteligent_în_fundal) {
    char date_poziție[512]; int eroare = Cale(Nume, date_poziție);
    return (uint32_t)(eroare ? eroare : 호출(3, (mașină_Word)date_poziție, configurație_Serviciu_de_transfer_inteligent_în_fundal, 0));
}
mașină_Word instrument_închide(mașină_Word Fișier_handle) { return (uint32_t)호출(4, Fișier_handle, 0, 0); }
mașină_Word 도구바이트읽기(mașină_Word Fișier_handle) {
    unsigned char SECOND_VALUE; intptr_t element_COUNT = 호출(2, Fișier_handle, (mașină_Word)&SECOND_VALUE, 1);
    return (uint32_t)(element_COUNT == 1 ? SECOND_VALUE : element_COUNT == 0 ? 256 : element_COUNT);
}
mașină_Word instrument_scriere_byte(mașină_Word Fișier_handle, mașină_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Fișier_handle, (mașină_Word)&SECOND_VALUE, 1);
}
mașină_Word 도구읽기(mașină_Word Nume, mașină_Word destinație_date_adresa) {
    if (꾸러미사용중) {
        char date_poziție[512]; int eroare = Cale(Nume, date_poziție); if (eroare) return (uint32_t)eroare;
        unsigned element_COUNT = 0; while (date_poziție[element_COUNT]) element_COUNT++;
        if (element_COUNT >= 6) for (unsigned 순번 = 0; 순번 < element_COUNT - 6; 순번++) if (date_poziție[순번] == '.') date_poziție[순번] = '/';
        unsigned char 바이트들[16384]; mașină_Word *destinație_VALUE_poziție = (mașină_Word *)destinație_date_adresa;
        int RECEIVED_COUNT = 꾸러미읽기(date_poziție, 바이트들, destinație_VALUE_poziție[0] < sizeof(바이트들) ? destinație_VALUE_poziție[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) destinație_VALUE_poziție[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Fișier_handle = 꾸러미사용중 ? -2 : (int32_t)instrument_crea(Nume, 0);
    if (Fișier_handle < 0) {
        char date_poziție[512]; int eroare = Cale(Nume, date_poziție); if (eroare) return (uint32_t)eroare;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Următorul_OFFSET = 자바클래스들[순번].Nume; unsigned 안쪽순번 = 0;
            while (date_poziție[안쪽순번] && date_poziție[안쪽순번] == Următorul_OFFSET[안쪽순번]) 안쪽순번++;
            if (date_poziție[안쪽순번] || Următorul_OFFSET[안쪽순번]) continue;
            mașină_Word *destinație_VALUE_poziție = (mașină_Word *)destinație_date_adresa;
            if (destinație_VALUE_poziție[0] < 자바클래스들[순번].Mărime) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Mărime; 안쪽순번++) destinație_VALUE_poziție[안쪽순번 + 1] = 자바클래스들[순번].date[안쪽순번];
            return 자바클래스들[순번].Mărime;
        }
        return (uint32_t)Fișier_handle;
    }
    mașină_Word *첫째값 = (mașină_Word *)destinație_date_adresa;
    intptr_t Mărime = 호출(9, Fișier_handle, 0, 0), Finalizate_sumă = 0;
    if (Mărime < 0 || (mașină_Word)Mărime > 첫째값[0]) { instrument_închide(Fișier_handle); return (uint32_t)(Mărime < 0 ? Mărime : -27); }
    unsigned char bloc_de_date[256];
    while (Finalizate_sumă < Mărime) {
        intptr_t element_COUNT = 호출(2, Fișier_handle, (mașină_Word)bloc_de_date, Mărime - Finalizate_sumă < 256 ? Mărime - Finalizate_sumă : 256);
        if (element_COUNT <= 0) { instrument_închide(Fișier_handle); return (uint32_t)(element_COUNT ? element_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) 첫째값[1 + Finalizate_sumă + 순번] = bloc_de_date[순번];
        Finalizate_sumă += element_COUNT;
    }
    instrument_închide(Fișier_handle); return Finalizate_sumă;
}
mașină_Word instrument_scriere(mașină_Word Nume, mașină_Word 원본자료, mașină_Word intrare_COUNT) {
    const mașină_Word *첫째값 = (const mașină_Word *)원본자료;
    if (intrare_COUNT > 첫째값[0] || intrare_COUNT > 16384) return (uint32_t)-27;
    int Fișier_handle = (int32_t)instrument_crea(Nume, 577); if (Fișier_handle < 0) return (uint32_t)Fișier_handle;
    unsigned char bloc_de_date[256]; mașină_Word Finalizate_sumă = 0;
    while (Finalizate_sumă < intrare_COUNT) {
        mașină_Word element_COUNT = intrare_COUNT - Finalizate_sumă < 256 ? intrare_COUNT - Finalizate_sumă : 256;
        for (mașină_Word 순번 = 0; 순번 < element_COUNT; 순번++) bloc_de_date[순번] = 첫째값[1 + Finalizate_sumă + 순번];
        intptr_t KR = 호출(1, Fișier_handle, (mașină_Word)bloc_de_date, element_COUNT);
        if (KR <= 0) { instrument_închide(Fișier_handle); return (uint32_t)(KR ? KR : -5); }
        Finalizate_sumă += KR;
    }
    instrument_închide(Fișier_handle); return intrare_COUNT;
}
mașină_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mașină_Word instrument_argument(mașină_Word LOOKUP_INDEX) {
    static const mașină_Word 빈값[1] = {0};
    if (LOOKUP_INDEX >= 8) return (mașină_Word)빈값;
    unsigned char 입력결과[256]; intptr_t element_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *date_poziție = 꾸러미진입클래스(); element_COUNT = 0; while (date_poziție[element_COUNT] && element_COUNT < 255) { 입력결과[element_COUNT] = date_poziție[element_COUNT]; element_COUNT++; } }
    else element_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mașină_Word)입력결과, sizeof(입력결과));
    if (element_COUNT < 0) return (mașină_Word)빈값;
    mașină_Word *KR_date = 전달인수[LOOKUP_INDEX]; unsigned intrare_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < element_COUNT;) {
        unsigned cod_caracter = 입력결과[순번++], 더있음 = cod_caracter < 128 ? 0 : cod_caracter >= 0xc2 && cod_caracter < 0xe0 ? 1 : cod_caracter < 0xf0 && cod_caracter >= 0xe0 ? 2 : cod_caracter >= 0xf0 && cod_caracter <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > element_COUNT) { KR_date[++intrare_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) cod_caracter &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { cod_caracter = (cod_caracter << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || cod_caracter < 최소값 || cod_caracter > 0x10ffff || (cod_caracter >= 0xd800 && cod_caracter <= 0xdfff)) cod_caracter = 0xfffd;
        if (cod_caracter >= 65536) { cod_caracter -= 65536; KR_date[++intrare_COUNT] = 0xd800 | (cod_caracter >> 10); KR_date[++intrare_COUNT] = 0xdc00 | (cod_caracter & 1023); }
        else KR_date[++intrare_COUNT] = cod_caracter;
    }
    KR_date[0] = intrare_COUNT; return (mașină_Word)KR_date;
}
mașină_Word 도구분류(void) { return zonă_VALUE; }
void 커널중단(const char *înștiințare_SMS) {
    const char *date_poziție = înștiințare_SMS; while (*date_poziție) date_poziție++;
    바이트들("Java tool runtime error: ", 25); 바이트들(înștiințare_SMS, date_poziție - înștiințare_SMS); caracter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int buta_utilizator_program(int metodă_mod) {
    zonă_VALUE = metodă_mod;
    unsigned char 첫항목[256]; intptr_t element_COUNT = 호출(15, 0, (mașină_Word)첫항목, sizeof(첫항목));
    if (metodă_mod == 2 || (metodă_mod == 1 && element_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metodă_mod == 2 ? 0 : 1;
        char Fișier_intrare_nume[256]; intptr_t lungime_date = 호출(15, 꾸러미인수이동, (mașină_Word)Fișier_intrare_nume, sizeof(Fișier_intrare_nume));
        if (lungime_date <= 0 || 꾸러미열기(Fișier_intrare_nume) < 0) {
            static const char eroare[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(eroare, sizeof(eroare) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int KR = 자바진입();
    if (대기중짝글자) caracter(0xfffd);
    return KR;
}

// UDP는 propriu 커널의 SVC를 통과하며 curent_element 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Familie, număr_port; uint32_t adresa; unsigned char zero_VALUE[8]; };
static struct 자바주소 UDP_adresa(unsigned număr_port) {
    struct 자바주소 첫째값 = {2, (uint16_t)((număr_port << 8) | (număr_port >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mașină_Word instrument_UDP_crea(mașină_Word număr_port) {
    intptr_t Fișier_handle = 호출(32, 2, 2, 17); if (Fișier_handle < 0) return (uint32_t)Fișier_handle;
    struct 자바주소 첫째값 = UDP_adresa(număr_port);
    첫째값.adresa = 0;
    intptr_t Stare_VALUE = 호출(33, Fișier_handle, (mașină_Word)&첫째값, sizeof(첫째값));
    if (Stare_VALUE < 0) { instrument_închide(Fișier_handle); return (uint32_t)Stare_VALUE; }
    return Fișier_handle;
}
mașină_Word instrument_UDP_trimite(mașină_Word Fișier_handle, mașină_Word număr_port, mașină_Word ARRAY_VALUE, mașină_Word lungime_VALUE) {
    const mașină_Word *원본주소 = (const mașină_Word *)ARRAY_VALUE; unsigned char date[512];
    if (lungime_VALUE > 512 || lungime_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mașină_Word 순번 = 0; 순번 < lungime_VALUE; 순번++) date[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(număr_port);
    return (uint32_t)사용자호출(34, Fișier_handle, (mașină_Word)date, lungime_VALUE, 0, (mașină_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t element_COUNT) { return (element_COUNT>>24)|((element_COUNT>>8)&0xff00)|((element_COUNT<<8)&0xff0000)|(element_COUNT<<24); }
mașină_Word instrument_UDP_trimite_adresa(mașină_Word Fișier_handle, mașină_Word adresa, mașină_Word număr_port, mașină_Word ARRAY_VALUE, mașină_Word lungime_VALUE) {
    const mașină_Word *원본주소 = (const mașină_Word *)ARRAY_VALUE; unsigned char date[512];
    if (lungime_VALUE > 512 || lungime_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mașină_Word 순번 = 0; 순번 < lungime_VALUE; 순번++) date[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(număr_port); 첫째값.adresa = 바이트순서뒤집기(adresa);
    return (uint32_t)사용자호출(34, Fișier_handle, (mașină_Word)date, lungime_VALUE, 0, (mașină_Word)&첫째값, sizeof(첫째값));
}
mașină_Word instrument_conecta(mașină_Word Fișier_handle, mașină_Word adresa, mașină_Word număr_port) {
    struct 자바주소 첫째값 = UDP_adresa(număr_port); 첫째값.adresa = 바이트순서뒤집기(adresa);
    uint32_t Pornește = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t KR = 호출(37, Fișier_handle, (mașină_Word)&첫째값, sizeof(첫째값));
        if (KR != -115) return (uint32_t)KR;
        if ((uint32_t)(호출(7, 0, 0, 0) - Pornește) >= 1000) return (uint32_t)-110;
    }
}
mașină_Word 도구전문받기(mașină_Word Fișier_handle, mașină_Word ARRAY_VALUE, mașină_Word tampon_capacitate) {
    mașină_Word *destinație_adresa = (mașină_Word *)ARRAY_VALUE; unsigned char date[512];
    if (tampon_capacitate > 512 || destinație_adresa[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned lungime_date = sizeof(첫째값);
    intptr_t element_COUNT = 사용자호출(35, Fișier_handle, (mașină_Word)date, tampon_capacitate, 0, (mașină_Word)&첫째값, (mașină_Word)&lungime_date);
    if (element_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) destinație_adresa[순번 + 1] = date[순번]; destinație_adresa[513] = (첫째값.număr_port << 8 | 첫째값.număr_port >> 8) & 65535; destinație_adresa[514] = 바이트순서뒤집기(첫째값.adresa); }
    return (uint32_t)element_COUNT;
}
mașină_Word instrument_UDP_muta(mașină_Word Fișier_handle) {
    struct 자바주소 첫째값; unsigned lungime_date = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Fișier_handle, (mașină_Word)&첫째값, (mașină_Word)&lungime_date);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.număr_port << 8 | 첫째값.număr_port >> 8) & 65535);
}
mașină_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mașină_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mașină_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mașină_Word 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
mașină_Word instrument_dreptunghi(mașină_Word coordonata_X, mașină_Word 세로좌표, mașină_Word 너비값, mașină_Word 높이값, mașină_Word 색상) {
    return (uint32_t)사용자호출(13, coordonata_X, 세로좌표, 색상, 너비값, 높이값, 0);
}

mașină_Word instrument_flux(mașină_Word Acțiuni,mașină_Word Fișier_handle,mașină_Word VALUE){
    if(Acțiuni==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_adresa(VALUE);
    if(Acțiuni==1){첫째값.adresa=0;intptr_t 반환값=호출(33,Fișier_handle,(mașină_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Fișier_handle,4,0));}
    if(Acțiuni==2)return (uint32_t)호출(37,Fișier_handle,(mașină_Word)&첫째값,sizeof(첫째값));
    if(Acțiuni==3)return (uint32_t)호출(39,Fișier_handle,0,0);
    if(Acțiuni==4)return instrument_UDP_muta(Fișier_handle);
    if(Acțiuni==5)return (uint32_t)호출(40,Fișier_handle,0,0);
    return (uint32_t)-22;
}
mașină_Word instrument_GUI(mașină_Word Acțiuni,mașină_Word identificator_VALUE,mașină_Word 첫째값,mașină_Word SECOND_VALUE,mașină_Word cod_caracter,mașină_Word destinație_date){return (uint32_t)사용자호출(20,Acțiuni,identificator_VALUE,첫째값,SECOND_VALUE,cod_caracter,destinație_date);}
mașină_Word instrument_GUI_SMS(mașină_Word identificator_VALUE,mașină_Word ARRAY_VALUE,mașină_Word element_COUNT){
    const mașină_Word *원본주소=(const mașină_Word *)ARRAY_VALUE;uint32_t date[127];unsigned intrare_COUNT=0;
    if(element_COUNT>원본주소[0])return (uint32_t)-22;
    for(mașină_Word 순번=0;순번<element_COUNT;순번++){unsigned codificare_caractere=원본주소[순번+1];if(codificare_caractere>=0xd800&&codificare_caractere<=0xdbff&&순번+1<element_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;codificare_caractere=0x10000+((codificare_caractere-0xd800)<<10)+낮은값-0xdc00;}if(intrare_COUNT==127)return (uint32_t)-22;date[intrare_COUNT++]=codificare_caractere;}
    return (uint32_t)사용자호출(21,identificator_VALUE,(mașină_Word)date,intrare_COUNT,0,0,0);
}
