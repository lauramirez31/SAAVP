-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-10-2025 a las 23:12:44
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `saavp`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre`) VALUES
(1, 'Arriendo'),
(2, 'Remates'),
(3, 'Compra_Nuevo'),
(4, 'Compra_Usado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propiedad`
--

CREATE TABLE `propiedad` (
  `id_propiedad` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `precio` int(11) NOT NULL,
  `disponible` enum('si','no') NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `detalles` text DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `idUsuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_login`
--

CREATE TABLE `registro_login` (
  `id` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro_login`
--

INSERT INTO `registro_login` (`id`, `idUsuario`, `fecha`) VALUES
(1, 13, '2025-09-16 18:08:58'),
(2, 14, '2025-09-16 21:04:32'),
(3, 11, '2025-09-16 21:50:40'),
(4, 15, '2025-10-06 20:25:22'),
(5, 15, '2025-10-06 20:33:31'),
(6, 15, '2025-10-06 20:36:01'),
(7, 15, '2025-10-06 20:36:56'),
(8, 15, '2025-10-06 20:37:38'),
(9, 15, '2025-10-06 20:38:51');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `idRol` int(11) NOT NULL,
  `nombreRol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`idRol`, `nombreRol`) VALUES
(1, 'Admin'),
(2, 'Usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_inmueble`
--

CREATE TABLE `tipo_inmueble` (
  `idTipo` int(11) NOT NULL,
  `descripcion_tipo` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_inmueble`
--

INSERT INTO `tipo_inmueble` (`idTipo`, `descripcion_tipo`) VALUES
(1, 'Apartamento'),
(2, 'Apartaestudio'),
(3, 'Casa'),
(4, 'Local'),
(5, 'Oficina'),
(6, 'Edificio'),
(7, 'Bodega'),
(8, 'Finca');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `reset_token` varchar(255) DEFAULT NULL,
  `token_expiry` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `username`, `password`, `reset_token`, `token_expiry`) VALUES
(3, 'HOMERO', 'HOMERO', 'XDDDD@asdasd', 'scrypt:32768:8:1$LEVFklXewC3HKMTl$535a080511169d3c6b1b6c424e971b89caf118dbe53a93c90afe9a302779eb06764ab7c0ffdae722a2c9864eab8f5e8994bc464b18e94361df0048311d0dcbe1', NULL, NULL),
(6, 'dfdfdfdfdf', '69', '11234@1234.COM', 'scrypt:32768:8:1$8YcewvN6rmamtuZE$6c79435dfa056c5dc895303a68b7e17e7f82d7d9553682c7c4452b1a8c3baf80b32f4dc4ad6b965de029a6077234ad4a0652d42e92a09a79ff2696c56948c0c8', 'L59jmiICjmvog355iCW9rXernZ41NfFRA9PWenpG65M', '2025-08-05 17:01:51'),
(8, 'Cristian', 'Valencia', 'david.lapras.cristian75@gmail.com', 'scrypt:32768:8:1$YWFAlU1Qy7zogNHg$e071aba1d0c4500d0d3d613b77eb0d921ce7b930ce8aa874c208496ef13e479337029eded6c9e882ac20474bc9a3b837705b70980b340c11a034e132d3a914ce', NULL, NULL),
(9, 'homero', 'chino', '1234@1234', 'scrypt:32768:8:1$soxOZQioVPfDpoEr$6be38776ba9d66b6fbd8b63e845f8e8be706ec0831ec109b493f8dc5548b15b0a257480b83ca2c27c90b8661bcdb809d7fbfde45f3deb04199e1340f7c8f4e61', NULL, NULL),
(11, 'hola', 'somos', 'saavp@gmail.com', 'scrypt:32768:8:1$F1Qr7VjhZc8keAmd$920c49933eda66729e11e67d11893488e0a1442de1923be6429d951201cce009739a37cc0d82bc8f7837213c155e8658816fd5da182785f93f1cd0c3f0db1d73', NULL, NULL),
(12, 'peter', 'grinin', 'peter@gmailcom', 'scrypt:32768:8:1$RbKLmxZ0AbX66Qy4$0df5f623d73786b06a4484216bb3bcb3826103fbba5d532c2636658a11cfde22d48da21e1f6746c78b0abef90a053757ac4a67af3ed6315e7ed12e0db8b37207', NULL, NULL),
(13, 'roca', 'roco', 'laroca@gmail.com', 'scrypt:32768:8:1$1s9pnoSs3N2dWlBp$edb800c12375e0c2c90c19040024f223756cf3c55f5145a04f05a48389f65fde00e7b5f7f62f7c60fe87dcbe5fc30a151204719f38e23e54c86b76a5dfb92859', NULL, NULL),
(14, 'o', 'o', 'o@gmail.com', 'scrypt:32768:8:1$0hbvbQ7uqTdOqBzX$11cc4dc8885798fd67677b6f0aca03a4432507a0e995be3a8ff58e9d884b6d30142ee89f42afdc23f26626cd03c18b16405277dfa6f0acbe1dc38ce2b7163fd0', NULL, NULL),
(15, 'hola', 'hola', 'e@e', 'scrypt:32768:8:1$QsIQlhDq07j6uhFr$b963fc16829559666e738307a81d749c20378de710345935ef6b41d831b41edb8c5926e945cdb97263a88ca9bd9e7f5d9f2bad284f59487be1e1d0955873b41c', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_rol`
--

CREATE TABLE `usuario_rol` (
  `idUsuario` int(11) NOT NULL,
  `idRol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario_rol`
--

INSERT INTO `usuario_rol` (`idUsuario`, `idRol`) VALUES
(11, 1),
(12, 2),
(13, 2),
(14, 2),
(15, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `propiedad`
--
ALTER TABLE `propiedad`
  ADD PRIMARY KEY (`id_propiedad`);

--
-- Indices de la tabla `registro_login`
--
ALTER TABLE `registro_login`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idUsuario` (`idUsuario`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`idRol`);

--
-- Indices de la tabla `tipo_inmueble`
--
ALTER TABLE `tipo_inmueble`
  ADD PRIMARY KEY (`idTipo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `usuario_rol`
--
ALTER TABLE `usuario_rol`
  ADD PRIMARY KEY (`idUsuario`,`idRol`),
  ADD KEY `idRol` (`idRol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `propiedad`
--
ALTER TABLE `propiedad`
  MODIFY `id_propiedad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `registro_login`
--
ALTER TABLE `registro_login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `idRol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tipo_inmueble`
--
ALTER TABLE `tipo_inmueble`
  MODIFY `idTipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `registro_login`
--
ALTER TABLE `registro_login`
  ADD CONSTRAINT `registro_login_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuario_rol`
--
ALTER TABLE `usuario_rol`
  ADD CONSTRAINT `usuario_rol_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `usuario_rol_ibfk_2` FOREIGN KEY (`idRol`) REFERENCES `roles` (`idRol`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
