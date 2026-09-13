package fat

//import . "unsafe"
import . "util"
import . "단말기"
import . "구동장치들/고급기술결합"
import . "파일시스템/MSDOS파티션"

type T바이오스파라미터블록32 struct{
	jmp [3] uint8	
	softName [8] byte
	bytesPerSector uint16
	sectorsPerCluster uint8
	reservedSectors uint16
	fatCopies uint8
	rootDirEntries uint16
	totalSectors uint16
	mediaType uint8
	fatSectorCount uint16
	sectorPerTrack uint16
	headCount uint16
	hiddenSectors uint32
	totalSectorCount uint32

	tableSize uint32
	extFlags uint16
	fatVersion uint16
	rootCluster uint32
	fatInfo uint16
	backupSector uint16
	reserved0 [12]uint8
	driveNumber uint8
	reserved uint8
	bootSignature uint8
	volumeId uint32
	volumeLabel [11]byte
	fatTypeLabel [8]byte	
}

func (자신 *T바이오스파라미터블록32) M초기화( data [90] byte){
	copy(자신.jmp[:3], data[0:3])
	copy(자신.softName[:8], data[3:11])
	
	자신.bytesPerSector = (uint16(data[11]) | uint16(data[12]) << 8)
	자신.sectorsPerCluster = data[13]
	자신.reservedSectors = (uint16(data[14]) | uint16(data[15]) << 8)
	자신.fatCopies = data[16]
	자신.rootDirEntries = (uint16(data[17]) | uint16(data[18]) << 8)
	자신.totalSectors = (uint16(data[19]) | uint16(data[20]) << 8)
	자신.mediaType = data[21]
	자신.fatSectorCount = (uint16(data[22]) | uint16(data[23]) << 8)
	자신.sectorPerTrack = (uint16(data[24]) | uint16(data[25]) << 8)
	자신.headCount = (uint16(data[26]) | uint16(data[27]) << 8)
	
	var buf1 [4]byte
	copy(buf1[:4], data[28:32])	
	자신.hiddenSectors = Uint32_R(ArrayToUint32(buf1))

	copy(buf1[:4], data[32:36])	
	자신.totalSectorCount = Uint32_R(ArrayToUint32(buf1))

	copy(buf1[:4], data[36:40])	
	자신.tableSize = Uint32_R(ArrayToUint32(buf1))

	자신.extFlags = (uint16(data[40]) | uint16(data[41]) << 8)
	자신.fatVersion = (uint16(data[42]) | uint16(data[43]) << 8)

        copy(buf1[:4], data[44:48])    
        자신.rootCluster = Uint32_R(ArrayToUint32(buf1))

	자신.fatInfo = (uint16(data[48]) | uint16(data[49]) << 8)
	자신.backupSector = (uint16(data[50]) | uint16(data[51]) << 8)

	copy(자신.reserved0[:12], data[52:64])
	
	자신.driveNumber = data[64]
	자신.reserved = data[65]
	자신.bootSignature = data[66]

        copy(buf1[:4], data[67:71])
        자신.volumeId = Uint32_R(ArrayToUint32(buf1))
	
	copy(자신.volumeLabel[:11], data[71:82])
	copy(자신.fatTypeLabel[:8], data[82:90])


}

