# WasteWise: Konteks & Rencana Pengerjaan untuk Claude Code

> Simpan file ini di repo sebagai `docs/PLAN.md`. Ini sumber konteks dan rencana kerja utama. Baca seluruhnya sebelum mulai, lalu kerjakan sesuai aturan di bawah.

---

## 1. Siapa saya

- Nama: Muhammad Nabiel Yandra (Nabiel), mahasiswa S1 Sistem Informasi, FILKOM Universitas Brawijaya (angkatan 2024).
- Minat: AI, machine learning, data analytics. Portfolio: https://nabielyr.github.io, GitHub: https://github.com/nabielyr
- Project saya sebelumnya: sentiment analysis IndoBERT, analisis tren tech layoffs (Jupyter), dashboard Streamlit berbasis GitHub REST API (`what-gets-starred`), deteksi bahasa isyarat (MediaPipe + Random Forest), game typing (vanilla JS + Canvas). Jadi saya sudah nyaman dengan Python, pandas, scikit-learn, Jupyter, dan Streamlit.
- Topik rencana skripsi saya terkait supply chain management (SCM) dan food waste. Project ini adalah eksplorasi teknis yang mendukung topik itu.
- Bahasa: jelaskan ke saya dalam **Bahasa Indonesia santai**. Kode, nama variabel, docstring, dan pesan commit dalam **Bahasa Inggris**.

## 2. Apa itu WasteWise

**WasteWise** adalah dashboard prediksi permintaan (demand forecasting) dan simulasi food waste untuk supply chain makanan.

Masalah yang diangkat: bisnis makanan (dapur pusat, katering, restoran berjaringan) sering menyiapkan bahan atau porsi berdasarkan perkiraan kasar. Kalau perkiraannya terlalu tinggi, sisa makanan terbuang (waste). Kalau terlalu rendah, terjadi stockout dan pelanggan tidak terlayani.

Pertanyaan utama project:
1. Seberapa akurat permintaan mingguan per pusat distribusi dan per menu bisa diprediksi?
2. Kalau keputusan stok memakai hasil forecast ML (bukan perkiraan naif), **berapa banyak waste yang bisa dikurangi** tanpa menaikkan stockout secara berlebihan?
3. Faktor apa yang paling memengaruhi permintaan (harga, promo, tipe menu, lokasi)?

Output akhir:
- Pipeline data dan model yang rapi dan bisa dijalankan ulang (reproducible).
- Dashboard Streamlit interaktif (bilingual ID/EN) yang di-deploy publik.
- README yang menjelaskan metodologi, hasil, dan keterbatasan dengan jujur.

## 3. Dataset

Dataset utama: **Food Demand Forecasting** (Kaggle, berasal dari hackathon Genpact/Analytics Vidhya). Data order mingguan sebuah perusahaan meal delivery dengan beberapa fulfilment center.

File yang diharapkan (verifikasi setelah download, jangan diasumsikan):
- `train.csv`: `id, week, center_id, meal_id, checkout_price, base_price, emailer_for_promotion, homepage_featured, num_orders`
- `fulfilment_center_info.csv`: `center_id, city_code, region_code, center_type, op_area`
- `meal_info.csv`: `meal_id, category, cuisine`
- `test.csv` tidak punya `num_orders`, jadi **tidak dipakai untuk evaluasi**. Evaluasi memakai holdout berbasis waktu dari `train.csv`.

Catatan penting:
- Dataset ini **tidak punya kolom waste**. Waste dihitung lewat **simulasi kebijakan stok** (lihat Fase 8). Ini harus dijelaskan terang-terangan di README dan di dashboard.
- Satuan harga di dataset tidak jelas mata uangnya. Jangan klaim Rupiah. Pakai "unit harga", dan sediakan parameter konversi yang bisa diatur.
- Download butuh Kaggle API token (`~/.kaggle/kaggle.json`). Saya yang menyiapkan token-nya. Kalau belum ada, berhenti dan minta saya.
- Kalau dataset di atas tidak bisa diakses atau isinya beda, berhenti dan laporkan ke saya sebelum memilih alternatif.

## 4. Tech stack

- Python 3.11+, dependency di `pyproject.toml` (lokal pakai Python 3.12 + venv, lihat `decisions.md`)
- Data: pandas, numpy, pyarrow (parquet)
- Model: scikit-learn, LightGBM, (opsional) statsmodels untuk baseline
- Explainability: SHAP
- Visualisasi: Plotly (dashboard), matplotlib/seaborn (notebook)
- Dashboard: Streamlit (multipage)
- Kualitas: ruff (lint + format), pytest, pre-commit
- CI: GitHub Actions
- Deploy: Streamlit Community Cloud

