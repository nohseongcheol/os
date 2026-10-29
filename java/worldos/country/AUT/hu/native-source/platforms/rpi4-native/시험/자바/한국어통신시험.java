// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.saját.*;

/** 동일 바이트코드를 OpenJDK와 saját JVM에서 실행하는 kommunikáció 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumentumok) throws I_O_kivétel {
        fogad_port port_ÉRTÉK = ismerős_szállítás.수신열기(0);
        ismerős vendég_ÉRTÉK = ismerős_szállítás.Megnyitás("127.0.0.1", port_ÉRTÉK.portszám());
        ismerős tulajdonos_azonosító = port_ÉRTÉK.fogad();
        vendég_ÉRTÉK.IDŐTÚLLÉPÉS(200); tulajdonos_azonosító.IDŐTÚLLÉPÉS(200);
        검사.참인지(vendég_ÉRTÉK.연결됨() && !vendég_ÉRTÉK.informatikai_részleg_lezárt(), "Kapcsolódás Állapot_ÉRTÉK");
        검사.참인지(tulajdonos_azonosító.portszám() == vendég_ÉRTÉK.helyi_portszám(), "társ_ÉRTÉK portszám");
        검사.참인지(vendég_ÉRTÉK.portszám() == tulajdonos_azonosító.helyi_portszám(), "helyi_hatókör portszám");
        bemeneti_adatfolyam bevitel_ÉRTÉK = tulajdonos_azonosító.bevitel_ÉRTÉK(); kimeneti_adatfolyam kimenet_lap = vendég_ÉRTÉK.Kimenet();
        byte[] e_mail = 문자.kódolás("한글 Stream_ÉRTÉK");
        kimenet_lap.Írás(e_mail, 0, e_mail.length); kimenet_lap.내보내기();
        byte[] KAPOTT_SMS = new byte[e_mail.length];
        int 읽은수 = 0;
        while (읽은수 < KAPOTT_SMS.length) {
            int 더읽음 = bevitel_ÉRTÉK.Olvasás(KAPOTT_SMS, 읽은수, KAPOTT_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fájl 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.visszafejt_adat(KAPOTT_SMS), "한글 Stream_ÉRTÉK"), "부분 읽기와 Írás");
        kimenet_lap.Írás(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = bevitel_ÉRTÉK.Olvasás(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "TÖMB_ÉRTÉK Olvasás");
        if (첫읽기 == 1) 두바이트[1] = (byte)bevitel_ÉRTÉK.Olvasás();
        검사.참인지(두바이트[1] == 18, "나머지 Olvasás");
        tulajdonos_azonosító.Kimenet().Írás(255);
        검사.참인지(vendég_ÉRTÉK.bevitel_ÉRTÉK().Olvasás() == 255, "kódolás_ÉRTÉK 없는 한 bájt_ÉRTÉK");
        kimenet_lap.Bezárás();
        검사.참인지(vendég_ÉRTÉK.informatikai_részleg_lezárt() && bevitel_ÉRTÉK.Olvasás() == -1, "닫기와 Fájl 끝");
        bevitel_ÉRTÉK.Bezárás(); 검사.참인지(tulajdonos_azonosító.informatikai_részleg_lezárt(), "bevitel_ÉRTÉK Stream_ÉRTÉK Bezárás");
        vendég_ÉRTÉK.Bezárás(); tulajdonos_azonosító.Bezárás();
        port_ÉRTÉK.IDŐTÚLLÉPÉS(15);
        boolean végrehajtás_IDŐTÚLLÉPÉS = false;
        try { port_ÉRTÉK.fogad(); } catch (várj_IDŐTÚLLÉPÉS_kivétel 예상한오류) { végrehajtás_IDŐTÚLLÉPÉS = true; }
        검사.참인지(végrehajtás_IDŐTÚLLÉPÉS, "fogad_ÉRTÉK IDŐTÚLLÉPÉS");
        port_ÉRTÉK.Bezárás(); 검사.참인지(port_ÉRTÉK.informatikai_részleg_lezárt(), "fogad_port Bezárás");
        datagram_Csatorna 받는곳 = datagram_Csatorna.Megnyitás(0), 보내는곳 = datagram_Csatorna.Megnyitás(0);
        받는곳.IDŐTÚLLÉPÉS(200);
        보내는곳.küld("127.0.0.1", 받는곳.portszám(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.fogad(), "datagram 한글"), "datagram 송수신");
        보내는곳.Bezárás(); 받는곳.Bezárás();
        검사.참인지(보내는곳.informatikai_részleg_lezárt() && 받는곳.informatikai_részleg_lezárt(), "datagram Bezárás");
        Kimenet.ír_sor("magyar kommunikáció igazol: Kapcsolódás datagram Stream_ÉRTÉK végrehajtás_IDŐTÚLLÉPÉS Bezárás");
    }
}
