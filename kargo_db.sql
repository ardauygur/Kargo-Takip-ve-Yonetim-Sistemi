-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 21, 2025 at 05:27 PM
-- Server version: 8.0.40
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kargo_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `kargolar`
--

CREATE TABLE `kargolar` (
  `id` int NOT NULL,
  `takip_kodu` varchar(20) COLLATE utf8mb4_turkish_ci NOT NULL,
  `gonderici_ad` varchar(100) COLLATE utf8mb4_turkish_ci NOT NULL,
  `gonderici_tel` varchar(20) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `alici_ad` varchar(100) COLLATE utf8mb4_turkish_ci NOT NULL,
  `alici_tel` varchar(20) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `alici_adres` text COLLATE utf8mb4_turkish_ci,
  `varis_birimi` varchar(50) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `durum` varchar(50) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `kargo_agirlik` varchar(20) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `odeme_turu` varchar(50) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `kargo_tipi` varchar(50) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `cikis_tarihi` datetime DEFAULT CURRENT_TIMESTAMP,
  `teslim_tarihi` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Dumping data for table `kargolar`
--

INSERT INTO `kargolar` (`id`, `takip_kodu`, `gonderici_ad`, `gonderici_tel`, `alici_ad`, `alici_tel`, `alici_adres`, `varis_birimi`, `durum`, `kargo_agirlik`, `odeme_turu`, `kargo_tipi`, `cikis_tarihi`, `teslim_tarihi`) VALUES
(7, 'TR576825', 'Arda Uygur', '5436754535', 'Ege Karanfil', '5347346534', 'Yenibosna Merkez, Mithatpaşa Cd. No:17, 34225 Bahçelievler/İstanbul', 'İstanbul', '✅ Teslim Edildi', '4', 'Gönderici Ödemeli', 'Standart Koli', '2025-12-21 13:19:37', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `kargo_tarihce`
--

CREATE TABLE `kargo_tarihce` (
  `id` int NOT NULL,
  `kargo_id` int NOT NULL,
  `eski_durum` varchar(50) COLLATE utf8mb4_turkish_ci DEFAULT NULL,
  `yeni_durum` varchar(50) COLLATE utf8mb4_turkish_ci NOT NULL,
  `degisim_tarihi` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Dumping data for table `kargo_tarihce`
--

INSERT INTO `kargo_tarihce` (`id`, `kargo_id`, `eski_durum`, `yeni_durum`, `degisim_tarihi`) VALUES
(21, 7, 'Sistem Girişi', '📦 Hazırlanıyor', '2025-12-21 13:19:37'),
(22, 7, '📦 Hazırlanıyor', '🚛 Yola Çıktı', '2025-12-21 13:19:47'),
(23, 7, '🚛 Yola Çıktı', '🛵 Dağıtımda', '2025-12-21 13:19:54'),
(24, 7, '🛵 Dağıtımda', '✅ Teslim Edildi', '2025-12-21 13:19:59');

-- --------------------------------------------------------

--
-- Table structure for table `personel`
--

CREATE TABLE `personel` (
  `id` int NOT NULL,
  `kullanici_adi` varchar(50) COLLATE utf8mb4_turkish_ci NOT NULL,
  `sifre` varchar(100) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Dumping data for table `personel`
--

INSERT INTO `personel` (`id`, `kullanici_adi`, `sifre`) VALUES
(1, 'admin', '12345');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kargolar`
--
ALTER TABLE `kargolar`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `takip_kodu` (`takip_kodu`);

--
-- Indexes for table `kargo_tarihce`
--
ALTER TABLE `kargo_tarihce`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kargo_id` (`kargo_id`);

--
-- Indexes for table `personel`
--
ALTER TABLE `personel`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `kullanici_adi` (`kullanici_adi`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kargolar`
--
ALTER TABLE `kargolar`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `kargo_tarihce`
--
ALTER TABLE `kargo_tarihce`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `personel`
--
ALTER TABLE `personel`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `kargo_tarihce`
--
ALTER TABLE `kargo_tarihce`
  ADD CONSTRAINT `kargo_tarihce_ibfk_1` FOREIGN KEY (`kargo_id`) REFERENCES `kargolar` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
