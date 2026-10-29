// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kärna_värde 안의 연결형 byte_värde flöde_värde. Ethernet/TCP 패킷 스택이 아닌 루프백 socket nivå_värde. */
public final class flöde_nätverk {
    static int[] status_värde = new int[16], port_värde = new int[16], 짝 = new int[16], peer_port = new int[16], vänta_värde = new int[16], informationsteknik_gräns = new int[16];
    static int[] framåtvänd_värde = new int[16], nummer = new int[16], data = new int[16 * 1024];
    static int Nästa_objekt = 50000;
    static int verifiera(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && status_värde[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int portnummer) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_värde[Loop_INDEX] != 0 && informationsteknik_gräns[Loop_INDEX] != 0 && port_värde[Loop_INDEX] == portnummer) return true; return false; }
    public static int Skapa_post() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_värde[Loop_INDEX] == 0) { status_värde[Loop_INDEX] = 1; peer_port[Loop_INDEX] = port_värde[Loop_INDEX] = framåtvänd_värde[Loop_INDEX] = nummer[Loop_INDEX] = vänta_värde[Loop_INDEX] = informationsteknik_gräns[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_deltagare(int 열린파일번호, int socket_ADRESS, int portnummer) {
        int Loop_INDEX = verifiera(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (socket_ADRESS != 0 && socket_ADRESS != 0x7f000001) return -99;
        if (status_värde[Loop_INDEX] != 1 || portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer == 0) { do { portnummer = Nästa_objekt++; if (Nästa_objekt > 65535) Nästa_objekt = 50000; } while (사용중(portnummer)); }
        if (사용중(portnummer)) return -98; port_värde[Loop_INDEX] = portnummer; informationsteknik_gräns[Loop_INDEX] = 1; status_värde[Loop_INDEX] = 2; return 0;
    }
    public static int lyssna_deltagare(int 열린파일번호, int kvarvarande_uppgifter) { int Loop_INDEX = verifiera(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_värde[Loop_INDEX] != 2 || kvarvarande_uppgifter < 1) return -22; status_värde[Loop_INDEX] = 3; return 0; }
    public static int Anslut(int 열린파일번호, int socket_ADRESS, int portnummer) {
        int Loop_INDEX = verifiera(열린파일번호); if (Loop_INDEX < 0) return -9; if (socket_ADRESS != 0x7f000001) return -101;
        if (portnummer < 1 || portnummer > 65535 || status_värde[Loop_INDEX] > 2) return -22;
        int få_page = -1; for (int inre_koppling_placera = 0; inre_koppling_placera < 16; inre_koppling_placera++) if (status_värde[inre_koppling_placera] == 3 && port_värde[inre_koppling_placera] == portnummer) få_page = inre_koppling_placera;
        if (få_page < 0) return -111;
        int 대기여부 = 0; for (int inre_koppling_placera = 0; inre_koppling_placera < 16; inre_koppling_placera++) if (vänta_värde[inre_koppling_placera] == få_page + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (status_värde[Loop_INDEX] == 1) { int 처리값 = BIND_deltagare(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Skapa_post(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        status_värde[Loop_INDEX] = status_värde[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_värde[다른번호] = portnummer; peer_port[Loop_INDEX] = portnummer; peer_port[다른번호] = port_värde[Loop_INDEX]; vänta_värde[다른번호] = få_page + 1; return 0;
    }
    public static int acceptera_kontakt(int 열린파일번호) { int Loop_INDEX = verifiera(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_värde[Loop_INDEX] != 3) return -22; for (int inre_koppling_placera = 0; inre_koppling_placera < 16; inre_koppling_placera++) if (status_värde[inre_koppling_placera] != 0 && vänta_värde[inre_koppling_placera] == Loop_INDEX + 1) { vänta_värde[inre_koppling_placera] = 0; return inre_koppling_placera + 40; } return -11; }
    public static int Skriv(int 열린파일번호, int post_ANTAL) {
        int Loop_INDEX = verifiera(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_värde[Loop_INDEX] != 4) return -107;
        if (post_ANTAL < 0 || post_ANTAL > 512) return -22; if (post_ANTAL == 0) return 0;
        int inre_koppling_placera = 짝[Loop_INDEX]; if (inre_koppling_placera < 0) return -32; int summa_ANTAL = 1024 - nummer[inre_koppling_placera]; if (summa_ANTAL == 0) return -11; if (summa_ANTAL > post_ANTAL) summa_ANTAL = post_ANTAL;
        for (int Jämförelse_placera = 0; Jämförelse_placera < summa_ANTAL; Jämförelse_placera++) data[inre_koppling_placera * 1024 + (framåtvänd_värde[inre_koppling_placera] + nummer[inre_koppling_placera] + Jämförelse_placera) % 1024] = loopback_nätverk.Framåt_värde[Jämförelse_placera]; nummer[inre_koppling_placera] += summa_ANTAL; return summa_ANTAL;
    }
    public static int Läs(int 열린파일번호, int post_ANTAL) {
        int Loop_INDEX = verifiera(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_värde[Loop_INDEX] != 4) return -107; if (post_ANTAL < 0 || post_ANTAL > 512) return -22;
        if (post_ANTAL == 0) return 0; if (nummer[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (post_ANTAL > nummer[Loop_INDEX]) post_ANTAL = nummer[Loop_INDEX];
        for (int Jämförelse_placera = 0; Jämförelse_placera < post_ANTAL; Jämförelse_placera++) loopback_nätverk.Framåt_värde[Jämförelse_placera] = data[Loop_INDEX * 1024 + (framåtvänd_värde[Loop_INDEX] + Jämförelse_placera) % 1024]; framåtvänd_värde[Loop_INDEX] = (framåtvänd_värde[Loop_INDEX] + post_ANTAL) % 1024; nummer[Loop_INDEX] -= post_ANTAL; return post_ANTAL;
    }
    public static int läsa_deltagare_port(int 열린파일번호) { int Loop_INDEX = verifiera(열린파일번호); return Loop_INDEX < 0 ? -9 : port_värde[Loop_INDEX]; }
    public static int läsa_peer_port(int 열린파일번호) { int Loop_INDEX = verifiera(열린파일번호); return Loop_INDEX < 0 ? -9 : peer_port[Loop_INDEX]; }
    public static int Stäng(int 열린파일번호) {
        int Loop_INDEX = verifiera(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (status_värde[Loop_INDEX] == 3) for (int inre_koppling_placera = 0; inre_koppling_placera < 16; inre_koppling_placera++) if (vänta_värde[inre_koppling_placera] == Loop_INDEX + 1) { if (짝[inre_koppling_placera] >= 0) 짝[짝[inre_koppling_placera]] = -1; status_värde[inre_koppling_placera] = vänta_värde[inre_koppling_placera] = informationsteknik_gräns[inre_koppling_placera] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; status_värde[Loop_INDEX] = informationsteknik_gräns[Loop_INDEX] = nummer[Loop_INDEX] = vänta_värde[Loop_INDEX] = 0; return 0;
    }
}
