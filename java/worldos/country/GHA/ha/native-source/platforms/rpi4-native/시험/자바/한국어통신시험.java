// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws I_O_banbanchi {
        수신창구 fot_Daraja = 연결통신.수신열기(0);
        haɗi baƙo_Daraja = 연결통신.Buɗe("127.0.0.1", fot_Daraja.lambar_kafa());
        haɗi mamallaki_mai_ganewa = fot_Daraja.받기();
        baƙo_Daraja.대기시간(200); mamallaki_mai_ganewa.대기시간(200);
        검사.참인지(baƙo_Daraja.연결됨() && !baƙo_Daraja.닫힘(), "Haɗi Matsayi_Daraja");
        검사.참인지(mamallaki_mai_ganewa.lambar_kafa() == baƙo_Daraja.na_gida_lambar_kafa(), "Fiya_Daraja lambar_kafa");
        검사.참인지(baƙo_Daraja.lambar_kafa() == mamallaki_mai_ganewa.na_gida_lambar_kafa(), "na_gida_Kima lambar_kafa");
        입력흐름 입력 = mamallaki_mai_ganewa.입력(); 출력흐름 출력쪽 = baƙo_Daraja.출력();
        byte[] imel_8c783e64 = 문자.부호화("한글 watsuwa_Daraja");
        출력쪽.Yi_Rubutu(imel_8c783e64, 0, imel_8c783e64.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[imel_8c783e64.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.Yi_Karatu(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fayil 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.Bude_Tarin_bayani(받은글), "한글 watsuwa_Daraja"), "부분 읽기와 Yi_Rubutu");
        출력쪽.Yi_Rubutu(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Yi_Karatu(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "TSARI_Daraja Yi_Karatu");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Yi_Karatu();
        검사.참인지(두바이트[1] == 18, "나머지 Yi_Karatu");
        mamallaki_mai_ganewa.출력().Yi_Rubutu(255);
        검사.참인지(baƙo_Daraja.입력().Yi_Karatu() == 255, "Juyar_da_bayanai_zuwa_lamba_Daraja 없는 한 bayit_Daraja");
        출력쪽.Rufe();
        검사.참인지(baƙo_Daraja.닫힘() && 입력.Yi_Karatu() == -1, "닫기와 Fayil 끝");
        입력.Rufe(); 검사.참인지(mamallaki_mai_ganewa.닫힘(), "입력 watsuwa_Daraja Rufe");
        baƙo_Daraja.Rufe(); mamallaki_mai_ganewa.Rufe();
        fot_Daraja.대기시간(15);
        boolean 시간제한 = false;
        try { fot_Daraja.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        fot_Daraja.Rufe(); 검사.참인지(fot_Daraja.닫힘(), "수신창구 Rufe");
        전문통로 받는곳 = 전문통로.Buɗe(0), 보내는곳 = 전문통로.Buɗe(0);
        받는곳.대기시간(200);
        보내는곳.Aika("127.0.0.1", 받는곳.lambar_kafa(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Rufe(); 받는곳.Rufe();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Rufe");
        출력.Rubuta_Layi("한국어 통신 Tabbatar_da: Haɗi 전문 watsuwa_Daraja 시간제한 Rufe");
    }
}
