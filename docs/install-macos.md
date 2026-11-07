# ติดตั้ง LightCraft บน Mac / macOS installation

**รุ่นไทยยังไม่เผยแพร่** ขั้นตอนนี้ใช้ไฟล์ต้นฉบับ [v0.19.0](https://github.com/storytold/lightcraft/releases/tag/v0.19.0)

1. ตรวจรุ่น macOS และชิปจาก Apple → About This Mac และอ่านข้อกำหนดระบบใน Release
2. [ดาวน์โหลด Mac Universal DMG ต้นฉบับ](https://github.com/storytold/lightcraft/releases/download/v0.19.0/lightcraft-0.19.0-macos-universal.dmg) หรือเปิด Assets ใน Release
3. บันทึกงานและปิดแอปเดิม เปิด DMG แล้วลากแอปเข้า Applications
4. Eject ดิสก์ติดตั้ง แล้วเปิดแอปจาก Applications
5. ตรวจ [SHA-256 ของต้นฉบับ](https://github.com/storytold/lightcraft/releases/download/v0.19.0/SHA256SUMS.txt) ให้ตรงกับชื่อไฟล์และรุ่นเดียวกัน

Source code ZIP ต้อง build ก่อน ไม่ใช่แอปพร้อมติดตั้ง การเซ็นและข้อกำหนดระบบให้ยึด Release ต้นฉบับ ไม่ใช้สถานะ ad-hoc ของแอปรุ่นไทยตัวอื่นมาอธิบายไฟล์นี้

อ่าน [คู่มือ GitHub/DMG บนวันละ Craft](https://tapanapon.com/blog/one-per-craft-install-mac-github) โดยสังเกตว่าตาราง TH ในบทความเป็นคนละรุ่นกับลิงก์ต้นฉบับของแอปนี้

## English

No Thai installer is published for this project yet. Download the verified upstream v0.19.0 Universal DMG, check its system requirements and matching checksum, quit the old app, drag the app to Applications, eject the image and launch from Applications. Use the upstream release's signing and compatibility notes.
