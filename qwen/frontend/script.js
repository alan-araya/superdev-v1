document.addEventListener("DOMContentLoaded", () => {
    const seatsContainer = document.getElementById("seats-container");
  
    // Função para buscar os assentos da API
    async function fetchSeats() {
      try {
        const response = await fetch("http://127.0.0.1:5000/flight/seats");
        const seats = await response.json();
        renderSeats(seats);
      } catch (error) {
        console.error("Erro ao buscar assentos:", error);
      }
    }
  
    // Função para renderizar os assentos
    function renderSeats(seats) {
      seatsContainer.innerHTML = ""; // Limpa o conteúdo anterior
  
      // Agrupa os assentos por fileira
      const rows = {};
      seats.forEach((seat) => {
        const rowNumber = parseInt(seat.seat.match(/\d+/)[0]); // Extrai o número da fileira
        if (!rows[rowNumber]) rows[rowNumber] = [];
        rows[rowNumber].push(seat);
      });
  
      // Renderiza cada fileira
      for (const [rowNumber, rowSeats] of Object.entries(rows)) {
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("row");
  
        // Número da fileira
        const rowNumberDiv = document.createElement("div");
        rowNumberDiv.classList.add("row-number");
        rowNumberDiv.textContent = rowNumber;
        rowDiv.appendChild(rowNumberDiv);
  
        // Grupo esquerdo (A, B, C)
        const leftGroup = document.createElement("div");
        leftGroup.classList.add("group");
        addSeatsToGroup(leftGroup, rowSeats, ["A", "B", "C"], rowNumber);
  
        // Espaço entre os grupos
        const spacer = document.createElement("div");
        spacer.style.width = "50px";
  
        // Grupo direito (D, E, F)
        const rightGroup = document.createElement("div");
        rightGroup.classList.add("group");
        addSeatsToGroup(rightGroup, rowSeats, ["D", "E", "F"], rowNumber);
  
        // Adiciona os grupos à fileira
        rowDiv.appendChild(leftGroup);
        rowDiv.appendChild(spacer);
        rowDiv.appendChild(rightGroup);
  
        // Adiciona a fileira ao contêiner
        seatsContainer.appendChild(rowDiv);
      }
    }
  
    // Função para adicionar assentos a um grupo
    function addSeatsToGroup(group, seats, letters, rowNumber) {
      letters.forEach((letter) => {
        const seat = seats.find((s) => s.seat === `${rowNumber}${letter}`);
        const seatDiv = document.createElement("div");
  
        if (seat) {
          seatDiv.classList.add("seat");
          seatDiv.textContent = letter;
  
          if (!seat.is_free) {
            seatDiv.classList.add("seat-occupied");
          } else {
            switch (seat.seat_type) {
              case "Premium":
                seatDiv.classList.add("seat-premium");
                break;
              case "Economy Premium":
                seatDiv.classList.add("seat-economy-premium");
                break;
              case "Economy":
                seatDiv.classList.add("seat-economy");
                break;
            }
          }
        } else {
          // Assento inválido (bloco cinza)
          seatDiv.classList.add("seat", "seat-invalid");
        }
  
        group.appendChild(seatDiv);
      });
    }
  
    // Atualiza os assentos a cada 1 segundo
    setInterval(fetchSeats, 1000);
  
    // Carrega os assentos pela primeira vez
    fetchSeats();
  });