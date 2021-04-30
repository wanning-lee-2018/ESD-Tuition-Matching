-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 22, 2021 at 04:04 AM
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
-- Database: `assignment`
--
CREATE DATABASE IF NOT EXISTS `assignment` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `assignment`;
-- --------------------------------------------------------

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
CREATE TABLE IF NOT EXISTS `assignment` (
  `AssignmentID` int(2) NOT NULL AUTO_INCREMENT,
  `TuteeID` int(2) NOT NULL,
  `TutorID` int(2) DEFAULT NULL,
  `AssignmentDayTime` text NOT NULL,
  `Subject` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Rate` float NOT NULL,
  `Status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TimePosted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `TimeLastModified` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`AssignmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `assignment`
--

INSERT INTO `assignment` (`AssignmentID`, `TuteeID`, `TutorID`, `AssignmentDayTime`, `Subject`, `Rate`, `Status`, `TimePosted`, `TimeLastModified`) VALUES
(1, 4, NULL, 'Monday, 7pm', 'Chemistry', 30, 'Open', '2021-03-18 10:14:04', NULL),
(2, 4, 1, 'Tuesday, 4pm', 'History', 25, 'Accepted', '2021-03-19 09:17:18', NULL),
(3, 4, 1, 'Friday, 12pm', 'Geography', 25, 'Accepted', '2021-03-19 11:17:18', NULL),
(4, 4, NULL, 'Wednesday, 3pm', 'Biology', 45, 'Open', '2021-03-20 09:17:18', NULL),
(5, 4, 1, 'Tuesday, 6pm', 'Economics', 50, 'Pending', '2021-03-21 12:21:53', NULL),
(6, 2, 1, 'Monday, 10am', 'Physics', 55, 'Accepted', '2021-03-22 08:15:04', NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
