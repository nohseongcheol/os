// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.eigin.*;

/** 동일 바이트코드를 OpenJDK와 eigin JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Viðföng) throws I_Ú_undantekning {
        수신창구 gátt_VALUE = tenging_flutningur.수신열기(0);
        tenging gestur_VALUE = tenging_flutningur.Opna("127.0.0.1", gátt_VALUE.tengisnúmer());
        tenging eigandi_auðkenni = gátt_VALUE.받기();
        gestur_VALUE.TIMEOUT(200); eigandi_auðkenni.TIMEOUT(200);
        검사.참인지(gestur_VALUE.연결됨() && !gestur_VALUE.upplýsingatækni_lokað(), "Tengjast staða_VALUE_e10195a1");
        검사.참인지(eigandi_auðkenni.tengisnúmer() == gestur_VALUE.staðbundið_tengisnúmer(), "jafningi_VALUE tengisnúmer");
        검사.참인지(gestur_VALUE.tengisnúmer() == eigandi_auðkenni.staðbundið_tengisnúmer(), "staðbundið_umfang tengisnúmer");
        입력흐름 입력 = eigandi_auðkenni.입력(); úttak_Stream úttak_síða = gestur_VALUE.úttak();
        byte[] skeyti = 문자.부호화("한글 Stream_VALUE");
        úttak_síða.Skrift(skeyti, 0, skeyti.length); úttak_síða.내보내기();
        byte[] RECEIVED_SMS = new byte[skeyti.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Lestur(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Skrá 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dulráða_gögn(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Skrift");
        úttak_síða.Skrift(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Lestur(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Lestur");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Lestur();
        검사.참인지(두바이트[1] == 18, "나머지 Lestur");
        eigandi_auðkenni.úttak().Skrift(255);
        검사.참인지(gestur_VALUE.입력().Lestur() == 255, "kóðun_VALUE 없는 한 bæti_VALUE");
        úttak_síða.Loka();
        검사.참인지(gestur_VALUE.upplýsingatækni_lokað() && 입력.Lestur() == -1, "닫기와 Skrá 끝");
        입력.Loka(); 검사.참인지(eigandi_auðkenni.upplýsingatækni_lokað(), "입력 Stream_VALUE Loka");
        gestur_VALUE.Loka(); eigandi_auðkenni.Loka();
        gátt_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { gátt_VALUE.받기(); } catch (Bíddu_TIMEOUT_undantekning 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        gátt_VALUE.Loka(); 검사.참인지(gátt_VALUE.upplýsingatækni_lokað(), "수신창구 Loka");
        전문통로 받는곳 = 전문통로.Opna(0), 보내는곳 = 전문통로.Opna(0);
        받는곳.TIMEOUT(200);
        보내는곳.senda("127.0.0.1", 받는곳.tengisnúmer(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Loka(); 받는곳.Loka();
        검사.참인지(보내는곳.upplýsingatækni_lokað() && 받는곳.upplýsingatækni_lokað(), "전문 Loka");
        úttak.skrifa_lína("Íslenska 통신 sannprófa: Tengjast 전문 Stream_VALUE 시간제한 Loka");
    }
}
