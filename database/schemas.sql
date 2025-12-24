
USE railway;

-- TABLA 1: Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLA 2: Libros (estructura adaptada para los 20 libros)
CREATE TABLE IF NOT EXISTS Libros (
    id_libro INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    descripcion TEXT,
    anio_publicacion INT,
    precio DECIMAL(10, 2) NOT NULL,
    imagen_url VARCHAR(500),
    stock_compra INT DEFAULT 5,
    stock_alquiler INT DEFAULT 3
);

-- TABLA 3: Compras
CREATE TABLE IF NOT EXISTS Compras (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    fecha_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    precio_pagado DECIMAL(10, 2) NOT NULL,
    direccion_envio VARCHAR(255),
    metodo_pago ENUM('tarjeta', 'transferencia', 'contraentrega') NOT NULL,
    estado ENUM('pendiente', 'procesando', 'enviado', 'entregado') DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES Libros(id_libro)
);

-- TABLA 4: Alquileres
CREATE TABLE IF NOT EXISTS Alquileres (
    id_alquiler INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    dias_alquiler INT NOT NULL,
    fecha_devolucion DATE,
    estado ENUM('activo', 'devuelto', 'vencido') DEFAULT 'activo',
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES Libros(id_libro)
);

-- TABLA 5: Contactos
CREATE TABLE IF NOT EXISTS Contactos (
    id_contacto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    leido BOOLEAN DEFAULT FALSE
);

-- ============================================
-- 3. ÍNDICES (TUS ÍNDICES PARA MEJORAR RENDIMIENTO)
-- ============================================
CREATE INDEX idx_libros_titulo ON Libros(titulo);
CREATE INDEX idx_libros_autor ON Libros(autor);
CREATE INDEX idx_compras_usuario ON Compras(id_usuario);
CREATE INDEX idx_alquileres_usuario ON Alquileres(id_usuario);

-- ============================================
-- 4. INSERTAR LOS 20 LIBROS (DATOS REALES)
-- ============================================

