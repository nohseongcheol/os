// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import isiXhosa.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 iphothi_ixabiso = 연결통신.수신열기(0);
        uqhagamshelo undwendwe_ixabiso = 연결통신.Vula("127.0.0.1", iphothi_ixabiso.접속번호());
        uqhagamshelo umnini_isalathisi = iphothi_ixabiso.받기();
        undwendwe_ixabiso.대기시간(200); umnini_isalathisi.대기시간(200);
        검사.참인지(undwendwe_ixabiso.연결됨() && !undwendwe_ixabiso.닫힘(), "Nxulumanisa imo_ixabiso");
        검사.참인지(umnini_isalathisi.접속번호() == undwendwe_ixabiso.지역접속번호(), "untanga_ixabiso 접속번호");
        검사.참인지(undwendwe_ixabiso.접속번호() == umnini_isalathisi.지역접속번호(), "eyale_ndawo_umda 접속번호");
        입력흐름 입력 = umnini_isalathisi.입력(); 출력흐름 출력쪽 = undwendwe_ixabiso.출력();
        byte[] umyalezo = 문자.부호화("한글 Stream_ixabiso");
        출력쪽.Bhala(umyalezo, 0, umyalezo.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[umyalezo.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.Funda(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 iFayili 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.buyisela_ubhalo_oluqhelekileyo_iingcombolo(받은글), "한글 Stream_ixabiso"), "부분 읽기와 Bhala");
        출력쪽.Bhala(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Funda(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ULUHLU_ixabiso Funda");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Funda();
        검사.참인지(두바이트[1] == 18, "나머지 Funda");
        umnini_isalathisi.출력().Bhala(255);
        검사.참인지(undwendwe_ixabiso.입력().Funda() == 255, "ujiko_nkcukacha_zibe_ziikhowudi_ixabiso 없는 한 ibhayithi_ixabiso");
        출력쪽.Vala();
        검사.참인지(undwendwe_ixabiso.닫힘() && 입력.Funda() == -1, "닫기와 iFayili 끝");
        입력.Vala(); 검사.참인지(umnini_isalathisi.닫힘(), "입력 Stream_ixabiso Vala");
        undwendwe_ixabiso.Vala(); umnini_isalathisi.Vala();
        iphothi_ixabiso.대기시간(15);
        boolean 시간제한 = false;
        try { iphothi_ixabiso.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        iphothi_ixabiso.Vala(); 검사.참인지(iphothi_ixabiso.닫힘(), "수신창구 Vala");
        전문통로 받는곳 = 전문통로.Vula(0), 보내는곳 = 전문통로.Vula(0);
        받는곳.대기시간(200);
        보내는곳.thumela("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Vala(); 받는곳.Vala();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Vala");
        출력.bhala_umgca("isiXhosa 통신 ngqinisisa: Nxulumanisa 전문 Stream_ixabiso 시간제한 Vala");
    }
}
