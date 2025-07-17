-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 17. Jul 2025 um 05:33
-- Server-Version: 10.4.32-MariaDB
-- PHP-Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `kniffeln`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `benutzer`
--

CREATE TABLE `benutzer` (
  `id` int(11) NOT NULL,
  `benutzername` varchar(50) NOT NULL,
  `passwort_hash` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `ist_aktiv` tinyint(1) DEFAULT 1,
  `erstellt_am` datetime DEFAULT current_timestamp(),
  `ist_admin` tinyint(1) DEFAULT 0,
  `theme` varchar(10) DEFAULT 'light'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Daten für Tabelle `benutzer`
--

INSERT INTO `benutzer` (`id`, `benutzername`, `passwort_hash`, `email`, `ist_aktiv`, `erstellt_am`, `ist_admin`, `theme`) VALUES
(1, 'Admin', '$2b$12$H.2iGm8r4F8xuikzH0GZ8e91kVfDAnvBzrTc8vFZ6Yrd8SYZRaW9q', 'sebastian.pokern@googlemail.com', 1, '2025-06-05 13:27:34', 1, 'light'),
(2, 'Basti', '$2b$12$nqlvTdp4mZBv43s6AbYVUOC0nEr0KM4/IABKcr.0QFb44ruGVTTpu', 'sebastian.pokern@googlemail.com', 1, '2025-06-05 13:27:34', 1, 'dark'),
(3, 'Max', '1IEIvDaR3z', NULL, 1, '2025-07-15 13:13:09', 0, 'light'),
(4, 'Vérénice', 'Fj2XlBJVK9', NULL, 1, '2025-07-15 13:13:09', 0, 'light'),
(5, 'Tom', 'scrypt:32768:8:1$qYpGHqlRcuHKzMHy$ca66db315801634d34c929695a5d6f52f4de460891d2eead734c03d1b1fe95d08e902491918802e0166ac29193ff19de3be247e7879805d87fd9afa3e92baf67', NULL, 1, '2025-07-15 13:54:16', 0, 'light'),
(6, 'Maria', 'GZKFs4UDlF', NULL, 1, '2025-07-16 22:46:10', 0, 'light'),
(7, 'DB', 'p8YdmXlC1T', NULL, 1, '2025-07-16 22:46:10', 0, 'light'),
(8, 'Bla', 'xvhweOTVvf', NULL, 1, '2025-07-17 05:23:33', 0, 'light'),
(9, 'Blub', 'U3FsspeOWd', NULL, 1, '2025-07-17 05:23:33', 0, 'light');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `einstellungen`
--

CREATE TABLE `einstellungen` (
  `id` int(11) NOT NULL,
  `email_empfaenger` varchar(255) DEFAULT NULL,
  `anzahl_logeintraege` int(11) DEFAULT 20,
  `max_mitspieler` int(11) DEFAULT 3
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Daten für Tabelle `einstellungen`
--

INSERT INTO `einstellungen` (`id`, `email_empfaenger`, `anzahl_logeintraege`, `max_mitspieler`) VALUES
(1, 'sebastian.pokern@googlemail.com', 20, 3);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `spielpartien`
--

CREATE TABLE `spielpartien` (
  `id` int(11) NOT NULL,
  `startzeit` datetime NOT NULL DEFAULT current_timestamp(),
  `beendet` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `spielpartien`
--

INSERT INTO `spielpartien` (`id`, `startzeit`, `beendet`) VALUES
(1, '2025-07-10 16:56:24', 0),
(4, '2025-07-15 13:13:09', 0),
(5, '2025-07-15 13:39:47', 0),
(6, '2025-07-15 13:54:16', 0),
(7, '2025-07-15 14:06:52', 0),
(8, '2025-07-16 22:46:10', 0),
(9, '2025-07-17 05:23:33', 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `spielteilnehmer`
--

CREATE TABLE `spielteilnehmer` (
  `id` int(11) NOT NULL,
  `spiel_id` int(11) NOT NULL,
  `benutzer_id` int(11) NOT NULL,
  `punkte` int(11) DEFAULT 0,
  `ist_aktiv` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `spielteilnehmer`
--

INSERT INTO `spielteilnehmer` (`id`, `spiel_id`, `benutzer_id`, `punkte`, `ist_aktiv`) VALUES
(1, 1, 1, 0, 0),
(2, 1, 2, 0, 0),
(5, 4, 2, 0, 0),
(6, 4, 3, 0, 0),
(7, 4, 4, 0, 0),
(8, 5, 2, 0, 0),
(9, 5, 4, 0, 0),
(10, 5, 3, 0, 0),
(11, 6, 2, 0, 0),
(12, 6, 4, 0, 0),
(13, 6, 5, 0, 0),
(14, 7, 2, 56, 1),
(15, 7, 3, 0, 0),
(16, 7, 4, 0, 0),
(17, 8, 2, 109, 0),
(18, 8, 6, 0, 1),
(19, 8, 7, 0, 0),
(20, 9, 4, 0, 0),
(21, 9, 8, 0, 0),
(22, 9, 9, 0, 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `spielzuege`
--

CREATE TABLE `spielzuege` (
  `id` int(11) NOT NULL,
  `teilnehmer_id` int(11) NOT NULL,
  `wurf_nummer` int(11) NOT NULL,
  `wurfzeit` datetime NOT NULL DEFAULT current_timestamp(),
  `wuerfelwerte` varchar(20) NOT NULL,
  `gewertet` tinyint(1) NOT NULL DEFAULT 0,
  `punktekategorie` varchar(50) DEFAULT NULL,
  `punkte` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `spielzuege`
--

INSERT INTO `spielzuege` (`id`, `teilnehmer_id`, `wurf_nummer`, `wurfzeit`, `wuerfelwerte`, `gewertet`, `punktekategorie`, `punkte`) VALUES
(1, 2, 1, '2025-07-10 16:56:25', '2,2,4,4,6', 1, 'Zweimal Zweier', 8),
(7, 14, 3, '2025-07-16 21:29:31', '3,3,1,3,3', 1, 'Dreien', 12),
(8, 14, 3, '2025-07-16 22:04:22', '5,6,5,1,5', 1, 'Dreierpasch', 22),
(9, 14, 3, '2025-07-16 22:04:26', '5,6,5,1,5', 1, 'Dreierpasch', 22),
(10, 17, 3, '2025-07-16 22:46:48', '6,2,2,2,2', 1, 'Zweien', 8),
(11, 17, 3, '2025-07-16 23:21:32', '6,6,2,6,6', 1, 'Sechsen', 24),
(12, 17, 3, '2025-07-17 05:08:49', '5,6,5,6,5', 1, 'Full House', 25),
(13, 17, 3, '2025-07-17 05:09:42', '5,3,5,3,5', 1, 'Full House', 25),
(14, 17, 3, '2025-07-17 05:19:58', '4,4,2,4,1', 1, 'Dreierpasch', 15),
(15, 17, 3, '2025-07-17 05:22:28', '4,4,4,5,6', 1, 'Vieren', 12);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `benutzer`
--
ALTER TABLE `benutzer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `benutzername` (`benutzername`);

--
-- Indizes für die Tabelle `einstellungen`
--
ALTER TABLE `einstellungen`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `spielpartien`
--
ALTER TABLE `spielpartien`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `spielteilnehmer`
--
ALTER TABLE `spielteilnehmer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `spiel_id` (`spiel_id`),
  ADD KEY `benutzer_id` (`benutzer_id`);

--
-- Indizes für die Tabelle `spielzuege`
--
ALTER TABLE `spielzuege`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teilnehmer_id` (`teilnehmer_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `benutzer`
--
ALTER TABLE `benutzer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT für Tabelle `einstellungen`
--
ALTER TABLE `einstellungen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT für Tabelle `spielpartien`
--
ALTER TABLE `spielpartien`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT für Tabelle `spielteilnehmer`
--
ALTER TABLE `spielteilnehmer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT für Tabelle `spielzuege`
--
ALTER TABLE `spielzuege`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `spielteilnehmer`
--
ALTER TABLE `spielteilnehmer`
  ADD CONSTRAINT `spielteilnehmer_ibfk_1` FOREIGN KEY (`spiel_id`) REFERENCES `spielpartien` (`id`),
  ADD CONSTRAINT `spielteilnehmer_ibfk_2` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`);

--
-- Constraints der Tabelle `spielzuege`
--
ALTER TABLE `spielzuege`
  ADD CONSTRAINT `spielzuege_ibfk_1` FOREIGN KEY (`teilnehmer_id`) REFERENCES `spielteilnehmer` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
