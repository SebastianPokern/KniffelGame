-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 11. Jul 2025 um 17:35
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
(2, 'Basti', '$2b$12$nqlvTdp4mZBv43s6AbYVUOC0nEr0KM4/IABKcr.0QFb44ruGVTTpu', 'sebastian.pokern@googlemail.com', 1, '2025-06-05 13:27:34', 1, 'light');

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
(1, '2025-07-10 16:56:24', 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `spielteilnehmer`
--

CREATE TABLE `spielteilnehmer` (
  `id` int(11) NOT NULL,
  `spiel_id` int(11) NOT NULL,
  `benutzer_id` int(11) NOT NULL,
  `punkte` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `spielteilnehmer`
--

INSERT INTO `spielteilnehmer` (`id`, `spiel_id`, `benutzer_id`, `punkte`) VALUES
(1, 1, 1, 0),
(2, 1, 2, 0);

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
(1, 2, 1, '2025-07-10 16:56:25', '2,2,4,4,6', 1, 'Zweimal Zweier', 8);

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
-- AUTO_INCREMENT für Tabelle `spielpartien`
--
ALTER TABLE `spielpartien`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT für Tabelle `spielteilnehmer`
--
ALTER TABLE `spielteilnehmer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT für Tabelle `spielzuege`
--
ALTER TABLE `spielzuege`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `logeintraege`
--
ALTER TABLE `logeintraege`
  ADD CONSTRAINT `logeintraege_ibfk_1` FOREIGN KEY (`benutzer_id`) REFERENCES `benutzer` (`id`) ON DELETE SET NULL;

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
