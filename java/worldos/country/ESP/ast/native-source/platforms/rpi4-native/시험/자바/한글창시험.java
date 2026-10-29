// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Ventana;
import 한국어.자체.화면요소;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Ventana 화면;
    Etiqueta 안내;
    입력칸 입력;
    public void Executar() {
        검사.참인지(화면일정.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new Ventana("한국어 라이브러리 Ventana", 400, 280);
        안내 = 화면요소.표지("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = 화면요소.입력칸("Nome", 20, 65, 340, 30);
        화면.담기(안내);
        화면.담기(입력);
        화면.담기(화면요소.Botón("인사하기", 20, 110, 180, 32, this));
        화면.보이기();
        Salida.줄쓰기("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 Eventu) {
        검사.참인지(화면일정.사건처리중인가(), "한국어 Aición 되부름");
        검사.참인지(Eventu.번호() == 1001 && Eventu.일어난곳() instanceof Botón, "한국어 Eventu 객체와 출처");
        검사.참인지(!((Object)Eventu.일어난곳() instanceof javax.swing.JButton), "표준 단추와 독립된 형식");
        검사.참인지(!((Object)Eventu instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 형식");
        안내.글쓰기("안녕하세요 " + 입력.글읽기());
        Salida.줄쓰기("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumentu) {
        화면일정.나중에실행(new 한글창시험());
    }
}
