// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.vlastné.*;

/** 동일 바이트코드를 OpenJDK와 vlastné JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumenty) throws vstup_a_výstup_výnimka {
        dostať_port port_VALUE = 연결통신.수신열기(0);
        kontakt hosť_VALUE = 연결통신.Otvoriť("127.0.0.1", port_VALUE.číslo_portu());
        kontakt vlastník_identifikátor = port_VALUE.dostať();
        hosť_VALUE.TIMEOUT(200); vlastník_identifikátor.TIMEOUT(200);
        검사.참인지(hosť_VALUE.연결됨() && !hosť_VALUE.닫힘(), "Pripojiť Stav_VALUE");
        검사.참인지(vlastník_identifikátor.číslo_portu() == hosť_VALUE.miestny_číslo_portu(), "partnerský_uzol_VALUE číslo_portu");
        검사.참인지(hosť_VALUE.číslo_portu() == vlastník_identifikátor.miestny_číslo_portu(), "miestny_Rozsah číslo_portu");
        vstupný_prúd_údajov vstup_VALUE = vlastník_identifikátor.vstup_VALUE(); výstupný_prúd_údajov 출력쪽 = hosť_VALUE.Výstup();
        byte[] e_mail = 문자.kódovať("한글 Stream_VALUE");
        출력쪽.Zápis(e_mail, 0, e_mail.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[e_mail.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = vstup_VALUE.Čítanie(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Súbor 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dešifrovať_údaje(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Zápis");
        출력쪽.Zápis(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = vstup_VALUE.Čítanie(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "pole_VALUE Čítanie");
        if (첫읽기 == 1) 두바이트[1] = (byte)vstup_VALUE.Čítanie();
        검사.참인지(두바이트[1] == 18, "나머지 Čítanie");
        vlastník_identifikátor.Výstup().Zápis(255);
        검사.참인지(hosť_VALUE.vstup_VALUE().Čítanie() == 255, "kódovanie_VALUE 없는 한 Byte_VALUE");
        출력쪽.Zatvoriť();
        검사.참인지(hosť_VALUE.닫힘() && vstup_VALUE.Čítanie() == -1, "닫기와 Súbor 끝");
        vstup_VALUE.Zatvoriť(); 검사.참인지(vlastník_identifikátor.닫힘(), "vstup_VALUE Stream_VALUE Zatvoriť");
        hosť_VALUE.Zatvoriť(); vlastník_identifikátor.Zatvoriť();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.dostať(); } catch (počkaj_TIMEOUT_výnimka 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "dostať_VALUE TIMEOUT");
        port_VALUE.Zatvoriť(); 검사.참인지(port_VALUE.닫힘(), "dostať_port Zatvoriť");
        datagram_Kanál 받는곳 = datagram_Kanál.Otvoriť(0), 보내는곳 = datagram_Kanál.Otvoriť(0);
        받는곳.TIMEOUT(200);
        보내는곳.odoslať("127.0.0.1", 받는곳.číslo_portu(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.dostať(), "datagram 한글"), "datagram 송수신");
        보내는곳.Zatvoriť(); 받는곳.Zatvoriť();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "datagram Zatvoriť");
        Výstup.zapísať_linka("Slovenský 통신 overiť: Pripojiť datagram Stream_VALUE 시간제한 Zatvoriť");
    }
}