## 5. Struktur repo target

```
wastewise/
├── .github/workflows/ci.yml
├── app/
│   ├── Home.py
│   ├── pages/
│   ├── components/
│   └── i18n/            # id.json, en.json
├── data/
│   ├── raw/             # gitignored
│   ├── interim/         # gitignored
│   ├── processed/       # gitignored
│   └── app/             # artefak kecil untuk dashboard, di-commit (< 50 MB total)
├── docs/
│   ├── PLAN.md          # file ini
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── decisions.md     # catatan keputusan teknis
├── models/              # artefak model, gitignored kecuali model final kecil
├── notebooks/
├── reports/figures/
├── src/wastewise/
│   ├── __init__.py
│   ├── config.py
│   ├── data/            # download.py, load.py, clean.py, validate.py
│   ├── features/        # build.py
│   ├── models/          # baselines.py, train.py, evaluate.py, predict.py
│   ├── simulation/      # inventory.py, costs.py
│   └── utils/
├── tests/
├── Makefile
├── pyproject.toml
├── README.md
└── LICENSE
```

## 6. Aturan kerja (WAJIB diikuti)

1. **Satu step = satu commit.** Jangan menggabungkan beberapa step dalam satu commit, dan jangan memecah satu step jadi commit-commit kosong atau kosmetik. Setiap commit harus berisi perubahan yang bermakna dan bisa dijelaskan.
2. Pesan commit pakai format **Conventional Commits** dalam Bahasa Inggris: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`, `ci:`, `style:`, `perf:`, `data:`. Contoh pesan sudah saya tulis di tiap step; boleh disesuaikan kalau isi perubahannya beda.
3. Sebelum commit: jalankan `ruff check`, `ruff format`, dan `pytest` (kalau sudah ada test). Jangan commit kalau test gagal.
4. Setelah tiap step selesai, centang checkbox step itu di `docs/PLAN.md` **di commit yang sama**.
5. **Berhenti di akhir setiap fase.** Kasih ringkasan singkat ke saya: apa yang selesai, hasil penting (angka metrik, temuan EDA), dan hal yang perlu saya putuskan. Tunggu saya bilang "lanjut" sebelum masuk fase berikutnya.
6. Jangan pernah commit: data mentah, file besar (> 10 MB per file), `kaggle.json`, `.env`, atau kredensial apa pun.
7. **Jangan mengarang angka.** Semua metrik dan temuan di README, notebook, dan dashboard harus berasal dari hasil run yang benar-benar dijalankan.
8. Pakai `git config` milik saya (jangan ubah user.name / user.email).
9. Kalau ada keputusan teknis penting (misalnya pilihan horizon forecast, split validasi, parameter simulasi), catat di `docs/decisions.md` dengan alasan singkat.
10. Kalau sebuah step ternyata perlu dipecah atau diganti, jelaskan dulu ke saya sebelum mengubah rencana.
11. Jangan push ke remote kecuali saya minta.
12. Jangan pakai em dash di mana pun (kode, docs, pesan commit, chat).
13. Jangan tambahkan trailer `Co-Authored-By` Claude atau atribusi Claude Code di commit maupun PR. Author commit hanya saya.
14. Kerjakan satu step per giliran: setelah step selesai, bilang selesai, tawarkan push ke GitHub, lalu tanya apakah lanjut ke step berikutnya.

---

## 7. Rencana pengerjaan

### Fase 0: Setup repository

- [x] **0.1** Init git repo, buat `README.md` minimal (nama project + satu kalimat deskripsi). → `chore: initialize repository`
- [x] **0.2** Tambah `.gitignore` untuk Python, Jupyter, data, model, dan kredensial. → `chore: add gitignore for python, data and secrets`
- [x] **0.2a** Tambah `.editorconfig` (charset, LF, indent, final newline) supaya setting editor konsisten. (Step tambahan.) → `chore: add editorconfig`
- [x] **0.3** Tambah `LICENSE` (MIT). → `chore: add MIT license`
- [x] **0.4** Buat `pyproject.toml` dengan metadata project dan dependency inti. → `build: add pyproject with core dependencies`
- [x] **0.5** Buat struktur folder (lihat bagian 5) dengan `.gitkeep` dan `src/wastewise/__init__.py`. → `chore: scaffold project directory structure`
- [x] **0.6** Konfigurasi ruff di `pyproject.toml`. → `style: configure ruff linting and formatting`
- [x] **0.7** Tambah `.pre-commit-config.yaml` (ruff, trailing whitespace, end-of-file, check-large-files). → `chore: add pre-commit hooks`
- [x] **0.8** Setup pytest + satu smoke test (`import wastewise`). → `test: add pytest setup and smoke test`
- [x] **0.9** Buat `Makefile` dengan target `install`, `lint`, `format`, `test`. → `chore: add makefile with dev commands`
- [x] **0.10** Buat `src/wastewise/config.py` berisi path project (pakai `pathlib`) dan konstanta global. → `feat: add central config with project paths`
- [x] **0.11** Tambah file ini sebagai `docs/PLAN.md` dan buat `docs/decisions.md` kosong dengan template. → `docs: add project plan and decision log`

### Fase 1: Akuisisi & pemahaman data

- [x] **1.1** Tulis `src/wastewise/data/download.py` untuk download dataset via Kaggle API ke `data/raw/`, dengan pesan error jelas kalau token tidak ada. → `feat: add kaggle dataset download script`
- [x] **1.2** Tambah target `make data` di Makefile. → `chore: add make target for data download`
- [x] **1.3** Tulis `src/wastewise/data/load.py`: fungsi load tiap CSV dengan dtype eksplisit. → `feat: add typed loaders for raw csv files`
- [x] **1.4** Tambah fungsi merge `train` + `center_info` + `meal_info` jadi satu dataframe. → `feat: add function to merge orders with center and meal info`
- [ ] **1.5** Tulis test untuk loader dan merge (pakai fixture data mini buatan di `tests/fixtures/`, bukan data asli). → `test: add tests for loaders and merge`
- [ ] **1.6** Buat `docs/data_dictionary.md`: arti tiap kolom, tipe, satuan, dan catatan. → `docs: add data dictionary`
- [ ] **1.7** Simpan data hasil merge ke `data/interim/` dalam format parquet. → `feat: persist merged dataset as parquet`

### Fase 2: Exploratory Data Analysis

Buat `notebooks/01_eda.ipynb`. Setiap step menambah satu bagian ke notebook, lengkap dengan markdown penjelasan temuan.

- [ ] **2.1** Ringkasan dataset: ukuran, rentang minggu, jumlah center, meal, dan kombinasi center-meal. → `docs(eda): add dataset overview section`
- [ ] **2.2** Cek missing value, duplikat, dan nilai aneh (harga 0, order negatif atau ekstrem). → `docs(eda): add data quality checks`
- [ ] **2.3** Distribusi `num_orders` (skewness, perlu transformasi log atau tidak). → `docs(eda): analyze target distribution`
- [ ] **2.4** Tren total order per minggu dan pola musiman. → `docs(eda): add weekly demand trend analysis`
- [ ] **2.5** Analisis per kategori menu dan cuisine. → `docs(eda): analyze demand by meal category and cuisine`
- [ ] **2.6** Analisis per center, center type, dan region. → `docs(eda): analyze demand by center and region`
- [ ] **2.7** Efek harga (diskon = base_price − checkout_price) dan promo (emailer, homepage) terhadap order. → `docs(eda): analyze price and promotion effects`
- [ ] **2.8** Cek kelengkapan time series: apakah tiap kombinasi center-meal punya data tiap minggu (gap, series pendek). → `docs(eda): check time series completeness per series`
- [ ] **2.9** Simpan figure penting ke `reports/figures/` dan tulis ringkasan temuan di akhir notebook. → `docs(eda): export key figures and summarize findings`

### Fase 3: Cleaning & validasi data

- [ ] **3.1** Tulis `src/wastewise/data/clean.py`: tangani masalah yang ditemukan di EDA (tipe data, outlier, nilai tidak valid). Catat keputusan di `decisions.md`. → `feat: add data cleaning pipeline`
- [ ] **3.2** Test untuk fungsi cleaning. → `test: add tests for cleaning functions`
- [ ] **3.3** Tulis `src/wastewise/data/validate.py`: cek skema dan aturan sederhana (kolom wajib ada, order ≥ 0, harga > 0, minggu berurutan). → `feat: add schema and sanity validation`
- [ ] **3.4** Test untuk validasi (termasuk kasus data yang sengaja salah). → `test: add tests for data validation`
- [ ] **3.5** Buat script `make clean-data` yang menghasilkan `data/processed/clean.parquet`. → `feat: add cli entrypoint to build clean dataset`

### Fase 4: Feature engineering

Semua fitur dibuat di `src/wastewise/features/build.py`. **Hindari data leakage**: fitur di minggu t hanya boleh memakai informasi sampai minggu t−1 (kecuali fitur harga dan promo minggu t, yang memang diketahui sebelum minggu berjalan).

- [ ] **4.1** Tentukan dan dokumentasikan horizon forecast (default: 1 minggu ke depan) dan skema split waktu di `decisions.md`. → `docs: define forecast horizon and validation scheme`
- [ ] **4.2** Fitur harga: diskon absolut, diskon persen, rasio harga terhadap rata-rata harga meal. → `feat: add price and discount features`
- [ ] **4.3** Fitur lag order (lag 1, 2, 3, 4, 8, 12 minggu) per center-meal. → `feat: add lagged demand features`
- [ ] **4.4** Fitur rolling (mean, std, min, max untuk window 4 dan 12 minggu), di-shift supaya tidak bocor. → `feat: add rolling window demand features`
- [ ] **4.5** Fitur agregat level lebih tinggi: rata-rata order per meal (semua center) dan per center (semua meal), juga lagged. → `feat: add aggregated center and meal level features`
- [ ] **4.6** Fitur kategorikal: encoding category, cuisine, center_type, region. → `feat: add categorical encodings`
- [ ] **4.7** Fitur waktu sederhana (minggu ke-n dalam siklus, indeks tren). → `feat: add time-based features`
- [ ] **4.8** Test anti-leakage: pastikan fitur lag dan rolling di minggu t tidak memakai nilai minggu t. → `test: add leakage tests for lag and rolling features`
- [ ] **4.9** Pipeline `make features` menghasilkan `data/processed/features.parquet`. → `feat: add feature building entrypoint`

### Fase 5: Baseline models

- [ ] **5.1** Tulis `src/wastewise/models/evaluate.py` berisi metrik: MAE, RMSE, RMSLE, WAPE, dan bias (forecast − actual). → `feat: add forecast evaluation metrics`
- [ ] **5.2** Test metrik dengan contoh angka yang dihitung manual. → `test: add unit tests for evaluation metrics`
- [ ] **5.3** Implementasi split berbasis waktu (train / validation / holdout 10 minggu terakhir). → `feat: add time-based train validation holdout split`
- [ ] **5.4** Baseline naive: order minggu ini = order minggu lalu. → `feat: add naive last-week baseline`
- [ ] **5.5** Baseline moving average 4 minggu dan seasonal naive (kalau relevan). → `feat: add moving average baselines`
- [ ] **5.6** Notebook `02_baselines.ipynb`: hasil baseline di validation dan holdout, simpan tabel hasil. → `docs: add baseline results notebook`

### Fase 6: Model machine learning

- [ ] **6.1** Tulis `src/wastewise/models/train.py`: training LightGBM dengan target `log1p(num_orders)`. → `feat: add lightgbm training pipeline`
- [ ] **6.2** Simpan model dan metadata (fitur, parameter, metrik, tanggal) ke `models/`. → `feat: persist trained model with metadata`
- [ ] **6.3** Time-series cross validation (expanding window, beberapa fold). → `feat: add time series cross validation`
- [ ] **6.4** Hyperparameter tuning sederhana (random search atau Optuna kalau mau ditambahkan) dengan budget terbatas. → `feat: add hyperparameter search`
- [ ] **6.5** Bandingkan dengan satu model lain (misalnya Ridge regression atau RandomForest) sebagai pembanding. → `feat: add alternative model for comparison`
- [ ] **6.6** Tulis `src/wastewise/models/predict.py`: hasilkan prediksi untuk periode holdout. → `feat: add prediction module`
- [ ] **6.7** Test pipeline end-to-end training + predict di data mini. → `test: add end-to-end training test on fixture data`
- [ ] **6.8** Notebook `03_modeling.ipynb`: tabel perbandingan semua model vs baseline. → `docs: add model comparison notebook`

### Fase 7: Evaluasi mendalam & explainability

- [ ] **7.1** Analisis error per kategori menu, center type, dan region. → `feat: add segmented error analysis`
- [ ] **7.2** Analisis error untuk series ber-volume rendah vs tinggi. → `feat: add error analysis by demand volume`
- [ ] **7.3** Feature importance (gain) dari LightGBM. → `feat: add feature importance extraction`
- [ ] **7.4** SHAP summary dan contoh penjelasan untuk beberapa prediksi. → `feat: add shap explanations`
- [ ] **7.5** Notebook `04_evaluation.ipynb` dengan semua analisis di atas dan kesimpulan. → `docs: add evaluation and explainability notebook`
- [ ] **7.6** Tulis bagian model dan evaluasi di `docs/methodology.md`. → `docs: document modeling methodology`

### Fase 8: Simulasi food waste

Logika inti: setiap minggu, center menyiapkan stok `Q = forecast × (1 + buffer)`. Lalu:
- `waste = max(Q − actual, 0)`
- `stockout = max(actual − Q, 0)`

Bandingkan beberapa kebijakan: naive, moving average, forecast ML, dan forecast ML dengan buffer optimal.

- [ ] **8.1** Tulis `src/wastewise/simulation/inventory.py`: fungsi simulasi untuk satu kebijakan stok. → `feat: add inventory policy simulation`
- [ ] **8.2** Test simulasi dengan kasus kecil yang hasilnya bisa dihitung manual. → `test: add tests for inventory simulation`
- [ ] **8.3** Tulis `src/wastewise/simulation/costs.py`: konversi waste ke estimasi biaya dan berat dengan asumsi yang bisa diatur (rasio biaya bahan terhadap harga, berat per porsi). Default asumsi dicatat di `decisions.md`. → `feat: add configurable waste cost estimation`
- [ ] **8.4** Hitung metrik simulasi: total waste, waste rate (%), stockout rate (%), service level (fill rate). → `feat: add simulation kpis`
- [ ] **8.5** Bandingkan semua kebijakan di periode holdout. → `feat: compare stocking policies on holdout`
- [ ] **8.6** Buat kurva trade-off waste vs stockout untuk berbagai nilai buffer. → `feat: add waste stockout tradeoff curve`
- [ ] **8.7** Cari buffer optimal untuk target service level tertentu (misalnya 95%). → `feat: add buffer optimization for target service level`
- [ ] **8.8** Notebook `05_waste_simulation.ipynb` dengan hasil dan interpretasi, termasuk keterbatasan simulasi. → `docs: add waste simulation notebook`
- [ ] **8.9** Ekspor artefak kecil untuk dashboard ke `data/app/` (agregat, prediksi holdout, hasil simulasi). Pastikan total < 50 MB. → `data: export lightweight artifacts for dashboard`

### Fase 9: Dashboard Streamlit

Desain: bersih, profesional, bukan template default Streamlit polos. Pakai tema custom di `.streamlit/config.toml`. Semua teks UI lewat file i18n supaya bisa ganti bahasa ID/EN.

- [ ] **9.1** Setup aplikasi multipage (`app/Home.py`) dengan tema custom. → `feat(app): scaffold streamlit multipage app with custom theme`
- [ ] **9.2** Sistem i18n sederhana (`app/i18n/id.json`, `en.json`) dan toggle bahasa di sidebar. → `feat(app): add bilingual id/en support`
- [ ] **9.3** Data loader dengan `st.cache_data` yang membaca `data/app/`. → `feat(app): add cached data loaders`
- [ ] **9.4** Komponen reusable: KPI card, chart wrapper Plotly dengan style konsisten. → `feat(app): add reusable kpi and chart components`
- [ ] **9.5** Halaman **Overview**: KPI utama (total order, akurasi model, waste yang bisa dikurangi) dan ringkasan cerita project. → `feat(app): add overview page`
- [ ] **9.6** Halaman **Demand Explorer**: filter center, meal, kategori, region; tren dan breakdown. → `feat(app): add demand explorer page`
- [ ] **9.7** Halaman **Forecast**: actual vs predicted per series, pilih model, tampilkan metrik. → `feat(app): add forecast page`
- [ ] **9.8** Halaman **Waste Simulator**: slider buffer, pilih kebijakan, parameter biaya; hasil waste, stockout, dan biaya update secara interaktif. → `feat(app): add interactive waste simulator page`
- [ ] **9.9** Tambahkan kurva trade-off waste vs stockout di Waste Simulator. → `feat(app): add tradeoff chart to simulator`
- [ ] **9.10** Halaman **Model Insights**: feature importance, SHAP, error per segmen. → `feat(app): add model insights page`
- [ ] **9.11** Halaman **Methodology / About**: dataset, metode, asumsi simulasi, keterbatasan, link GitHub dan portfolio. → `feat(app): add methodology and about page`
- [ ] **9.12** Fitur download hasil (CSV) untuk filter yang sedang aktif. → `feat(app): add csv export for filtered results`
- [ ] **9.13** Empty state dan error handling (filter tanpa data, file artefak hilang). → `fix(app): handle empty filters and missing artifacts`
- [ ] **9.14** Rapikan tampilan di layar kecil (layout kolom responsif). → `style(app): improve layout for small screens`
- [ ] **9.15** Test sederhana untuk fungsi non-UI di app (loader, i18n key lengkap di kedua bahasa). → `test(app): add tests for loaders and translation keys`

### Fase 10: Kualitas & CI

- [ ] **10.1** GitHub Actions: jalankan ruff dan pytest di setiap push dan pull request. → `ci: add lint and test workflow`
- [ ] **10.2** Tambah coverage report di CI (pytest-cov). → `ci: add test coverage reporting`
- [ ] **10.3** Tambah type hints di modul `src/` dan cek dengan mypy (mode tidak terlalu ketat). → `refactor: add type hints across source modules`
- [ ] **10.4** Tambah mypy ke CI. → `ci: add mypy type checking`
- [ ] **10.5** Logging yang rapi (modul `logging`, bukan `print`) di pipeline. → `refactor: replace prints with structured logging`
- [ ] **10.6** Target `make pipeline` yang menjalankan semua tahap dari data mentah sampai artefak dashboard. → `feat: add end-to-end pipeline make target`

### Fase 11: Dokumentasi & deploy

- [ ] **11.1** README lengkap: latar belakang masalah, pertanyaan, dataset, metode, hasil utama (angka asli dari run), screenshot, cara menjalankan, struktur repo. → `docs: write comprehensive readme`
- [ ] **11.2** Tambah badge (CI, Python version, license) di README. → `docs: add status badges to readme`
- [ ] **11.3** Lengkapi `docs/methodology.md` dengan bagian simulasi waste dan keterbatasan. → `docs: complete methodology with simulation and limitations`
- [ ] **11.4** Siapkan `requirements.txt` untuk Streamlit Cloud (generate dari pyproject). → `build: add requirements file for streamlit cloud`
- [ ] **11.5** Deploy ke Streamlit Community Cloud (saya yang login dan klik deploy; Claude Code siapkan konfigurasi dan instruksinya). → `chore: prepare streamlit cloud deployment config`
- [ ] **11.6** Tambahkan link demo live dan screenshot/GIF dashboard di README. → `docs: add live demo link and screenshots`
- [ ] **11.7** Tulis `CHANGELOG.md` dan tag rilis `v1.0.0`. → `docs: add changelog for v1.0.0`

### Fase 12: Integrasi portfolio (opsional)

- [ ] **12.1** Tulis ringkasan project (ID dan EN, 2-3 paragraf) untuk ditaruh di portfolio `nabielyr.github.io`. Simpan di `docs/portfolio_summary.md`. → `docs: add bilingual portfolio summary`
- [ ] **12.2** Buat thumbnail/cover image untuk kartu project di portfolio. → `docs: add project cover image`
- [ ] **12.3** Draft topik pengembangan lanjutan (data real dari UMKM/katering lokal, prediksi multi-minggu, integrasi data cuaca/hari libur Indonesia) di `docs/future_work.md`. Ini juga bahan diskusi untuk skripsi. → `docs: add future work and research directions`

---

## 8. Definition of Done

Project dianggap selesai kalau:
- `make pipeline` berjalan dari nol sampai menghasilkan artefak dashboard tanpa error.
- Semua test lulus dan CI hijau.
- Model ML lebih baik dari baseline naive di holdout (kalau ternyata tidak, laporkan dengan jujur dan analisis penyebabnya, jangan dimanipulasi).
- Dashboard live, bisa dibuka publik, dan berjalan di dua bahasa.
- README menjelaskan hasil dan keterbatasan dengan angka yang benar-benar dari hasil run.

## 9. Mulai dari sini

Konfirmasi dulu ke saya bahwa kamu sudah paham konteks dan aturannya (ringkas dalam 3-5 poin), sebutkan hal yang menurutmu perlu saya siapkan (misalnya Kaggle token), lalu mulai **Fase 0, step 0.1**.