INSERT INTO Libros (titulo, autor, descripcion, anio_publicacion, precio, imagen_url, stock_compra, stock_alquiler) VALUES
('La ciudad y los perros', 'Mario Vargas Llosa', 'Ambientada en el Colegio Militar Leoncio Prado, esta novela muestra la violencia, la hipocresía y la lucha por la identidad en un entorno represivo. Ganó el Premio Biblioteca Breve en 1962.', 1963, 35.00, 'https://www.rae.es/sites/default/files/la_ciudad_y_los_perros.jpg', 8, 3),
('Los ríos profundos', 'José María Arguedas', 'Narra la vida de Ernesto, un adolescente que enfrenta el choque entre la cultura andina y la occidental, mostrando la riqueza y el dolor del mundo indígena peruano.', 1958, 30.00, 'https://isbn.bnp.gob.pe/files/titulos/142178.jpg', 7, 4),
('Redoble por Rancas', 'Manuel Scorza', 'Primera entrega de la saga "La guerra silenciosa", es una denuncia poética contra los abusos hacia los campesinos andinos. Su estilo mezcla realismo y simbolismo.', 1970, 28.00, 'https://www.penguinlibros.com/pe/1718618/redoble-por-rancas.jpg', 6, 3),
('El zorro de arriba y el zorro de abajo', 'José María Arguedas', 'Última obra del autor, que combina mito, diario personal y novela social para representar el caos moral y cultural de la modernización peruana.', 1971, 40.00, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1482834617i/33615123.jpg', 5, 2),
('La tía Julia y el escribidor', 'Mario Vargas Llosa', 'Una divertida historia que mezcla el amor, la juventud y la literatura, inspirada en la vida del autor y ambientada en la Lima de los años 50.', 1977, 38.00, 'https://cdn.zendalibros.com/wp-content/uploads/2024/12/mario-vargas-llosa-la-tia-julia-y-el-escribidor.webp', 9, 5),
('Los heraldos negros', 'César Vallejo', 'Primer poemario de Vallejo, publicado en 1919, que refleja la angustia existencial y la injusticia social con un lenguaje profundamente humano y simbólico.', 1919, 25.00, 'https://www.bnp.gob.pe/wp-content/uploads/2019/10/HERALDOS-NEGROS.jpg', 10, 4),
('Trilce', 'César Vallejo', 'Obra revolucionaria del modernismo peruano, rompe las estructuras del lenguaje para expresar la soledad y el dolor humano de forma única.', 1922, 22.00, 'https://www.ecured.cu/images/f/f6/Trilce-1918-.jpg', 8, 3),
('El pez de oro', 'José María Arguedas', 'Una colección de relatos místicos y poéticos que conectan la cosmovisión andina con lo espiritual y lo cotidiano.', 1957, 33.00, 'https://hawansuyo.wordpress.com/wp-content/uploads/2019/07/66515359_2862151687134767_6223794120305934336_n.jpg', 7, 2),
('El sexto', 'José María Arguedas', 'Inspirada en la propia experiencia carcelaria del autor, muestra las injusticias políticas y sociales del Perú de los años 30.', 1961, 27.00, 'https://images.cdn2.buscalibre.com/fit-in/360x360/77/46/77464104435fcf47d2eda5580b37abff.jpg', 6, 3),
('Historia de Mayta', 'Mario Vargas Llosa', 'Una reflexión sobre el fracaso de las utopías revolucionarias en el Perú, a través de la historia de un idealista de izquierda.', 1984, 37.00, 'https://www.penguinlibros.com/pe/1717946/historia-de-mayta.jpg', 8, 4),
('Conversación en La Catedral', 'Mario Vargas Llosa', 'Considerada una de sus obras maestras, retrata la corrupción y el desencanto político en el Perú de Odría, a través de un diálogo introspectivo.', 1969, 45.00, 'https://roxanaorue.com/wp-content/uploads/2016/03/conversaciones-en-la-catedral1.jpg', 5, 2),
('La tumba del relámpago', 'Manuel Scorza', 'Parte del ciclo "La guerra silenciosa", esta obra denuncia las injusticias y luchas sociales en los Andes peruanos.', 1979, 32.00, 'https://m.media-amazon.com/images/I/A1v2+2OeeJL._AC_UF894,1000_QL80_.jpg', 7, 3),
('La palabra del mudo', 'Julio Ramón Ribeyro', 'Una recopilación de cuentos donde el autor retrata con ironía y sensibilidad a los marginados y soñadores del Perú urbano.', 1973, 29.00, 'https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1667833970i/26048242.jpg', 9, 5),
('Crónica de San Gabriel', 'Julio Ramón Ribeyro', 'Una novela que combina humor, realismo y tragedia para mostrar la decadencia de una familia rural en los Andes.', 1960, 34.00, 'https://bookscompany.pe/wp-content/uploads/2025/02/9786125044259.jpg', 6, 3),
('No una sino muchas muertes', 'Julio Ortega', 'Libro de cuentos que explora la violencia, la memoria y la esperanza en el contexto del Perú contemporáneo.', 1971, 25.00, 'https://pictures.abebooks.com/inventory/3837874163.jpg', 8, 4),
('Los geniecillos dominicales', 'Julio Ramón Ribeyro', 'Novela autobiográfica que sigue la juventud y frustraciones de Ludo, un escritor en el Perú de los años 50.', 1965, 26.00, 'https://imgv2-1-f.scribdassets.com/img/document/598986860/original/ae041a4c08/1?v=1', 7, 3),
('Abril rojo', 'Santiago Roncagliolo', 'Thriller ambientado en Ayacucho durante la posguerra interna, que combina misterio policial con crítica social.', 2006, 39.00, 'https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1631316524i/90601.jpg', 10, 5),
('La hora azul', 'Alonso Cueto', 'Narra la búsqueda de un abogado limeño por reconciliarse con el pasado violento de su familia durante el conflicto armado.', 2005, 36.00, 'https://cms.anagrama-ed.es/uploads/media/portadas/0001/19/3bfc021978a42d4fbe3dc7d5601f35fdfa54b60f.jpeg', 8, 4),
('Paco Yunque', 'César Vallejo', 'Cuento emblemático sobre la injusticia social y las desigualdades en la educación peruana. Narra la historia de un niño humilde que sufre abusos por parte del hijo del alcalde.', 1931, 20.00, 'https://www.elejandria.com/covers/Paco_Yunque-Cesar_Vallejo-lg.png', 12, 6),
('Un mundo para Julius', 'Alfredo Bryce Echenique', 'Una de las novelas más reconocidas de la literatura peruana contemporánea. Narra la historia de Julius, un niño de clase alta que observa con inocencia la desigualdad y el contraste entre su mundo privilegiado y el de los trabajadores de su casa.', 1970, 42.00, 'https://cms.anagrama-ed.es/uploads/media/portadas/0001/19/0ba934643314186e5affc4b9cdf6b13d26242e2b.jpeg', 9, 5);
