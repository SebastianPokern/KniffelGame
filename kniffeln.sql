-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 09. Jul 2025 um 07:45
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
(2, 'Basti', '$2b$12$nqlvTdp4mZBv43s6AbYVUOC0nEr0KM4/IABKcr.0QFb44ruGVTTpu', 'sebastian.pokern@googlemail.com', 1, '2025-06-05 13:27:34', 1, 'dark');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `einstellungen`
--

CREATE TABLE `einstellungen` (
  `id` int(11) NOT NULL,
  `email_empfaenger` varchar(255) DEFAULT NULL,
  `anzahl_logeintraege` int(11) DEFAULT 20
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Daten für Tabelle `einstellungen`
--

INSERT INTO `einstellungen` (`id`, `email_empfaenger`, `anzahl_logeintraege`) VALUES
(1, 'sebastian.pokern@googlemail.com', 20);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `logeintraege`
--

CREATE TABLE `logeintraege` (
  `id` int(11) NOT NULL,
  `zeitpunkt` datetime NOT NULL,
  `benutzer_id` int(11) DEFAULT NULL,
  `meldung` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Daten für Tabelle `logeintraege`
--

INSERT INTO `logeintraege` (`id`, `zeitpunkt`, `benutzer_id`, `meldung`) VALUES
(1, '2025-07-07 20:35:27', 2, 'Schalter aktiviert'),
(2, '2025-07-09 06:58:15', 2, 'Schalter aktiviert');

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
-- Indizes für die Tabelle `logeintraege`
--
ALTER TABLE `logeintraege`
  ADD PRIMARY KEY (`id`),
  ADD KEY `benutzer_id` (`benutzer_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `benutzer`
--
ALTER TABLE `benutzer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT für Tabelle `einstellungen`
--
ALTER TABLE `einstellungen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT für Tabelle `logeintraege`
--
ALTER TABLE `logeintraege`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `logeintraege`
--
ALTER TABLE `logeintraege`
  ADD CONSTRAINT `logeintraege_ibfk_1` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
