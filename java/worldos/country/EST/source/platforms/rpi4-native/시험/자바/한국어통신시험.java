// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Eesti.oma.*;

/** 동일 바이트코드를 OpenJDK와 oma JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumendid) throws I_O_erand {
        saama_port port_VALUE = ühendus_transport.수신열기(0);
        ühendus külaline_VALUE = ühendus_transport.Ava("127.0.0.1", port_VALUE.pordinumber());
        ühendus omanik_identifikaator = port_VALUE.saama();
        külaline_VALUE.TIMEOUT(200); omanik_identifikaator.TIMEOUT(200);
        검사.참인지(külaline_VALUE.연결됨() && !külaline_VALUE.infotehnoloogia_suletud(), "Ühendu Olek_VALUE");
        검사.참인지(omanik_identifikaator.pordinumber() == külaline_VALUE.kohalik_pordinumber(), "partner_VALUE pordinumber");
        검사.참인지(külaline_VALUE.pordinumber() == omanik_identifikaator.kohalik_pordinumber(), "kohalik_skoop pordinumber");
        sisendvoog 입력 = omanik_identifikaator.입력(); väljundvoog toodang_leht = külaline_VALUE.Väljund();
        byte[] meil = 문자.kodeerima("한글 voog_VALUE");
        toodang_leht.Kirjutamine(meil, 0, meil.length); toodang_leht.내보내기();
        byte[] RECEIVED_SMS = new byte[meil.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Lugemine(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fail 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dekrüptima_andmed(RECEIVED_SMS), "한글 voog_VALUE"), "부분 읽기와 Kirjutamine");
        toodang_leht.Kirjutamine(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Lugemine(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Lugemine");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Lugemine();
        검사.참인지(두바이트[1] == 18, "나머지 Lugemine");
        omanik_identifikaator.Väljund().Kirjutamine(255);
        검사.참인지(külaline_VALUE.입력().Lugemine() == 255, "kodeerimine_VALUE 없는 한 bait_VALUE");
        toodang_leht.Suletud();
        검사.참인지(külaline_VALUE.infotehnoloogia_suletud() && 입력.Lugemine() == -1, "닫기와 Fail 끝");
        입력.Suletud(); 검사.참인지(omanik_identifikaator.infotehnoloogia_suletud(), "입력 voog_VALUE Suletud");
        külaline_VALUE.Suletud(); omanik_identifikaator.Suletud();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.saama(); } catch (Oota_TIMEOUT_erand 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "saama_VALUE TIMEOUT");
        port_VALUE.Suletud(); 검사.참인지(port_VALUE.infotehnoloogia_suletud(), "saama_port Suletud");
        datagramm_Kanal 받는곳 = datagramm_Kanal.Ava(0), 보내는곳 = datagramm_Kanal.Ava(0);
        받는곳.TIMEOUT(200);
        보내는곳.saatma("127.0.0.1", 받는곳.pordinumber(), "datagramm 한글");
        검사.참인지(문자.같음(받는곳.saama(), "datagramm 한글"), "datagramm 송수신");
        보내는곳.Suletud(); 받는곳.Suletud();
        검사.참인지(보내는곳.infotehnoloogia_suletud() && 받는곳.infotehnoloogia_suletud(), "datagramm Suletud");
        Väljund.kirjutamine_liin("Eesti 통신 kinnitama: Ühendu datagramm voog_VALUE 시간제한 Suletud");
    }
}
