// Base de datos de libros con información adicional
const libros = [
  {
    id: 1,
    titulo: "La ciudad y los perros",
    autor: "Mario Vargas Llosa",
    anio: 1963,
    precio: 35.00,
    imagen: "https://www.rae.es/sites/default/files/la_ciudad_y_los_perros.jpg"
  },
  {
    id: 2,
    titulo: "Los ríos profundos",
    autor: "José María Arguedas",
    anio: 1958,
    precio: 30.00,
    imagen: "https://isbn.bnp.gob.pe/files/titulos/142178.jpg"
  },
  {
    id: 3,
    titulo: "Redoble por Rancas",
    autor: "Manuel Scorza",
    anio: 1970,
    precio: 28.00,
    imagen: "https://www.penguinlibros.com/pe/1718618/redoble-por-rancas.jpg"
  },
  {
    id: 4,
    titulo: "El zorro de arriba y el zorro de abajo",
    autor: "José María Arguedas",
    anio: 1971,
    precio: 40.00,
    imagen: "https://s3.amazonaws.com/img2.peruebooks.com/covers/covers-3/9789560008695.jpg"
  },
  {
    id: 5,
    titulo: "La tía Julia y el escribidor",
    autor: "Mario Vargas Llosa",
    anio: 1977,
    precio: 38.00,
    imagen: "https://cdn.zendalibros.com/wp-content/uploads/2024/12/mario-vargas-llosa-la-tia-julia-y-el-escribidor.webp"
  },
  {
    id: 6,
    titulo: "Los heraldos negros",
    autor: "César Vallejo",
    anio: 1919,
    precio: 25.00,
    imagen: "https://www.bnp.gob.pe/wp-content/uploads/2019/10/HERALDOS-NEGROS.jpg"
  },
  {
    id: 7,
    titulo: "Trilce",
    autor: "César Vallejo",
    anio: 1922,
    precio: 22.00,
    imagen: "https://www.ecured.cu/images/f/f6/Trilce-1918-.jpg"
  },
  {
    id: 8,
    titulo: "El pez de oro",
    autor: "José María Arguedas",
    anio: 1957,
    precio: 33.00,
    imagen: "https://hawansuyo.wordpress.com/wp-content/uploads/2019/07/66515359_2862151687134767_6223794120305934336_n.jpg"
  },
  {
    id: 9,
    titulo: "El sexto",
    autor: "José María Arguedas",
    anio: 1961,
    precio: 27.00,
    imagen: "https://images.cdn2.buscalibre.com/fit-in/360x360/77/46/77464104435fcf47d2eda5580b37abff.jpg"
  },
  {
    id: 10,
    titulo: "Historia de Mayta",
    autor: "Mario Vargas Llosa",
    anio: 1984,
    precio: 37.00,
    imagen: "https://www.penguinlibros.com/pe/1717946/historia-de-mayta.jpg"
  },
  {
    id: 11,
    titulo: "Conversación en La Catedral",
    autor: "Mario Vargas Llosa",
    anio: 1969,
    precio: 45.00,
    imagen: "https://roxanaorue.com/wp-content/uploads/2016/03/conversaciones-en-la-catedral1.jpg"
  },
  {
    id: 12,
    titulo: "La tumba del relámpago",
    autor: "Manuel Scorza",
    anio: 1979,
    precio: 32.00,
    imagen: "https://m.media-amazon.com/images/I/A1v2+2OeeJL._AC_UF894,1000_QL80_.jpg"
  },
  {
    id: 13,
    titulo: "La palabra del mudo",
    autor: "Julio Ramón Ribeyro",
    anio: 1973,
    precio: 29.00,
    imagen: "https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1667833970i/26048242.jpg"
  },
  {
    id: 14,
    titulo: "Crónica de San Gabriel",
    autor: "Julio Ramón Ribeyro",
    anio: 1960,
    precio: 34.00,
    imagen: "https://bookscompany.pe/wp-content/uploads/2025/02/9786125044259.jpg"
  },
  {
    id: 15,
    titulo: "No una sino muchas muertes",
    autor: "Julio Ortega",
    anio: 1971,
    precio: 25.00,
    imagen: "https://pictures.abebooks.com/inventory/3837874163.jpg"
  },
  {
    id: 16,
    titulo: "Los geniecillos dominicales",
    autor: "Julio Ramón Ribeyro",
    anio: 1965,
    precio: 26.00,
    imagen: "https://imgv2-1-f.scribdassets.com/img/document/598986860/original/ae041a4c08/1?v=1"
  },
  {
    id: 17,
    titulo: "Abril rojo",
    autor: "Santiago Roncagliolo",
    anio: 2006,
    precio: 39.00,
    imagen: "https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1631316524i/90601.jpg"
  },
  {
    id: 18,
    titulo: "La hora azul",
    autor: "Alonso Cueto",
    anio: 2005,
    precio: 36.00,
    imagen: "https://cms.anagrama-ed.es/uploads/media/portadas/0001/19/3bfc021978a42d4fbe3dc7d5601f35fdfa54b60f.jpeg"
  },
  {
    id: 19,
    titulo: "Paco Yunque",
    autor: "César Vallejo",
    anio: 1931,
    precio: 20.00,
    imagen: "https://www.elejandria.com/covers/Paco_Yunque-Cesar_Vallejo-lg.png"
  },
  {
    id: 20,
    titulo: "Un mundo para Julius",
    autor: "Alfredo Bryce Echenique",
    anio: 1970,
    precio: 42.00,
    imagen: "https://cms.anagrama-ed.es/uploads/media/portadas/0001/19/0ba934643314186e5affc4b9cdf6b13d26242e2b.jpeg"
  }
];

