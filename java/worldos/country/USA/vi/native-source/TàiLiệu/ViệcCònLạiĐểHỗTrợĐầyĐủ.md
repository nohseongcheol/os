# 전체 giáTrịHỗTrợ 요청의 phầnMụcHiệnTại giáTrịTrạngThái

yêuCầu 전체는 아직 완료되지 않았다. phầnMụcHiệnTại ISO는 tựThân Java AOT 커널과 제한형 JVM을 유지한다. 이번 확장에서는 dữLiệuThựcTế C POSIX 일부 기능, tiếngViệt API/mãNguồn tên, IDE Tệp 보존, 게스트 Java Tệp 흐름을 구현하고 시험했다. [구현과 giớiHạnRanhGiới](../posix-kor/HướngDẫn.md)를 기준으로 판단한다.

| yêuCầu 분야 | phầnMụcHiệnTại thựcThiLệnh 가능한 cắtXén | 전체 지원에 필요한 TácVụ |
|---|---|---|
| Java biênDịchNguồn·thựcThiLệnh | 게스트 제한형 javac/JVM, giáTrịTĩnh 단일 클래스와 일부 표준 giáTrịĐốiTượng | 일반 giáTrịĐốiTượng·giáTrịLớp nốiKết·ngoạiLệ·GC·스레드, 완전한 javac와 표준 giáTrịLớp thưViện |
| Tệp | POSIX mụcBộMôTả, Java 단일 giáTrịByte Tệp giáTrịLuồng, 전용 giáTrịPhươngTiện 보존 | 일반 java.io/nio, 디렉터리·giáTrịQuyền·giáTrịKhóa·일반 HệThốngTệp·giáTrịPhầnMởRộng 가능한 giáTrịSứcChứa |
| 네트워크 | AOT Java와 POSIX C의 IPv4 UDP Chủ 왕복 | 게스트 java.net, TCP·DNS·DHCP·IPv6·HTTP·TLS, thêmCuốiMục NIC |
| GUI·Swing | VGA KýTự VàoRaThiếtBịCuối | 프레임버퍼·giáTrịVào sựKiện·giáTrịPhôngChữ·cửaSổ giáTrịHệThốngĐiềuHành, AWT 네이티브 연결과 Swing thựcThiLệnh nềnTảng |
| POSIX | 문서화한 Tệp·VàoRaThiếtBịCuối·UDP giáTrịPhầnCon | giáTrịTiếnTrình·exec/fork·스레드·시그널·giáTrịThờiGian·mmap·poll·파이프 등과 적합성 thẩmĐịnh |
| 언어별 tên | tiếngViệt 46개 giáTrịPhépÁnhXạ giáTrịMục, dữLiệuThựcTế C/Java/Tệp tên 적용 | giáTrịĐốiĐích NgônNgữ giáTrịChốt, 언어별 용례·역사 근거와 해당 mãNguồn·도구의 thẩmĐịnh |

tựThân 커널을 유지하면 giáTrịĐỉnh nềnTảng 기능과 런타임 이식을 순차적으로 구현해야 한다. Linux nềnTảng thựcThiLệnh 환경을 추가하는 방식은 별도의 giáTrịNhân·루트 HệThốngTệp·OpenJDK·그래픽 giáTrịMáyChủ·영구 giáTrịCất 구성을 가진 thựcThiLệnh 경로가 된다. 후자는 기존 tựThân 커널에 OpenJDK가 이식되었다고 표시해서는 안 된다.

thựcThiLệnh 기반과 thêmCuốiMục giáTrịĐốiĐích 언어는 사용자에게 확인을 요청했으며 아직 답변을 받지 못했다. 그 결정 없이 기존 커널을 Linux로 교체하거나 여러 국가의 번역을 임의로 만들지 않았다. phầnMụcHiệnTại 원문과 KiểmThử 결과를 후속 구현의 출발점으로 보존한다.
