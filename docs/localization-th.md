# LightCraft TH: ติดตั้งจาก GitHub และเชื่อม Codex / Claude

เริ่มจาก [README](../README.md) สำหรับ DMG/MSI/Portable วิธีนี้สำหรับผู้ที่ต้องการ build ซอร์สหรือใช้ CLI ของรุ่นไทย 0.20.0-th.1

## ใช้ซอร์สบน Mac

ติดตั้ง Xcode Command Line Tools, Git และ Rust ที่รองรับ edition 2024 (อย่างน้อยเวอร์ชันที่ระบุใน `Cargo.toml`) จากนั้นใช้ Terminal:

```sh
git clone https://github.com/tapanapon-com/lightcraft-th.git
git clone https://github.com/storytold/craft-fonts.git
git -C craft-fonts checkout b076417b5880bd4154bd22f00695b1d28c6bea83
cd lightcraft-th
git checkout v0.20.0-th.1
CRAFT_FONTS_DIR=../craft-fonts CRAFT_FONTS_REQUIRED=1 \
  cargo build --release --locked -p lightcraft -p lightcraft-cli \
  --features lightcraft/heif,lightcraft-cli/heif
./target/release/lightcraft --memory
```

`--memory` เปิดคลังภาพสาธิตในหน่วยความจำ ใช้ `--library "/absolute/path/to/library"` เมื่อต้องการเก็บคลังภาพจริง อย่าใช้คลังภาพเดียวกันพร้อมกันในหลายโปรแกรม

## ใช้ซอร์สบน Windows

ติดตั้ง Git, Rust แบบ MSVC และ Visual Studio Build Tools พร้อม Desktop development with C++ / Windows SDK เพื่อให้มี linker จากนั้นเปิด PowerShell ในโฟลเดอร์งาน:

```powershell
git clone https://github.com/tapanapon-com/lightcraft-th.git
git clone https://github.com/storytold/craft-fonts.git
git -C craft-fonts checkout b076417b5880bd4154bd22f00695b1d28c6bea83
Set-Location lightcraft-th
git checkout v0.20.0-th.1
$env:CRAFT_FONTS_DIR = (Resolve-Path ..\craft-fonts).Path
$env:CRAFT_FONTS_REQUIRED = '1'
cargo build --release --locked -p lightcraft -p lightcraft-cli --features lightcraft/heif,lightcraft-cli/heif
.\target\release\lightcraft.exe --memory
```

การ build นี้ให้ executable สำหรับเครื่องที่ใช้ build ไม่ได้สร้าง MSI ให้โดยอัตโนมัติ การสร้างแพ็กเกจใช้ `packaging/windows/package.ps1` พร้อม WiX ตามเอกสารใน script

## ตำแหน่ง CLI ที่ติดตั้งแล้ว

| ระบบ | ตัวอย่างพาธ |
| --- | --- |
| Mac | `/Applications/LightCraft.app/Contents/MacOS/lightcraft-cli` |
| Windows ติดตั้งเฉพาะผู้ใช้ | `%LOCALAPPDATA%\Programs\ArtCraft\LightCraft\lightcraft-cli.exe` |
| Windows ติดตั้งทุกผู้ใช้ | `C:\Program Files\ArtCraft\LightCraft\lightcraft-cli.exe` |
| Windows Portable | `lightcraft-cli.exe` ในโฟลเดอร์ที่แตก ZIP |

เลือกพาธตามตำแหน่งติดตั้งจริง CLI ไม่จำเป็นต้องอยู่ใน PATH

## Codex: เริ่มจากคลังภาพสาธิต

```sh
codex mcp add lightcraft -- "/Applications/LightCraft.app/Contents/MacOS/lightcraft-cli" mcp --demo
codex mcp list
```

Windows PowerShell:

```powershell
codex mcp add lightcraft -- "$env:LOCALAPPDATA\Programs\ArtCraft\LightCraft\lightcraft-cli.exe" mcp --demo
```

`mcp --demo` เป็นคลังภาพสังเคราะห์ในหน่วยความจำ ไม่เปลี่ยนหน้าต่างแอปที่เปิดอยู่ เมื่อต้องการเก็บงานระหว่าง session ให้แทน `--demo` ด้วย `--library` และ absolute path ของคลังภาพทดสอบที่คุณเลือก

## Claude Code / Claude Desktop

```sh
claude mcp add --transport stdio lightcraft -- "/Applications/LightCraft.app/Contents/MacOS/lightcraft-cli" mcp --demo
```

Claude Desktop ใช้ config รูปแบบนี้ เปลี่ยน `command` เป็นพาธจริงบนเครื่อง ถ้าเป็น Windows ให้ escape `\` เป็น `\\` ใน JSON:

```json
{
  "mcpServers": {
    "lightcraft": {
      "command": "/Applications/LightCraft.app/Contents/MacOS/lightcraft-cli",
      "args": ["mcp", "--demo"]
    }
  }
}
```

## ให้ AI ทำงานกับหน้าต่างที่เปิดอยู่

เปิดแอปบน loopback control port แล้วลงทะเบียน MCP แบบ connect:

```sh
"/Applications/LightCraft.app/Contents/MacOS/LightCraft" --library "/absolute/path/to/test-library" --control 7980
codex mcp add lightcraft-app -- "/Applications/LightCraft.app/Contents/MacOS/lightcraft-cli" mcp --connect 127.0.0.1:7980
```

LightCraft ใช้ `--connect` สำหรับ live mode คลังภาพเปิดได้ทีละโปรแกรม ถ้า GUI เปิดคลังภาพนั้นอยู่ ให้ใช้ connect แทนการเปิด `mcp --library` ซ้ำ Headless เปิดคลังภาพของตัวเองและไม่ได้ควบคุมหน้าต่าง GUI

LightCraft ไม่มี `--automation-read-root` / `--automation-write-root` แบบ PhotoCraft หรือ VectorCraft; `--library` ระบุตำแหน่งคลังภาพ ไม่ใช่การจำกัดสิทธิ์อ่านเขียนไฟล์ โปรแกรมทำงานตามสิทธิ์ผู้ใช้ จึงเริ่มจากคลังภาพทดสอบและภาพสำเนาที่เลือกไว้

หลังลงทะเบียน ให้โหลดการเชื่อมต่อ MCP ใหม่และลองให้ client เรียกตรวจคลังภาพก่อนเริ่มแก้ไข `codex mcp list` ยืนยันการลงทะเบียนเท่านั้น ตัวอย่างคำสั่ง: “ตรวจรายการภาพในคลังสาธิตก่อน เลือกภาพหนึ่ง ปรับการรับแสงเล็กน้อย แล้วแสดง preview ก่อนส่งออกเป็นไฟล์ใหม่”

รายละเอียดเครื่องมือและ protocol: [MCP ต้นฉบับ](mcp.md) · [control protocol](control-protocol.md)