// Filtros activos
let filtrosActivos = {
  autor: null,
  anio: null,
  precio: null,
};

// Inicializar la página
document.addEventListener('DOMContentLoaded', function() {
  inicializarBotonesFiltro();
  inicializarBotonesAccion();
});

// Inicializar botones de filtro
function inicializarBotonesFiltro() {
  const botonesFiltro = document.querySelectorAll('.filtro-boton');
  
  botonesFiltro.forEach(boton => {
    boton.addEventListener('click', function() {
      const tipo = this.closest('.filtro-grupo').querySelector('h3').textContent;
      
      // Determinar qué tipo de filtro es
      if (tipo.includes('Autor')) {
        manejarFiltro('autor', this.dataset.autor, this);
      } else if (tipo.includes('Año')) {
        manejarFiltro('anio', this.dataset.anio, this);
      } else if (tipo.includes('Precio')) {
        manejarFiltro('precio', this.dataset.precio, this);
      }
    });
  });
}

// Manejar la selección/deselección de filtros
function manejarFiltro(tipo, valor, boton) {
  const botonesGrupo = boton.closest('.filtro-opciones').querySelectorAll('.filtro-boton');
  
  // Si ya está seleccionado, deseleccionar
  if (filtrosActivos[tipo] === valor) {
    filtrosActivos[tipo] = null;
    boton.classList.remove('activo');
  } else {
    // Deseleccionar otros botones del mismo grupo
    botonesGrupo.forEach(b => b.classList.remove('activo'));
    
    // Seleccionar este botón
    filtrosActivos[tipo] = valor;
    boton.classList.add('activo');
  }
  
  // Actualizar visualización de filtros activos
  actualizarFiltrosActivos();
}

// Actualizar la visualización de filtros activos
function actualizarFiltrosActivos() {
  const contenedor = document.getElementById('filtros-activos');
  contenedor.innerHTML = '';
  
  Object.entries(filtrosActivos).forEach(([tipo, valor]) => {
    if (valor) {
      const filtroActivo = document.createElement('div');
      filtroActivo.className = 'filtro-activo';
      
      let texto = '';
      switch(tipo) {
        case 'autor':
          texto = `Autor: ${valor}`;
          break;
        case 'anio':
          texto = `Año: ${obtenerTextoAnio(valor)}`;
          break;
        case 'precio':
          texto = `Precio: ${obtenerTextoPrecio(valor)}`;
          break;
      }
      
      filtroActivo.innerHTML = `
        ${texto}
        <button onclick="eliminarFiltro('${tipo}')">×</button>
      `;
      
      contenedor.appendChild(filtroActivo);
    }
  });
}

// Obtener texto descriptivo para año
function obtenerTextoAnio(valor) {
  const anios = {
    '1919': '1919 o antes',
    '1930': 'Años 1930',
    '1940': 'Años 1940',
    '1950': 'Años 1950',
    '1960': 'Años 1960',
    '1970': 'Años 1970',
    '1980': 'Años 1980',
    '1990': 'Años 1990',
    '2000': '2000 o después'
  };
  return anios[valor] || valor;
}

// Obtener texto descriptivo para precio
function obtenerTextoPrecio(valor) {
  const precios = {
    '0-20': 'Menos de S/ 20',
    '20-30': 'S/ 20 - S/ 30',
    '30-40': 'S/ 30 - S/ 40',
    '40-50': 'S/ 40 - S/ 50',
    '50-100': 'Más de S/ 50'
  };
  return precios[valor] || valor;
}

// Eliminar un filtro específico
function eliminarFiltro(tipo) {
  filtrosActivos[tipo] = null;
  
  // Actualizar botones
  const botones = document.querySelectorAll(`.filtro-boton[data-${tipo}]`);
  botones.forEach(boton => boton.classList.remove('activo'));
  
  // Actualizar visualización
  actualizarFiltrosActivos();
}

