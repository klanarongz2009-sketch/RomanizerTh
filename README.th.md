# RomanizerTh (ภาษาไทย)

RomanizerTh เป็น Python library และ command-line tool ขนาดเล็ก ไม่มี dependency สำหรับถอดอักษรไทยเป็นอักษรโรมันตาม scheme เฉพาะของโปรเจกต์นี้ แปลงทีละตัวอักษรจากตาราง mapping ตารางเดียว ออกเป็นตัวพิมพ์เล็ก เก็บช่องว่าง เครื่องหมายวรรคตอน และข้อความที่ไม่ใช่ภาษาไทยไว้ตามเดิม และรองรับทุก code point ใน Thai Unicode block

English: [README.md](README.md)

> โปรดอ่าน [PROJECT_NOTICE.md](PROJECT_NOTICE.md) (ภาษาอังกฤษ): โปรเจกต์นี้มีผู้ดูแลคนเดียว เข้ามาดูไม่สม่ำเสมอ และอาจตอบช้า

## ติดตั้ง

```sh
pip install git+https://github.com/klanarongz2009-sketch/RomanizerTh
```

ต้องใช้ Python 3.10 ขึ้นไป

## วิธีใช้

```python
from romanizer_th import romanize

print(romanize("สวัสดี"))  # swasde
print(romanize("อะไรใหม่ๆ"))  # oairihmm
```

Command line:

```sh
romanizerth วันจันทร์          # wanjantr
romanizerth สวัสดี ครับ        # swasde crab
echo "ดีๆ" | romanizerth      # dee (ถ้าไม่ใส่ข้อความ จะอ่านจาก standard input)
romanizerth --version
```

## หลักการทำงาน

1. ทำ NFC normalization และรวม `ํ` + `า` เป็น `ำ` ดังนั้น `ทํา` กับ `ทำ` ได้ `tum` เหมือนกัน
2. แทนอักษรไทยทีละตัวตามตาราง สระนำ (เ แ โ ใ ไ) ออกตามตำแหน่งที่พิมพ์ ไม่สลับลำดับ
3. วรรณยุกต์และเครื่องหมายที่ไม่มีค่าในตารางจะถูกข้าม
4. `ๆ` ซ้ำอักษรโรมันตัวสุดท้ายที่ออกมาก่อนหน้า: `ดีๆ` ได้ `dee`, `อะไรใหม่ๆ` ได้ `oairihmm` ช่องว่างก่อน `ๆ` จะถูกตัด
5. เลขไทยแปลงเป็นเลขอารบิก ยกเว้น `๕` (ดูคำถามที่ยังเปิดอยู่) ส่วน `ฯ`, `฿` และเครื่องหมายไทยอื่นคงไว้ตามเดิม

ไม่มีการ hard-code ทั้งคำ คำเดียวกันจึงได้ผลเหมือนกันทั้งตอนอยู่เดี่ยวและอยู่ในประโยค ตารางเต็มทุก code point อยู่ที่ [docs/SCHEME.md](docs/SCHEME.md)

## ตัวอย่าง

| Input | Output |
| --- | --- |
| วันจันทร์ | `wanjantr` |
| สวัสดี | `swasde` |
| อะไรใหม่ | `oairihm` |
| อะไรใหม่ๆ | `oairihmm` |
| ดีๆ | `dee` |
| สามารถ | `samart` |
| หนังสือ | `hnangsueo` |
| ฮา | `ha` |
| ๑๒๓ | `123` |

## คำถามที่ยังเปิดอยู่

ตัวอย่าง 3 คำในสเปกต้นฉบับขัดกับตาราง mapping ตอนนี้ library ยึดตาราง และเก็บแต่ละคำเป็น test แบบ `xfail` ไว้จนกว่าจะตัดสิน

| คำ | ตัวอย่างในสเปก | ผลจากตาราง | จุดที่ต่าง |
| --- | --- | --- | --- |
| เป็น | `apn` | `aphn` | ตาราง map ป เป็น `ph` |
| คำ | `kum` | `cum` | ตาราง map ค เป็น `c` |
| ฤดี | `hruede` | `ruede` | ตัวอย่างมี `h` นำหน้าที่ไม่มีแถวไหนในตารางให้ |

แถว `ณ น ๕ → n` ยังคงไว้ตามที่เขียน `๕` อาจเป็นการพิมพ์ผิดของ `ณ`

## พัฒนา

```sh
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest -v
```

## License

ยังไม่ได้เลือก license จนกว่าจะเพิ่มไฟล์ LICENSE สงวนสิทธิ์ทั้งหมดโดยผู้เขียน
