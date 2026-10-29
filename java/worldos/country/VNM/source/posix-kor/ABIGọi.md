# NgườiDùng gọiThựcHiện giáTrịRanhGiới

대상은 jkoros i386 ELF32다. Linux i386의 gọiThựcHiện 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `máy/CácLờiGọiHệThốngĐiềuHành.s`에서 EAX(sốHiệu), EBX·ECX·EDX·ESI·EDI(thứBậcĐầuTiên~thứBậcThứNăm cácĐốiSố)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. giáTrịNhân 실패는 giáTrịÂm lỗi sốHiệu, C thưViện 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 NgườiDùng giáTrịMiền 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C DữLiệu 주소는 giáTrịByte 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java Tệp 흐름의 어셈블리 경계가 별도 giáTrịByte 버퍼를 마련하여 같은 호출을 사용한다.

| sốHiệu | hànhĐộng | cácĐốiSố |
|---|---|---|
| 30 | mởTệp | NUL phầnKết tên địaChỉ, cácThiếtLập, cấpQuyềnQuyền |
| 31 | đọcDữLiệuTệp | mụcBộMôTả, DữLiệu địaChỉ, giáTrịByte trịSố |
| 32 | ghiDữLiệuTệp | mụcBộMôTả, DữLiệu địaChỉ, giáTrịByte trịSố |
| 33 | đóngTệp | mụcBộMôTả |
| 34 | dịchVịTệp | mụcBộMôTả, giáTrịBảngMã 있는 giáTrịĐộLệch, gốcCâyDựÁn |
| 35 | bộMôTảTệpBảnSao | mụcBộMôTả |
| 36 | tạiBộMôTảTệpBảnSao | mụcBộMôTả, 새 mụcBộMôTả |
| 37 | đọcTìnhTrạngTệp | mụcBộMôTả, 48바이트 giáTrịTrạngThái địaChỉ |
| 38 | gỡTênMụcTệp | NUL phầnKết tên địaChỉ |
| 39 | đặtGiáTrịĐộDàiTệp | mụcBộMôTả, 새 độDài |
| 40 | bộMôTảTệpĐiềuKhiển | mụcBộMôTả, lệnh, giáTrị |
| 41 | tạoĐiểmCuối | địaChỉ giáTrịHệThốngĐiềuHành, giáTrịLoại, giáTrịQuyƯớc sốHiệu |
| 42 | ràngBuộcĐịaChỉ | mụcBộMôTả, sockaddr_in địaChỉ, độDài |
| 43 | gửiDữLiệuĐiệnDữLiệu | mụcBộMôTả, DữLiệu địaChỉ, độDài, cácThiếtLập, yêuCầu địaChỉ |
| 44 | nhậnDữLiệuĐiệnDữLiệu | mụcBộMôTả, DữLiệu địaChỉ, độDài, cácThiếtLập, yêuCầu địaChỉ |
| 45 | đọcĐịaChỉỔCắmMạng | mụcBộMôTả, sockaddr địaChỉ, socklen_t địaChỉ |
| 46 | đặtGiáTrịHếtGiờNhận | mụcBộMôTả, 0~2000 miliGiây |
| 47 | lưuTrữTệpChốt | mụcBộMôTả |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 địaChỉ 두 칸이다. nhậnGiáTrị 주소가 NULL이면 giáTrịĐốiTác địaChỉ 기록을 생략한다. sockaddr_in은 16바이트이며 địaChỉ 체계는 ThiếtBị giáTrịByte giáTrịDãy, 접속번호와 IP 주소는 네트워크 giáTrịByte 차례다. 축소된 địaChỉ 버퍼에도 들어가는 앞부분을 쓰고 전체 địaChỉ cỡ 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 chươngTrìnhRa, 2·3은 기존 cácĐốiSố 조회다. phầnMụcHiệnTại 커널의 cácĐốiSố 목록이 thựcThiLệnh 이름을 제외하므로 C 진입기는 argv[0]에 고정 ChuỗiKýTự `jkoros-app`을 넣고 giáTrịSau 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX giáTrịTiếnTrình ABI와 다른 점이다.

표준 헤더의 SốNguyên cỡ, giáTrịCácCờ giáTrị, stat giáTrịTrường 순서는 `mãNguồn/TệpĐầuMục/`에 정의한다. 동적 nốiKết·다중 giáTrịTiếnTrình·스레드가 추가되면 lỗi sốHiệu 저장과 giáTrịTàiNguyên 수명, gọiThựcHiện 경계도 함께 검토해야 한다.