// Inicializar botones de acción
function inicializarBotonesAccion() {
  document.getElementById('aplicar-filtros').addEventListener('click', aplicarFiltros);
  document.getElementById('limpiar-filtros').addEventListener('click', limpiarFiltros);
  document.getElementById('ver-todos').addEventListener('click', verTodos);
}

// Aplicar filtros y mostrar resultados
function aplicarFiltros() {
  const librosFiltrados = filtrarLibros();
  mostrarResultados(librosFiltrados);
}

// Filtrar libros según criterios activos
function filtrarLibros() {
  return libros.filter(libro => {
    // Filtro por autor
    if (filtrosActivos.autor && libro.autor !== filtrosActivos.autor) {
      return false;
    }
    
    // Filtro por año
    if (filtrosActivos.anio) {
      const anioFiltro = parseInt(filtrosActivos.anio);
      const anioLibro = libro.anio;
      
      if (filtrosActivos.anio === '1919' && anioLibro > 1919) return false;
      if (filtrosActivos.anio === '1930' && (anioLibro < 1930 || anioLibro > 1939)) return false;
      if (filtrosActivos.anio === '1940' && (anioLibro < 1940 || anioLibro > 1949)) return false;
      if (filtrosActivos.anio === '1950' && (anioLibro < 1950 || anioLibro > 1959)) return false;
      if (filtrosActivos.anio === '1960' && (anioLibro < 1960 || anioLibro > 1969)) return false;
      if (filtrosActivos.anio === '1970' && (anioLibro < 1970 || anioLibro > 1979)) return false;
      if (filtrosActivos.anio === '1980' && (anioLibro < 1980 || anioLibro > 1989)) return false;
      if (filtrosActivos.anio === '1990' && (anioLibro < 1990 || anioLibro > 1999)) return false;
      if (filtrosActivos.anio === '2000' && anioLibro < 2000) return false;
    }
    
    // Filtro por precio
    if (filtrosActivos.precio) {
      const [min, max] = filtrosActivos.precio.split('-').map(Number);
      
      if (filtrosActivos.precio === '50-100' && libro.precio <= 50) return false;
      if (filtrosActivos.precio !== '50-100' && (libro.precio < min || libro.precio > max)) return false;
    }
    
    return true;
  });
}

// Mostrar resultados en la página
function mostrarResultados(librosFiltrados) {
  const contenedor = document.getElementById('resultados-libros');
  const contador = document.getElementById('contador-resultados');
  
  if (librosFiltrados.length === 0) {
    contenedor.innerHTML = `
      <p class="mensaje-inicial">
        No se encontraron libros con los filtros seleccionados. 
        Intenta con diferentes criterios de búsqueda.
      </p>
    `;
    contador.textContent = `Mostrando 0 de ${libros.length} libros`;
    return;
  }
  
  let html = '';
  
  librosFiltrados.forEach(libro => {
    html += `
      <div class="tarjeta-libro">
        <div class="contenedor-imagen">
          <img src="${libro.imagen}" alt="${libro.titulo}" 
               onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"250\" viewBox=\"0 0 200 250\"><rect width=\"200\" height=\"250\" fill=\"%23f5f5f5\"/><text x=\"100\" y=\"125\" font-family=\"Arial\" font-size=\"20\" text-anchor=\"middle\" fill=\"%238B0000\">📚</text></svg>'">
        </div>
        <div class="contenido-tarjeta">
          <h3>${libro.titulo}</h3>
          <p class="autor">${libro.autor}</p>
          <p class="precio">S/ ${libro.precio.toFixed(2)}</p>
          <div class="botones">
            <button onclick="location.href='alquiler.html'">Alquilar</button>
            <button onclick="location.href='compra.html'">Comprar</button>
            <a href="libro.html#libro${libro.id}" class="vermas">Ver más</a>
          </div>
        </div>
      </div>
    `;
  });
  
  contenedor.innerHTML = html;
  contador.textContent = `Mostrando ${librosFiltrados.length} de ${libros.length} libros`;
}

// Limpiar todos los filtros
function limpiarFiltros() {
  // Resetear filtros activos
  filtrosActivos = {
    autor: null,
    anio: null,
    precio: null,
  };
  
  // Deseleccionar todos los botones
  document.querySelectorAll('.filtro-boton').forEach(boton => {
    boton.classList.remove('activo');
  });
  
  // Actualizar visualización
  actualizarFiltrosActivos();
  
  // Mostrar mensaje inicial
  const contenedor = document.getElementById('resultados-libros');
  const contador = document.getElementById('contador-resultados');
  
  contenedor.innerHTML = `
    <p class="mensaje-inicial">Selecciona uno o más filtros y haz clic en "Aplicar Filtros" para ver los resultados.</p>
  `;
  contador.textContent = `Mostrando 0 de ${libros.length} libros`;
}

// Ver todos los libros sin filtros
function verTodos() {
  limpiarFiltros();
  mostrarResultados(libros);
}