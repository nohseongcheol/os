// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.propriu.*;

/** 동일 바이트코드를 OpenJDK와 propriu JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumente) throws I_O_excepție {
        primi_muta muta_VALUE = 연결통신.수신열기(0);
        conexiune invitat_VALUE = 연결통신.Deschide("127.0.0.1", muta_VALUE.număr_port());
        conexiune proprietar_identificator = muta_VALUE.primi();
        invitat_VALUE.TIMEOUT(200); proprietar_identificator.TIMEOUT(200);
        검사.참인지(invitat_VALUE.연결됨() && !invitat_VALUE.닫힘(), "Conectează Stare_VALUE");
        검사.참인지(proprietar_identificator.număr_port() == invitat_VALUE.local_număr_port(), "pereche_VALUE număr_port");
        검사.참인지(invitat_VALUE.număr_port() == proprietar_identificator.local_număr_port(), "local_gamă număr_port");
        flux_de_intrare 입력 = proprietar_identificator.입력(); flux_de_ieșire 출력쪽 = invitat_VALUE.Rezultat();
        byte[] mesaj = 문자.codifica("한글 flux_VALUE");
        출력쪽.Scriere(mesaj, 0, mesaj.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[mesaj.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Citire(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fișier 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.decripta_date(RECEIVED_SMS), "한글 flux_VALUE"), "부분 읽기와 Scriere");
        출력쪽.Scriere(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Citire(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Citire");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Citire();
        검사.참인지(두바이트[1] == 18, "나머지 Citire");
        proprietar_identificator.Rezultat().Scriere(255);
        검사.참인지(invitat_VALUE.입력().Citire() == 255, "codificare_VALUE 없는 한 byte_VALUE");
        출력쪽.Închide();
        검사.참인지(invitat_VALUE.닫힘() && 입력.Citire() == -1, "닫기와 Fișier 끝");
        입력.Închide(); 검사.참인지(proprietar_identificator.닫힘(), "입력 flux_VALUE Închide");
        invitat_VALUE.Închide(); proprietar_identificator.Închide();
        muta_VALUE.TIMEOUT(15);
        boolean executare_TIMEOUT = false;
        try { muta_VALUE.primi(); } catch (대기시간초과예외 예상한오류) { executare_TIMEOUT = true; }
        검사.참인지(executare_TIMEOUT, "primi_VALUE TIMEOUT");
        muta_VALUE.Închide(); 검사.참인지(muta_VALUE.닫힘(), "primi_muta Închide");
        diagramă_informații_Canal 받는곳 = diagramă_informații_Canal.Deschide(0), 보내는곳 = diagramă_informații_Canal.Deschide(0);
        받는곳.TIMEOUT(200);
        보내는곳.trimite("127.0.0.1", 받는곳.număr_port(), "diagramă_informații 한글");
        검사.참인지(문자.같음(받는곳.primi(), "diagramă_informații 한글"), "diagramă_informații 송수신");
        보내는곳.Închide(); 받는곳.Închide();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "diagramă_informații Închide");
        Rezultat.scriere_linie("Română 통신 verifica: Conectează diagramă_informații flux_VALUE executare_TIMEOUT Închide");
    }
}