var 단말기 = T단말기{}
func (자신 *T바이오스파라미터블록32) Len(hd *T고급기술결합, partEntry T파티션테이블엔트리, filename []byte) uint32{

	if partEntry.Partition_id == 0x00 {
		return 0
	}

	var buf1 [90]byte
	var bpbBytes = buf1[:]
	var partitionOffset = partEntry.Start_lba

	hd.M읽기28(partitionOffset, &bpbBytes, 90)

	var bpb = T바이오스파라미터블록32{}
	bpb.M초기화(buf1)

	var fatStart = partitionOffset + uint32(bpb.reservedSectors)
	var fatSize = bpb.tableSize
	
	var dataStart = fatStart + fatSize*uint32(bpb.fatCopies)

	var rootStart = dataStart + uint32(bpb.sectorsPerCluster)*(bpb.rootCluster-2)
	
	var buf2 [512]byte
	var direntBytes = buf2[:]
	hd.M읽기28(rootStart, &direntBytes, 512)

	var dirent = [16] T디렉토리엔트리FAT32{}

	for i:=0; i<16; i++{

		var buf3 [32] byte
		copy(buf3[:32], direntBytes[i*32:(i+1)*32])
		dirent[i].M초기화(buf3)	
	
		if dirent[i].name[0] == 0x00{
			break
		}

		if dirent[i].size >= 0xFFFFFFFF {
			continue
		}

		단말기.M출력(([]byte)("["))
		단말기.M출력(dirent[i].name[:len(dirent[i].name)])
		단말기.M출력(([]byte)("."))
		단말기.M출력(dirent[i].ext[:3])
		단말기.M출력(([]byte)(":"))
		if !EqualBytes(filename, dirent[i].name[:len(filename)]) {
			continue
		}
		단말기.MUint32출력(dirent[i].size)
		return dirent[i].size
	}
	return 0
}
func (자신 *T바이오스파라미터블록32) Read(hd *T고급기술결합, partEntry T파티션테이블엔트리, filename []byte, data []byte){


	if partEntry.Partition_id == 0x00 {
		return
	}

	var buf1 [90]byte
	var bpbBytes = buf1[:]
	var partitionOffset = partEntry.Start_lba

	hd.M읽기28(partitionOffset, &bpbBytes, 90)

	var bpb = T바이오스파라미터블록32{}
	bpb.M초기화(buf1)

	var fatStart = partitionOffset + uint32(bpb.reservedSectors)
	var fatSize = bpb.tableSize
	
	var dataStart = fatStart + fatSize*uint32(bpb.fatCopies)

	var rootStart = dataStart + uint32(bpb.sectorsPerCluster)*(bpb.rootCluster-2)
	
	var buf2 [512]byte
	var direntBytes = buf2[:]
	hd.M읽기28(rootStart, &direntBytes, 512)

	var dirent = [16] T디렉토리엔트리FAT32{}

	for i:=0; i<16; i++{

		var buf3 [32] byte
		copy(buf3[:32], direntBytes[i*32:(i+1)*32])
		dirent[i].M초기화(buf3)	
	
		if dirent[i].name[0] == 0x00{
			break
		}

		if dirent[i].size >= 0xFFFFFFFF {
			continue
		}

		단말기.M출력(([]byte)("["))
		단말기.M출력(dirent[i].name[:len(dirent[i].name)])
		if !EqualBytes(filename, dirent[i].name[:len(filename)]) {
			continue
		}
		단말기.M출력(([]byte)("."))
		단말기.M출력(dirent[i].ext[:3])
		단말기.M출력(([]byte)(":"))
		단말기.MUint32출력(dirent[i].size)

		var firstFileCluster = (uint32(dirent[i].firstClusterHi) << 16 | uint32(dirent[i].firstClusterLow))

		var SIZE = int32(dirent[i].size)
		var nextFileCluster = int32(firstFileCluster)
		var buffer [513] byte
		var fatbuffer [513]byte


		for ; SIZE>0; {
			var fileSector = dataStart  + uint32(bpb.sectorsPerCluster)*uint32(nextFileCluster-2)
			var sectorOffset int = 0

			for ; SIZE>0; SIZE -= 512{
				
				var buf3 []byte

				if dirent[i].size > 512 {
					buf3 = buffer[:512]
					hd.M읽기28(fileSector+uint32(sectorOffset), &buf3, 512)
		
				}else{
					buf3 = buffer[:dirent[i].size]
					hd.M읽기28(fileSector+uint32(sectorOffset), &buf3, int(dirent[i].size))
				}

				copy(data[int32(dirent[i].size) - SIZE:], buf3)
				/*
				if SIZE > 512 {
					copy(data[dirent[i].size - SIZE:], buf3)
					//copy(data[sectorOffset*512:], buf3)
				}else{
					copy(data[:SIZE], buf3)
					//copy(data[sectorOffset*512:], buf3)
				}
				*/
			
				//단말기.M출력(buf3)
				//data = append(data, buf3...)
				//copy(data, buf3)

				sectorOffset++
		
				if sectorOffset > int(bpb.sectorsPerCluster) {
					break
				}

			}

			var fatSectorForCurrentCluster = uint32(nextFileCluster/128)
			var fatbuf = fatbuffer[:512]
			hd.M읽기28(fatStart+fatSectorForCurrentCluster, &fatbuf, 512)

			var fatOffsetInSectorForCurrentCluster = nextFileCluster % 128
			var startOffset  = fatOffsetInSectorForCurrentCluster*4
			var endOffset  = fatOffsetInSectorForCurrentCluster*4+4

			var buf4[4]byte 
			copy(buf4[:4], fatbuffer[startOffset:endOffset])
			
			nextFileCluster = int32(Uint32_R(ArrayToUint32(buf4)))
		}
	}
}

type T디렉토리엔트리FAT32 struct{
	name [8]byte
	ext [3]byte
	attributes uint8
	reserved uint8
	cTimeTenth uint8
	cTime uint16
	cDate uint16
	aTime uint16
	firstClusterHi uint16
	wTime uint16
	wDate uint16
	firstClusterLow uint16
	size uint32
}

func (자신 *T디렉토리엔트리FAT32) MTest(){
}
func (자신 *T디렉토리엔트리FAT32) M초기화(data [32]byte) {
	copy(자신.name[:8], data[0:8])
	copy(자신.ext[:3], data[8:11])
	자신.attributes = data[11]
	자신.reserved = data[12]
	자신.cTimeTenth = data[13]
	자신.cTime = uint16(data[14]) | uint16(data[15]) << 8
	자신.cDate = uint16(data[16]) | uint16(data[17]) << 8
	자신.aTime = uint16(data[18]) | uint16(data[19]) << 8
	자신.firstClusterHi = uint16(data[20]) | uint16(data[21]) << 8
	자신.wTime = uint16(data[22]) | uint16(data[23]) << 8
	자신.wDate = uint16(data[24]) | uint16(data[25]) << 8
	자신.firstClusterLow = uint16(data[26]) | uint16(data[27]) << 8
	
	var buf [4] byte
	copy(buf[:4], data[28:32])
	자신.size = Uint32_R(ArrayToUint32(buf))
}
