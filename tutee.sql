-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 15, 2021 at 04:24 AM
-- Server version: 8.0.18
-- PHP Version: 7.4.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tutee`
--
CREATE DATABASE IF NOT EXISTS `tutee` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `tutee`;
-- --------------------------------------------------------

--
-- Table structure for table `tutee`
--

DROP TABLE IF EXISTS `tutee`;
CREATE TABLE IF NOT EXISTS `tutee` (
  `TuteeID` int(2) NOT NULL AUTO_INCREMENT,
  `TuteeName` varchar(20) NOT NULL,
  `TuteeGender` char(1) NOT NULL,
  `TuteePhone` int(8) NOT NULL,
  `TuteeGrade` varchar(20) NOT NULL,
  `TuteeLocation` varchar(50) NOT NULL,
  `TuteeTelegramID` varchar(20) NOT NULL,
  `TuteeTeleChatID` int(9) NOT NULL,
  `TuteeEmail` text NOT NULL,
  PRIMARY KEY (`TuteeID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tutee`
--


/* Take note! replace the fields such as Tutee Email and Tutee Telegram Chat ID with your own to test out the notification function*/
/* For more information on how to retrieve your own telegram chat id, refer to tuteebot.py*/
INSERT INTO `tutee` (`TuteeID`, `TuteeName`, `TuteeGender`, `TuteePhone`, `TuteeGrade`, `TuteeLocation`, `TuteeTelegramID`,`TuteeTeleChatID`,`TuteeEmail`) VALUES
(1, 'Wan Ning', 'F', XXXXXXXX, 'Sec 1', 'Bencoolen', 'XXX telegram username',XXXXXXXXX,'XXX email address'),
(2, 'Hong Haii', 'M', XXXXXXXX, 'JC 2', 'Simei', 'XXX telegram username',XXXXXXXXX,'XXX email address'),
(3, 'Jake', 'M', XXXXXXXX, 'Sec 4', 'Jurong', 'XXX telegram username',XXXXXXXXX,'XXX email address'),
(4, 'Anna', 'F', XXXXXXXX, 'Pri 6', 'Pasir Ris', 'XXX telegram username',XXXXXXXXX,'XXX email address'),
(5, 'Benjamin', 'M', XXXXXXXX, 'Sec 2', 'Orchard', 'XXX telegram username',XXXXXXXXX,'XXX email address');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
