# Nubmark

Nubmark adalah aplikasi Android untuk penghobi Gunpla dan model kit plastik yang ingin menyimpan koleksi dan cerita di balik setiap rakitan. Aplikasi ini berfokus pada perjalanan sebuah kit: dari masuk wishlist, dibeli, mulai dirakit, sampai selesai dan dipajang.

Saat koleksi bertambah, mudah lupa kit mana yang sudah dibeli atau sampai tahap mana sebuah rakitan dikerjakan. Nubmark menjadi tempat untuk mencatatnya, bersama foto progres, waktu merakit, dan biaya yang dikeluarkan.

> Nubmark masih dalam pengembangan. Ketersediaan fitur mengikuti progres implementasi di [roadmap](docs/PLAN.md).

## Koleksi yang mudah diikuti

Setiap kit memiliki informasi seperti nama, grade, skala, dan seri, serta status yang menjelaskan posisinya dalam koleksi:

| Status | Arti |
|---|---|
| Wishlist | Kit incaran yang belum dimiliki. |
| Backlog | Kit yang sudah dimiliki dan menunggu untuk dirakit. |
| Building | Kit yang sedang dikerjakan. |
| Completed | Kit yang sudah selesai dirakit. |

Wishlist terpisah dari jumlah kit yang dimiliki. Setelah dibeli, kit berpindah ke koleksi sebagai backlog. Pencarian dan filter membantu menemukan kit berdasarkan nama, status, atau grade.

## Catatan selama merakit

Nubmark menghubungkan setiap kit dengan checklist tahap perakitan, jurnal, dan galeri foto. Catatan tentang panel lining, decal yang belum dipasang, atau warna cat yang dipakai tetap tersimpan bersama kit yang bersangkutan.

Progres mengikuti checklist, dengan tahapan yang dapat disesuaikan atau dilewati sesuai kebutuhan kit. Keputusan untuk menyatakan rakitan selesai tetap ada pada pengguna. Rakitan juga dapat dibuka kembali tanpa kehilangan riwayatnya.

Timer dan riwayat sesi membantu mencatat waktu pengerjaan. Foto memperlihatkan perubahan dari kondisi awal, proses perakitan, hingga hasil akhirnya.

## Pengeluaran hobi

Biaya pembelian kit, cat, alat, dan kebutuhan lain dicatat dalam rupiah. Pengeluaran dapat dikaitkan dengan kit tertentu atau disimpan sebagai biaya umum, sehingga biaya satu rakitan dan total belanja hobi dapat dilihat secara terpisah.

## Ruang untuk koleksi pribadi

Nubmark memakai pendekatan local-first: data koleksi berada di perangkat, dengan penggunaan inti tanpa kewajiban akun atau koneksi internet. Backup lokal menjadi cara menyimpan salinan data beserta foto. Layanan cloud bersifat opsional untuk pencadangan dan sinkronisasi antarperangkat.

Tampilannya menggunakan latar putih, aksen biru, dan kartu yang menonjolkan foto kit. Lima bagian utama mengatur isi aplikasi:

| Bagian | Isi |
|---|---|
| Home | Ringkasan koleksi dan kit yang baru diperbarui. |
| Collection | Kit yang dimiliki beserta detailnya. |
| Wishlist | Kit incaran yang ingin dibeli. |
| Builds | Rakitan aktif, checklist, dan sesi merakit. |
| Profile | Statistik, preferensi, dan pengelolaan backup. |

## Dokumentasi proyek

- [PLAN.md](docs/PLAN.md): cakupan produk, aturan data, dan roadmap.
- [DESIGN.md](docs/DESIGN.md): panduan tampilan dan pengalaman pengguna.
- [AGENTS.md](AGENTS.md): panduan kontribusi dan alur kerja pengembangan.
