package fat

import . "util"
import . "drivers/ata"
import . "filesystem/msdospart"

type T바이오스_파라미터_블록32 struct{
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

func (self *T바이오스_파라미터_블록32) M초기화( data [90] byte){
	copy(self.jmp[:3], data[0:3])
	copy(self.softName[:8], data[3:11])
	
	self.bytesPerSector = (uint16(data[11]) | uint16(data[12]) << 8)
	self.sectorsPerCluster = data[13]
	self.reservedSectors = (uint16(data[14]) | uint16(data[15]) << 8)
	self.fatCopies = data[16]
	self.rootDirEntries = (uint16(data[17]) | uint16(data[18]) << 8)
	self.totalSectors = (uint16(data[19]) | uint16(data[20]) << 8)
	self.mediaType = data[21]
	self.fatSectorCount = (uint16(data[22]) | uint16(data[23]) << 8)
	self.sectorPerTrack = (uint16(data[24]) | uint16(data[25]) << 8)
	self.headCount = (uint16(data[26]) | uint16(data[27]) << 8)
	
	var buf1 [4]byte
	copy(buf1[:4], data[28:32])	
	self.hiddenSectors = Uint32_R(ArrayToUint32(buf1))

	copy(buf1[:4], data[32:36])	
	self.totalSectorCount = Uint32_R(ArrayToUint32(buf1))

	copy(buf1[:4], data[36:40])	
	self.tableSize = Uint32_R(ArrayToUint32(buf1))

	self.extFlags = (uint16(data[40]) | uint16(data[41]) << 8)
	self.fatVersion = (uint16(data[42]) | uint16(data[43]) << 8)

        copy(buf1[:4], data[44:48])    
        self.rootCluster = Uint32_R(ArrayToUint32(buf1))

	self.fatInfo = (uint16(data[48]) | uint16(data[49]) << 8)
	self.backupSector = (uint16(data[50]) | uint16(data[51]) << 8)

	copy(self.reserved0[:12], data[52:64])
	
	self.driveNumber = data[64]
	self.reserved = data[65]
	self.bootSignature = data[66]

        copy(buf1[:4], data[67:71])
        self.volumeId = Uint32_R(ArrayToUint32(buf1))
	
	copy(self.volumeLabel[:11], data[71:82])
	copy(self.fatTypeLabel[:8], data[82:90])


}

func (self *T바이오스_파라미터_블록32) Len(hd *T고급기술결합, partEntry TPartitionTableEntry, filename []byte) uint32{

	if partEntry.Partition_id == 0x00 {
		return 0
	}

	var buf1 [90]byte
	var bpbBytes = buf1[:]
	var partitionOffset = partEntry.Start_lba

	hd.M읽기28(partitionOffset, &bpbBytes, 90)

	var bpb = T바이오스_파라미터_블록32{}
	bpb.M초기화(buf1)

	var fatStart = partitionOffset + uint32(bpb.reservedSectors)
	var fatSize = bpb.tableSize
	
	var dataStart = fatStart + fatSize*uint32(bpb.fatCopies)

	var rootStart = dataStart + uint32(bpb.sectorsPerCluster)*(bpb.rootCluster-2)
	
	var buf2 [512]byte
	var direntBytes = buf2[:]
	hd.M읽기28(rootStart, &direntBytes, 512)

	var dirent = [16] TDirectoryEntryFat32{}

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

		if !EqualBytes(filename, dirent[i].name[:len(filename)]) {
			continue
		}

		return dirent[i].size
	}
	return 0
}
func (self *T바이오스_파라미터_블록32) Read(hd *T고급기술결합, partEntry TPartitionTableEntry, filename []byte, data []byte){


	if partEntry.Partition_id == 0x00 {
		return
	}

	var buf1 [90]byte
	var bpbBytes = buf1[:]
	var partitionOffset = partEntry.Start_lba

	hd.M읽기28(partitionOffset, &bpbBytes, 90)

	var bpb = T바이오스_파라미터_블록32{}
	bpb.M초기화(buf1)

	var fatStart = partitionOffset + uint32(bpb.reservedSectors)
	var fatSize = bpb.tableSize
	
	var dataStart = fatStart + fatSize*uint32(bpb.fatCopies)

	var rootStart = dataStart + uint32(bpb.sectorsPerCluster)*(bpb.rootCluster-2)
	
	var buf2 [512]byte
	var direntBytes = buf2[:]
	hd.M읽기28(rootStart, &direntBytes, 512)

	var dirent = [16] TDirectoryEntryFat32{}

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

		if !EqualBytes(filename, dirent[i].name[:len(filename)]) {
			continue
		}

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

type TDirectoryEntryFat32 struct{
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
func (self *TDirectoryEntryFat32) M초기화(data [32]byte) {
	copy(self.name[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cTimeTenth = data[13]
	self.cTime = uint16(data[14]) | uint16(data[15]) << 8
	self.cDate = uint16(data[16]) | uint16(data[17]) << 8
	self.aTime = uint16(data[18]) | uint16(data[19]) << 8
	self.firstClusterHi = uint16(data[20]) | uint16(data[21]) << 8
	self.wTime = uint16(data[22]) | uint16(data[23]) << 8
	self.wDate = uint16(data[24]) | uint16(data[25]) << 8
	self.firstClusterLow = uint16(data[26]) | uint16(data[27]) << 8
	
	var buf [4] byte
	copy(buf[:4], data[28:32])
	self.size = Uint32_R(ArrayToUint32(buf))
}
