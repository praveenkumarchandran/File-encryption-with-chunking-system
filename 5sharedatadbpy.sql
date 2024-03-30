-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 28, 2024 at 06:44 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `5sharedatadbpy`
--

-- --------------------------------------------------------

--
-- Table structure for table `filekeytb`
--

CREATE TABLE `filekeytb` (
  `id` bigint(20) NOT NULL auto_increment,
  `fid` bigint(20) NOT NULL,
  `OwnerName` varchar(250) NOT NULL,
  `FileInfo` varchar(500) NOT NULL,
  `FileName` varchar(250) NOT NULL,
  `Pukey` varchar(250) NOT NULL,
  `GroupId` varchar(20) NOT NULL,
  `Fkeyword` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `filekeytb`
--


-- --------------------------------------------------------

--
-- Table structure for table `filetb`
--

CREATE TABLE `filetb` (
  `id` bigint(20) NOT NULL auto_increment,
  `OwnerName` varchar(250) NOT NULL,
  `FileInfo` varchar(500) NOT NULL,
  `FileName` varchar(250) NOT NULL,
  `Pukey` varchar(250) NOT NULL,
  `GroupId` varchar(20) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `filetb`
--

INSERT INTO `filetb` (`id`, `OwnerName`, `FileInfo`, `FileName`, `Pukey`, `GroupId`) VALUES
(1, 'owner', 'my', '5521tamil8.txt', '325ed9e3b4f90a34a8cf7dbcb52a220a8f29b0907cf0ef0759bfd34f9fb06808', 'A'),
(2, 'owner', 'muu', '7351 (1).jpg', '239a2a0c5b0cad1905b48bd20ecddfcfc418d86722f69ca40d10149ffd23141f', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `ownertb`
--

CREATE TABLE `ownertb` (
  `id` bigint(20) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  `LoginKey` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `ownertb`
--

INSERT INTO `ownertb` (`id`, `Name`, `Mobile`, `Email`, `Address`, `UserName`, `Password`, `Status`, `LoginKey`) VALUES
(1, 'sangeeth Kumar', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'owner', 'owner', 'Active', '9401');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(20) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  `LoginKey` varchar(250) NOT NULL,
  `GroupName` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Mobile`, `Email`, `Address`, `UserName`, `Password`, `Status`, `LoginKey`, `GroupName`) VALUES
(1, 'sangeeth Kumar', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'user', 'user', 'Active', '8135', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `userfiletb`
--

CREATE TABLE `userfiletb` (
  `id` bigint(20) NOT NULL auto_increment,
  `FileId` varchar(250) NOT NULL,
  `OwnerName` varchar(250) NOT NULL,
  `Filename` varchar(250) NOT NULL,
  `PrKey` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  `GroupId` varchar(250) NOT NULL,
  `Keyword` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `userfiletb`
--

INSERT INTO `userfiletb` (`id`, `FileId`, `OwnerName`, `Filename`, `PrKey`, `UserName`, `Status`, `GroupId`, `Keyword`) VALUES
(1, '1', 'owner', '5521tamil8.txt', '325ed9e3b4f90a34a8cf7dbcb52a220a8f29b0907cf0ef0759bfd34f9fb06808', 'user', 'Approved', 'A', 'my');
