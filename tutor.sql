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
-- Database: `tutor`
--
CREATE DATABASE IF NOT EXISTS `tutor` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `tutor`;
-- --------------------------------------------------------

--
-- Table structure for table `tutor`
--

DROP TABLE IF EXISTS `tutor`;
CREATE TABLE IF NOT EXISTS `tutor` (
  `TutorID` int(2) NOT NULL AUTO_INCREMENT,
  `TutorName` varchar(20) NOT NULL,
  `TutorGender` char(1) NOT NULL,
  `TutorPhone` int(8) NOT NULL,
  `TutorAge` int(2) NOT NULL,
  `TutorQualification` varchar(200) NOT NULL,
  `TutorTelegramID` varchar(20) NOT NULL,
  `TutorTeleChatID` int(9) NOT NULL,
  `TutorEmail` text NOT NULL,
  PRIMARY KEY (`TutorID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tutor`
--
/* Take note! replace the fields such as Tutor Email and Tutor Telegram Chat ID with your own to test out the notification function*/
/* For more information on how to retrieve your own telegram chat id, refer to tuteebot.py*/
INSERT INTO `tutor` (`TutorID`, `TutorName`, `TutorGender`, `TutorPhone`, `TutorAge`, `TutorQualification`, `TutorTelegramID`, `TutorTeleChatID`,`TutorEmail`) VALUES
(1, 'Ling Li', 'F', XXXXXXXX, 21, 'Degree','XXX telegram username',XXXXXXXXX,'XXX email address'),
(2, 'Trisha', 'F', XXXXXXXX, 20, 'A level','XXX telegram username',XXXXXXXXX,'XXX email address'),
(3, 'Manny', 'M', XXXXXXXX, 24, 'Degree','XXX telegram username',XXXXXXXXX,'XXX email address'),
(4, 'Tony', 'M', XXXXXXXX, 21, 'A levels','XXX telegram username',XXXXXXXXX,'XXX email address');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
