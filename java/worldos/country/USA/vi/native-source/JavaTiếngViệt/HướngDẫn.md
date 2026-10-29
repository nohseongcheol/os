# tiếngViệt Java giáTrịPhụGiúp thưViện

OpenJDK 11 이상과 함께 쓰는 프로젝트 giáTrịChủSởHữu API다. 표준 Java thưViện 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·ngoạiLệ·자료형은 그대로 함께 쓴다.

전체 22개 giáTrịPhụGiúp 메서드의 cácĐốiSố·giáTrịĐãTrảVề·제약, HệĐiềuHành 안의 사용법, Python·C++ gọiThựcHiện 방법은 **[tiếngViệt thưViện HướngDẫnNgườiDùng](HướngDẫnNgườiDùng.md)**에 정리했다. [Python gọiThựcHiện VíDụ](VíDụ/NgônNgữKhác/GọiPython.py)와 [C++ JNI gọiThựcHiện VíDụ](VíDụ/NgônNgữKhác/GọiJava.cpp)도 제공한다.

`make`로 `build/JavaTiếngViệt.jar`를 만든다. `javac -encoding UTF-8 -cp build/JavaTiếngViệt.jar VíDụ/LờiChào.java`로 예제를 컴파일한다. 실행은 `java -cp build/JavaTiếngViệt.jar:VíDụ LờiChào`toánHạngThứBa.

`LờiChào` 예제는 그래픽 화면이 없으면 Tệp·KýTự·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 thựcThiLệnh HướngDẫn](../platforms/rpi4/README.md)의 `make run`으로 부팅한 giáTrịLùi VNC 데스크톱의 터미널을 사용한다.

| giáTrịLớp | 제공 기능 |
|---|---|
| Tệp | UTF-8 텍스트·giáTrịByte đọc/ghi, 디렉터리·danhSáchMục |
| KýTự | UTF-8 chuyểnĐổiGiáTrị, NFC chuẩnHóaGiáTrị, giáTrịMã 포인트 trịSố, 언어별 từTừVựng giáTrịRanhGiới |
| TruyềnThông | HTTP(S) yêuCầu, 제한시간을 가진 TCP nốiKết |
| TácVụ | 스레드 chạy·합류·chờGiáTrị, TácVụ TrìnhKhởiChạyChươngTrình |
| MànHình | Swing 이벤트 처리와 cửaSổ sinh |
| KhôngGianLàmViệc | mãNguồn giáTrịSửa·biênDịchNguồn·thựcThiLệnh·thựcThiLệnh Tệp sinh MànHình |

`char`는 UTF-16 giáTrịMã 단위이므로 이모지 등을 한 글자로 처리할 때 giáTrịMã 포인트 또는 KýTự giáTrịRanhGiới API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/giáTrịPhôngChữ/입력기 조합을 각각 검증한 것은 아니다.

이름은 phầnMụcHiệnTại 의미가 분명한 tiếngViệt 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. giáTrịTàiNguyên 종료와 ngoạiLệ 처리는 표준 API의 계약을 따른다.
