# Nubmark

**Catat koleksimu. Ikuti progres rakitanmu. Simpan cerita setiap kit.**

Nubmark adalah aplikasi Android yang dikembangkan untuk membantu penghobi Gunpla dan model kit plastik mengelola koleksi serta mendokumentasikan proses merakit. Mulai dari kit yang ingin dibeli, tumpukan backlog, hingga hasil rakitan yang selesai, semuanya direncanakan dapat dicatat dalam satu aplikasi.

Pendekatannya **local-first**: fitur utama ditargetkan dapat digunakan tanpa akun dan tanpa koneksi internet. Akun, pencadangan cloud, dan sinkronisasi antarperangkat akan hadir sebagai fitur opsional pada tahap berikutnya.

> **Status pengembangan:** tahap awal. Repository saat ini berisi kerangka aplikasi Android dengan Jetpack Compose dan dokumen perencanaan. Fitur produk di bawah merupakan target pengembangan, belum tersedia pada aplikasi saat ini.

## Mengapa Nubmark?

Koleksi yang bertambah sering membuat daftar kit, foto progres, waktu merakit, dan pengeluaran tersebar di banyak tempat. Nubmark dirancang untuk membantu menjawab:

- Kit apa saja yang sudah dimiliki dan mana yang masih masuk wishlist?
- Kit mana yang belum dirakit atau sedang dikerjakan?
- Seberapa jauh progres setiap rakitan?
- Berapa waktu dan biaya yang sudah dihabiskan untuk hobi ini?
- Bagaimana menyimpan catatan serta foto dari awal hingga hasil akhir?

## Fitur yang direncanakan

### Milestone A — Local MVP

| Fitur | Kegunaan |
|---|---|
| Manajemen koleksi | Menambah dan mengubah data kit, termasuk nama, grade, skala, seri, dan status. |
| Pencarian dan filter | Menemukan kit berdasarkan nama, status, dan grade. |
| Wishlist | Mencatat kit incaran dan memindahkannya ke koleksi setelah dibeli. |
| Checklist build | Mencatat tahap perakitan dengan progres berdasarkan tahapan yang berlaku. |
| Jurnal dan galeri foto | Menyimpan catatan bertanggal, foto progres, dan hasil akhir setiap kit. |
| Timer dan riwayat sesi | Mencatat durasi sesi merakit pada setiap kit. |
| Catatan pengeluaran | Mencatat biaya kit, cat, alat, dan kebutuhan lain dalam rupiah. |
| Ringkasan koleksi | Menampilkan jumlah kit, status rakitan, dan statistik dasar dari data pengguna. |
| Backup dan restore lokal | Mengekspor serta memulihkan data dan foto melalui arsip ZIP. |

Seluruh fitur pada milestone ini ditargetkan berjalan secara lokal tanpa backend.

### Milestone B — Cloud Beta

- Akun opsional untuk menghubungkan data lokal dengan layanan cloud.
- Pencadangan dan sinkronisasi koleksi, jurnal, sesi, pengeluaran, serta foto.
- Pemulihan data pada perangkat lain.
- Antrean perubahan saat offline dan penanganan konflik sinkronisasi.

Data lokal tetap menjadi sumber utama aplikasi. Pengguna direncanakan tetap dapat melihat dan mengedit koleksi tanpa koneksi; unggah dan penggabungan data saat pertama kali masuk akun memerlukan persetujuan pengguna.

### Pengembangan lanjutan

Statistik lanjutan, widget, ekspor CSV, tema gelap, inventaris cat dan alat, serta kartu build untuk dibagikan berada dalam rencana pengembangan setelah fitur inti.

## Alur koleksi

```text
Wishlist → Backlog → Building → Completed
```

- **Wishlist:** kit yang ingin dimiliki; tidak dihitung sebagai koleksi milik pengguna.
- **Backlog:** kit yang sudah dimiliki dan belum mulai dirakit.
- **Building:** kit yang sedang dikerjakan.
- **Completed:** kit yang sudah dinyatakan selesai oleh pengguna.

Build dapat dikembalikan ke backlog atau dibuka kembali tanpa menghapus riwayatnya. Checklist yang mencapai 100% tidak otomatis mengubah status menjadi Completed; penyelesaian tetap menjadi keputusan pengguna.

## Tampilan aplikasi

Desain yang disetujui menggunakan tampilan terang dengan latar putih, aksen biru yang halus, Material 3, dan kartu koleksi yang menonjolkan foto kit.

Lima tab utama yang direncanakan:

| Tab | Isi utama |
|---|---|
| Home | Ringkasan koleksi, aktivitas terbaru, dan akses cepat. |
| Collection | Daftar kit milik pengguna, pencarian, filter, dan detail kit. |
| Wishlist | Daftar kit incaran dan aksi pindah ke koleksi. |
| Builds | Rakitan aktif, checklist progres, timer, dan riwayat sesi. |
| Profile | Statistik dasar, preferensi, backup/restore, dan pengaturan cloud pada tahap berikutnya. |

Bahasa antarmuka ditargetkan menggunakan English sebagai default, dengan sumber terjemahan Bahasa Indonesia bila memungkinkan.

## Teknologi

**Sudah digunakan dalam kerangka proyek:** Kotlin, Jetpack Compose, Material 3, Gradle Kotlin DSL, dan version catalog.

**Direncanakan untuk Local MVP:** Room, DataStore, Coroutines/Flow, Hilt, Navigation Compose, Coil, dan Android Photo Picker, dengan pola MVVM serta aliran data satu arah.

**Direncanakan untuk Cloud Beta:** Python dan Flask, PostgreSQL, SQLAlchemy, migrasi database, REST API berversi, penyimpanan foto privat, serta WorkManager untuk sinkronisasi Android. Backend belum tersedia dalam repository.

Application ID: `id.my.chromazone.nubmark`.

## Menjalankan proyek Android

1. Buka folder repository ini di Android Studio; proyek Gradle berada di root.
2. Siapkan Android SDK sesuai konfigurasi `app/build.gradle.kts` dan JDK sesuai `gradle/gradle-daemon-jvm.properties` (saat ini JDK 25).
3. Jalankan Gradle Sync, lalu pilih modul `app` dan emulator atau perangkat Android.
4. Jalankan aplikasi. Saat ini layar yang tersedia masih berupa tampilan awal `Hello Android!`.

Perintah dari root repository pada PowerShell:

```powershell
.\gradlew.bat assembleDebug
.\gradlew.bat testDebugUnitTest
.\gradlew.bat lintDebug
```

Konfigurasi awal saat ini menggunakan `minSdk 24` dan `compileSdk`/`targetSdk 37`. Rencana produk menetapkan minimum API 26; perbedaan ini perlu diselaraskan saat implementasi fondasi. Angka konfigurasi tersebut bukan klaim kesiapan rilis.

## Dokumentasi dan kontribusi

- [Rencana produk dan roadmap](docs/PLAN.md): cakupan rilis, aturan data, alur pengguna, dan tahapan implementasi.
- [Panduan desain](docs/DESIGN.md): arah visual, navigasi, komponen, dan spesifikasi layar.
- [Aturan kontribusi](AGENTS.md): arsitektur, verifikasi, serta alur branch dan commit.

Baca dokumen tersebut sebelum mengerjakan perubahan. Setiap fitur baru dan perubahan besar harus memakai branch tersendiri; perubahan minor boleh dikerjakan di `main`. Setiap task yang selesai dibuatkan commit terpisah setelah verifikasi, termasuk pembaruan dokumentasi yang terkait.
