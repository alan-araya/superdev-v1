// Função para extrair o número (fileira) da string do assento (ex.: "23A" retorna 23)
function getRowNumber(seatLabel) {
  const match = seatLabel.match(/^(\d+)/);
  return match ? parseInt(match[1], 10) : null;
}

// Função para extrair a letra do assento (ex.: "23A" retorna "A")
function getSeatLetter(seatLabel) {
  const match = seatLabel.match(/[A-Z]+$/);
  return match ? match[0] : null;
}

// Cria o elemento HTML para um assento válido, aplicando as classes conforme tipo e disponibilidade
function createSeatElement(seat) {
  const seatDiv = document.createElement('div');
  seatDiv.classList.add('seat-item');

  // Converte para minúsculas para comparar o tipo
  let seatType = seat.seat_type.toLowerCase();

  // Se o assento estiver ocupado, aplica a classe de ocupado
  if (!seat.is_free) {
    seatDiv.classList.add('seat-occupied');
  } else {
    // Se livre, aplica a classe de acordo com o tipo
    if (seatType === 'premium') {
      seatDiv.classList.add('seat-premium');
    } else if (seatType === 'economy premium' || seatType === 'economy-premium') {
      seatDiv.classList.add('seat-economy-premium');
    } else if (seatType === 'economy') {
      seatDiv.classList.add('seat-economy');
    }
  }
  // Exibe somente a letra do assento (a numeração da fileira já será exibida)
  let letter = getSeatLetter(seat.seat);
  seatDiv.textContent = letter;
  return seatDiv;
}

// Cria um elemento para o bloco inválido (placeholder) – sem conteúdo
function createInvalidSeatElement() {
  const seatDiv = document.createElement('div');
  seatDiv.classList.add('seat-item', 'seat-invalid');
  return seatDiv;
}

// Renderiza o mapa de assentos a partir dos dados retornados pela API
function renderSeatMap(seatsData) {
  // Agrupa os assentos por fileira usando o número extraído
  const rows = {};
  seatsData.forEach(seat => {
    const rowNum = getRowNumber(seat.seat);
    const letter = getSeatLetter(seat.seat);
    if (rowNum !== null && letter !== null) {
      if (!rows[rowNum]) {
        rows[rowNum] = {};
      }
      rows[rowNum][letter] = seat;
    }
  });

  // Container onde os assentos serão renderizados
  const container = document.getElementById('seat-map-container');
  container.innerHTML = ''; // Limpa o conteúdo anterior

  // Itera pelas 34 fileiras
  for (let row = 1; row <= 34; row++) {
    // Determina o tipo da fileira:
    // Fileiras 1 a 10 – Premium;
    // Fileiras 11 e 23 – Economy Premium;
    // Fileiras 12 a 22 e 24 a 34 – Economy.
    let rowType = '';
    if (row >= 1 && row <= 10) {
      rowType = 'Premium';
    } else if (row === 11 || row === 23) {
      rowType = 'Economy Premium';
    } else if ((row >= 12 && row <= 22) || (row >= 24 && row <= 34)) {
      rowType = 'Economy';
    }

    // Cria a div da fileira e o rótulo com o número da fileira
    const rowDiv = document.createElement('div');
    rowDiv.classList.add('seat-row');

    const rowLabel = document.createElement('div');
    rowLabel.classList.add('row-label');
    rowLabel.textContent = row;
    rowDiv.appendChild(rowLabel);

    // Cria os dois grupos de assentos: grupo esquerdo e grupo direito
    const leftGroup = document.createElement('div');
    leftGroup.classList.add('seat-group-left');
    const rightGroup = document.createElement('div');
    rightGroup.classList.add('seat-group-right');

    if (rowType === 'Economy Premium') {
      // Para fileiras Economy Premium: cada grupo possui 2 assentos válidos e um placeholder para manter 3 posições

      // Grupo esquerdo: letras A e B
      ['A', 'B'].forEach(letter => {
        if (rows[row] && rows[row][letter]) {
          leftGroup.appendChild(createSeatElement(rows[row][letter]));
        } else {
          leftGroup.appendChild(createInvalidSeatElement());
        }
      });
      // Placeholder para completar 3 posições
      leftGroup.appendChild(createInvalidSeatElement());

      // Grupo direito: letras C e D
      ['C', 'D'].forEach(letter => {
        if (rows[row] && rows[row][letter]) {
          rightGroup.appendChild(createSeatElement(rows[row][letter]));
        } else {
          rightGroup.appendChild(createInvalidSeatElement());
        }
      });
      // Placeholder para completar 3 posições
      rightGroup.appendChild(createInvalidSeatElement());
    } else {
      // Para fileiras Premium e Economy: cada grupo possui 3 assentos válidos (ou placeholder se ausente)
      // Grupo esquerdo: letras A, B, C
      ['A', 'B', 'C'].forEach(letter => {
        if (rows[row] && rows[row][letter]) {
          leftGroup.appendChild(createSeatElement(rows[row][letter]));
        } else {
          leftGroup.appendChild(createInvalidSeatElement());
        }
      });
      // Grupo direito: letras D, E, F
      ['D', 'E', 'F'].forEach(letter => {
        if (rows[row] && rows[row][letter]) {
          rightGroup.appendChild(createSeatElement(rows[row][letter]));
        } else {
          rightGroup.appendChild(createInvalidSeatElement());
        }
      });
    }

    // Adiciona os grupos na fileira com um espaçador no meio
    rowDiv.appendChild(leftGroup);
    const spacer = document.createElement('div');
    spacer.classList.add('seat-spacer');
    rowDiv.appendChild(spacer);
    rowDiv.appendChild(rightGroup);

    // Acrescenta a fileira ao container principal
    container.appendChild(rowDiv);
  }
}

// Função que busca os dados da API e atualiza a tela
function fetchAndRenderSeats() {
  fetch("http://127.0.0.1:5000/flight/seats")
    .then(response => response.json())
    .then(data => {
      // Como a API já retorna os assentos ordenados (veja instruções na API),
      // basta renderizar os dados recebidos.
      renderSeatMap(data);
    })
    .catch(error => {
      console.error("Erro ao buscar dados da API:", error);
    });
}

// Atualiza a tela a cada 1 segundo
setInterval(fetchAndRenderSeats, 1000);

// Inicia a busca dos dados assim que a página for carregada
window.onload = fetchAndRenderSeats;
