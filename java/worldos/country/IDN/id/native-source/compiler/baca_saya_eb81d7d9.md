# Java 네이티브 컴파일러

OpenJDK Asli 소스를 빌드하는 **`--target openjdk-build`**와 Asli kernel_VALUE ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [bangun 방법·aktual_data validasi·kernel_VALUE 이식 klip](OpenJDK-sumber_build_AND-자체커널-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C buat 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `컴파일러.py`는 이전 perintah·API 및 OpenJDK 도구를 위한 호환 진입점이다. Asli Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 이전 경로와 Python 호출을 위한 호환 진입점이다. fungsi_VALUE·variabel_VALUE·buat C 이름의 뜻과 예외는 [Indonesia 명명 baca_saya_eb81d7d9](../platforms/rpi4-native/명명/baca_saya_eb81d7d9.md)를 참고한다. [ARM64 bangun·dukung_VALUE klip](../platforms/rpi4-native/baca_saya_eb81d7d9.md)에 Jalankan_perintah 조건이 있다. 전체 OpenJDK나 일반 Kelas_VALUE 실행기는 아니다.

Jalankan_perintah 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java Asli AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·akses_entri kontrol_VALUE·TYPE_VALUE 검사는 JDK의 `javac`에 맡기고, Java 8 Kelas_VALUE 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java kodeSumber → javac의 문법·TYPE_VALUE 검사 → 임시 .class
          → Asli x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 Jalankan_perintah

bangun host: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. saat_ini_item 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. eksternal_VALUE Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 pengujian 성공

python3 컴파일러.py --target linux --entry 계산.jalankan \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 Jalankan_perintah 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 수 있다. 정상 Linux host 또는 해당 실행을 허용한 pengujian 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int jalankan()` 또는 `static void jalankan()`처럼 인수가 없어야 한다. `--entry 패키지.Kelas_VALUE.fungsi_VALUE`로 선택한다. `int` 반환값은 Linux 프로세스 Keluar_apl 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` Jalankan_perintah 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 awal_mesin 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target kernel --entry Inti.jalankan \
    --export kernel_dispatch=panggilan_sistem.Proses_VALUE_entri \
    -o os/build/java.o os/kodeSumber/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `ruang_pengguna` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `Ponsel_VALUE` 클래스의 하드웨어 직접 접근은 거부한다. ruang_pengguna ELF는 Linux Jalankan_perintah berkas ABI와 다르므로 호스트에서 실행하지 않는다. buat·daftar_entri 방법은 [ruang_pengguna Jalankan_perintah baca_saya_eb81d7d9](../os/ruang_pengguna/baca_saya_eb81d7d9.md)에 있다. `--export 외부기호=Kelas_VALUE.fungsi_VALUE`는 오버로드되지 않은 statik_VALUE 함수를 Asli operand_tumpuk ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. keluaranTeks 옆의 `.s`는 생성된 어셈블리, `.json`은 kodeSumber SHA-256 및 네이티브 simbol↔Java fungsi_VALUE 대응표다. Indonesia 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 mesin 기호를 쓴다. bangun_sumber·조립·Sambung 중 실패하면 기존 hasil 파일을 덮어쓰지 않는다.

## dukung_VALUE klip

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TYPE_VALUE CONVERT_VALUE.
- statik_VALUE 필드와 statik_VALUE fungsi_VALUE, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 inisialisasi Siklus_VALUE.
- 조건문, 반복문, 단락 평가, 삼항식, bilangan_bulat `switch`, 넓은 lokal_Cakupan variabel_VALUE 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_VALUE 연산과 gerak_VALUE. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` buat·초기값 0·panjang_VALUE·Baca·Tulis·Referensi 비교. 256KiB 고정 ARRAY_VALUE wilayah_VALUE, 널/subskrip_VALUE/Ukuran/surel_wilayah 검사.
- string_VALUE 리터럴과 `String` Referensi, `length()` 및 `charAt()`. 문자열은 UTF-16 CODE_VALUE 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- Indonesia Kelas_VALUE·fungsi_VALUE·variabel_VALUE·berkas Nama_2.

`new Object`, 인스턴스 nilai_bidang/fungsi_VALUE, 상속/인터페이스, `long/float/double` Jalankan_perintah bedah_VALUE, `int[]` 이외 ARRAY_VALUE, string_VALUE 동적 결합, Java 표준 pustaka, pengecualian Proses_VALUE_entri, 스레드·sinkro·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 eksternal_VALUE 호출을 발견하면 실패한다. 사용되지 않는 nilai_default 생성자는 Jalankan_perintah 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 수 있다는 뜻은 아니다.

pengecualian objek_VALUE 대신 런타임 galat 번호로 중단한다. Linux와 jkoros ruang_pengguna 대상에서는 `100 + INDEX`로 종료하고 kernel_VALUE 대상에서는 `JKOROS PANIC INDEX`를 출력하고 정지한다. ruang_pengguna 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEX | 원인 |
| --- | --- |
| 1 | 0으로 Divisi_KR |
| 2 | 널 Referensi |
| 3 | ARRAY_VALUE/string_VALUE subskrip_VALUE klip 초과 |
| 4 | 음수 ARRAY_VALUE Ukuran |
| 5 | ARRAY_VALUE wilayah_VALUE 부족 |

ARRAY_VALUE 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 경계 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kernel_VALUE 및 신뢰할 수 있는 작은 프로그램용 keadaan_awal 구현이다.

## native 경계와 ABI

kernel_VALUE 대상에서는 `os/kodeSumber/Ponsel_VALUE.java`, ruang_pengguna 대상에서는 `os/ruang_pengguna/deklarasi_4f4f026b/ruang_pengguna.java`의 정확한 metode_nama_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/ruang_pengguna 대상의 하드웨어 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java kodeSumber 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 Kelas_VALUE jalur/kodeSumber 경로에서 명시한 소스만 컴파일한다.

## 검증과 implementasi 근거

`pengujian/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 bedah_VALUE hasil 대조, Kelas_VALUE inisialisasi, bilangan_bulat 극값, string_VALUE/ARRAY_VALUE, 재귀·switch·wide, 런타임 오류와 미지원 기능 tolak_VALUE, kegagalan_VALUE 시 keluaranTeks 보존, ruang_pengguna ELF/izin_VALUE 경계 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

perintah 의미와 Kelas_VALUE berkas 형식은 Oracle의 [JVM perintah spes](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [Kelas_VALUE berkas spes](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
