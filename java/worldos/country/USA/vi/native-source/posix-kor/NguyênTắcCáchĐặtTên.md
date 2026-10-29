# tiếngViệt cáchĐặtTên 원칙과 근거

이 문서의 새 이름은 jkoros 프로젝트의 선택이다. tiếngViệt 전체나 특정 국가의 유일한 NgônNgữ 철학을 대표한다고 주장하지 않는다. 기존에 분명한 용어는 유지하고, 모호한 음역이나 여러 의미가 섞인 이름은 phầnMụcHiệnTại 코드의 동작을 중심으로 고친다. 다른 언어판은 giáTrịĐốiĐích 언어와 용례를 별도로 검토해야 한다.

함수는 대상과 동작을 결합한다. `đọcDữLiệuTệp`, `dịchVịTệp`, `ràngBuộcĐịaChỉ`처럼 무엇에 무엇을 하는지 이름에서 읽히게 한다. 변수는 값의 역할과 단위를 나타내도록 `bộMôTảTệp`, `sốLượngByte`, `nhậnMiliGiâyHếtGiờ`, `sốThếHệ`로 쓴다. 구동기는 장치를 움직이는 phầnCàiĐặt, 처리기는 특정 입력을 처리하는 구현으로 구분한다.

어원은 설계 개념을 이해하는 근거로 사용한다. 역사적 은유를 그대로 번역해서 phầnMụcHiệnTại 동작을 흐리게 만들지 않는다. 확인되지 않은 고어·최초 giáTrịDùng 시점은 만들어 넣지 않는다. 아래의 tiếngViệt 표현이 해당 시기의 dữLiệuThựcTế 번역어였다는 의미도 아니다.

| 개념 | 선택한 tên | 의미와 역사적 근거 |
|---|---|---|
| file descriptor | bộMôTảTệp | 열린 대상을 가리키는 SốNguyên giáTrịCănCước. trạngTháiBanĐầu UNIX 문헌도 open/create가 돌려주는 서술자로 시스템 표의 đầuRaĐầuVào 위치를 찾는 구조를 설명한다. tên ChuỗiKýTự·Tệp 본체·열린 Tệp 상태를 구분한다. |
| open file description | 열린 Tệp giáTrịBộMôTả | mở 설정과 phầnMụcHiệnTại 위치를 담는 공유 giáTrịTrạngThái. mụcBộMôTả 자체와 구별하는 POSIX의 정의를 따른다. |
| unlink | gỡTênMụcTệp | Tệp giáTrịNộiDung 즉시 폐기가 아닌 tên nốiKết gỡMục. 열린 참조가 남으면 내용이 살아 있는 의미를 반영한다. |
| seek / offset | dịchVịTệp / giáTrịĐộLệch | 읽고 쓰는 위치를 기준점에서 이동한다. 수색·탐색이라는 일반어보다 해당 함수의 phầnMụcHiệnTại 역할을 표현한다. |
| socket | ĐiểmCuốiỔCắmMạng | 통신이 드나드는 논리적 điểmKếtThúc. 1971년 RFC 147도 전송의 giáTrịRờiĐi·giáTrịĐến 식별자로 socket을 설명했다. 당시 32비트·짝홀 구분을 현대 API에 그대로 적용하지 않는다. |
| network port | sốCổng | 인터넷 địaChỉ 안에서 TruyềnThông 상대를 구분하는 sốHiệu. RFC 768의 giáTrịRờiĐi/giáTrịĐến cổngPhầnCứng 정의를 반영하며 CPU đầuRaĐầuVào 주소와 구별한다. |
| datagram | 자료전문 | 경계를 가진 하나의 메시지. RFC 768의 datagram 방식과 UDP độDài 필드가 가리키는 단위를 드러낸다. |
| driver | 구동기 | ThiếtBị 초기화와 송수신 명령을 수행하는 giáTrịMã. RTL8139 phầnCàiĐặt 이름은 망장치구동기다. |
| RAM file | HệTệpBộNhớ | thựcThiLệnh 중 자료가 주기억에 놓이는 KiếnTrúc. thiếtBịLưuTrữ 보존 계층과 역할을 구분한다. |
| snapshot / generation | saoChépĐãGiữNguyên / sốThếHệ | đồngBộHóa 시점의 Tệp 표와 DữLiệu 전체 및 그 giáTrịThứTự. 단순한 백업 làĐầyĐủ 표식과 dữLiệuThựcTế 본문을 구분한다. |
| stream | Tệp giáTrịVào/ĐầuRa giáTrịLuồng | 바이트를 순서대로 읽고 쓰는 hànhĐộng. 표준 Java 클래스의 이름은 호환성을 위해 FileInputStream/FileOutputStream으로 유지한다. |

표의 UNIX 역사 서술은 [Ritchie·Thompson의 UNIX 논문 재록본](https://cm-bell-labs.github.io/who/dmr/cacm.html)에 근거한다. 열린 giáTrịTrạngThái·vịTrí·삭제의 의미는 POSIX의 [open](https://pubs.opengroup.org/onlinepubs/9799919799/functions/open.html), [dup](https://pubs.opengroup.org/onlinepubs/9799919799/functions/dup.html), [lseek](https://pubs.opengroup.org/onlinepubs/9799919799/functions/lseek.html), [unlink](https://pubs.opengroup.org/onlinepubs/000095399/functions/unlink.html)를 참고했다. TruyềnThông 용어의 역사와 phầnMụcHiệnTại 규약은 [RFC 147](https://www.rfc-editor.org/info/rfc147/)과 [RFC 768](https://www.rfc-editor.org/info/rfc768/)을 참고했다.

표준 이름을 번역된 심벌로 강제로 바꾸면 기존 프로그램과 도구가 연결되지 않는다. 따라서 POSIX/C의 공개 심벌, Java 표준 giáTrịLớp·giáTrịPhươngThức, ELF/x86 ABI, giáTrịPhầnCứng 레지스터 명칭과 `Makefile` 같은 CôngCụ giáTrịĐiểmMục 파일은 유지한다. tiếngViệt API는 같은 동작의 별칭이다. `đọcCổngPhầnCứng` 같은 프로젝트 내부 식별자는 đầuRaĐầuVào giáTrịByte 접근으로 뜻을 좁혀 dữLiệuThựcTế 코드와 네이티브 연결표까지 함께 바꿨다. dữLiệuThựcTế 적용 목록은 [phépÁnhXạThuậtNgữ.tsv](phépÁnhXạThuậtNgữ.tsv)에 있다.
